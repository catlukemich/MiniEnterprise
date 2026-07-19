from .Layout import *
from ..utils.Vector2D import *
from ..utils.Alignment import *


class VerticalLayout(Layout):
  
  def layout_widgets(self, parent):
    widgets = parent.get_widgets()
    if len(widgets) == 0: return
    
    # Calculate the column width:
    col_width = 0
    for widget in widgets:
      width = widget.get_whole_width()
      if width > col_width: col_width = width
    
  
    col_height = 0
    for widget in widgets:
      height = widget.get_whole_height()
      col_height += height

    parent_size = parent.get_content_size()
    parent_offset_vector  = Aligner.get_alignment_offset(
      parent_size.x, parent_size.y, 
      col_width, col_height, Align.CENTER)

    current_y = 0
    for widget in widgets:
      widget_size = widget.get_whole_size()
      widget_align = widget.get_align()
      widget_offset_vector = Aligner.get_alignment_offset(
        col_width, 0, widget_size.x, 0, widget_align
      )

      position_x = parent_offset_vector.x + widget_offset_vector.x
      position_y = current_y + parent_offset_vector.y+ widget_offset_vector.y
      widget.set_position(position_x, position_y)
      
      current_y += widget_size.y
      


  def get_width(self, parent):
    widgets = parent.get_widgets()
    if len(widgets) == 0: return
    
    # Calculate the row height:
    col_width = 0
    for widget in widgets:
      width = widget.get_whole_width()
      if width > col_width: col_width = width
    
    return col_width

  def get_height(self, parent):
    widgets = parent.get_widgets()
    if len(widgets) == 0: return
    
    col_height = 0
    for widget in widgets:
      height = widget.get_whole_height()
      col_height += height

    return col_height




