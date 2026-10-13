import json
from pathlib import Path


ARCHIVO_PEDIDOS = Path("pedidos.json")

MENU = {
    "1": {"nombre": "Hamburguesa clásica", "precio": 18000},
    "2": {"nombre": "Pizza personal", "precio": 22000},
    "3": {"nombre": "Jugo natural", "precio": 7000},
    "4": {"nombre": "Pasta del día", "precio": 16000},
      
}

ESTADOS = ["Recibido", "Preparando", "Listo", "Entregado", "Cancelado"]


def formato_pesos(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")


def cargar_pedidos():
    if not ARCHIVO_PEDIDOS.exists():
        return []

    with ARCHIVO_PEDIDOS.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_pedidos(pedidos):
    with ARCHIVO_PEDIDOS.open("w", encoding="utf-8") as archivo:
        json.dump(pedidos, archivo, ensure_ascii=False, indent=2)


def mostrar_menu():
    print("\n--- Menú de La Buena Mesa ---")
    for numero, producto in MENU.items():
        precio = formato_pesos(producto["precio"])
        print(f"{numero}. {producto['nombre']} - {precio}")


def crear_pedido():
    cliente = input("Nombre del cliente: ").strip()

    if not cliente:
        print("Escribe un nombre para el pedido.")
        return

    mostrar_menu()
    print("Escribe 0 cuando termines de agregar productos.")

    items = []

    while True:
        numero = input("Número del producto: ").strip()

        if numero == "0":
            break

        if numero not in MENU:
            print("Ese producto no está en el menú.")
            continue

        cantidad_texto = input("Cantidad: ").strip()

        if not cantidad_texto.isdigit() or int(cantidad_texto) < 1:
            print("La cantidad debe ser un número mayor que cero.")
            continue

        producto = MENU[numero]
        items.append(
            {
                "producto": producto["nombre"],
                "precio": producto["precio"],
                "cantidad": int(cantidad_texto),
            }
        )

    if not items:
        print("No se creó el pedido porque no agregaste productos.")
        return

    pedidos = cargar_pedidos()
    nuevo_id = max((pedido["id"] for pedido in pedidos), default=0) + 1
    total = sum(item["precio"] * item["cantidad"] for item in items)

    pedido = {
        "id": nuevo_id,
        "cliente": cliente,
        "items": items,
        "total": total,
        "estado": "Recibido",
    }

    pedidos.append(pedido)
    guardar_pedidos(pedidos)

    print(f"\nPedido #{nuevo_id} guardado para {cliente}.")
    print(f"Total: {formato_pesos(total)}")


def listar_pedidos():
    pedidos = cargar_pedidos()

    if not pedidos:
        print("\nTodavía no hay pedidos.")
        return

    print("\n--- Pedidos registrados ---")
    for pedido in pedidos:
        total = formato_pesos(pedido["total"])
        print(
            f"#{pedido['id']} | {pedido['cliente']} | "
            f"{total} | {pedido['estado']}"
        )


def cambiar_estado():
    pedidos = cargar_pedidos()

    if not pedidos:
        print("\nNo hay pedidos para actualizar.")
        return

    listar_pedidos()
    id_texto = input("\nNúmero del pedido que quieres actualizar: ").strip()

    if not id_texto.isdigit():
        print("Escribe un número de pedido válido.")
        return

    id_pedido = int(id_texto)
    pedido = next(
        (pedido for pedido in pedidos if pedido["id"] == id_pedido),
        None,
    )

    if pedido is None:
        print("No se encontró ese pedido.")
        return

    print("\nEstados disponibles:")
    for numero, estado in enumerate(ESTADOS, start=1):
        print(f"{numero}. {estado}")

    opcion = input("Elige el nuevo estado: ").strip()

    if not opcion.isdigit() or not 1 <= int(opcion) <= len(ESTADOS):
        print("Elige uno de los números de la lista.")
        return

    pedido["estado"] = ESTADOS[int(opcion) - 1]
    guardar_pedidos(pedidos)

    print(f"El pedido #{id_pedido} ahora está: {pedido['estado']}.")


def main():
    while True:
        print("\n=== La Buena Mesa: pedidos ===")
        print("1. Crear pedido")
        print("2. Ver pedidos")
        print("3. Cambiar estado de un pedido")
        print("4. Ver menú")
        print("5. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            crear_pedido()
        elif opcion == "2":
            listar_pedidos()
        elif opcion == "3":
            cambiar_estado()
        elif opcion == "4":
            mostrar_menu()
        elif opcion == "5":
            print("¡Gracias por usar La Buena Mesa!")
            break
        else:
            print("Opción no válida. Elige un número del 1 al 5.")


if __name__ == "__main__":
    main()