from .Frame import Frame
from gui.controls.Box import Box
from gui.utils.Pad import *
from gui.utils.Vector2D import *
from gui.utils.utils import *
from gui.utils.Color import Color
from gui.controls.ImageButton import ImageButton
from gui.drawers.PressedBorderDrawer import PressedBorderDrawer


class Scrolls():
    VERTICAL = 1
    HORIZONTAL = 2
    HORIZONTAL_AND_VERTICAL = 4

    UP_ARROW_PATH = "gui/resources/up_arrow.png"
    DOWN_ARROW_PATH = "gui/resources/down_arrow.png"
    LEFT_ARROW_PATH = "gui/resources/left_arrow.png"
    RIGHT_ARROW_PATH = "gui/resources/right_arrow.png"

class ScrollUpArrow(ImageButton):

    def __init__(self, vertical_scrolls):
        ImageButton.__init__(self, load_image(Scrolls.UP_ARROW_PATH))
        self.pressed_border_drawer = PressedBorderDrawer(Color(150, 150, 150))
        self.vertical_scrolls = vertical_scrolls
        self.set_dimensions(11, 11)
        self.set_borders(Pad(0, 0, 0, 1))

    def on_click(self, event):
        old_percentage = self.vertical_scrolls.get_scroll_percentage()
        new_percentage = old_percentage - 10
        self.vertical_scrolls.scroll_to_percentage(new_percentage)


class ScrollDownArrow(ImageButton):
    def __init__(self, vertical_scrolls):
        ImageButton.__init__(self, load_image(Scrolls.DOWN_ARROW_PATH))
        self.pressed_border_drawer = PressedBorderDrawer(Color(150, 150, 150))
        self.vertical_scrolls = vertical_scrolls
        self.set_dimensions(11, 11)
        self.set_borders(Pad(0, 0, 1, 0))

    def on_click(self, event):
        old_percentage = self.vertical_scrolls.get_scroll_percentage()
        new_percentage = old_percentage + 10
        self.vertical_scrolls.scroll_to_percentage(new_percentage)


class VerticalKnob(Box):
    def __init__(self, vertical_scrolls):
        Box.__init__(self)
        self.vertical_scrolls = vertical_scrolls

        self.set_width(11)
        self.set_height(30)

        self.set_borders(Pad(0, 0, 1, 1))

    def on_drag(self, event):
        scrolls_height = self.vertical_scrolls.get_height()
        own_height = self.get_whole_height()
        up_arrow_height = self.vertical_scrolls.scroll_up_arrow.get_whole_height()
        down_arrow_height = self.vertical_scrolls.scroll_down_arrow.get_whole_height()

        mouse_rel_y = event.rel[1]
        own_pos = Vector2D(self.get_position())
        own_pos.y += mouse_rel_y

        if own_pos.y < up_arrow_height:
            own_pos.y = up_arrow_height
        if own_pos.y > scrolls_height - own_height - down_arrow_height:
            own_pos.y = scrolls_height - own_height - down_arrow_height

        self.set_position(own_pos)

        scroll_percentage = map_range(
            own_pos.y,
            up_arrow_height, scrolls_height - down_arrow_height - own_height,
            0, 100
        )
        self.vertical_scrolls.set_scroll_percentage(scroll_percentage)

    def draw(self, surface):
        Box.draw(self, surface)
        area = self.get_content_area()
        height = self.get_height()
        width = self.get_width()

        middle = round(height / 2.0)

        line1_co1 = (area.top_left.x + 2, area.top_left.y + middle - 2)
        line1_co2 = (area.top_left.x + width - 2, area.top_left.y + middle - 2)
        pygame.draw.line(surface, pygame.Color(0, 0, 0, 255), line1_co1, line1_co2)

        line2_co1 = (area.top_left.x + 2, area.top_left.y + middle)
        line2_co2 = (area.top_left.x + width - 2, area.top_left.y + middle)
        pygame.draw.line(surface, pygame.Color(0, 0, 0, 255), line2_co1, line2_co2)

        line3_co1 = (area.top_left.x + 2, area.top_left.y + middle + 2)
        line3_co2 = (area.top_left.x + width - 2, area.top_left.y + middle + 2)
        pygame.draw.line(surface, pygame.Color(0, 0, 0, 255), line3_co1, line3_co2)


