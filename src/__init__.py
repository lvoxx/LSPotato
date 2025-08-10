bl_info = {
    "name": "BPotato",
    "author": ("Lvoxx"),
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "3D View > Properties > BPotato",
    "description": "A collection of utility tools for the LSCherry project, including node group management and additional workflow helpers.",
    "category": "Tool",
}

if "bpy" in locals():
    import importlib

    importlib.reload(properties)
    importlib.reload(operators)
    importlib.reload(panels)
else:
    from . import properties, operators, panels

import bpy  # type: ignore

classes = [
    properties.BPotatoProperties,
    operators.ReplaceNodeGroups,
    operators.MakeLocalOperator,
    panels.BPotatoPanel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bpotato = bpy.props.PointerProperty(
        type=properties.BPotatoProperties
    )


def unregister():
    del bpy.types.Scene.bpotato
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
