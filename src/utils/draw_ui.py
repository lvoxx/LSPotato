import bpy  # type: ignore
import textwrap


def show_custom_popup(message, title="Notification", icon="INFO"):
    """Display a custom popup notification with the given message.

    Args:
        message (str): The message to display in the popup.
        title (str, optional): The title of the popup. Defaults to "Notification".
        icon (str, optional): The icon to use (e.g., 'INFO', 'ERROR', 'WARNING'). Defaults to 'INFO'.
    """

    def draw_popup(self, context):
        layout = self.layout
        wrapped = textwrap.wrap(message, width=40)  # Wrap text to fit popup
        for line in wrapped:
            layout.label(text=line)

    bpy.context.window_manager.popup_menu(draw_popup, title=title, icon=icon)
