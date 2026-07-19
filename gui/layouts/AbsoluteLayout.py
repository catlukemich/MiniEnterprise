from gui.layouts.Layout import *


class AbsoluteLayout(Layout):
  def get_width(self, parent):
    dimensions = parent.get_dimensions()
    return dimensions.x


  def get_height(self, parent):
    dimensions = parent.get_dimensions()
    return dimensions.y