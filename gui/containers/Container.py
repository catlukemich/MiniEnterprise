from gui.Widget import *

# Basic container class that allows grouping of controls and laying them out.
class Container(Widget):  
 
  def __init__(self):
    Widget.__init__(self)
    self.widgets = []

  def add_widget(self, widget):
    self.widgets.append(widget)
    widget.set_parent(self)

  def remove_widget(self, widget):
    self.widgets.remove(widget)
    widget.set_parent(None)

  def get_widgets(self):
    return self.widgets

  def draw(self, surface):
    for widget in self.widgets:
      widget.draw(surface)