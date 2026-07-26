import serial
import time
import mss
from PIL import Image
import pyautogui
from pynput.keyboard import Controller, Key

microbit = serial.Serial("COM3", 115200)

time.sleep(2)

keyboard = Controller()

w_gedrueckt = False
letztes_pixel = ""

with mss.mss() as sct:

    while True:

        # ------------------
        # DOOM Bild senden
        # ------------------

        screenshot = sct.grab(sct.monitors[1])

        bild = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )


        bild = bild.resize(
            (5, 5),
            Image.Resampling.NEAREST
        )


        pixel = ""


        for y in range(5):

            for x in range(5):

                r, g, b = bild.getpixel((x, y))


                helligkeit = (
                    r * 0.299 +
                    g * 0.587 +
                    b * 0.114
                )


                if helligkeit < 60:

                    pixel += "0"

                else:

                    pixel += "1"



        if pixel != letztes_pixel:

            microbit.write(
                ("P" + pixel).encode()
            )

            letztes_pixel = pixel
        # ------------------
        # micro:bit Befehle
        # ------------------

        if microbit.in_waiting:

            daten = microbit.readline().decode().strip()

            print("Empfangen:", daten)


            # Schießen
            if "Cshoot" in daten:

                pyautogui.mouseDown()

                time.sleep(0.05)

                pyautogui.mouseUp()



            # Benutzen
            if "Cuse" in daten:

                keyboard.press("e")

                time.sleep(0.05)

                keyboard.release("e")



            # Vorwärts laufen
            if "Cforward_on" in daten and not w_gedrueckt:

                keyboard.press("w")

                w_gedrueckt = True



            if "Cforward_off" in daten and w_gedrueckt:

                keyboard.release("w")

                w_gedrueckt = False



            # Links drehen (ein Impuls)
            if "Cleft" in daten:

                keyboard.press(Key.left)

                time.sleep(0.08)

                keyboard.release(Key.left)



            # Rechts drehen (ein Impuls)
            if "Cright" in daten:

                keyboard.press(Key.right)

                time.sleep(0.08)

                keyboard.release(Key.right)