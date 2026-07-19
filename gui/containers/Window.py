from gui.containers.ScrollFrame import *
from gui.controls.Label import Label
from gui.drawers.BackgroundDrawer import BackgroundDrawer
from gui.drawers.BorderDrawer import BorderDrawer
from gui.controls.Box import Box
from gui.controls.ImageButton import ImageButton
from gui.utils.utils import *
import pygame


class Window(Frame):

    CLOSE_BUTTON_PATH = "gui/resources/close_button_normal.png"

    def __init__(self, label_text):
        Frame.__init__(self)

        self.label = WindowLabel(label_text, self)
        self.label.set_text_color(Color(255, 255, 255))
        self.label.set_background_drawer(BackgroundDrawer())
        self.label.set_background_color(Color(0, 0, 0))
        self.label.set_border_drawer(BorderDrawer())
        self.label.set_borders(Pad(0, 0, 0, 1))
        self.label.set_paddings(Pad(2, 2, 0, 0))

        self.close_button = CloseButton(self)

        self.horizontal_scroll_percentage = 0
        self.vertical_scroll_percentage = 0

        self.inner_frame = Frame()
        self.inner_frame.set_margins(EqualPad(0))
        self.inner_frame.set_borders(EqualPad(0))
        self.inner_frame.set_paddings(EqualPad(0))
        self.inner_frame.set_border_drawer(None)
        self.inner_frame.set_background_drawer(None)
        Frame.add_widget(self, self.inner_frame)

        Frame.add_widget(self, self.label)
        Frame.add_widget(self, self.close_button)

        self.vertical_scrolls = WindowVerticalScrolls(self)
        self.horizontal_scrolls = WindowHorizontalScrolls(self)
        self.vertical_scrolls.set_width(11)
        self.horizontal_scrolls.set_height(11)
        self.filler = ResizeKnob(self)

        Frame.add_widget(self, self.vertical_scrolls)
        Frame.add_widget(self, self.horizontal_scrolls)
        Frame.add_widget(self, self.filler)

        self.set_vertical_scroll_percentage(0)

    def set_layout(self, layout):
        self.inner_frame.set_layout(layout)

    def set_paddings(self, paddings):
        self.inner_frame.set_paddings(paddings)

    def add_widget(self, widget):
        self.inner_frame.add_widget(widget)

    def remove_widget(self, widget):
        self.inner_frame.remove_widget(widget)

    def layout_widgets(self):
        own_dimensions = self.get_dimensions()

        self.reposition_close_button()

        label_height = self.label.get_whole_height()

        vertical_scrolls_top = label_height
        vertical_scrolls_width = self.vertical_scrolls.get_whole_width()
        vertical_scrolls_left = own_dimensions.x - vertical_scrolls_width
        self.vertical_scrolls.set_position(vertical_scrolls_left, label_height)

        horizontal_scrolls_height = self.horizontal_scrolls.get_whole_height()
        horizontal_scrolls_top = own_dimensions.y - horizontal_scrolls_height
        self.horizontal_scrolls.set_position(0, horizontal_scrolls_top)

        self.filler.set_position(
            own_dimensions.x - vertical_scrolls_width,
            own_dimensions.y - horizontal_scrolls_height
        )

    def set_dimensions(self, x, y=None):
        Frame.set_dimensions(self, x, y)

        own_dimensions = self.get_dimensions()
        label_paddings = self.label.get_paddings()

        self.reposition_close_button()

        self.label.set_width(own_dimensions.x - label_paddings.left - label_paddings.right)

        horizontal_scrolls_height = self.horizontal_scrolls.get_whole_height()
        vertical_scrolls_width = self.vertical_scrolls.get_whole_width()

        label_height = self.label.get_whole_height()
        vertical_scrolls_height = own_dimensions.y - horizontal_scrolls_height - label_height
        horizontal_scrolls_width = own_dimensions.x - vertical_scrolls_width

        inner_frame_dims = self.inner_frame.get_dimensions()
        inner_frame_pos = Vector2D(self.inner_frame.get_position())
        view_dimensions_width = own_dimensions.x - vertical_scrolls_width
        view_dimensions_height = own_dimensions.y - horizontal_scrolls_height - label_height
        inner_frame_visible_y = inner_frame_dims.y + inner_frame_pos.y - label_height
        if inner_frame_pos.y < label_height and inner_frame_visible_y < view_dimensions_height:
            delta_y = view_dimensions_height - inner_frame_visible_y
            inner_frame_pos.y += delta_y
            if inner_frame_pos.y > label_height: inner_frame_pos.y = label_height
            self.inner_frame.set_position(inner_frame_pos)

        inner_frame_visible_x = inner_frame_dims.x + inner_frame_pos.x
        if inner_frame_pos.x < 0 and inner_frame_visible_x < view_dimensions_width:
            delta_x = view_dimensions_width - inner_frame_visible_x
            inner_frame_pos.x += delta_x
            if inner_frame_pos.x > 0: inner_frame_pos.x = 0
            self.inner_frame.set_position((inner_frame_pos))

        self.filler.set_dimensions(vertical_scrolls_width, horizontal_scrolls_height)

        self.vertical_scrolls.set_height(vertical_scrolls_height)
        self.horizontal_scrolls.set_width(horizontal_scrolls_width)

    def reposition_close_button(self):
        own_dimensions = self.get_dimensions()

        label_height = self.label.get_whole_height()
        close_button_width = self.close_button.get_width()
        close_button_height = self.close_button.get_height()
        delta_height = label_height - close_button_height
        offset = delta_height / 2
        self.close_button.set_position(
            own_dimensions.x - close_button_width,
            offset
        )

    def set_vertical_scroll_percentage(self, percentage):
        self.vertical_scroll_percentage = percentage
        frame_height = self.inner_frame.get_whole_height()
        own_height = self.get_height()
        if self.horizontal_scrolls != None:
            own_height = self.get_height() - self.horizontal_scrolls.get_height() - self.label.get_whole_height()

        delta_height = frame_height - own_height
        if delta_height < 0: return
        scroll_amount = map_range(self.vertical_scroll_percentage,
                                  0, 100,
                                  0, -delta_height
                                  )
        inner_frame_pos = Vector2D(self.inner_frame.get_position())
        inner_frame_pos.y = scroll_amount + self.label.get_whole_height()
        self.inner_frame.set_position(inner_frame_pos)

    def set_horizontal_scroll_percentage(self, percentage):
        self.horizontal_scroll_percentage = percentage
        frame_width = self.inner_frame.get_whole_width()
        own_width = self.get_width()
        if self.vertical_scrolls != None:
            own_width = self.get_width() - self.vertical_scrolls.get_width()

        delta_width = frame_width - own_width
        if delta_width < 0: return
        scroll_amount = map_range(self.horizontal_scroll_percentage,
                                  0, 100,
                                  0, -delta_width
                                  )
        inner_frame_pos = Vector2D(self.inner_frame.get_position())
        inner_frame_pos.x = scroll_amount
        self.inner_frame.set_position(inner_frame_pos)

    def resize_to_fit(self):
        return


