from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

#Nota importante: al ejecutar las solicitudes se tardo demasiado en dar respuestas

def sumar(a,b):
    return a+b

def restar(a,b):
    return a-b
def multiplicar(a,b):
    return a*b
def dividir(a,b):
    try:
        resp = a/b
        return resp
    except ZeroDivisionError:
        print("No se puede dividir entre cero")
        return None

# Creamos la ruta del servidor SOAP
dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "Sumar",
    sumar,
    returns={"salida": int},
    args={"a": int, "b": int},
    
)
dispatcher.register_function(
    "Restar",
    restar,
    returns={"salida": int},
    args={"a": int, "b": int},
    
)

dispatcher.register_function(
    "Multiplicar",
    multiplicar,
    returns={"salida": int},
    args={"a": int, "b": int},
    
)
dispatcher.register_function(
    "Dividir",
    dividir,
    returns={"salida": float},
    args={"a": int, "b": int},
    
)
# Iniciamos el servidor HTTP
server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()