class VerticalScrolls(Frame):
    def __init__(self, scroll_frame):
        Frame.__init__(self)
        self.scroll_frame = scroll_frame
        self.scroll_percentage = 0

        self.set_borders(Pad(1, 0, 0, 0))

        self.scroll_up_arrow = ScrollUpArrow(self)
        self.scroll_down_arrow = ScrollDownArrow(self)
        self.knob = VerticalKnob(self)

        Frame.add_widget(self, self.scroll_down_arrow)
        Frame.add_widget(self, self.scroll_up_arrow)
        Frame.add_widget(self, self.knob)

    def layout_widgets(self):
        Frame.layout_widgets(self)
        up_arrow_height = self.scroll_up_arrow.get_whole_height()
        self.knob.set_position(0, up_arrow_height)
        own_dimensions = self.get_dimensions()
        down_arrow_height = self.scroll_down_arrow.get_whole_height()
        self.knob.set_position(0, up_arrow_height)
        self.scroll_down_arrow.set_position(0, own_dimensions.y - down_arrow_height)

    def get_scroll_percentage(self):
        return self.scroll_percentage

    def set_scroll_percentage(self, percentage):
        self.scroll_percentage = percentage
        self.scroll_frame.set_vertical_scroll_percentage(percentage)

    def scroll_to_percentage(self, percentage):
        if percentage < 0: percentage = 0
        if percentage > 100: percentage = 100
        self.set_scroll_percentage(percentage)
        own_height = self.get_height()
        knob_height = self.knob.get_whole_height()
        up_arrow_height = self.scroll_up_arrow.get_whole_height()
        down_arrow_height = self.scroll_down_arrow.get_whole_height()

        new_knob_position = Vector2D()
        new_knob_position.x = 0
        new_knob_position.y = map_range(
            percentage,
            0, 100,
            up_arrow_height, own_height - down_arrow_height - knob_height
        )
        self.knob.set_position(0, new_knob_position.y)

    def set_dimensions(self, x, y=None):
        Frame.set_dimensions(self, x, y)


class ScrollLeftArrow(ImageButton):

    def __init__(self, horizontal_scrolls):
        ImageButton.__init__(self, load_image(Scrolls.LEFT_ARROW_PATH))
        self.pressed_border_drawer = PressedBorderDrawer(Color(150, 150, 150))
        self.horizontal_scrolls = horizontal_scrolls
        self.set_dimensions(11, 11)
        self.set_borders(Pad(0, 1, 0, 0))

    def on_click(self, event):
        old_percentage = self.horizontal_scrolls.get_scroll_percentage()
        new_percentage = old_percentage - 10
        self.horizontal_scrolls.scroll_to_percentage(new_percentage)


class ScrollRightArrow(ImageButton):
    def __init__(self, horizontal_scrolls):
        ImageButton.__init__(self, load_image(Scrolls.RIGHT_ARROW_PATH))
        self.pressed_border_drawer = PressedBorderDrawer(Color(150, 150, 150))
        self.horizontal_scrolls = horizontal_scrolls
        self.set_dimensions(11, 11)
        self.set_borders(Pad(1, 0, 0, 0))

    def on_click(self, event):
        old_percentage = self.horizontal_scrolls.get_scroll_percentage()
        new_percentage = old_percentage + 10
        self.horizontal_scrolls.scroll_to_percentage(new_percentage)


