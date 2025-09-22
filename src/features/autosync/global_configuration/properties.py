def toggle_autosync_global(self, context):
    """Callback when global autosync toggle changes"""
    from .sync import sync_global_settings, get_global_settings_state
    from ....utils.get_lscherry_things import has_lscherry_collection

    # Check if LSCherry collection exists before enabling
    if self.autosync_global_enabled and not has_lscherry_collection():
        self.autosync_global_enabled = False
        return

    if self.autosync_global_enabled:
        # Perform immediate sync for all objects
        sync_global_settings()
        
        # Initialize tracking data AFTER initial sync
        self.autosync_last_global_state = get_global_settings_state()


def update_global_blend_mode(self, context):
    """Callback when global blend mode changes"""
    if hasattr(self, 'autosync_global_enabled') and self.autosync_global_enabled:
        from .sync import sync_global_settings
        sync_global_settings()


def update_global_value_enhance(self, context):
    """Callback when global value enhance changes"""
    if hasattr(self, 'autosync_global_enabled') and self.autosync_global_enabled:
        from .sync import sync_global_settings
        sync_global_settings()


def update_global_world_color(self, context):
    """Callback when global world color changes"""
    if hasattr(self, 'autosync_global_enabled') and self.autosync_global_enabled:
        from .sync import sync_global_settings
        sync_global_settings()
    
def update_global_world_value_enhance(self, context):
    """Callback when global world value enhance changes"""
    if hasattr(self, 'autosync_global_enabled') and self.autosync_global_enabled:
        from .sync import sync_global_settings
        sync_global_settings()