class WindowLabel(Label):
    def __init__(self, text, window):
        Label.__init__(self, text)
        self.window = window

    def on_drag(self, event):
        position = Vector2D(self.window.get_position())
        position.x += event.rel[0]
        position.y += event.rel[1]
        self.window.set_position(position)


class CloseButton(ImageButton):

    def __init__(self, window):
        ImageButton.__init__(
            self,
            load_image("gui/resources/close_button_normal.png")

        )
        self.window = window

        self.set_dimensions(11, 14)
        self.set_borders(EqualPad(0))

    def on_click(self, event):
        ImageButton.on_click(self, event)
        window_parent = self.window.get_parent()
        window_parent.remove_widget(self.window)


class WindowHorizontalScrolls(HorizontalScrolls):
    def __init__(self, window):
        HorizontalScrolls.__init__(self, window)

    def layout_widgets(self):
        Frame.layout_widgets(self)
        own_dimensions = self.get_dimensions()

        left_arrow_width = self.scroll_left_arrow.get_whole_width()
        right_arrow_width = self.scroll_right_arrow.get_whole_width()

        inner_frame_pos = self.scroll_frame.inner_frame.get_position()
        inner_frame_dims = self.scroll_frame.inner_frame.get_dimensions()
        view_width = self.scroll_frame.get_width() - self.scroll_frame.vertical_scrolls.get_whole_width()
        scroll_width = inner_frame_dims.x - view_width
        if scroll_width > 0:
            scroll_percentage = map_range(inner_frame_pos.x,
                                          0, -scroll_width,
                                          0, 100
                                          )
            rails_width = own_dimensions.x - left_arrow_width - right_arrow_width
            knob_width = self.knob.get_whole_width()
            knob_x = map_range(scroll_percentage,
                               0, 100,
                               left_arrow_width, left_arrow_width + rails_width - knob_width
                               )

            self.knob.set_position(knob_x, 0)
        else:
            self.knob.set_position(left_arrow_width, 0)
        self.scroll_right_arrow.set_position(own_dimensions.x - right_arrow_width, 0)


