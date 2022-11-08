from deepface import DeepFace
import cv2
import pyttsx3
from dbface import baseDatos as bd
import datetime
def reconocimiento(frame):
    try:
        recognition = DeepFace.find(frame,db_path="db", model_name="VGG-Face", silent=True)
        recognition2 = recognition["identity"][0]
        nombre = recognition2.split("\\")[1].split("/")[0]
        return nombre
    except ValueError:
        return "Rostro no detectado"
    except KeyError:
        return "Rostro no detectado"    

def saludar(mensaje): 
    engine.say("hola" + mensaje)
    engine.runAndWait()

def guardarBD(base, mensaje):
    base.agregarRegistro(mensaje, datetime.datetime.now())


base = bd()
base.crearTabla()
vid = cv2.VideoCapture(0)
engine = pyttsx3.init()
engine.setProperty("rate", 125)
mensajeAnterior = ""
cv2.namedWindow("Proyecto", cv2.WINDOW_NORMAL)

while True:
    ret, frame = vid.read()
    if not ret:
        break

    mensaje = reconocimiento(frame)
    if mensaje != mensajeAnterior and mensaje != "Rostro no detectado":
        guardarBD(base, mensaje)
        saludar(mensaje)

    cv2.putText(frame, mensaje, (0,115), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow("Proyecto", frame)
    if cv2.waitKey(1) == ord("q"):
        break
    mensajeAnterior = mensaje
    
vid.release()
cv2.destroyAllWindowsS()