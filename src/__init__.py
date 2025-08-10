bl_info = {
    "name": "BPotato",
    "author": ("Lvoxx"),
    "version": (1, 0, 0),
    "blender": (4, 3, 0),  
    "location": "View3D > Sidebar > BPotato",
    "description": "A collection of utility tools for the LSCherry project, including node group management and additional workflow helpers.",
    "category": "Tool",
}

from .operators import GenerateLinkedGraphOperator
from .panels import LinkedGraphPanel
import bpy
from operators import *

def register():
    bpy.utils.register_class(LinkedGraphPanel)
    bpy.utils.register_class(GenerateLinkedGraphOperator)
    bpy.utils.register_class(BrowseWorkspaceOperator)
    bpy.utils.register_class(LinkedGraphProperties)
    bpy.types.Scene.linked_graph_props = bpy.props.PointerProperty(type=LinkedGraphProperties)

def unregister():
    bpy.utils.unregister_class(LinkedGraphPanel)
    bpy.utils.unregister_class(GenerateLinkedGraphOperator)
    bpy.utils.unregister_class(BrowseWorkspaceOperator)
    bpy.utils.unregister_class(LinkedGraphProperties)
    del bpy.types.Scene.linked_graph_props

if __name__ == "__main__":
    register()