class WindowVerticalScrolls(VerticalScrolls):
    def __init__(self, window):
        VerticalScrolls.__init__(self, window)

    def layout_widgets(self):
        Frame.layout_widgets(self)
        up_arrow_height = self.scroll_up_arrow.get_whole_height()
        self.knob.set_position(0, up_arrow_height)
        own_dimensions = self.get_dimensions()
        down_arrow_height = self.scroll_down_arrow.get_whole_height()

        if hasattr(self.scroll_frame, "horizontal_scrolls"):
            inner_frame_pos = self.scroll_frame.inner_frame.get_position()
            inner_frame_dims = self.scroll_frame.inner_frame.get_dimensions()
            label_height = self.scroll_frame.label.get_whole_height()
            view_height = self.scroll_frame.get_height() - self.scroll_frame.horizontal_scrolls.get_whole_height() - label_height
            scroll_height = inner_frame_dims.y - view_height
            if scroll_height > 0:
                scroll_percentage = map_range(inner_frame_pos.y - label_height,
                                              0, -scroll_height,
                                              0, 100
                                              )

                rails_height = own_dimensions.y - up_arrow_height - down_arrow_height
                knob_height = self.knob.get_whole_height()
                knob_y = map_range(scroll_percentage,
                                   0, 100,
                                   up_arrow_height, up_arrow_height + rails_height - knob_height
                                   )

                self.knob.set_position(0, knob_y)
            else:
                self.knob.set_position(0, up_arrow_height)

        self.scroll_down_arrow.set_position(0, own_dimensions.y - down_arrow_height)


class ResizeKnob(Box):

    def __init__(self, window):
        Box.__init__(self)
        self.window = window

    def draw(self, surface):
        Box.draw(self, surface)
        content_area = self.get_content_area()
        line1_start_x = content_area.bottom_right.x
        line1_start_y = content_area.bottom_right.y - 12
        line1_end_x = content_area.bottom_right.x - 12
        line1_end_y = content_area.bottom_right.y
        pygame.draw.aaline(surface, (0, 0, 0), (line1_start_x, line1_start_y), (line1_end_x, line1_end_y))

        line2_start_x = content_area.bottom_right.x
        line2_start_y = content_area.bottom_right.y - 8
        line2_end_x = content_area.bottom_right.x - 8
        line2_end_y = content_area.bottom_right.y
        pygame.draw.aaline(surface, (0, 0, 0), (line2_start_x, line2_start_y), (line2_end_x, line2_end_y))

        line3_start_x = content_area.bottom_right.x
        line3_start_y = content_area.bottom_right.y - 3
        line3_end_x = content_area.bottom_right.x - 3
        line3_end_y = content_area.bottom_right.y
        pygame.draw.aaline(surface, (0, 0, 0), (line3_start_x, line3_start_y), (line3_end_x, line3_end_y))

    def on_drag(self, event):
        window_dimensions = Vector2D(self.window.get_dimensions())
        window_dimensions.x += event.rel[0]
        window_dimensions.y += event.rel[1]
        self.window.set_dimensions(window_dimensions)


