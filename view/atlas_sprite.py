from .sprite import Sprite


#       ___
#   ,--[___]--,
#  /           \
# |,.--'```'--.,|    ,
# |'-.,_____,.-'|    ||
# |'-.,_____,.-'|    ||
# |             |   _||_
# |  P A I N T  |  ///\\\
# |             |  HHHHHH
# |'-.,_____,.-'|  ||||||
# `'-.,_____,.-''  ||||||  jgs


class AtlasSprite(Sprite):

    def __init__(self, location=..., atlas_image=None):
        super().__init__(location, atlas_image)
        self.image_idx = 0 # <--- The image index 

    def set_image_idx(self, idx):
        self.image_idx = idx

    def do_draw(self, blitfun=None):
        return super().do_draw(blitfun)