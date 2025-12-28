print("***********************************")
print("**  Calculadora de Descuentos  **")
print("***********************************\n")

# ==================================================================
# Utilidades de entrada (float) y validacion
# ==================================================================

print("Ingresa tu nombre: ")
nombre = input()
print("Ingresa tu apellido: ")
apellido = input()

nombre_completo = nombre + " " + apellido
print(" ")

print("Bienvenido al programa de descuentos", nombre_completo)
print("")

lista_compras = []

# Validacion de que se selecccione una de las opciones ofrecidas, de lo contrario se muestra el mensaje de entrada invalida

def pedir_texto(mensaje: str, *, pedir_vacio: bool = False, valor_actual: str | None = None) -> str:
    while True:
        if valor_actual is not None:
            entrada = input(f"{mensaje} actual: {valor_actual}): ").strip()
        else:
            entrada = input(f"{mensaje}: ").strip()
        
        if pedir_vacio and entrada == "":
            print("Entrada invalida. Este campo no puede estar vacio.")
            continue
        return entrada
    
# Validacion de cantidades y precio, asigne un vcalor minimo y maximo que el usuario puede escoger del producto que ingrese al sistema
    
def pedir_precio(mensaje: str, *, pedir_vacio: bool = False, valor_actual: float | None = None, min_val: float | None = None, max_val: float | None = None) -> float | None:
    while True:
        if valor_actual is not None:
            entrada = input(f"{mensaje} (actual: {valor_actual}): ").strip()
        else:
            entrada = input(f"{mensaje}: ").strip()
        if pedir_vacio and entrada == "":
            return None
        try:
            numero = float(entrada)
        except ValueError:
            print("Entrada no valida. Debes ingresar un numero.")
            continue
        if min_val is not None and numero < min_val:
            print(f"Entrada no valida. Debe ser >= {min_val}")
            continue
        if max_val is not None and numero > max_val:
            print(f"Entrada no valida. Debe ser <= {max_val}.")
            continue
        return numero
    
# Confirmacion de eliminacion de un producto, le coloque la condicional al usuario para que introduzca las opciones que aparece en el texto, de lo contrario devuelve el mensaje de respuesta no valida 
    
def pedir_confirmacion(mensaje: str) -> bool:
    while True:
        entrada = input(f"{mensaje} (S/N): ").strip().lower()
        if entrada in ("s", "si", "sí"): return True
        if entrada in ("n", "no"): return False
        print("Respuesta no valida")

def seleccionar_indice_producto() -> int | None:
    if not lista_compras:
        print("\n---- Lista de compras ----")
        print("No hay productos registrados.")
        return None
    
    print("---- Lista de compras -----")
    for i, articulo in enumerate(lista_compras, start=1):
        print(f"{i}. articulo: {articulo.get('articulo')}, precio: {articulo.get('precio')}, cantidad: {articulo.get('cantidad')}")

    numero = pedir_precio("Ingresa el numero del producto: ", min_val=1, max_val=len(lista_compras))
    return (int(numero) - 1) if numero is not None else None


# =================================================================
# Funciones principales del CRUD
# =================================================================

def agregar_articulo():
    print("\n--- Agregar Producto ---")
    articulo = pedir_texto("Introduce el nombre del producto")
    precio = pedir_precio("Introduce el precio", min_val=0.25, max_val=10000)
    cantidad = pedir_precio("Introduce la cantidad a llevar", min_val=1, max_val=100)

    nuevo_producto = {"articulo": articulo, "precio": float(precio), "cantidad": int(cantidad) }

    lista_compras.append(nuevo_producto)
    print(f"Producto '{cantidad} {articulo}' agregado.")

def mostrar_lista():
    print("\n--- Lista de compras ---")
    if not lista_compras:
        print("No hay productos registrados.")
        return
    for i, articulo in enumerate(lista_compras, start=1):
        print(f"{i}. Producto: {articulo.get('articulo')}, Precio: {articulo.get('precio')}, Cantidad: {articulo.get('cantidad')}")

def eliminar_producto():
    print("\n--- Eliminar Producto ---")
    indice = seleccionar_indice_producto()
    if indice is None: return

    articulo = lista_compras [indice]
    if pedir_confirmacion(f"¿Eliminar '{articulo['cantidad']} {articulo['articulo']}'?"):
        lista_compras.pop(indice)
        print("Producto eliminado.")

def editar_producto():
    print("\n--- Editar Producto ---")
    indice = seleccionar_indice_producto()
    if indice is None: return
    articulo = lista_compras[indice]

    nuevo_articulo = input(f"Nuevo Producto (actual: {articulo.get('articulo')}): ").strip()
    entrada_precio = input(f"Nuevo Precio (actual: {articulo.get('precio')}): ").strip()
    entrada_cantidad = input(f"Nueva Cantidad (actual: {articulo.get('cantidad')}): ").strip()

    editado = False
    if nuevo_articulo != "":
        articulo["articulo"] = nuevo_articulo
        editado = True
    if entrada_precio != "":
        try:
            articulo["precio"] = float(entrada_precio)
            editado = True
        except ValueError:
            print("Precio no válido. No se cambió el precio.")
    if entrada_cantidad != "":
        try:
            articulo["cantidad"] = int(entrada_cantidad)
            editado = True
        except ValueError:
            print("Cantidad no válida. No se cambió la cantidad.")

    if editado:
        print("Datos actualizados.")
    else:
        print("No se realizaron cambios.")

def calcular_total(precio_unitario, cantidad, descuento_pct=10):
    total = precio_unitario * cantidad
    if cantidad > 2:
        total *= (1 - descuento_pct / 100)
        descuento_aplicado = True
    else:
        descuento_aplicado = False
    return total, descuento_aplicado


def revisar_descuentos(descuento_pct: float = 10.0):
    if not lista_compras:
        print("\nNo hay productos en la lista.")
        return
    total_carrito = 0.0
    print("\n--- Revisión de descuentos ---")
    for articulo in lista_compras:
        nombre = articulo.get("articulo")
        precio = float(articulo.get("precio"))
        cantidad = int(articulo.get("cantidad"))
        subtotal = precio * cantidad
        if cantidad > 2:
            descuento = subtotal * (descuento_pct / 100)
            subtotal_desc = subtotal - descuento
            aplicado = True
        else:
            descuento = 0.0
            subtotal_desc = subtotal
            aplicado = False
        total_carrito += subtotal_desc
        if aplicado:
            print(f"{nombre}: {cantidad} x {precio:.2f} -> descuento {descuento_pct}% aplicado. Subtotal: {subtotal_desc:.2f}")
        else:
            print(f"{nombre}: {cantidad} x {precio:.2f} -> sin descuento. Subtotal: {subtotal_desc:.2f}")
    print(f"Total a pagar: {total_carrito:.2f}")

if __name__ == "__main__":
    while True:
        print("\n1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Editar producto")
        print("4. Mostrar lista de compras")
        print("5. Revisar descuento aplicable")
        print("0. Salir")
        try:
            respuesta = int(input("Ingresa la opcion a elegir: "))
        except ValueError:
            print("Entrada invalida. Ingresa un numero.")
            continue

        if respuesta == 1:
            agregar_articulo()
        elif respuesta == 2:
            eliminar_producto()
        elif respuesta == 3:
            editar_producto()
        elif respuesta == 4:
            mostrar_lista()
        elif respuesta == 5:
            revisar_descuentos()
        elif respuesta == 0:
            print("Saliendo...")
            break
        else:
            print("Opcion no valida.")



        

