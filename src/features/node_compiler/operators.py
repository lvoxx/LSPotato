"""
NodeCompiler Operators
Compile node groups into the correct subfolder of src/nodes/compiled/,
matching the LSCherry scene hierarchy used by node_impl.py.
"""

from __future__ import annotations
import os
import traceback

import bpy  # type: ignore

from ...exception.base_handler import OperatorExceptionMixin
from ...exception.handler.node_compiler_handler import NodeCompilerHandler
from ...exception.model.node_compiler_exceptions import (
    BlendFileNotSavedException,
    ExportIOException,
)
from ...utils.logger import get_logger

from .compiler.analyzer import analyze_node_group
from .compiler.code_gen import generate_class
from .compiler.flattener import needs_flatten, flatten_info
from .compiler.sorter import topological_sort, get_all_node_groups
from .compiler.router import (
    make_bl_label,
    make_import_prefix,
    build_direct_material_ng_map,
    material_name_to_route,
)
from .compiler.exporter import (
    write_compiled_file,
    write_all_inits,
    export_packed_images,
    ng_name_to_filename,
    ng_name_to_class,
)
from .compiler.geometry_exporter import export_geometry

logger = get_logger("NodeCompiler")


class LSPOTATO_OT_compile_node_groups(bpy.types.Operator, OperatorExceptionMixin):
    """Compile all node groups into locked Python-based custom nodes"""

    bl_idname  = "lspotato.compile_node_groups"
    bl_label   = "Compile Node Groups"
    bl_description = (
        "Analyse every node group and generate a Python module per group. "
        "Files are placed in the configured folder, mirroring the LSCherry hierarchy."
    )
    bl_options = {"REGISTER"}

    handler_class = NodeCompilerHandler

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)

    def _execute_impl(self, context):
        props = context.scene.lspotato_compiler

        # ── 1. Guard: blend file must be saved ──────────────────────────────
        blend_path = bpy.data.filepath
        if not blend_path:
            raise BlendFileNotSavedException()

        blend_dir = os.path.dirname(os.path.abspath(blend_path))
        raw_folder = props.compiled_folder or "./compiled"
        out_dir = os.path.normpath(os.path.join(blend_dir, raw_folder))

        try:
            os.makedirs(out_dir, exist_ok=True)
        except OSError as exc:
            raise ExportIOException(out_dir, str(exc)) from exc

        # ── 2. Collect & topological-sort node groups ────────────────────────
        all_ngs = get_all_node_groups()
        if not all_ngs:
            self.report({"WARNING"}, "No node groups found in this file.")
            return {"CANCELLED"}

        sorted_ngs = topological_sort(all_ngs)

        # ── 3. Build material → node group map (direct ownership only) ─────────
        direct_mat_map = build_direct_material_ng_map()

        # ── 4. Compile each group ────────────────────────────────────────────
        # subpath_modules: { subpath → [module_stem, ...] }
        subpath_modules: dict[str, list[str]] = {}
        # compiled_nodes: original ng.name → (compiled classname, stable node-tree key)
        # Built incrementally (topological order ensures dependencies come first).
        compiled_nodes: dict[str, tuple[str, str]] = {}
        # Predefined (packed) textures to copy out: filename → bpy.types.Image.
        predefined_images: dict = {}
        # Raw analyzed infos, keyed by ng.name. Topological order guarantees a
        # group's children are already cached before it is flattened.
        analyzed_infos: dict[str, dict] = {}
        attr_memo: dict = {}  # group_has_attribute memoisation
        n_ok  = 0
        errors: list[str] = []

        for ng in sorted_ngs:
            # Route by the material that directly owns this node group.
            # Falls back to lscherry root for unowned groups (e.g. standalone utilities).
            mat_name = direct_mat_map.get(ng.name)
            if mat_name:
                route = material_name_to_route(mat_name)
                subpath, label_prefix = route if route else ("lscherry", "lscherry")
            else:
                subpath, label_prefix = "lscherry", "lscherry"

            bl_label      = make_bl_label(ng.name, label_prefix)
            import_prefix = make_import_prefix(subpath)
            module_stem   = ng_name_to_filename(ng.name)
            class_name    = ng_name_to_class(ng.name, ng.type)
            filename      = module_stem + ".py"

            # Register this node group so later (parent) nodes can reference it
            compiled_nodes[ng.name] = (class_name, "." + bl_label)

            # Analyze
            try:
                info = analyze_node_group(ng)
            except Exception as exc:
                logger.warning(f"Analysis failed for '{ng.name}': {exc}\n{traceback.format_exc()}")
                errors.append(ng.name)
                continue

            # Cache the RAW info before flattening so parents can inline it.
            analyzed_infos[ng.name] = info

            # Inject bl_label into info so code_gen can use it
            info["bl_label"] = bl_label

            # Flatten inline-forcing nested groups into this tree. Blender doesn't
            # bind geometry attributes through a ShaderNodeCustomGroup boundary,
            # and a placeholder image buried in a nested group can't be exposed as
            # this node's own texture input — so any Attribute node or placeholder
            # TEX_IMAGE must land in this group's own tree.
            if needs_flatten(info, analyzed_infos, attr_memo):
                info = flatten_info(info, analyzed_infos, attr_memo)

            # Collect predefined textures to copy out (dedup by filename).
            for fn, img in info.get("_predefined_images", []):
                predefined_images.setdefault(fn, img)

            # Generate code (pass compiled_nodes so GROUP refs use create_node_group)
            try:
                code = generate_class(info, class_name, import_prefix, compiled_nodes)
            except Exception as exc:
                logger.warning(f"Code gen failed for '{ng.name}': {exc}\n{traceback.format_exc()}")
                errors.append(ng.name)
                continue

            # Write file
            try:
                write_compiled_file(out_dir, subpath, filename, code)
            except OSError as exc:
                raise ExportIOException(
                    os.path.join(out_dir, subpath, filename), str(exc)
                ) from exc

            subpath_modules.setdefault(subpath, []).append(module_stem)
            n_ok += 1
            logger.info(f"Compiled: {ng.name} → {subpath}/{filename}  [{bl_label}]")

        # ── 4. Write __init__.py for every folder ────────────────────────────
        try:
            write_all_inits(out_dir, subpath_modules)
        except OSError as exc:
            raise ExportIOException(out_dir, str(exc)) from exc

        # ── 4b. Copy predefined (packed) textures into images/ ───────────────
        if predefined_images:
            try:
                saved = export_packed_images(out_dir, predefined_images)
                logger.info(
                    f"Exported {len(saved)} predefined image(s) → {out_dir}/images"
                )
            except Exception as exc:
                logger.warning(f"Could not export predefined images: {exc}")

        # ── 5. Optionally copy the blend file ────────────────────────────────
        if props.copy_blend:
            blend_copy = os.path.join(out_dir, "source.blend")
            try:
                bpy.ops.wm.save_as_mainfile(filepath=blend_copy, copy=True)
                logger.info(f"Blend copy saved → {blend_copy}")
            except Exception as exc:
                logger.warning(f"Could not copy blend file: {exc}")

        # ── 5c. Export geometry node groups (library.blend + hashes.json) ─────
        # Geometry groups take a different path than shaders: rather than Python,
        # they are written verbatim into <out_dir>/geometry/ for the runtime
        # loader to append. Failure here must not sink a successful shader compile.
        n_geo = 0
        if props.compile_geometry:
            try:
                n_geo = export_geometry(out_dir)
                if n_geo:
                    logger.info(
                        f"Exported {n_geo} geometry node group(s) → {out_dir}/geometry"
                    )
            except Exception as exc:
                logger.warning(f"Could not export geometry node groups: {exc}")

        # ── 6. Report ────────────────────────────────────────────────────────
        n_err = len(errors)
        msg   = f"✅ Compiled {n_ok} node group(s)"
        if n_err:
            msg += f", {n_err} failed (see system console)"
        if n_geo:
            msg += f", {n_geo} geometry group(s)"
        msg += f". Output: {out_dir}"
        self.report({"INFO"}, msg)
        logger.info(f"Compile complete: {n_ok} ok, {n_err} failed, {n_geo} geometry.")

        return {"FINISHED"}