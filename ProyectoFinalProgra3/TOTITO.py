import random
import tkinter as tk
from graphviz import Digraph
nivel_inteligencia = 0
# Integracion de AVL
class NodoAVL:
    def __init__(self, estado):
        self.estado = estado
        self.puntaje = 0
        self.izq = None
        self.der = None
class AVL:
    def __init__(self):
        self.raiz = None
    def insertar(self, estado):
        self.raiz = self._insertar(self.raiz, estado)
    def _insertar(self, n, estado):
        if not n:
            return NodoAVL(estado)
        if estado < n.estado:
            n.izq = self._insertar(n.izq, estado)
        elif estado > n.estado:
            n.der = self._insertar(n.der, estado)
        return n
    def buscar(self, estado):
        return self._buscar(self.raiz, estado)
    def _buscar(self, n, estado):
        if not n or n.estado == estado:
            return n
        if estado < n.estado:
            return self._buscar(n.izq, estado)
        return self._buscar(n.der, estado)
# Integracion de lista enlazada
class NodoH:
    def __init__(self, estado):
        self.estado = estado
        self.sig = None
class Historial:
    def __init__(self):
        self.cabeza = None
    def agregar(self, estado):
        n = NodoH(estado)
        n.sig = self.cabeza
        self.cabeza = n
# ARBOL B
class Clave:
    def __init__(self, idp, res, estado):
        self.id = idp
        self.res = res
        self.estado = estado
        self.sig = None
class ArbolB:
    def __init__(self):
        self.raiz = None
        self.id = 1
    def insertar(self, res, estado):
        n = Clave(self.id, res, estado)
        self.id += 1
        if not self.raiz:
            self.raiz = n
        else:
            a = self.raiz
            while a.sig:
                a = a.sig
            a.sig = n
    def mostrar(self):
        a = self.raiz
        if not a:
            print("Sin historial")
            return
        while a:
            print("ID:", a.id, "|", a.res, "|", a.estado)
            a = a.sig
# =========================
def verificar(e):
    comb = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in comb:
        if e[a]==e[b]==e[c] and e[a]!="_":
            return e[a]
    return None
def lleno(e):
    for c in e:
        if c == "_":
            return False
    return True
# RESULT SI PIERDO O GANA
def minimax(e, maximo):
    g = verificar(e)
    if g == "O": return 1
    if g == "X": return -1
    if lleno(e): return 0
    if maximo:
        mejor = -999
        for i in range(9):
            if e[i] == "_":
                val = minimax(e[:i]+"O"+e[i+1:], False)
                if val > mejor:
                    mejor = val
        return mejor
    else:
        mejor = 999
        for i in range(9):
            if e[i] == "_":
                val = minimax(e[:i]+"X"+e[i+1:], True)
                if val < mejor:
                    mejor = val
        return mejor
# DECISION
def mejor_mov(e, avl):
    global nivel_inteligencia
    if nivel_inteligencia > 300:
        mejor = -999
        pos = 0
        for i in range(9):
            if e[i] == "_":
                val = minimax(e[:i]+"O"+e[i+1:], False)
                if val > mejor:
                    mejor = val
                    pos = i
        return pos
    #APRENDE AUTONOMO
    mejor = -9999
    pos = 0
    for i in range(9):
        if e[i] == "_":
            nuevo = e[:i]+"O"+e[i+1:]
            nodo = avl.buscar(nuevo)
            p = nodo.puntaje if nodo else 0
            p += random.randint(-50,50)
            if p > mejor:
                mejor = p
                pos = i
    return pos
# GRAPHVIZ
def generar_dot(historial, idp, avl):
    dot = Digraph(comment=f"Partida {idp}")
    dot.attr(rankdir="LR")
    actual = historial.cabeza
    i = 0
    while actual and actual.sig:
        nodo = avl.buscar(actual.estado)
        peso = nodo.puntaje if nodo else 0
        n1 = f"{i}\n{actual.estado}\nP:{peso}"
        n2 = f"{i+1}\n{actual.sig.estado}"
        dot.node(n1)
        dot.node(n2)
        dot.edge(n1, n2)
        actual = actual.sig
        i += 1
    dot.render(f"partida_{idp}", format="png", cleanup=True)
