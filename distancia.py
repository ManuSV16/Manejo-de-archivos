# Se importan bibliotecas para la comunicación con la Raspberry y manejar las fechas.
import RPi.GPIO as GPIO  #Biblioteca para manejo de pines
import time              #Biblioteca para funciones de tiempo
from datetime import datetime   #Biblioteca para manejo de fechas

#Configuración de pines
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
GPIO.output(GPIO_TRIGGER,False)

sFileStamp = time.strftime("%Y%m%d%H")  #Se define el formato de fecha
sFileName = "\out" + sFileStamp + ".txt" #Se genera un archivo donde se almacena el nombre que tendrá el archibo

f = open(sFileName, "a")    #Se abre el archivo dándole como argumento la variable que se creó para almacenar el nombre del archivo
f.write("TimeStamp, Value" + "\n")  #Se imprime una primera líena en el documento
print("Inicia la toma de datos") #Se envía un mensaje en cosola que indica que se inicia la toma de datos

#Intentar lo siguiente
try:
    #Repetir indefinidamente
    while True:
        print("Acerque el objeto para medir la distancia")
        
        #Bloque que activa al sensor
        GPIO.output(GPIO_TRIGGER,True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER,False)
        
        #Medir la señal de respuesta del sensor
        start = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()
            
        #Calcular el periodo del pulso de respuesta del sensor
        elapsed = stop-start
        
        #Ecuación para calcularl a distancia
        distancia = (elapsed*343000)/2
        
        #Realizar log en archivo de texto
        sTimeStamp = time.strftime("%Y%m%d%H%M%S")
        f.write(sTimeStamp + "," + str(distancia) + "\n")
        print(sTimeStamp + " " + str(distancia))
        
        #Espera entre lecturas
        time.sleep(1)
        
        #Reportar y crear el archivo en caso de que no exista
        sTmpFileStamp = time.strftime('%Y%m%d%H')
        if sTmpFileStamp != sFileStamp:
            f.close
            sFileName = "out/" + sTmpFileStamp + ".txt"
            f = open(sFileName, "a")
            sFileStamp = sTmpFileStamp
            print("Creando el archivo")
            
#Acciones a realizar ante un error o interrupción del programa
except KeyboardInterrupt:
    print("\n" + "Termina la captura de datos" + "\n")
    
    #Cerrar el archivo
    f.close
    
    #Liberar los recursos de manejo de hardware
    GPIO.cleanup()

#Token para GitHub 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