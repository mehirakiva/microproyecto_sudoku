import random
import copy
import os

# Modo de visualización
conversiones = {
    'numerico': ['1', '2', '3', '4'],
    'letras': ['A', 'B', 'C', 'D'],
    'simbolos': ['', '', '', '']
}

tablero_solucion = [
    [1, 2, 3, 4],
    [3, 4, 1, 2],
    [4, 1, 2, 3],
    [2, 3, 4, 1]
]

def imprimir_tablero(tablero, modo='numerico', dificultad='facil'):
    valores = conversiones.get(modo, conversiones['numerico'])
    marco = '*' if dificultad == 'facil' else '-'
    letras_col = [' A ', ' B ', ' C ', ' D ']

    print("\n    " + "   ".join(letras_col))
    print("  " + marco * 17)
    for i, fila in enumerate(tablero):
        fila_convertida = [valores[num - 1] if num != 0 else ' ' for num in fila]
        print(f"{i+1} {marco} " + ' | '.join(fila_convertida) + f" {marco}")
        print("  " + marco * 17)

def generar_tablero(dificultad):
    tablero = copy.deepcopy(tablero_solucion)
    vaciar = 6 if dificultad == 'facil' else 10
    posiciones = [(i, j) for i in range(4) for j in range(4)]
    random.shuffle(posiciones)
    for i in range(vaciar):
        fila, col = posiciones[i]
        tablero[fila][col] = 0
    return tablero

def verificar_tablero(tablero_usuario):
    return tablero_usuario == tablero_solucion

def jugar(tablero_original, modo, dificultad, puntos, racha):
    tablero_usuario = copy.deepcopy(tablero_original)

    while True:
        imprimir_tablero(tablero_usuario, modo, dificultad)
        print(f"\n⭐ Puntaje actual: {puntos} | Racha: {racha}")
        print("\n📝 Opciones:")
        print(" - Escribe 'fila,columna,valor' para llenar una casilla (ej: 2,B,3)")
        print(" - Escribe 'verificar' para comprobar si terminaste")
        print(" - Escribe 'reiniciar' para comenzar de nuevo")
        print(" - Escribe 'menu' para volver al menú principal")
        entrada = input("👉 Tu entrada: ").strip().lower()

        if entrada == 'verificar':
            if verificar_tablero(tablero_usuario):
                bonificacion = 2 ** racha if racha > 0 else 0
                puntos_ganados = 10 + bonificacion
                puntos += puntos_ganados
                racha += 1
                print(f"\n🎉 ¡Correcto! Ganaste {puntos_ganados} puntos (10 base + {bonificacion} bonus)")
                return puntos, racha
            else:
                print("❌ Hay errores en tu tablero. Tu racha se reinicia.")
                racha = 0
        elif entrada == 'reiniciar':
            print("🔄 Reiniciando el tablero...")
            return 'reiniciar', racha
        elif entrada == 'menu':
            print("🏠 Volviendo al menú principal...")
            return puntos, racha
        else:
            try:
                partes = entrada.replace(' ', '').split(',')
                if len(partes) != 3:
                    raise ValueError

                fila = int(partes[0]) - 1
                columna = 'abcd'.index(partes[1])
                valor = int(partes[2])

                if not (0 <= fila <= 3 and 0 <= columna <= 3 and 1 <= valor <= 4):
                    raise ValueError

                if tablero_original[fila][columna] == 0:
                    tablero_usuario[fila][columna] = valor
                else:
                    print("🚫 Esa casilla no se puede modificar (es parte del tablero original).")
            except:
                print("⚠️ Entrada inválida. Usa el formato correcto: fila,columna,valor (ej: 2,B,3)")

# NUEVO: Cargar mejores puntajes desde archivo
def cargar_mejores_puntajes():
    if not os.path.exists("mejores_puntajes.txt"):
        return []
    with open("mejores_puntajes.txt", "r") as f:
        lineas = f.readlines()
    puntajes = []
    for linea in lineas:
        if '-' in linea:
            nombre, puntaje = linea.strip().split('-')
            puntajes.append((nombre.strip(), int(puntaje.strip())))
    return sorted(puntajes, key=lambda x: x[1], reverse=True)[:5]

# NUEVO: Guardar un nuevo puntaje si es uno de los mejores
def guardar_nuevo_puntaje(nombre, puntos):
    puntajes = cargar_mejores_puntajes()
    puntajes.append((nombre, puntos))
    puntajes_ordenados = sorted(puntajes, key=lambda x: x[1], reverse=True)[:5]
    with open("mejores_puntajes.txt", "w") as f:
        for nombre, p in puntajes_ordenados:
            f.write(f"{nombre} - {p}\n")

def mostrar_mejores_puntajes():
    print("\n🏆 Mejores Puntajes:")
    puntajes = cargar_mejores_puntajes()
    if not puntajes:
        print("No hay puntajes registrados aún.")
    else:
        for i, (nombre, p) in enumerate(puntajes, 1):
            print(f"{i}. {nombre} - {p} puntos")

def main():
    puntos = 0
    racha = 0

    while True:
        print("\n🔷🔷🔷 SUDOKU 4x4 🔷🔷🔷")
        print("1️⃣ Jugar Sudoku")
        print("2️⃣ Salir")
        print("3️⃣ Ver mejores puntajes")  # NUEVO
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            print("\n📌 Selecciona tipo de visualización:")
            print("1. Numérico (1-4)")
            print("2. Letras (A-D)")
            print("3. Símbolos (,,,)")
            tipo = input("Opción: ")
            modo = {'1': 'numerico', '2': 'letras', '3': 'simbolos'}.get(tipo, 'numerico')

            print("\n🎯 Selecciona nivel de dificultad:")
            dificultad = 'facil' if input("1. Fácil\n2. Difícil\nOpción: ") == '1' else 'dificil'

            while True:
                tablero = generar_tablero(dificultad)
                resultado, racha = jugar(tablero, modo, dificultad, puntos, racha)
                if resultado != 'reiniciar':
                    puntos = resultado
                    break

        elif opcion == '2':
            print(f"\n👋 Gracias por jugar. Puntaje final: {puntos}")
            puntajes_actuales = cargar_mejores_puntajes()
            if not puntajes_actuales or puntos > puntajes_actuales[-1][1]:
                nombre = input("🎖️ Nuevo puntaje alto. Escribe tu nombre: ")
                guardar_nuevo_puntaje(nombre, puntos)
                print("✅ Puntaje guardado.")
            break

        elif opcion == '3':
            mostrar_mejores_puntajes()
        else:
            print("❌ Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    main()
