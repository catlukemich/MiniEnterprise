class Color():
  # def __init__(self, red = 255, green = 255, blue = 255, alpha = 255):
  #   self.red    = red
  #   self.green  = green
  #   self.blue   = blue
  #   self.alpha  = alpha

  def __init__(self, *values):
    red = 0
    green = 0
    blue = 0
    alpha = 255

    if len(values) == 1:
      red = values[0]
      green = values[0]
      blue = values[0]

    if len(values) == 3:
      red = values[0]
      green = values[1]
      blue = values[2]

    if len(values) == 4:
      red = values[0]
      green = values[1]
      blue = values[2]
      alpha = values[3]

    self.red = red
    self.green = green
    self.blue = blue
    self.alpha = alpha




