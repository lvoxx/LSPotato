bl_info = {
    "name": "LSPotato",
    "author": ("Lvoxx"),
    "version": (1, 0, 3),
    "blender": (4, 3, 0),
    "location": "3D View > Properties > LSPotato",
    "description": "A collection of utility tools for the LSCherry project, including node groups management and additional workflow helpers.",
    "category": "Tool",
}

import bpy  # type: ignore
from .features.find_lscherry.properties import LSCherryProperties
from .features.find_lscherry.operators import DownloadAndLinkLSCherry, RepairLSCherry, CleanDiskLSCherry
from .features.replace_nodes.properties import LSPotatoProperties
from .features.replace_nodes.operators import ReplaceNodeGroups
from .features.make_local.operators import MakeLocalOperator
from .features.panels import LSPotatoPanel


rgt_classes = [
    LSCherryProperties,
    LSPotatoProperties,
    DownloadAndLinkLSCherry,
    RepairLSCherry,
    CleanDiskLSCherry,
    ReplaceNodeGroups,
    MakeLocalOperator,
    LSPotatoPanel,
]


def register():
    for cls in rgt_classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.lspotato = bpy.props.PointerProperty(type=LSPotatoProperties)
    bpy.types.Scene.lscherry = bpy.props.PointerProperty(type=LSCherryProperties)


def unregister():
    del bpy.types.Scene.lspotato
    del bpy.types.Scene.lscherry

    for cls in reversed(rgt_classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
