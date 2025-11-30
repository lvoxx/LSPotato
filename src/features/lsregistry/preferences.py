import bpy  # type: ignore
from bpy.types import AddonPreferences # type: ignore
from bpy.props import StringProperty # type: ignore


class LSPotatoPreferences(AddonPreferences):
    """Addon preferences for LSPotato including GitHub credentials"""
    bl_idname = "LSPotato"  # Must match your addon folder name exactly
    
    # GitHub token for private repositories
    github_token_default: StringProperty(
        name="Default GitHub Token",
        description="GitHub personal access token for accessing private repositories",
        default="",
        subtype='PASSWORD'
    )
    
    # You can add more credential fields as needed
    # github_token_custom: StringProperty(...)
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="GitHub Credentials", icon='KEYINGSET')  # Changed from 'KEY'
        box.prop(self, "github_token_default")
        
        box.label(text="Generate tokens at: https://github.com/settings/tokens", icon='URL')
        box.label(text="Required scopes: repo (for private repos)")