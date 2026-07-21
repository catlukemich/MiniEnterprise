import pygame

from ..utils.Vector2D import *

from ..Style import *

# A base background drawer class. Draws a simple solid background.
class BackgroundDrawer():

  def __init__(self, color = None):
    if color == None:
      self.color = Style.background_color
    else:
      self.color = color

  def set_color(self, color):
    self.color = color


  def draw_background(self, widget, surface):
    absolute_position = widget.calc_absolute_position()

    margin = widget.get_margins()
    border = widget.get_borders()
    padding = widget.get_paddings()
    dimensions = widget.get_dimensions()

    # Drawing background:
    background_top_left = Vector2D(
      absolute_position.x + margin.left + border.left, 
      absolute_position.y + margin.top + border.top)
    background_bottom_right = Vector2D(
      absolute_position.x + margin.left + border.left + padding.left + dimensions.x + padding.right ,
      absolute_position.y + margin.top + border.top + padding.top + dimensions.y + padding.bottom , )
    
    draw_width = background_bottom_right.x - background_top_left.x
    draw_height = background_bottom_right.y - background_top_left.y

    background_rect = pygame.Rect(background_top_left.x, background_top_left.y, draw_width, draw_height)
    
    pygame_color = pygame.Color(self.color.red, self.color.green, self.color.blue, self.color.alpha)
    pygame.draw.rect(surface, pygame_color, background_rect )
