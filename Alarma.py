#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path 
import os
import sys
import time
import logging
import configparser
import threading
import socket
import pkgutil 
import cv2
from queue import Queue
from pytg.receiver import Receiver  # get messages
from pytg.sender import Sender  # send messages, and other querys.
from pytg.utils import coroutine

logging.basicConfig(level=logging.DEBUG)
time.sleep(2)
logging.info("Arranca AlarmaPy")

global rpgpiofound 
rpgpio=pkgutil.find_loader('RPi')
rpgpiofound = rpgpio is not None
logging.info("rpgpiofound :" +str(rpgpiofound))
if rpgpiofound :
    import RPi.GPIO as GPIO
    logging.info("Modulo RPi Importado.")
else:
    logging.info("Modulo RPi NO Importado.")

global wspconf
global wspport
global tlgconf
global tlgport
global conexiones
global configuracion
global confestado
global archconf
global archestado
global grupolog
global spylog
global grupolog
global spylog
#global Emsg
global ColaMsg
global camera_port
global ramp_frames
global conectado
global foto
global SWhat
global txtenergia
global stackin
global Htermina
global Qtermina
global Hilos
global HTimers
global SirenaTime
global Sirena
global videotiempo

wspconf=False
wspport=7701
tlgconf=True
tlgport=7702
Hilos={}
HTimers={}
SirenaTime=30
txtenergia=["Con Energia.", "Sin Energia", "No Valor"]
#Emsg=threading.Event()
#Emsg.set()
ColaMsg=Queue(maxsize=0)
grupolog="5493416648977-1471182091@g.us"
spylog="5493416648977@s.whatsapp.net"
archconf="telefonos.cfg"
archestado="estado.stat"
configuracion = configparser.ConfigParser()
confestado = configparser.ConfigParser()
camera_port = 0
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 60
foto = "/tmp/foto.png"
video = "/tmp/video.avi"
videotiempo=15
Htermina=False
Qtermina=False
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 7777 # Arbitrary non-privileged port
SOCKPASS = "secret1308"

conexiones={"5493416648977@s.whatsapp.net":{"Pass":"secret1703","Timeout":600,"Login":False,"Last":0,"Nombre":"Sebastian"},"5493416648977-1471182091@g.us":{"Pass":"secret1703","Timeout":600,"Login":False,"Last":0,"Nombre":"GrupoAlarma"},"5493416649051@s.whatsapp.net":{"Pass":"ana13","Timeout":600,"Login":False,"Last":0,"Nombre":"Ana Ines"},"5493412601700@s.whatsapp.net":{"Pass":"tatu1309","Timeout":600,"Login":False,"Last":0,"Nombre":"Martina"},"5493413029747@s.whatsapp.net":{"Pass":"p0mp1s","Timeout":600,"Login":False,"Last":0,"Nombre":"Amanda"},"5493413029752@s.whatsapp.net":{"Pass":"agus10","Timeout":600,"Login":False,"Last":0,"Nombre":"Agustina"},"5493415104315@s.whatsapp.net":{"Pass":"seba1703","Timeout":600,"Login":False,"Last":0,"Nombre":"SebaMuni"}}


def configDefault():
    try :
        global confestado
        conffile=None
        logging.info("Creando Configuracion por Defecto ESTADO.")
        confestado.add_section('Alarma')
        confestado.set('Alarma', 'Armado', '0')
        confestado.set('Alarma', 'Disparo', '0')
        confestado.set('Alarma', 'ArmadoUser', '')
        confestado.set('Alarma', 'ArmadoTime', '0')
        confestado.set('Alarma', 'DisparoSensor', '')
        confestado.set('Alarma', 'DisparoTime', '0')
        confestado.set('Alarma', 'Log', '0')
        # Writing our configuration file to 'example.cfg'
        with open(archestado, 'w') as conffile:
            confestado.write(conffile)
    except Exception as e:
        logging.info("*ERROR* exception on %s!" % conffile)
        logging.info("*ERROR* exception on %s!" % str(e))    


