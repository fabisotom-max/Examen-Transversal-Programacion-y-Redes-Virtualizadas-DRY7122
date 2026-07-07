import requests
import itertools

API_KEY = "a4e0fa61-126f-4249-bc8a-9a177475a304"

VEHICULOS = {"1": "car", "2": "bike", "3": "foot"}


def geocodificar(ciudad, pais=None):
    r = requests.get("https://graphhopper.com/api/1/geocode",
                     params={"q": ciudad, "limit": 5, "key": API_KEY})
    hits = r.json().get("hits", [])

    if pais:
        hits.sort(key=lambda h: 0 if h.get("country", "").lower() == pais.lower() else 1)

    return [{"lat": h["point"]["lat"], "lng": h["point"]["lng"],
             "nombre": h.get("name", ciudad), "pais": h.get("country", "")} for h in hits]


def calcular_ruta(origen, destino, vehiculo):
    r = requests.get("https://graphhopper.com/api/1/route", params={
        "point": [f"{origen['lat']},{origen['lng']}", f"{destino['lat']},{destino['lng']}"],
        "vehicle": vehiculo,
        "locale": "es",
        "instructions": "true",
        "key": API_KEY
    })

    data = r.json()
    return data["paths"][0] if data.get("paths") else None


def main():
    while True:
        origen = input("Ciudad de Origen: ")

        if origen.lower() == "s":
            break

        destino = input("Ciudad de Destino: ")

        if destino.lower() == "s":
            break

        origenes = geocodificar(origen, "Chile")
        destinos = geocodificar(destino, "Argentina")

        if not origenes or not destinos:
            print("No encontré esas ciudades.\n")
            continue

        print("1 Auto  2 Bici  3 A pie  s Salir")
        opcion = input("Medio de transporte: ")

        if opcion.lower() == "s":
            break

        vehiculo = VEHICULOS.get(opcion)

        if vehiculo is None:
            print("Opción inválida.\n")
            continue

        path = None

        for o, d in itertools.product(origenes, destinos):
            path = calcular_ruta(o, d, vehiculo)

            if path:
                break

        if not path:
            print("No se pudo calcular la ruta.\n")
            continue

        km = path["distance"] / 1000
        millas = km * 0.621371
        minutos = path["time"] / 60000

        print(f"\nDistancia: {km:.1f} km / {millas:.1f} millas")
        print(f"Duración: {int(minutos // 60)}h {int(minutos % 60)}min")

        print("\nNarrativa del viaje:")

        for i, paso in enumerate(path.get("instructions", []), 1):
            print(f"{i}. {paso['text']}")

        print()

    print("Saliendo del script!!")


main()
