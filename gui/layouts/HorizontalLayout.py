from .Layout import *
from ..utils.Vector2D import *
from ..utils.Alignment import *


class HorizontalLayout(Layout):
  
  def layout_widgets(self, parent):
    widgets = parent.get_widgets()
    if len(widgets) == 0: return
    
    # Calculate the row height:
    row_height = 0
    for widget in widgets:
      height = widget.get_whole_height()
      if height > row_height: row_height = height
    
    row_width = 0
    for widget in widgets:
      width = widget.get_whole_width()
      row_width += width

    parent_size = parent.get_content_size()
    parent_offset_vector  = Aligner.get_alignment_offset(
      parent_size.x, parent_size.y, 
      row_width, row_height, Align.CENTER)

    current_x = 0
    for widget in widgets:
      widget_size = widget.get_whole_size()
      widget_align = widget.get_align()
      widget_offset_vector = Aligner.get_alignment_offset(
        0, row_height, 0, widget_size.y, widget_align
      )
      position_x = current_x + parent_offset_vector.x + widget_offset_vector.x
      position_y = parent_offset_vector.y + widget_offset_vector.y
      widget.set_position(position_x, position_y)
      
      current_x += widget_size.x

  def get_width(self, parent):
    widgets = parent.get_widgets()
    if len(widgets) == 0: return
    
    row_width = 0
    for widget in widgets:
      width = widget.get_whole_width()
      row_width += width

    return row_width

  def get_height(self, parent):
    widgets = parent.get_widgets()
    if len(widgets) == 0: return
    
    # Calculate the row height:
    row_height = 0
    for widget in widgets:
      height = widget.get_whole_height()
      if height > row_height: row_height = height
    
    return row_height

