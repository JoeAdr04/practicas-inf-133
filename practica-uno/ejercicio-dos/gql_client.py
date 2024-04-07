import requests
# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
# listar todas las plantas
response = requests.post(url, json={'query': query_lista})
print(response.text)

query_crear = """
muatation{
    crearPlanta(nombre: "asdf", especie: "fddf", edad: 2, altura: 4.4, frutos: True){
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

# buscar plantas por especie
query = """
    {
        plantaPorEspecie(especie: "flor"){
            nombre
        }
    }
"""

# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query})
print(response.text)

#bsucar las plantas que tienen frutos

query = """
    {
        plantaPorFruto(fruto: True){
        nombre
        }
    }
"""

response = requests.post(url,json= {'query': query})
print(response.text)

query_update = """
mutation{
    updatePlanta(id: 2, nombre: "manzanilla", especie: "ramas", edad: 1, altura: 2, frutos: False){
        plata{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response_mutation = requests.post(url,json={'query': query_update})
print(response_mutation.text)

query_eliminar = """
mutation{
    deletePlanta(id: 1){
        planta{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response_mutation = requests.post(url,json={'query': query_eliminar})
print(response_mutation.text)