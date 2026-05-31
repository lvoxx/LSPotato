"""
NodeCompiler Operators
Provides the "Compile Node Groups" operator for LSPotato Dev Mode.
"""

from __future__ import annotations
import os
import traceback

import bpy  # type: ignore

from ...exception.base_handler import OperatorExceptionMixin
from ...exception.handler.node_compiler_handler import NodeCompilerHandler
from ...exception.model.node_compiler_exceptions import (
    BlendFileNotSavedException,
    NodeGroupAnalysisException,
    NodeGroupCompileException,
    ExportIOException,
)
from ...utils.logger import get_logger

from .compiler.analyzer import analyze_node_group
from .compiler.code_gen import generate_class
from .compiler.sorter import topological_sort, get_all_node_groups
from .compiler.exporter import (
    write_compiled_file,
    write_init,
    ng_name_to_filename,
    ng_name_to_class,
)

logger = get_logger("NodeCompiler")


class LSPOTATO_OT_compile_node_groups(bpy.types.Operator, OperatorExceptionMixin):
    """Compile all node groups into locked Python-based custom nodes"""

    bl_idname  = "lspotato.compile_node_groups"
    bl_label   = "Compile Node Groups"
    bl_description = (
        "Analyse every node group in this file and generate a Python module "
        "that recreates each group procedurally — just like the Parallax addon. "
        "Output is written to the configured folder."
    )
    bl_options = {"REGISTER"}

    handler_class = NodeCompilerHandler

    # ------------------------------------------------------------------ invoke
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    # ------------------------------------------------------------------ execute
    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)

    def _execute_impl(self, context):
        props = context.scene.lspotato_compiler

        # 1. Guard: blend file must be saved
        blend_path = bpy.data.filepath
        if not blend_path:
            raise BlendFileNotSavedException()

        blend_dir    = os.path.dirname(os.path.abspath(blend_path))
        raw_folder   = props.compiled_folder or "./compiled"
        out_dir      = os.path.normpath(os.path.join(blend_dir, raw_folder))

        try:
            os.makedirs(out_dir, exist_ok=True)
        except OSError as exc:
            raise ExportIOException(out_dir, str(exc)) from exc

        # 2. Collect & sort node groups
        all_ngs = get_all_node_groups()
        if not all_ngs:
            self.report({"WARNING"}, "No node groups found in this file.")
            return {"CANCELLED"}

        sorted_ngs = topological_sort(all_ngs)

        # 3. Compile each group
        compiled_modules: list[str] = []
        skipped: list[str]          = []
        errors: list[str]           = []

        for ng in sorted_ngs:
            module_name = ng_name_to_filename(ng.name)
            class_name  = ng_name_to_class(ng.name, ng.type)
            filename    = module_name + ".py"

            try:
                info = analyze_node_group(ng)
            except Exception as exc:
                msg = f"Analysis failed for '{ng.name}': {exc}"
                logger.warning(msg)
                errors.append(ng.name)
                continue

            try:
                code = generate_class(info, class_name)
            except Exception as exc:
                msg = f"Code generation failed for '{ng.name}': {exc}"
                logger.warning(msg)
                errors.append(ng.name)
                continue

            try:
                write_compiled_file(out_dir, filename, code)
            except OSError as exc:
                raise ExportIOException(os.path.join(out_dir, filename), str(exc)) from exc

            compiled_modules.append(module_name)
            logger.info(f"Compiled: {ng.name} → {filename}")

        # 4. Write __init__.py
        try:
            write_init(out_dir, compiled_modules)
        except OSError as exc:
            raise ExportIOException(os.path.join(out_dir, "__init__.py"), str(exc)) from exc

        # 5. Optionally copy the blend file
        if props.copy_blend:
            blend_copy = os.path.join(out_dir, "source.blend")
            try:
                bpy.ops.wm.save_as_mainfile(filepath=blend_copy, copy=True)
                logger.info(f"Blend copy saved → {blend_copy}")
            except Exception as exc:
                logger.warning(f"Could not copy blend file: {exc}")

        # 6. Report
        n_ok  = len(compiled_modules)
        n_err = len(errors)
        msg   = f"✅ Compiled {n_ok} node group(s)"
        if n_err:
            msg += f", {n_err} failed (see system console)"
        msg += f". Output: {out_dir}"
        self.report({"INFO"}, msg)
        logger.info(f"Compile complete: {n_ok} ok, {n_err} failed.")

        return {"FINISHED"}
