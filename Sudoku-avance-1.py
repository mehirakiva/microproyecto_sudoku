import random
import copy

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

def jugar(tablero_original, modo, dificultad):
    tablero_usuario = copy.deepcopy(tablero_original)

    while True:
        imprimir_tablero(tablero_usuario, modo, dificultad)
        print("\n📝 Opciones:")
        print(" - Escribe 'fila,columna,valor' para llenar una casilla (ej: 2,B,3)")
        print(" - Escribe 'verificar' para comprobar si terminaste")
        print(" - Escribe 'reiniciar' para comenzar de nuevo")
        print(" - Escribe 'menu' para volver al menú principal")
        entrada = input("👉 Tu entrada: ").strip().lower()

        if entrada == 'verificar':
            if verificar_tablero(tablero_usuario):
                print("🎉 ¡Felicidades, completaste el Sudoku correctamente!")
                return
            else:
                print("❌ Hay errores en tu tablero. ¡Sigue intentando!")
        elif entrada == 'reiniciar':
            print("🔄 Reiniciando el tablero...")
            return 'reiniciar'
        elif entrada == 'menu':
            print("🏠 Volviendo al menú principal...")
            return

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

def main():
    while True:
        print("\n🔷🔷🔷 SUDOKU 4x4 🔷🔷🔷")
        print("1️⃣ Jugar Sudoku")
        print("2️⃣ Salir")
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
                resultado = jugar(tablero, modo, dificultad)
                if resultado != 'reiniciar':
                    break

        elif opcion == '2':
            print("👋 Gracias por jugar. ¡Hasta la próxima!")
            break
        else:
            print("❌ Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    main()

