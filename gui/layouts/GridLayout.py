from ..utils.Alignment import *
from .Layout import Layout

class GridLayout(Layout):
  def __init__(self, cols, rows):
    self.cols = cols
    self.rows = rows

  def layout_widgets(self, parent):
    widgets = parent.get_widgets()

    columns_widths  = []
    for x in range(0, self.cols): columns_widths.append([])
    rows_heights = []
    for x in range(0, self.rows): rows_heights.append([])

    columns_max_widths  = []
    rows_max_heights    = []


    # Populate the columns widths and columns heights arrays:
    i = 0
    for widget in widgets:
      size = widget.get_whole_size()
      
      widget_column = i % self.cols
      columns_widths[widget_column].append(size.x)

      widget_row = i // self.cols
      rows_heights[widget_row].append(size.y)

      i += 1


    # Calculate max columns widths and heights:
    for i in range(0, self.cols):
      max_width = 0
      widths = columns_widths[i]
      for width in widths:
        if width > max_width: max_width = width

      columns_max_widths.append(max_width)
    
    for i in range(0, self.rows):
      max_height = 0
      heights = rows_heights[i]
      for height in heights:
        if height > max_height: max_height = height

      rows_max_heights.append(max_height)


    # Place the controls
    i = 0
    for widget in widgets:
      widget_size = widget.get_whole_size()
      
      widget_column = i % self.cols
      current_column_x = 0
      for col in range(0, widget_column): current_column_x += columns_max_widths[col]
    
      widget_row = i // self.cols
      current_row_y = 0
      for row in range(0, widget_row): current_row_y += rows_max_heights[row]

      max_width = columns_max_widths[widget_column]
      max_height = rows_max_heights[widget_row]

      widget_align = widget.get_align()
      widget_offset = Aligner.get_alignment_offset(
        max_width     , max_height, 
        widget_size.x , widget_size.y, 
        widget_align
      )
     
      widget.set_position(current_column_x + widget_offset.x, current_row_y + widget_offset.y)

      i += 1


  def get_width(self, parent):
    widgets = parent.get_widgets()

    columns_widths  = []
    for x in range(0, self.cols): columns_widths.append([])
    
    columns_max_widths  = []
    
    # Populate the columns widths and columns heights arrays:
    i = 0
    for widget in widgets:
      size = widget.get_whole_size()
      
      widget_column = i % self.cols
      columns_widths[widget_column].append(size.x)

      i += 1

    # Calculate max columns widths and heights:
    for i in range(0, self.cols):
      max_width = 0
      widths = columns_widths[i]
      for width in widths:
        if width > max_width: max_width = width

      columns_max_widths.append(max_width)
    
    total_width = 0
    for width in columns_max_widths:
      total_width += width

    return total_width


  def get_height(self, parent):
    widgets = parent.get_widgets()

    rows_heights = []
    for x in range(0, self.rows): rows_heights.append([])

    rows_max_heights    = []

    # Populate the columns widths and columns heights arrays:
    i = 0
    for widget in widgets:
      size = widget.get_whole_size()
      
      widget_row = i // self.cols
      rows_heights[widget_row].append(size.y)

      i += 1


    # Calculate max rows heights:
    for i in range(0, self.rows):
      max_height = 0
      heights = rows_heights[i]
      for height in heights:
        if height > max_height: max_height = height

      rows_max_heights.append(max_height)

    total_height = 0
    for height in rows_max_heights:
      total_height += height

    return total_height