def leeconfestado():
    try :
        logging.info("Lee Configuracion ESTADO.")
        confestado.read(archestado)
    except Exception as e:
        logging.info("*ERROR* exception on %s!" % e)

def guardaconfestado():
    try :
        logging.info("Guarda Configuracion ESTADO.")
        # Writing our configuration file to 'example.cfg'
        with open(archestado, 'w') as conffile:
            confestado.write(conffile)

    except Exception as e:
        logging.info("*ERROR* exception on %s!" % str(e))

def setconfestado(seccion, variable, valor):
    try :
        global confestado
        confestado.set(seccion, variable, valor)
        # Writing our configuration file to 'example.cfg'
        #with open(archestado, 'w') as conffile:
        #    confestado.write(conffile)
    except Exception as e:
        logging.info("*ERROR* exception on %s!" % e)
        
                
def int_callback22(channel): 
    texto="Activado Movimiento Sensor 22"
    logging.info(texto)
    global confestado,Sirena
    global HTimers
    val=Gpioget(22)
    if ((int(confestado.get('Alarma', 'Armado')) > 0) and val==0 and Sirena != 0):
        confestado.set('Alarma', 'Disparo', '1')
        confestado.set('Alarma', 'DisparoSensor', 'Movimiento Sensor 22')
        confestado.set('Alarma', 'DisparoTime', time.strftime("%c"))
        logging.info("int_callback22 :" + str(val))
        #EnviaMsgQ(grupolog,'texto',texto)
        #EchoLayer.sendEvento('Activado Movimiento Sensor 22!', grupolog)
        Sirena=0
        Gpioset(23, Sirena)
        gpiotimer=threading.Thread(target=timergpio, name='Timergpio23',args=(23,))
        gpiotimer.setDaemon(True)
        logging.info("int_callback22 - Timergpio23 :" + str("Timergpio22" in HTimers))
        if "Timergpio22" in HTimers :
            logging.info("int_callback22 - Timergpio23 Existe :" + str(HTimers["Timergpio23"].isAlive()))
        if "Timergpio22" in HTimers and HTimers["Timergpio23"].isAlive():
            logging.info("int_callback22 - Timergpio23 Vivo :" + str(HTimers["Timergpio23"].isAlive()))
        else:
            logging.info("int_callback22 - Timergpio23 Arranca.")
            gpiotimer.start()
            HTimers["Timergpio23"]=gpiotimer

   # EchoLayer.sendEvento('Activado Sensor 23!', spylog) 
    if ((int(confestado.get('Alarma', 'Log')) > 0) and val==0):
        logging.info("int_callback22 :" + str(val))
        #EnviaMsgQ(spylog,'texto',texto) 

def int_callback27(channel):
    #if GPIO.input(27): 
    #    texto="Sin Energia Sensor 27"
    #else:
    #    texto="Con Energia Sensor 27"
    imsg=Gpioget(27)
    if imsg < 2 :
        texto=txtenergia[imsg]
        #Gpioset(24, not(imsg))
    else:
        texto=txtenergia[imsg]
    logging.info(texto)
    #EnviaMsgQ(grupolog,'texto',texto)
    #EnviaMsgQ(spylog,'texto',texto) 

def int_callback17(channel): 
    texto="Activado Pulsador Sensor 17 !"
    logging.info(texto)
    global confestado,Sirena
    if (int(confestado.get('Alarma', 'Armado')) > 0):
        confestado.set('Alarma', 'Disparo', '1')
        confestado.set('Alarma', 'DisparoSensor', 'Pulsador Sensor 17')
        confestado.set('Alarma', 'DisparoTime', time.strftime("%c"))
        Sirena=0
        Gpioset(23, Sirena)
        #EnviaMsgQ(grupolog,'texto',texto)
    #outgoingMessage = TextMessageProtocolEntity(texto.encode("utf-8") if sys.version_info >= (3,0) else texto, to = grupolog)
    #self.toLower(outgoingMessage)    
    #EnviaMsgQ(spylog,'texto',texto)

