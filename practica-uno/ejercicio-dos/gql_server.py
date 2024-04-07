from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, Float, List, Schema, Field, Mutation

class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Float()
    frutos = Boolean()

    def set_nombre(self, nombre):
        self.nombre = nombre
    def set_especie(self, especie):
        self.nombre = especie
    def set_edad(self, edad):
        self.nombre = edad
    def set_altura(self, altura):
        self.nombre = altura
    def set_frutos(self, frutos):
        self.nombre = frutos


class Query(ObjectType):
    plantas = List(Planta)
    planta_por_especie = Field(Planta, especie=String())
    planta_por_fruto = Field(Planta, fruto = Boolean())
    def resolve_plantas(root, info):
        return plantas
    
    def resolve_planta_por_especie(root,info,especie):
        for planta in plantas:
            if planta.especie == especie:
                return planta
        return None
    
    def resolve_planta_por_fruto(root,info,fruto):
        for planta in plantas:
            if planta.fruto == fruto:
                return planta
        return None
    
    
class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Float()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre, especie, edad, altura, frutos):
        nueva_planta = Planta(
            id=len(plantas) + 1,
            nombre = nombre, 
            especie=especie, 
            edad = edad,
            altura = altura,
            frutos=frutos
        )
        plantas.append(nueva_planta)

        return CrearPlanta(planta=nueva_planta)

class UpdatePlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String()
        especie = String()
        edad = Int()
        altura = Float()
        frutos = Boolean()
        
    planta = Field(Planta)
    planta_por_id = Field(Planta, id=Int())

    def mutate(root, info, id, nombre, especie, edad, altura, frutos):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                planta.set_nombre(nombre)
                planta.set_especie(especie)
                planta.set_edad(edad)
                planta.set_altura(altura)
                planta.set_frutos(frutos)

                return UpdatePlanta(planta=planta)
        return None

class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None

##class ModificarPlanta(Mutation)

class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()
    update_planta = UpdatePlanta.Field()

plantas = [
    Planta(id=1, nombre="Girasol", especie="flor", edad = 2, altura = 3.33,  frutos=False),
    Planta(id=2, nombre="Ciruelo", especie="arbol", edad = 8, altura = 2.22, frutos=True),
]

schema = Schema(query=Query, mutation=Mutations)



class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()