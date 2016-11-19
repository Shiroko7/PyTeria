# PyTeria

TEST
E
S
T
 main.py tiene el loop de la bateria 
 funciones.py tiene las funciones que se encargan de recorrer todos los archivos para que funcione, configuraciones y sonidos.

la weaita esta programada para que funcione asi:

        Carpeta principal:
          deberia tener main.py, funciones.py y las carpetas configs y kits

        carpeta kits:
          dentro de esta va cada sub-carpeta con archivos .wav

        carpeta configs:
          almacena todas las configuraciones
                cada archivo .cfg tiene la estructur kit;;TOCANDO1::TOCANDO2.....::TOCANDON
                
                donde kit es el nombre de la sub-carpeta con los archivos .wav, y TOCANDOX la configuracion de las piezas



El Arduinoria.py hace toda la weaita por el momento falta por implementar la interfaz gráfica

Quiero agregar una weaita para cambiar el umbral de activación de una pieza mientras tocas, el arduino esta programado para que tenga uno minimo pero en caso que sea muy sensible cambiarlo

Descompriman el zip con los sonidos de la bateria

La tecla ESC cierra el Arduinoria
SPACE detiene el loop de la bateria y regresa a la interfaz
