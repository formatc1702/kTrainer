ADJUST   = const( 0)
BLANK    = const( 1)
CHECK    = const( 2)
DONE     = const( 3)
LEFT     = const( 4)
MINUS    = const( 5)
MUTE     = const( 6)
PAUSE    = const( 7)
PENDING  = const( 8)
PLAY     = const( 9)
PLUS     = const(10)
REPORT   = const(11)
RESTART  = const(12)
RIGHT    = const(13)
SKIP     = const(14)
SKIPPED  = const(15)
SOUND    = const(16)
WEIGHT   = const(17)
X        = const(18)

class MyGFX:
    def __init__(self, pixel):
        self.pixel = pixel
        self.f = open("bitmaps.bin","br")

    def draw_bitmap(self, bmp, x, y, color=1, size=8):
        bmpbytes = self.load_bmp(bmp)
        for row, rowbyte in enumerate(bmpbytes):
            for col in reversed(range(0,size)):
                self.pixel(x+col,y+row,(rowbyte >> (size-col-1) & 0b1) ^ (1-color))

    def load_bmp(self, pos):
        self.f.seek(pos * 8)
        return self.f.read(8)

    def button_icons3(self, icon1, icon2, icon3, row=24):
        self.draw_bitmap(icon1,  0,row)
        self.draw_bitmap(icon2, 60,row)
        self.draw_bitmap(icon3,120,row)

    def button_icons4(self, icon1, icon2, icon3, icon4, row=24):
        self.draw_bitmap(icon1,  0,row)
        self.draw_bitmap(icon2, 40,row)
        self.draw_bitmap(icon3, 80,row)
        self.draw_bitmap(icon4,120,row)
