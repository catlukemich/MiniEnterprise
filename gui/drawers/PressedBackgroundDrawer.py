from gui.drawers.BackgroundDrawer import *


class PressedBackgroundDrawer(BackgroundDrawer):
  def __init__(self, bg_color = None, shadow_color = None):
    BackgroundDrawer.__init__(self, bg_color)
    if shadow_color == None:
      self.shadow_color = Style.pressed_shadow_color
    else:
      self.shadow_color = shadow_color

  def draw_background(self, widget, surface):
    BackgroundDrawer.draw_background(self, widget, surface)
    padded_area = widget.get_padded_area()
    pygame_color = pygame.Color(self.shadow_color.red, self.shadow_color.green, self.shadow_color.blue, self.shadow_color.alpha)
    
    # Draw the left shadow:
    start_x = padded_area.top_left.x
    end_x = start_x + 2
    start_y = padded_area.top_left.y
    end_y = padded_area.bottom_right.y
    width = end_x - start_x
    height = end_y - start_y
    
    draw_rect = pygame.Rect(start_x, start_y, width, height)
    pygame.draw.rect(surface, pygame_color, draw_rect)

    # Draw the top shadow:
    start_x = padded_area.top_left.x
    end_x = padded_area.bottom_right.x
    start_y = padded_area.top_left.y
    end_y = start_y + 2
    width = end_x - start_x
    height = end_y - start_y

    draw_rect = pygame.Rect(start_x, start_y, width, height)
    pygame.draw.rect(surface, pygame_color, draw_rect)
    