def timergpio(pin):
    global SirenaTime,Sirena
    logging.info("Timer Sirena Creado.")
    texto="Sirena Temporizada :" + str(SirenaTime)
    time.sleep(SirenaTime)
    setconfestado('Alarma', 'Disparo','0' )
    guardaconfestado()
    Sirena=1
    Gpioset(pin, Sirena)    
    logging.info("Timer Sirena Off.")
    #EnviaMsgQ(grupolog,'texto',texto)    

def iniciaSocketServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info("SocketServer Creado.")
    try:
       s.bind((HOST, PORT))
    except socket.error as msg:
       logging.info("*ERROR* Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
       sys.exit()
    logging.info("SocketServer Bind Completo.")
    s.listen(10)
    logging.info("SocketServer Listening.")
    while not(Htermina):
        try:
            conn, addr = s.accept()
            texto="SocketServer Conexion :" + addr[0] + ':' + str(addr[1])
            logging.info(texto)
            #EnviaMsgQ(spylog,'texto',texto) 
            hilosock=threading.Thread(target=clientthread, args=(conn,))
            logging.info("Hilo SocketServer Estado Vivo:" + str(hilosock.isAlive()))
            hilosock.start()    
            #start_new_thread(clientthread ,(conn,))
        except Exception as e:
            logging.info("*ERROR* Error iniciaSocketServer : %s %s %s" % (e.message,e.args,e))
    s.close()

def clientthread(conn):
    global Sirena
    SOCKLOGIN=False
    while not(Htermina):
        datab = conn.recv(1024)
        if not datab: 
            break
        dataa = str(datab.decode()).replace('\n','')
        logging.info("Mensaje Socket:" + str(dataa))
        data = str(dataa).replace('\r','')
        logging.info("Mensaje Socket:" + str(data))
        reply="mmmm..."
        logging.info("CLIENTTHR - Socket SOCKPASS and SOCKLOGIN:" + str(SOCKPASS) + str(SOCKLOGIN)+ str(data == SOCKPASS))
        if SOCKLOGIN==False and data == SOCKPASS:
            SOCKLOGIN=True
            reply=";)"
        elif SOCKLOGIN==True:
            if data== "Activar" :
                setconfestado('Alarma', 'Armado','1' )
                setconfestado('Alarma', 'ArmadoUser',"Socket")
                setconfestado('Alarma', 'ArmadoTime',time.strftime("%c"))
                guardaconfestado()
                reply="Activada."
            elif data== "Desactivar" :
                setconfestado('Alarma', 'Armado','0' )
                setconfestado('Alarma', 'ArmadoUser',"Socket")
                setconfestado('Alarma', 'ArmadoTime',time.strftime("%c"))
                guardaconfestado()
                reply="DESActivada."
            elif data== "Sos" :
                setconfestado('Alarma', 'Disparo','1' )
                setconfestado('Alarma', 'ArmadoUser',"Socket")
                setconfestado('Alarma', 'DisparoTime',time.strftime("%c"))
                guardaconfestado()
                reply="Disparo Sirena!"
                Sirena=0
                Gpioset(23, Sirena)
            elif data== "Stop" :
                setconfestado('Alarma', 'Disparo','0' )
                setconfestado('Alarma', 'ArmadoUser',"Socket")
                setconfestado('Alarma', 'DisparoTime',time.strftime("%c"))
                guardaconfestado()
                reply="Stop Sirena."
                Sirena=1
                Gpioset(23, Sirena)
            elif data== "Wifi" :
                reply="Wifi Encendido."
                Gpioset(24, 1)                                                  
            elif data== "Nowifi" :
                reply="Wifi Apagado."
                Gpioset(24, 0)                                                  
            elif data== "Energia" :
                imsg=Gpioget(27)
                texto=txtenergia[imsg]
                reply="Energia Sensor: "+ texto
            elif data== "Foto" :
                if CamaraArchivo(): 
                    reply="Foto Creada."
                else:
                    reply="No se puede enviar Foto."
            elif data== "Estado" :
                 imsg=Gpioget(27)
                 msg=txtenergia[imsg]
                 reply="Estado: " + str(confestado.get('Alarma', 'Armado')) \
                 + "\nEstadoUser: " + str(confestado.get('Alarma', 'ArmadoUser')) \
                 + "\nEstadoTime: " + str(confestado.get('Alarma', 'ArmadoTime')) \
                 + "\nDisparo: " + str(confestado.get('Alarma', 'Disparo')) \
                 + "\nDisparoSensor: " + str(confestado.get('Alarma', 'DisparoSensor')) \
                 + "\nDisparoTime: " + str(confestado.get('Alarma', 'DisparoTime')) \
                 + "\nLog: " + str(confestado.get('Alarma', 'Log')) \
                 + "\nEnergia: " + msg  + "\n"
            elif data== "Quit" :
                 break
            else:
                 reply="No entiendo el Mensaje."

        conn.sendall((reply+"\n").encode())
    conn.close()



def Gpioconf():
    global Sirena
    try:
        if rpgpiofound :
            logging.info("Modulo RPi Configurando.")
            GPIO.setmode(GPIO.BCM)
            # entrada Pulsador  
            #GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # entrada Energia
            GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
            # entrada Movimiento
            GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # salida rele Sirena
            GPIO.setup(23, GPIO.OUT)  
            # salida rele Wifi
            #GPIO.setup(24, GPIO.OUT)
            time.sleep(0.5)
            #GPIO.output(24,1)  
            Sirena=1
            GPIO.output(23,Sirena)
            time.sleep(1)
            #GPIO.add_event_detect(17, GPIO.RISING, callback=int_callback17, bouncetime=500)  
            GPIO.add_event_detect(27, GPIO.RISING, callback=int_callback27, bouncetime=300)
            GPIO.add_event_detect(22, GPIO.FALLING, callback=int_callback22, bouncetime=300)
        else:
            logging.info("Modulo RPi NO Configurando.")
    except Exception as e:
        logging.info("*ERROR* Modulo RPi %s !" % e)


def Gpioconfestado():
    global Sirena
    try:
        if str(confestado.get('Alarma', 'Disparo')) == 1 :
            Sirena=0
            Gpioset(23, Sirena)
            logging.info("RPi ConfEstado Disparada..")
        else:
            Sirena=1
            Gpioset(23, Sirena)
            logging.info("RPi ConfEstado NO Disparada..")
    except Exception as e:
        logging.info("*ERROR* RPi CONFESTAD %s !" % e)


def Gpioget(pin):
    salida=2
    try:
        if rpgpiofound :
            salida=GPIO.input(pin)
            logging.info("RPi GPIO GET : %s %s" % (pin,salida) )
        else:
            logging.info("RPi NO Configurando GPIO GET : %s " % (pin) )
    except Exception as e:
        logging.info("*ERROR* RPi GPIO GET %s !" % e)
        return salida
    return salida

def Gpioset(pin,valor):
    try:
        if rpgpiofound :
            logging.info("RPi GPIO SET : %s %s" % (pin,valor) )
            GPIO.output(pin, valor)
        else:
            logging.info("RPi NO Configurando GPIO SET : %s %s" % (pin,valor) )
    except Exception as e:
        logging.info("*ERROR* RPi GPIO SET %s !" % e)

def get_image(camera):
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = camera.read()
    return im

def CamaraArchivo():
    salida=False
    camera = cv2.VideoCapture(camera_port)
    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary
    if (camera.isOpened()): 
        #camera.set(3,1280)
        #camera.set(4,1024)
        for i in xrange(ramp_frames):
            temp = get_image(camera)
        logging.info("Taking image...")
        # Take the actual image we want to keep
        camera_capture = get_image(camera)
        # A nice feature of the imwrite method is that it will automatically choose the
        # correct format based on the file extension you provide. Convenient!
        cv2.imwrite(foto, camera_capture)
        # You'll want to release the camera, otherwise you won't be able to create a new
        # capture object until your script exits
        salida=True
    del(camera)
    return salida

def VideoArchivo():
    salida=False
    camera = cv2.VideoCapture(camera_port)
    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary
    fourcc = cv2.cv.CV_FOURCC(*'DIVX')
   # fourcc = cv2.cv.CV_FOURCC(*'X264')
    out = cv2.VideoWriter(video,fourcc, 15.0, (640,480))
    #out = cv2.VideoWriter('/tmp/output.avi', -1, 20.0, (640,480))
    time.sleep(2)
    tiempoi=time.time()
    while(camera.isOpened()): 
        #camera.set(3,1280)
        #camera.set(4,1024)
        ret, frame = camera.read()
        if ret==True:
            #frame = cv2.flip(frame,180)
            out.write(frame)
        else:
            break
        tiempof=time.time()
        if (tiempof > (tiempoi + videotiempo)):
            salida=True
            logging.info("Taking video...")
            break 
    camera.release()
    out.release()
    del(camera)
    return salida


def iniciaSockettlg():
    # get a Receiver instance, to get messages.
    receiver = Receiver(host="localhost", port=6767)

    # get a Sender instance, to send messages, and other querys.
    sender = Sender(host="localhost", port=6767)

    # start the Receiver, so we can get messages!
    receiver.start()  # note that the Sender has no need for a start function.

    # add "example_function" function as message listener. You can supply arguments here (like sender).
    receiver.message(handler_tlg(sender))  # now it will call the example_function and yield the new messages.

    # continues here, after exiting the while loop in example_function()

    # please, no more messages. (we could stop the the cli too, with sender.safe_quit() )
    receiver.stop()

    print("I am done!")

    # the sender will disconnect after each send, so there is no need to stop it.
    # if you want to shutdown the telegram cli:
    # sender.safe_quit() # this shuts down the telegram cli.
    # sender.quit() # this shuts down the telegram cli, without waiting for downloads to complete.


# this is the function which will process our incoming messages
@coroutine
def handler_tlg(sender):  # name "example_function" and given parameters are defined in main()
    global Sirena
    quit = False
    try:
        while not quit:  # loop for messages
            msg = (yield)  # it waits until the generator has a has message here.
            sender.status_online()  # so we will stay online.
            # (if we are offline it might not receive the messages instantly,
            #  but eventually we will get them)
            print(msg)
            if msg.event != "message":
                continue  # is not a message.
            if msg.own:  # the bot has send this message.
                continue  # we don't want to process this message.
            if not "text" in msg:  # we have media instead.
                continue  # and again, because we want to process only text message.
            # Everything in pytg will be unicode. If you use python 3 thats no problem,
            # just if you use python 2 you have to be carefull! (better switch to 3)
            # for convinience of py2 users there is a to_unicode(<string>) in pytg.encoding
            # for python 3 the using of it is not needed.
            # But again, use python 3, as you have a chat with umlaute and emojis.
            # This WILL brake your python 2 code at some point!
            if msg.text == u"Activar":
                setconfestado('Alarma', 'Armado','1' )
                setconfestado('Alarma', 'ArmadoUser',msg.peer.phone)
                setconfestado('Alarma', 'ArmadoTime',time.strftime("%c"))
                guardaconfestado()
                sender.send_msg(msg.peer.cmd, u"Activada.")  # unicode support :D
            elif msg.text== u"Desactivar" :
                setconfestado('Alarma', 'Armado','0' )
                setconfestado('Alarma', 'ArmadoUser',msg.peer.phone)
                setconfestado('Alarma', 'ArmadoTime',time.strftime("%c"))
                guardaconfestado()
                sender.send_msg(msg.peer.cmd, u"DESActivada.")  # unicode support :D
            elif msg.text == u"Log" :
                setconfestado('Alarma', 'Log','1' )
                guardaconfestado()
                sender.send_msg(msg.peer.cmd, u"ConLog.")  # unicode support :D
            elif msg.text == u"Nolog" :
                setconfestado('Alarma', 'Log','0' )
                guardaconfestado()
                sender.send_msg(msg.peer.cmd, u"SinLog.")  # unicode support :D
            elif msg.text == u"Sos" :
                setconfestado('Alarma', 'Disparo','1' )
                setconfestado('Alarma', 'DisparoSensor',msg.peer.phone)
                setconfestado('Alarma', 'DisparoTime',time.strftime("%c"))
                guardaconfestado()
                sender.send_msg(msg.peer.cmd, u"Disparo Sirena!")  # unicode support :D
                Sirena=0
                Gpioset(23, Sirena)
            elif msg.text == u"Stop" :
                setconfestado('Alarma', 'Disparo','0' )
                setconfestado('Alarma', 'DisparoSensor',msg.peer.phone)
                setconfestado('Alarma', 'DisparoTime',time.strftime("%c"))
                guardaconfestado()
                sender.send_msg(msg.peer.cmd, u"Stop Sirena.")  # unicode support :D
                Sirena=1
                Gpioset(23, Sirena)
            elif msg.text == u"Wifi" :
                sender.send_msg(msg.peer.cmd, u"Wifi Encendido.")  # unicode support :D
                Gpioset(24, 1)                                                  
            elif msg.text == u"Nowifi" :
                sender.send_msg(msg.peer.cmd, u"Wifi Apagado.")  # unicode support :D
                Gpioset(24, 0)                                                  
            elif msg.text == u"Energia" :
                imsg=Gpioget(27)
                msg=txtenergia[imsg]
                sender.send_msg(msg.peer.cmd, u"Energia Sensor: "+ msg)  # unicode support :D
            elif msg.text == u"Estado" :
                imsg=Gpioget(27)
                msgs=txtenergia[imsg]
                salida="Estado: " + str(confestado.get('Alarma', 'Armado')) \
                + "\nEstadoUser: " + str(confestado.get('Alarma', 'ArmadoUser')) \
                + "\nEstadoTime: " + str(confestado.get('Alarma', 'ArmadoTime')) \
                + "\nDisparo: " + str(confestado.get('Alarma', 'Disparo')) \
                + "\nDisparoSensor: " + str(confestado.get('Alarma', 'DisparoSensor')) \
                + "\nDisparoTime: " + str(confestado.get('Alarma', 'DisparoTime')) \
                + "\nLog: " + str(confestado.get('Alarma', 'Log')) \
                + "\nEnergia: " + msgs  + "\n"
                sender.send_msg(msg.peer.cmd, salida)  # unicode support :D
            elif msg.text == u"Foto" :
                if CamaraArchivo():
                    sender.send_photo(msg.peer.cmd,foto,"Guardian") 
                else:
                    salida="No se puede enviar Foto."
                    sender.send_msg(msg.peer.cmd, salida)  # unicode support :D
            elif msg.text == u"Video" :
                if VideoArchivo(): 
                    sender.send_video(msg.peer.cmd,video,"Guardian") 
                else:
                    salida="No se puede enviar Video."
                    sender.send_msg(msg.peer.cmd, salida)  # unicode support :D
            else:
                sender.send_msg(msg.peer.cmd, u"No entiendo el Mensaje.")  # unicode support :D
            
    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C)
        pass
    else:
        # the loop exited without exception, becaues _quit was set True
        pass

