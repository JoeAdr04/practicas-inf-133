from zeep import Client

client = Client('http://localhost:8000')

respuesta = client.service.Sumar(a=2, b=3)
print(respuesta)
respuesta = client.service.Restar(a=3, b=2)
print(respuesta)
respuesta = client.service.Multiplicar(a=2, b=3)
print(respuesta)
respuesta = client.service.Dividir(a=6, b=4)
print(respuesta)