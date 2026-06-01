"""
NodeCompiler Operators
Compile node groups into the correct subfolder of src/nodes/compiled/,
matching the LSCherry scene hierarchy used by node_impl.py.
"""

from __future__ import annotations
import os

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
from .compiler.sorter import topological_sort, get_all_node_groups
from .compiler.router import (
    resolve,
    make_bl_label,
    make_import_prefix,
    build_material_ng_map,
    sanitize_material_name,
)
from .compiler.exporter import (
    write_compiled_file,
    write_all_inits,
    ng_name_to_filename,
    ng_name_to_class,
)

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

        # ── 3. Build material → node group map (for fallback routing) ────────
        material_ng_map = build_material_ng_map()

        # ── 4. Compile each group ────────────────────────────────────────────
        # subpath_modules: { subpath → [module_stem, ...] }
        subpath_modules: dict[str, list[str]] = {}
        n_ok  = 0
        errors: list[str] = []

        for ng in sorted_ngs:
            # Determine subfolder + bl_label from ng.name
            subpath, label_prefix = resolve(ng.name)

            # Fallback to root lscherry — try material-based routing instead
            if subpath == "lscherry":
                mat_name = material_ng_map.get(ng.name)
                if mat_name:
                    folder = sanitize_material_name(mat_name)
                    subpath = f"lscherry/{folder}"
                    label_prefix = mat_name

            bl_label      = make_bl_label(ng.name, label_prefix)
            import_prefix = make_import_prefix(subpath)
            module_stem   = ng_name_to_filename(ng.name)
            class_name    = ng_name_to_class(ng.name, ng.type)
            filename      = module_stem + ".py"

            # Analyze
            try:
                info = analyze_node_group(ng)
            except Exception as exc:
                logger.warning(f"Analysis failed for '{ng.name}': {exc}")
                errors.append(ng.name)
                continue

            # Inject bl_label into info so code_gen can use it
            info["bl_label"] = bl_label

            # Generate code
            try:
                code = generate_class(info, class_name, import_prefix)
            except Exception as exc:
                logger.warning(f"Code gen failed for '{ng.name}': {exc}")
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

        # ── 5. Optionally copy the blend file ────────────────────────────────
        if props.copy_blend:
            blend_copy = os.path.join(out_dir, "source.blend")
            try:
                bpy.ops.wm.save_as_mainfile(filepath=blend_copy, copy=True)
                logger.info(f"Blend copy saved → {blend_copy}")
            except Exception as exc:
                logger.warning(f"Could not copy blend file: {exc}")

        # ── 6. Report ────────────────────────────────────────────────────────
        n_err = len(errors)
        msg   = f"✅ Compiled {n_ok} node group(s)"
        if n_err:
            msg += f", {n_err} failed (see system console)"
        msg += f". Output: {out_dir}"
        self.report({"INFO"}, msg)
        logger.info(f"Compile complete: {n_ok} ok, {n_err} failed.")

        return {"FINISHED"}