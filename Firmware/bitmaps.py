ADJUST   = const( 0)
BLANK    = const( 1)
CHECK    = const( 2)
LEFT     = const( 3)
MINUS    = const( 4)
MUTE     = const( 5)
PAUSE    = const( 6)
PLAY     = const( 7)
PLUS     = const( 8)
REPORT   = const( 9)
RESTART  = const(10)
RIGHT    = const(11)
SKIP     = const(12)
SOUND    = const(13)
X        = const(14)

def load_bmp(pos):
    f = open("bitmaps.bin","br")
    f.seek(pos * 8)
    return f.read(8)
    f.close()

class MyGFX:
    def __init__(self, pixel):
        self.pixel = pixel

    def draw_bitmap(self, bmp, x, y, color=1, size=8):
        for row, rowbyte in enumerate(bmp):
            for col in reversed(range(0,size)):
                self.pixel(x+col,y+row,(rowbyte >> (size-col-1) & 0b1) ^ (1-color))

    def button_icons3(self, icon1, icon2, icon3, row=24):
        self.draw_bitmap(load_bmp(icon1),  0,row)
        self.draw_bitmap(load_bmp(icon2), 60,row)
        self.draw_bitmap(load_bmp(icon3),120,row)
