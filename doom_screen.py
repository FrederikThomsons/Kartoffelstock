import serial
import time
import mss
from PIL import Image

# micro:bit verbinden
microbit = serial.Serial("COM3", 115200)

time.sleep(2)

with mss.mss() as sct:
    while True:

        # Bildschirm aufnehmen
        screenshot = sct.grab(sct.monitors[1])

        bild = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        # auf 5x5 Pixel verkleinern
        bild = bild.resize((5, 5))

        pixel = ""

        for y in range(5):
            for x in range(5):

                r, g, b = bild.getpixel((x, y))

                helligkeit = (r + g + b) / 3

                if helligkeit < 160:
                    pixel += "1"
                else:
                    pixel += "0"

        # P = "Picture", damit der micro:bit weiß:
        # das ist ein Bild
        microbit.write(("P" + pixel).encode())

        time.sleep(0.03)