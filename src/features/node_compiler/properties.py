"""
NodeCompiler Properties
Scene-level properties for the Dev Mode / NodeCompiler feature.
"""

import bpy  # type: ignore


class NodeCompilerProperties(bpy.types.PropertyGroup):
    compiled_folder: bpy.props.StringProperty(
        name="Output Folder",
        description="Destination folder for compiled node files (relative to the .blend file)",
        default="./compiled",
        subtype="DIR_PATH",
    )  # type: ignore

    include_nested: bpy.props.BoolProperty(
        name="Include Nested Groups",
        description="Recursively compile node groups that are used inside other groups",
        default=True,
    )  # type: ignore

    copy_blend: bpy.props.BoolProperty(
        name="Copy .blend File",
        description="Save a copy of the current .blend file into the output folder",
        default=True,
    )  # type: ignore

    compile_geometry: bpy.props.BoolProperty(
        name="Compile Geometry Nodes",
        description=(
            "Also export geometry node groups into <output>/geometry/ as a "
            "library.blend + hashes.json (instead of generating Python)."
        ),
        default=True,
    )  # type: ignore
