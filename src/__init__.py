if "bpy" in locals():
    import importlib
    importlib.reload(properties)
    importlib.reload(operators)
    importlib.reload(panels)
else:
    from . import properties
    from . import operators
    from . import panels

import bpy # type: ignore

classes = [
    properties.BPotatoProperties,
    operators.ReplaceNodeGroups,
    operators.MakeLocalOperator,
    panels.BPotatoPanel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bpotato = bpy.props.PointerProperty(type=properties.BPotatoProperties)

def unregister():
    del bpy.types.Scene.bpotato
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()