class HorizontalKnob(Box):
    def __init__(self, horizontal_scrolls):
        Box.__init__(self)
        self.horizontal_scrolls = horizontal_scrolls

        self.set_width(30)
        self.set_height(11)

        self.set_borders(Pad(1, 1, 0, 0))

    def on_drag(self, event):

        scrolls_width = self.horizontal_scrolls.get_width()
        own_width = self.get_whole_width()
        left_arrow_width = self.horizontal_scrolls.scroll_left_arrow.get_whole_width()
        right_arrow_width = self.horizontal_scrolls.scroll_right_arrow.get_whole_width()

        mouse_rel_x = event.rel[0]
        own_pos = Vector2D(self.get_position())
        own_pos.x += mouse_rel_x

        if own_pos.x < left_arrow_width:
            own_pos.x = left_arrow_width
        if own_pos.x > scrolls_width - own_width - right_arrow_width:
            own_pos.x = scrolls_width - own_width - right_arrow_width

        self.set_position(own_pos)

        scroll_percentage = map_range(
            own_pos.x,
            left_arrow_width, scrolls_width - right_arrow_width - own_width,
            0, 100
        )

        self.horizontal_scrolls.set_scroll_percentage(scroll_percentage)

    def draw(self, surface):
        Box.draw(self, surface)
        area = self.get_content_area()
        height = self.get_height()
        width = self.get_width()

        middle = round(width / 2.0)

        line1_co1 = (area.top_left.x + middle - 2, area.top_left.y + 2)
        line1_co2 = (area.top_left.x + middle - 2, area.top_left.y + height - 2)
        pygame.draw.line(surface, pygame.Color(0, 0, 0, 255), line1_co1, line1_co2)

        line2_co1 = (area.top_left.x + middle, area.top_left.y + 2)
        line2_co2 = (area.top_left.x + middle, area.top_left.y + height - 2)
        pygame.draw.line(surface, pygame.Color(0, 0, 0, 255), line2_co1, line2_co2)

        line3_co1 = (area.top_left.x + middle + 2, area.top_left.y + 2)
        line3_co2 = (area.top_left.x + width - 2, area.top_left.y + middle + 2)
        line3_co2 = (area.top_left.x + middle + 2, area.top_left.y + height - 2)
        pygame.draw.line(surface, pygame.Color(0, 0, 0, 255), line3_co1, line3_co2)


class HorizontalScrolls(Frame):
    def __init__(self, scroll_frame):
        Frame.__init__(self)
        self.scroll_frame = scroll_frame
        self.scroll_percentage = 0

        self.set_borders(Pad(0, 0, 1, 0))

        self.scroll_left_arrow = ScrollLeftArrow(self)
        self.scroll_right_arrow = ScrollRightArrow(self)
        self.knob = HorizontalKnob(self)

        Frame.add_widget(self, self.scroll_left_arrow)
        Frame.add_widget(self, self.scroll_right_arrow)
        Frame.add_widget(self, self.knob)

    def layout_widgets(self):
        Frame.layout_widgets(self)
        own_dimensions = self.get_dimensions()

        left_arrow_width = self.scroll_left_arrow.get_whole_width()
        right_arrow_width = self.scroll_right_arrow.get_whole_width()

        self.knob.set_position(left_arrow_width, 0)

        self.scroll_right_arrow.set_position(own_dimensions.x - right_arrow_width, 0)

    def get_scroll_percentage(self):
        return self.scroll_percentage

    def set_scroll_percentage(self, percentage):
        self.scroll_percentage = percentage
        self.scroll_frame.set_horizontal_scroll_percentage(percentage)

    def scroll_to_percentage(self, percentage):
        if percentage < 0: percentage = 0
        if percentage > 100: percentage = 100
        self.set_scroll_percentage(percentage)
        own_width = self.get_width()
        knob_width = self.knob.get_whole_width()
        left_arrow_width = self.scroll_left_arrow.get_whole_width()
        right_arrow_width = self.scroll_right_arrow.get_whole_width()

        new_knob_position = Vector2D()
        new_knob_position.y = 0
        new_knob_position.x = map_range(
            percentage,
            0, 100,
            left_arrow_width, own_width - right_arrow_width - knob_width
        )
        self.knob.set_position(new_knob_position.x, 0)


