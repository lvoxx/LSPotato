bl_info = {
    "name": "BPotato",
    "author": ("Lvoxx"),
    "version": (1, 0, 1),
    "blender": (4, 3, 0),
    "location": "3D View > Properties > BPotato",
    "description": "A collection of utility tools for the LSCherry project, including node group management and additional workflow helpers.",
    "category": "Tool",
}

import bpy  # type: ignore
from .features.find_lscherry.properties import LSCherryProperties
from .features.find_lscherry.operators import DownloadAndLinkLSCherry
from .features.replace_nodes.properties import BPotatoProperties
from .features.replace_nodes.operators import ReplaceNodeGroups
from .features.make_local.operators import MakeLocalOperator
from .features.panels import BPotatoPanel


rgt_classes = [
    LSCherryProperties,
    BPotatoProperties,
    DownloadAndLinkLSCherry,
    ReplaceNodeGroups,
    MakeLocalOperator,
    BPotatoPanel,
]


def register():
    for cls in rgt_classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bpotato = bpy.props.PointerProperty(type=BPotatoProperties)
    bpy.types.Scene.lscherry = bpy.props.PointerProperty(type=LSCherryProperties)


def unregister():
    del bpy.types.Scene.bpotato
    del bpy.types.Scene.lscherry

    for cls in reversed(rgt_classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
