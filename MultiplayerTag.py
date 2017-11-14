from microbit import display, i2c, button_a, button_b, accelerometer
import radio
import array
import music
from ustruct import pack_into

# LCD Control constants
screen = bytearray(513)  # send byte plus pixels
screen[0] = 0x40
zoom = 1
pixelIndex = 0
pixelsX = array.array("b", [0, 0, 0, 0, 0, 0])
pixelsY = array.array("b", [0, 0, 0, 0, 0, 0])
barVal = 0
shipX = 10
shipY = 10

def command(c):
    i2c.write(0x3C, b'\x00' + bytearray(c))


def set_pos(col=0, page=0):
    command([0xb0 | page])  # page number
    # take upper and lower value of col * 2
    c1, c2 = col * 2 & 0x0F, col >> 3
    command([0x00 | c1])  # lower start column address
    command([0x10 | c2])  # upper start column address


def clear_pixels():
    global pixelIndex
    if pixelIndex > 0:
        for i in range(pixelIndex):
            if (pixelsX[i] > 0):
                set_px(pixelsX[i], pixelsY[i], 0, 0)
        pixelIndex = 0


# 64 x 32
def set_px(x, y, color, draw=1):
    if (color == 1):
        global pixelIndex
        pixelsX[pixelIndex] = x
        pixelsY[pixelIndex] = y
        pixelIndex += 1
    page, shift_page = divmod(y, 8)
    ind = x * 2 + page * 128 + 1
    b = screen[ind] | (1 << shift_page) if color else screen[ind] & ~ (1 << shift_page)
    pack_into(">BB", screen, ind, b, b)
    if draw:
        set_pos(x, page)
        i2c.write(0x3c, bytearray([0x40, b, b]))


def draw_screen():
    set_pos()
    i2c.write(0x3C, screen)

    
# GAME START =======================

cmd = [
    [0xAE],                     # SSD1306_DISPLAYOFF
    [0xA4],                     # SSD1306_DISPLAYALLON_RESUME
    [0xD5, 0xF0],               # SSD1306_SETDISPLAYCLOCKDIV
    [0xA8, 0x3F],               # SSD1306_SETMULTIPLEX
    [0xD3, 0x00],               # SSD1306_SETDISPLAYOFFSET
    [0 | 0x0],                  # line #SSD1306_SETSTARTLINE
    [0x8D, 0x14],               # SSD1306_CHARGEPUMP
    # 0x20 0x00 horizontal addressing
    [0x20, 0x00],               # SSD1306_MEMORYMODE
    [0x21, 0, 127],             # SSD1306_COLUMNADDR
    [0x22, 0, 63],              # SSD1306_PAGEADDR
    [0xa0 | 0x1],               # SSD1306_SEGREMAP
    [0xc8],                     # SSD1306_COMSCANDEC
    [0xDA, 0x12],               # SSD1306_SETCOMPINS
    [0x81, 0xCF],               # SSD1306_SETCONTRAST
    [0xd9, 0xF1],               # SSD1306_SETPRECHARGE
    [0xDB, 0x40],               # SSD1306_SETVCOMDETECT
    [0xA6],                     # SSD1306_NORMALDISPLAY
    [0xd6, 1],                  # zoom on
    [0xaf],                     # SSD1306_DISPLAYON
]
for c in cmd:
    command(c)

# command([0xa7 - 1])  # inverted display

radio.on()
playing = True
boost = 1

while playing:

    barVal += 0.1
    if (barVal > 5):
        barVal = 5

    display.clear()
    for y in range(0, int(barVal)):
        for x in range(0, 5):
            display.set_pixel(x, y, 9)

    if button_a.is_pressed() and barVal == 5:
        barVal = 0
        radio.send("fire")
        for freq in range(1400, 1000, -40):
            music.pitch(freq, 1)

    if button_b.is_pressed() and barVal > 1:
        boost = 2
        barVal -= 0.2
        music.pitch(1200, 1)
    else:
        boost = 1
        
    shipX = int(shipX - ((accelerometer.get_x() / 200) * boost))
    shipY = int(shipY - ((accelerometer.get_y() / 200) * boost))

    if (shipX < 1):
        shipX = 1

    if (shipX > 62):
        shipX = 62

    if (shipY < 1):
        shipY = 1

    if (shipY > 30):
        shipY = 30       

    incoming = radio.receive()

    clear_pixels()

    # draw ship
    set_px(shipX, shipY, 1, 0)
    set_px(shipX + 1, shipY, 1, 0)
    set_px(shipX, shipY + 1, 1, 0)
    set_px(shipX + 1, shipY + 1, 1, 0)
    
    # draw other ship
    if (incoming is not None):
        if incoming == "dead":
            playing = False
            display.clear()
            for i in range(0, 5):
                display.set_pixel(i, 2, 9)
                display.set_pixel(2, i, 9)
        elif incoming == "fire":
            if (otherShipX - shipX) < 2 and (otherShipX - shipX) > -2 and (otherShipY - shipY) < 2 and (otherShipY - shipY) > -2:
                playing = False
                radio.send("dead")
                display.clear()
                for i in range(0, 5):
                    display.set_pixel(i, i, 9)
                    display.set_pixel(4 - i, i, 9)
        else:
            otherShipX = int(incoming[:2])
            otherShipY = int(incoming[2:])
            set_px(otherShipX, otherShipY, 1, 0)


    radioSend = ""
    if shipX < 10:
        radioSend += "0" + str(shipX)
    else:
        radioSend += str(shipX)

    if shipY < 10:
        radioSend += "0" + str(shipY)
    else:
        radioSend += str(shipY)

    radio.send(radioSend)
    draw_screen()