# GUI
def gui(avl, b):
    global nivel_inteligencia
    estado = "_________"
    terminado = False
    hist = Historial()
    v = tk.Tk()
    v.title("TOTITO SUPERIOR")
    v.geometry("320x360")
    botones = {}
    def actualizar():
        for i in range(9):
            botones[i]["text"] = estado[i] if estado[i]!="_" else ""
    def fin(msg):
        nonlocal terminado
        terminado = True
        b.insertar(msg, estado)
        pts = 500 if msg=="YO GANO" else -500 if msg=="GANASTE" else 100
        n = hist.cabeza
        while n:
            nodo = avl.buscar(n.estado)
            if nodo:
                nodo.puntaje += pts
            n = n.sig
        generar_dot(hist, b.id-1, avl)
        label["text"] = msg
    def click(i):
        nonlocal estado
        if terminado or estado[i]!="_":
            return
        hist.agregar(estado)
        estado = estado[:i]+"X"+estado[i+1:]
        if avl.buscar(estado) is None:
            avl.insertar(estado)
        actualizar()
        if verificar(estado): return fin("GANASTE")
        if lleno(estado): return fin("EMPATE")
        pos = mejor_mov(estado, avl)
        estado = estado[:pos]+"O"+estado[pos+1:]
        if avl.buscar(estado) is None:
            avl.insertar(estado)
        actualizar()
        if verificar(estado): return fin("YO GANO")
        if lleno(estado): return fin("EMPATE")
    def reset():
        nonlocal estado, terminado, hist
        estado = "_________"
        terminado = False
        hist = Historial()
        label["text"] = "Nueva"
        actualizar()
    for i in range(9):
        btt = tk.Button(v, text="", width=6, height=3,
                        font=("Arial",14),
                        command=lambda i=i: click(i))
        btt.grid(row=i//3, column=i%3)
        botones[i] = btt
    label = tk.Label(v, text="JUEGA")
    label.grid(row=3, column=0, columnspan=3)
    tk.Button(v, text="OTRA PARTIDA", command=reset)\
        .grid(row=4, column=0, columnspan=3)
    v.mainloop()
# REFUERZO
def entrenar(avl, b, n):
    global nivel_inteligencia
    for _ in range(n):
        estado = "_________"
        hist = Historial()
        turno = "X"
        while True:
            hist.agregar(estado)
            pos = random.randint(0,8)
            while estado[pos] != "_":
                pos = random.randint(0,8)
            estado = estado[:pos] + turno + estado[pos+1:]
            if avl.buscar(estado) is None:
                avl.insertar(estado)
            g = verificar(estado)
            if g or lleno(estado):
                pts = 500 if g=="O" else -500 if g=="X" else 100
                n2 = hist.cabeza
                while n2:
                    nodo = avl.buscar(n2.estado)
                    if nodo:
                        nodo.puntaje += pts
                    n2 = n2.sig
                b.insertar(g, estado)
                generar_dot(hist, b.id-1, avl)
                nivel_inteligencia += 1
                break
            turno = "O" if turno=="X" else "X"
def limpiar_estructura(arbol_jugadas, historial_partidas):
    arbol_jugadas.raiz = None
    historial_partidas.raiz = None
    historial_partidas.id = 1
    print("\nEHistorial de partidas reestablecido")
def mostrar_integrantes():
    print("\n===== INTEGRANTES =====")
    print("Nombre: Ricardo Andrés Monroy Morales")
    print("Carnet: 9490-24-5193")
    print("Sección: B")
    print("-----------------------")
    print("Nombre: Josselin Lisbeth Méndez Morales")
    print("Carnet: 9490-12-7444")
    print("Sección: B")
    print("=======================")
def buscar_victoria(arbol_jugadas, historial_partidas):
    intentos = 0
    while True:
        intentos += 1
        tablero = "_________"
        simbolo_turno = "X"
        while True:
            posicion = random.randint(0,8)
            while tablero[posicion] != "_":
                posicion = random.randint(0,8)
            tablero = tablero[:posicion] + simbolo_turno + tablero[posicion+1:]
            ganador = verificar(tablero)
            if ganador == "O":
                print("\nLa IA alcanzó victoria.")
                print("Iteraciones necesarias:", intentos)
                return
            if ganador or lleno(tablero):
                break
            simbolo_turno = "O" if simbolo_turno=="X" else "X"
def limpiar_estructura(arbol_jugadas, historial_partidas):
    global nivel_inteligencia
    arbol_jugadas.raiz = None
    historial_partidas.raiz = None
    historial_partidas.id = 1
    nivel_inteligencia = 0
    print("\nEstructuras reiniciadas correctamente.")
def mostrar_integrantes():
    print("\n===== INTEGRANTES =====")
    print("Nombre: Ricardo Andrés Monroy Morales")
    print("Carnet: 9490-24-5193")
    print("Sección: B")
    print("-----------------------")
    print("Nombre: Josselin Lisbeth Méndez Morales")
    print("Carnet: 9490-12-7444")
    print("Sección: B")
    print("======================")
def consultar_iteraciones():
    global nivel_inteligencia

    if nivel_inteligencia == 0:
        print("\nLa IA aún no ha ganado partidas.")
    else:
        print("\nIteraciones de aprendizaje:", nivel_inteligencia)
def menu():
    arbol_jugadas = AVL()
    historial_partidas = ArbolB()
    while True:
        print("\n========== MENU TOTITO ==========")
        print("1. Entrenar sistema manualmente")
        print("2. Entrenamiento automático")
        print("3. Jugar Totito")
        print("4. Ver historial de partidas")
        print("5. Consultar iteraciones de aprendizaje")
        print("6. Limpiar estructura de datos")
        print("7. Integrantes del grupo")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            print("\nEntrenamiento manual")
            partidas = int(input("¿Cuántas partidas desea entrenar al totito?: "))
            entrenar(arbol_jugadas, historial_partidas, partidas)
            print("Entrenamiento completado.")
        elif opcion == "2":
            print("\nEntrenamiento automático")
            partidas = int(input("Número de simulaciones automáticas: "))
            entrenar(arbol_jugadas, historial_partidas, partidas)
            print("Entrenamiento automático finalizado.")
        elif opcion == "3":
            gui(arbol_jugadas, historial_partidas)
        elif opcion == "4":
            print("\nHISTORIAL")
            historial_partidas.mostrar()
        elif opcion == "5":
            consultar_iteraciones()
        elif opcion == "6":
            limpiar_estructura(arbol_jugadas, historial_partidas)
        elif opcion == "7":
            mostrar_integrantes()
        elif opcion == "8":
            print("\nBye vuelve pronto :D")
            break
        else:
            print("\nOpción inválida.")
menu()