'''
def onTextMessage(self,messageProtocolEntity):
        # just print info
        global conexiones
        global confestado
        logging.info("Llego el mensaje de TEXTO : %s" % (messageProtocolEntity.getBody()))
        if messageProtocolEntity.getBody() == conexiones[messageProtocolEntity.getFrom()]["Pass"] :
            conexiones[messageProtocolEntity.getFrom()]["Login"]=True
            conexiones[messageProtocolEntity.getFrom()]["Last"]=time.time()
            logging.info("Login :"+ conexiones[messageProtocolEntity.getFrom()]["Nombre"] + " - " + str(messageProtocolEntity.getFrom()) + " - "+ str(conexiones[messageProtocolEntity.getFrom()]["Last"]))
            EnviaMsgQ(messageProtocolEntity.getFrom(),"texto",";)")
        elif conexiones[messageProtocolEntity.getFrom()]["Login"] == True :
            if conexiones[messageProtocolEntity.getFrom()]["Last"] + conexiones[messageProtocolEntity.getFrom()]["Timeout"] > time.time() :
                    if messageProtocolEntity.getBody()== "Activar" :
                        setconfestado('Alarma', 'Armado','1' )
                        setconfestado('Alarma', 'ArmadoUser',messageProtocolEntity.getFrom())
                        setconfestado('Alarma', 'ArmadoTime',time.strftime("%c"))
                        guardaconfestado()
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","Activada.")
                    elif messageProtocolEntity.getBody()== "Desactivar" :
                        setconfestado('Alarma', 'Armado','0' )
                        setconfestado('Alarma', 'ArmadoUser',messageProtocolEntity.getFrom())
                        setconfestado('Alarma', 'ArmadoTime',time.strftime("%c"))
                        guardaconfestado()
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","DESActivada.")
                    elif messageProtocolEntity.getBody()== "Log" :
                        setconfestado('Alarma', 'Log','1' )
                        guardaconfestado()
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","ConLog.")
                    elif messageProtocolEntity.getBody()== "Nolog" :
                        setconfestado('Alarma', 'Log','0' )
                        guardaconfestado()
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","SinLog.")
                    elif messageProtocolEntity.getBody()== "Sos" :
                        setconfestado('Alarma', 'Disparo','1' )
                        setconfestado('Alarma', 'DisparoSensor',messageProtocolEntity.getFrom())
                        setconfestado('Alarma', 'DisparoTime',time.strftime("%c"))
                        guardaconfestado()
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","Disparo Sirena!")
                        Gpioset(23, 0)
                    elif messageProtocolEntity.getBody()== "Stop" :
                        setconfestado('Alarma', 'Disparo','0' )
                        setconfestado('Alarma', 'DisparoSensor',messageProtocolEntity.getFrom())
                        setconfestado('Alarma', 'DisparoTime',time.strftime("%c"))
                        guardaconfestado()
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","Stop Sirena.")
                        Gpioset(23, 1)                                                  
                    elif messageProtocolEntity.getBody()== "Wifi" :
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","Wifi Encendido.")
                        Gpioset(24, 1)                                                  
                    elif messageProtocolEntity.getBody()== "Nowifi" :
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","Wifi Apagado.")
                        Gpioset(24, 0)                                                  
                    elif messageProtocolEntity.getBody()== "Energia" :
                        imsg=Gpioget(27)
                        msg=txtenergia[imsg]
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","Energia Sensor: "+ msg)
                    elif messageProtocolEntity.getBody()== "Estado" :
                        imsg=Gpioget(27)
                        msg=txtenergia[imsg]
                        salida="Estado: " + str(confestado.get('Alarma', 'Armado')) \
                        + "\nEstadoUser: " + str(confestado.get('Alarma', 'ArmadoUser')) \
                        + "\nEstadoTime: " + str(confestado.get('Alarma', 'ArmadoTime')) \
                        + "\nDisparo: " + str(confestado.get('Alarma', 'Disparo')) \
                        + "\nDisparoSensor: " + str(confestado.get('Alarma', 'DisparoSensor')) \
                        + "\nDisparoTime: " + str(confestado.get('Alarma', 'DisparoTime')) \
                        + "\nLog: " + str(confestado.get('Alarma', 'Log')) \
                        + "\nEnergia: " + msg  + "\n"
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto",salida)
                    elif messageProtocolEntity.getBody()== "Foto" :
                        if CamaraArchivo(): 
                            EnviaMsgQ(messageProtocolEntity.getFrom(),"imagen","Guardian.",foto)
                        else:
                            salida="No se puede enviar Foto."
                            EnviaMsgQ(messageProtocolEntity.getFrom(),"texto",salida)
                    elif messageProtocolEntity.getBody()== "Video" :
                        if VideoArchivo(): 
                            EnviaMsgQ(messageProtocolEntity.getFrom(),"video","Guardian.",video)
                        else:
                            salida="No se puede enviar Video."
                            EnviaMsgQ(messageProtocolEntity.getFrom(),"texto",salida)
                    else:
                        EnviaMsgQ(messageProtocolEntity.getFrom(),"texto","No entiendo el Mensaje.")
                        #os.system("notify-send 'Mensaje de Whatsapp' '{mensje}'".format(mensje=messageProtocolEntity.getBody()))
                        #os.system("espeak -ves '%s'" % (messageProtocolEntity.getBody()))
                    #content="Ok.Gracias."
                    #outgoingMessage = TextMessageProtocolEntity(content.encode("utf-8") if sys.version_info >= (3,0) else content, to = messageProtocolEntity.getFrom())
                    #self.toLower(outgoingMessage)
                    

            else:
                conexiones[messageProtocolEntity.getFrom()]["Login"]= False

'''



