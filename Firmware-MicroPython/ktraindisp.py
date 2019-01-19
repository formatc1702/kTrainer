import ssd1306
import bitmapfont
import bitmaps
import gfx

class MetaDisplay:
    def __init__(self, i2c, width, height, rotate=False):
        self.width = width
        self.height = height
        self.oled = ssd1306.SSD1306_I2C  (width, height, i2c)
        if rotate == True: # rotate 180 deg
            self.oled.write_cmd(0xa0 | 0x00) # flip X
            self.oled.write_cmd(0xc0 | 0x00) # flip Y
        self.bf = bitmapfont.BitmapFont(width, height, self.oled.pixel, self.oled.framebuf.fill_rect)
        self.bf.init()
        self.bmp = bitmaps.MyGFX(self.oled.pixel)
        self.gfx = gfx.GFX(width, height, self.oled.pixel)

    def fill(self, *args, **kwargs):
        self.oled.fill(*args, **kwargs)

    def show(self):
        self.oled.show()

    def disp_topbar(self, date, time):
        self.gfx.fill_rect(0,0,self.width,9,1)
        self.bf.text(date, 1,1,1,0)
        self.bf.text(time,98,1,1,0)

    def disp_progress_bar(self, x, y, w, h, p, c=1):
        self.gfx.rect(x,y,w,h,c)
        self.gfx.fill_rect(x+1,y+1, w-2,   h-2,1-c)
        self.gfx.fill_rect(x+1,y+1,(w-2)*p,h-2,  c)

    def disp_before(self, exname, exweight, exparams, exstatus):
        x = 0
        y = 11
        c = 0
        # Exercise name
        self.gfx.fill_rect(x+0,y+0,28,20,1)
        if len(exname) <= 2:
            self.bf.text(exname,x+3,y+3,2,c)
        else:
            self.bf.text(exname[0],  x+ 3,y+ 3,2,c)
            self.bf.text(exname[1],  x+15,y+ 4,1,c)
            self.bf.text(exname[2:4],x+15,y+11,1,c)
        # Exercise weight
        self.bmp.draw_bitmap(17,x+30,y+3)
        self.bf.text("{:>3}".format(exweight),x+42,y+3,2,1)
        # Exercise parameters
        for i, k in enumerate(exparams.items()):
            self.bf.text("{:<3} {:>4}".format(k[0][0:3],k[1][0:4]),81,y+3+8*i,1,1)
        # Exercise status
        if exstatus == 0:
            s = 'Pending'
        elif exstatus == 1:
            s = 'Done'
        elif exstatus == 2:
            s = 'Skipped'
        self.bf.text(s,x,y+28,1,1)

from machine import Pin, I2C
DISP_W = const(128)
DISP_H = const( 64)
i2c  = I2C(scl=Pin(14), sda=Pin(16), freq=100000)

md = MetaDisplay(i2c, DISP_W, DISP_H, True)
md.fill(0)
# md.oled.pixel(0,0,1)
# md.bf.text('BABA',1,1,9,1)
# md.oled.framebuf.fill_rect(124,60,4,4,1)
# md.oled.framebuf.fill_rect(125,61,2,2,0)
md.disp_topbar('2017-04-15','13:15')
md.disp_before('F2',223,{'P': '1', 'L': '3', 'Bew': '17', 'Griff':'vert'},0)
md.bmp.button_icons4(4,7,9,13,56)
md.gfx.hline(0,54,md.width,1)
md.disp_progress_bar(61,1,36,7,0.5,0)
md.show()
