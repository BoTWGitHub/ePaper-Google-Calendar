import os
from PIL import Image,ImageDraw,ImageFont

EPD_WIDTH       = 800
EPD_HEIGHT      = 480
BLACK  = 0x000000   #   00  BGR
WHITE  = 0xffffff   #   01
YELLOW = 0x00ffff   #   10
RED    = 0x0000ff   #   11

BLACK_RGBA  = 0xff000000   #   00  BGR
WHITE_RGBA  = 0xffffffff   #   01
YELLOW_RGBA = 0xff00ffff   #   10
RED_RGBA    = 0xff0000ff   #   11

def main():
    picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'calendar')
    fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')

    dinFont = ImageFont.truetype(os.path.join(fontdir, 'DIN Bold.ttf'), 40)
    avantFont = ImageFont.truetype(os.path.join(fontdir, 'Avgardm.ttf'), 50)
    msjhFont = ImageFont.truetype(os.path.join(fontdir, 'msjhbd.ttc'), 40)
    helvaticaFont100 = ImageFont.truetype(os.path.join(fontdir, 'helvetica-compressed.ttf'), 100)
    helvaticaFont34 = ImageFont.truetype(os.path.join(fontdir, 'Helvetica-Bold.ttf'), 34)

    Himage = Image.open(os.path.join(picdir, 'Calendar_Cloud.bmp')).convert('RGBA')

    TextImage = Image.new('RGBA', (EPD_WIDTH, EPD_HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(TextImage)

    draw.text((50, 20), '2023', font = dinFont, fill = WHITE_RGBA)
    draw.text((250, 75), 'Apr.', font = avantFont, fill = WHITE_RGBA)
    draw.text((365, 50), '18', font = helvaticaFont100, fill = YELLOW_RGBA)
    draw.text((510, 77), '四', font = msjhFont, fill = WHITE_RGBA)
    draw.text((627, 30), '22', font = helvaticaFont34, fill = WHITE_RGBA)
    draw.text((670, 30), '°', font = helvaticaFont34, fill = RED_RGBA)

    out = Image.alpha_composite(Himage, TextImage)
    out.convert('RGB')
    out.show()

if __name__=='__main__':
    main()