#MAIN #

try:
    if not os.path.exists(archestado):
        print("No existe Arch Conf")
        configDefault()
    leeconfestado()
    logging.info("MAIN - leeconfestado." )
except Exception as e:
    logging.info("*ERROR* Error main Conf : %s %s %s" % (e.message,e.args,e))

Gpioconf()
logging.info("MAIN - Gpioconf." )
Gpioconfestado()
logging.info("MAIN - Gpioconfestado." )

while not(Htermina):
    try:
        logging.info("MAIN - Hilos Activos:" + str(threading.active_count()))
        #logging.info("MAIN - Lista Hilos Activos:" + str(threading.enumerate()))
        Qtermina=False
        logging.info("MAIN - Qtermina :" + str(Qtermina))

        if "HiloSockServ" in Hilos :
            logging.info("MAIN - HiloS HiloSockServ Existe :" + str("HiloSockServ" in Hilos))
        if "HiloSockServ" in Hilos and Hilos["HiloSockServ"].isAlive():
            logging.info("MAIN - HiloS HiloSockServ Vivo :" + str(Hilos["HiloSockServ"].isAlive()))
        else:
            hilosockserv=threading.Thread(target=iniciaSocketServer, name='HiloSockServ')
            hilosockserv.setDaemon(True)
            logging.info("MAIN - Hilo SockServ Arranca.")
            hilosockserv.start()
            Hilos["HiloSockServ"]=hilosockserv

        if wspconf :
            hilosockwsp=threading.Thread(target=iniciaSocketwsp, name='HiloSockWSP')
            hilosockwsp.setDaemon(True)
            if "HiloSockWSP" in Hilos :
                logging.info("MAIN - HiloSockWSP  Existe :" + str("HiloSockWSP" in Hilos ))
            if Hilos.has_key("HiloSockWSP") and Hilos["HiloSockWSP"].isAlive():
                logging.info("MAIN - HiloS HiloSockWSP Vivo :" + str(Hilos["HiloSockWSP"].isAlive()))
            else:
                logging.info("MAIN - Hilo HiloSockWSP Arranca.")
                hilosockwsp.start()
                Hilos["HiloSockWSP"]=hilosockwsp
            
        time.sleep(2)
        
        if tlgconf :
            hilosocktlg=threading.Thread(target=iniciaSockettlg, name='HiloSockTLG')
            hilosocktlg.setDaemon(True)
            if "HiloSockTLG" in Hilos :
                logging.info("MAIN - HiloSockTLG  Existe :" + str("HiloSockTLG" in Hilos))
            if "HiloSockTLG" in Hilos and Hilos["HiloSockTLG"].isAlive():
                logging.info("MAIN - HiloS HiloSockTLG Vivo :" + str(Hilos["HiloSockTLG"].isAlive()))
            else:
                logging.info("MAIN - Hilo HiloSockTLG Arranca.")
                hilosocktlg.start()
                Hilos["HiloSockTLG"]=hilosocktlg
            
    except Exception as e:
        logging.info("*ERROR* Error main : %s " % str(e))
        #Emsg.set()
        #if rpgpiofound :
        #    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
        pass
  
    logging.info("MAIN - Qtermina set:"+ str(Qtermina))
    Qtermina=True
    logging.info("MAIN - time.sleep(30)")
    time.sleep(30)      
    #logging.info("MAIN - Emsg.set ")
    #Emsg.set()
if rpgpiofound :
    GPIO.cleanup()           # clean up GPIO on normal exit  