class ScrollFrame(Frame):
    def __init__(self, scrolls=Scrolls.HORIZONTAL_AND_VERTICAL):
        Frame.__init__(self)

        self.horizontal_scroll_percentage = 0
        self.vertical_scroll_percentage = 0

        self.inner_frame = Frame()
        self.inner_frame.set_margins(EqualPad(0))
        self.inner_frame.set_borders(EqualPad(0))
        self.inner_frame.set_paddings(EqualPad(0))
        self.inner_frame.set_border_drawer(None)
        self.inner_frame.set_background_drawer(None)
        Frame.add_widget(self, self.inner_frame)

        self.horizontal_scrolls = None
        self.vertical_scrolls = None
        self.filler = None
        if scrolls & Scrolls.VERTICAL:
            self.vertical_scrolls = VerticalScrolls(self)
            self.vertical_scrolls.set_width(11)
        if scrolls & Scrolls.HORIZONTAL:
            self.horizontal_scrolls = HorizontalScrolls(self)
            self.horizontal_scrolls.set_height(11)
        if scrolls & Scrolls.HORIZONTAL_AND_VERTICAL:
            self.vertical_scrolls = VerticalScrolls(self)
            self.vertical_scrolls.set_width(11)
            self.horizontal_scrolls = HorizontalScrolls(self)
            self.horizontal_scrolls.set_height(11)
            self.filler = Box()

        if self.vertical_scrolls != None:
            Frame.add_widget(self, self.vertical_scrolls)
        if self.horizontal_scrolls != None:
            Frame.add_widget(self, self.horizontal_scrolls)
        if self.filler != None:
            pass
        Frame.add_widget(self, self.filler)

    def set_layout(self, layout):
        self.inner_frame.set_layout(layout)

    def set_paddings(self, paddings):
        self.inner_frame.set_paddings(paddings)

    def add_widget(self, widget):
        self.inner_frame.add_widget(widget)

    def remove_widget(self, widget):
        self.inner_frame.remove_widget(widget)

    def set_dimensions(self, x, y=None):
        Frame.set_dimensions(self, x, y)
        own_dimensions = self.get_dimensions()

        if self.vertical_scrolls != None and self.horizontal_scrolls != None:
            horizontal_scrolls_height = self.horizontal_scrolls.get_whole_height()
            vertical_scrolls_width = self.vertical_scrolls.get_whole_width()
            vertical_scrolls_height = own_dimensions.y - horizontal_scrolls_height
            horizontal_scrolls_width = own_dimensions.x - vertical_scrolls_width

            self.vertical_scrolls.set_height(vertical_scrolls_height)
            self.horizontal_scrolls.set_width(horizontal_scrolls_width)

            self.filler.set_dimensions(vertical_scrolls_width, horizontal_scrolls_height)

        if self.vertical_scrolls != None and self.horizontal_scrolls == None:
            vertical_scrolls_height = own_dimensions.y
            self.vertical_scrolls.set_height(vertical_scrolls_height)

        if self.horizontal_scrolls != None and self.vertical_scrolls == None:
            horizontal_scrolls_width = own_dimensions.x
            self.horizontal_scrolls.set_width(horizontal_scrolls_width)

    def set_vertical_scroll_percentage(self, percentage):
        self.vertical_scroll_percentage = percentage
        frame_height = self.inner_frame.get_whole_height()
        own_height = self.get_height()
        if self.horizontal_scrolls != None:
            own_height = self.get_height() - self.horizontal_scrolls.get_height()

        delta_height = frame_height - own_height
        if delta_height < 0: return
        scroll_amount = map_range(self.vertical_scroll_percentage,
                                  0, 100,
                                  0, -delta_height
                                  )
        inner_frame_pos = Vector2D(self.inner_frame.get_position())
        inner_frame_pos.y = scroll_amount
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

    def layout_widgets(self):
        own_dimensions = self.get_dimensions()

        if self.vertical_scrolls != None and self.horizontal_scrolls != None:
            vertical_scrolls_width = self.vertical_scrolls.get_whole_width()
            vertical_scrolls_left = own_dimensions.x - vertical_scrolls_width
            self.vertical_scrolls.set_position(vertical_scrolls_left, 0)

            horizontal_scrolls_height = self.horizontal_scrolls.get_whole_height()
            horizontal_scrolls_top = own_dimensions.y - horizontal_scrolls_height
            self.horizontal_scrolls.set_position(0, horizontal_scrolls_top)

            self.filler.set_position(
                own_dimensions.x - vertical_scrolls_width,
                own_dimensions.y - horizontal_scrolls_height
            )
        if self.horizontal_scrolls != None and self.vertical_scrolls == None:
            horizontal_scrolls_height = self.horizontal_scrolls.get_whole_height()
            horizontal_scrolls_top = own_dimensions.y - horizontal_scrolls_height

            self.horizontal_scrolls.set_position(0, horizontal_scrolls_top)

        if self.vertical_scrolls != None and self.horizontal_scrolls == None:
            vertical_scrolls_width = self.vertical_scrolls.get_whole_width()
            vertical_scrolls_left = own_dimensions.x - vertical_scrolls_width

            self.vertical_scrolls.set_position(vertical_scrolls_left, 0)

    def resize_to_fit(self):
        return
