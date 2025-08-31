import bpy  # type: ignore


def draw_update_notification(layout, context):
    """Draw update notification UI"""
    props = context.scene.lspotato.github_updater

    # Show update notification if available and not dismissed
    if props.update_available and not props.update_dismissed:
        box = layout.box()
        box.alert = True  # Red background

        # Header row with title and dismiss button
        row = box.row()
        row.label(text=f"Update available ({props.latest_version})", icon="INFO")

        # Dismiss button
        dismiss_row = row.row()
        dismiss_row.alignment = "RIGHT"
        dismiss_row.scale_x = 1.2
        dismiss_row.operator("lspotato.dismiss_update", text="", icon="X", emboss=True)

        # Update button
        update_row = box.row()
        update_row.scale_y = 1.2
        update_row.operator("lspotato.install_update", text="Update now", icon="IMPORT")

    # Manual check button (always available)
    row = layout.row()
    if props.checking_update:
        row.label(text="Checking for updates...", icon="FILE_REFRESH")
    else:
        row.operator(
            "lspotato.check_updates", text="Check for Updates", icon="FILE_REFRESH"
        )
