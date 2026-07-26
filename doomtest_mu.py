from microbit import *
import music


uart.init(baudrate=115200)


display.show(Image.HAPPY)
sleep(1000)
display.clear()


bild = "0000000000000000000000000"


# Tastenstatus

a_alt = False
b_alt = False


# Drehstatus

links_ausgeloest = False
rechts_ausgeloest = False


# Cooldowns

letzter_schuss = 0
letzte_tuer = 0


# Soundsteuerung

sound = None
sound_start = 0



while True:


    jetzt = running_time()



    # ------------------
    # Sounds abspielen
    # ------------------

    if sound == "shoot":

        music.pitch(120, 40)
        music.pitch(80, 40)

        sound = None


    elif sound == "use":

        music.pitch(220, 50)
        music.pitch(330, 50)
        music.pitch(440, 70)

        sound = None




    # ------------------
    # Bilder empfangen
    # ------------------

    if uart.any():

        daten = uart.read()


        if daten:

            nachricht = daten.decode()


            if nachricht.startswith("P"):


                bild = nachricht[1:26]


                if len(bild) == 25:


                    for i in range(25):

                        px = i % 5
                        py = i // 5


                        if bild[i] == "1":

                            display.set_pixel(px, py, 9)

                        else:

                            display.set_pixel(px, py, 0)





    # ------------------
    # Tasten lesen
    # ------------------

    a_jetzt = button_a.is_pressed()
    b_jetzt = button_b.is_pressed()



    # ------------------
    # Tür benutzen A+B
    # ------------------

    if a_jetzt and b_jetzt and not a_alt:


        if jetzt - letzte_tuer > 300:


            uart.write("Cuse\n")

            sound = "use"

            letzte_tuer = jetzt





    # ------------------
    # Schießen A
    # ------------------

    elif a_jetzt and not a_alt:


        if jetzt - letzter_schuss > 150:


            uart.write("Cshoot\n")

            sound = "shoot"

            letzter_schuss = jetzt





    a_alt = a_jetzt





    # ------------------
    # Laufen B
    # ------------------

    if b_jetzt and not b_alt:


        uart.write("Cforward_on\n")



    if not b_jetzt and b_alt:


        uart.write("Cforward_off\n")



    b_alt = b_jetzt





    # ------------------
    # Drehen durch Neigung
    # ------------------

    x = accelerometer.get_x()



    if x < -500 and not links_ausgeloest:


        uart.write("Cleft\n")

        links_ausgeloest = True




    if x > -200:


        links_ausgeloest = False





    if x > 500 and not rechts_ausgeloest:


        uart.write("Cright\n")

        rechts_ausgeloest = True




    if x < 200:


        rechts_ausgeloest = False
