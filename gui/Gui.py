from gui.utils.Input import *
from gui.containers.Frame import *
from .utils.Pad import *


class Gui(Container, MouseListener, KeyboardListener):
    def __init__(self, input):
        Container.__init__(self)
        self.hover_widget = None
        self.focus_widget = None
        self.active_widget = None
        self.drag_widget = None

        self.set_margins(EqualPad(0))
        self.set_borders(EqualPad(0))
        self.set_paddings(EqualPad(0))

    def mouse_button_down(self, event):
        if self.hover_widget != None:
            event_consumed = self.hover_widget.on_mouse_button_down(event)
            self.drag_widget = self.hover_widget
            if event_consumed:
                return True

        old_focus = self.focus_widget
        new_focus = self.hover_widget
        if old_focus != None:
            old_focus.on_focus_lost(event)
        if new_focus != None:
            new_focus.on_focus_gain(event)

        self.focus_widget = self.hover_widget
        self.active_widget = self.hover_widget

        return False

    def mouse_motion(self, event):
        event_consumed = False
        if self.drag_widget != None:
            event_consumed = self.drag_widget.on_drag(event)
            if event_consumed:
                return True  # The event is consumed by dragging a widget.

        old_hover_widget = self.hover_widget
        new_hover_widget = self.find_hover_widget(event.pos[0], event.pos[1])
        if new_hover_widget != old_hover_widget:

            if old_hover_widget != None:
                event_consumed = old_hover_widget.on_mouse_out(event)

            if new_hover_widget != None:
                event_consumed = new_hover_widget.on_mouse_over(event)

            self.hover_widget = new_hover_widget
            if event_consumed:
                return True

        if (
            old_hover_widget == new_hover_widget
            and old_hover_widget != None
            and new_hover_widget != None
        ):
            event_consumed = self.hover_widget.on_mouse_move(event)
            if event_consumed:
                return True

        return False

    def find_hover_widget(self, mouse_x, mouse_y, parent=None):
        if parent == None:
            widgets = self.get_widgets()
        else:
            widgets = parent.get_widgets()

        widgets = reversed(widgets)

        for widget in widgets:
            if isinstance(widget, Container):
                hover_widget = self.find_hover_widget(mouse_x, mouse_y, widget)
                if hover_widget == None:
                    parent_area = widget.get_bordered_area()
                    if isinstance(widget, Frame):
                        parent_area = widget.get_hover_rectangle()
                    mouse = Vector2D(mouse_x, mouse_y)
                    if parent_area.contains_point(mouse):
                        return widget
                else:
                    return hover_widget
            else:
                widget_area = widget.get_bordered_area()
                mouse = Vector2D(mouse_x, mouse_y)

                if parent != None and isinstance(parent, Frame):
                    parent_hover_rectangle = parent.get_hover_rectangle()
                    target_area = widget_area.intersection(parent_hover_rectangle)
                    if target_area.contains_point(mouse):
                        return widget
                else:
                    if widget_area.contains_point(mouse):
                        return widget

        return None

    def mouse_button_up(self, event):
        event_consumed = False

        self.drag_widget = None

        if self.hover_widget != None:
            event_consumed = self.hover_widget.on_mouse_button_up(event)
        if (
            self.hover_widget != None
            and self.active_widget != None
            and self.hover_widget == self.active_widget
        ):
            event_consumed = self.active_widget.on_click(event)

        return event_consumed

    def on_window_resize(self, event):
        print(event)
        for widget in self.widgets:
            widget.on_window_resize(event)

    def key_down(self, event):
        event_consumed = False
        if self.focus_widget != None:
            event_consumed = self.focus_widget.on_key_down(event)
        return event_consumed
