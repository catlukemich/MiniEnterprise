import globs
from .tools_panel import ToolsPanel


class UI:

    def __init__(self):
        self.visible = False
        self.tools_panel = ToolsPanel()

    def show(self):
        self.visible = True
        globs.gui.add_widget(self.tools_panel)

    def hide(self):
        self.hidden = False
        globs.gui.remove_widget(self.tools_panel)