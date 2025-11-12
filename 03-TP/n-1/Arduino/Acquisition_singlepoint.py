from pyfirmata import Arduino, util
import time

carte=Arduino('/dev/ttyACM0')
acquisition=util.Iterator(carte)
acquisition.start()

#affichage de Vs#
tension_A1=carte.get_pin('a:1:i')
tension_A2=carte.get_pin('a:2:i')
tension_A3=carte.get_pin('a:3:i')
time.sleep(1.0)
V1=tension_A1.read()*5
V2=tension_A2.read()*5
V3=tension_A3.read()*5
print(V1, V2, V3)
carte.exit()


