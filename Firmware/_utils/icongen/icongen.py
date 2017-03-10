from PIL import Image
import os

sourcedir = "imgsource/"
outputdir = "output/"
binpath   = "output/bitmaps.bin"

binfile = open(binpath, 'wb')

counter = 0
listy = []
maxlen = 0

for file in os.listdir(sourcedir):
    if file.endswith(".png"):
        infile  = os.path.join(sourcedir, file)
        outfile = os.path.join(outputdir, file)
        iconname = file.split('.')[0]
        if len(iconname) > maxlen:
            maxlen = len(iconname)
        img = Image.open(infile).convert('1')
        w, h = img.size
        print("{} ({}x{})".format(file,w,h))

        for y in range(0,h):
            b = 0b0
            for x in range(0,w):
                # print(img.getpixel((x,y)))
                if (img.getpixel((x,y)) == 0):
                    # print("-", end="")
                    b = (b << 1 | 0b1)
                else:
                    # print("X", end="")
                    b = b << 1
            # print(" ")
            print("{:08b}".format(b))
            binfile.write(b.to_bytes(1,'big'))


        img.save(outfile)
        listy.append((counter, iconname))
        counter += 1

        print(" ")

binfile.close()
for item in listy:
    print("{:<8} = const({:>2})".format(item[1].upper(),item[0]))
# img = Image.open("play.png")
