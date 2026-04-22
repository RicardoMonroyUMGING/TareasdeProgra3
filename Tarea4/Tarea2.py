import csv
import os
from graphviz import Source

# ---------------- NODO ----------------
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 1


# ---------------- ABB ----------------
class ABB:
    def insertar(self, raiz, valor):
        if not raiz:
            return Nodo(valor)
        elif valor < raiz.valor:
            raiz.izq = self.insertar(raiz.izq, valor)
        else:
            raiz.der = self.insertar(raiz.der, valor)
        return raiz

    def buscar(self, raiz, valor):
        if not raiz or raiz.valor == valor:
            return raiz
        if valor < raiz.valor:
            return self.buscar(raiz.izq, valor)
        return self.buscar(raiz.der)

    def minimo(self, nodo):
        while nodo.izq:
            nodo = nodo.izq
        return nodo

    def eliminar(self, raiz, valor):
        if not raiz:
            return raiz

        if valor < raiz.valor:
            raiz.izq = self.eliminar(raiz.izq, valor)
        elif valor > raiz.valor:
            raiz.der = self.eliminar(raiz.der, valor)
        else:
            if not raiz.izq:
                return raiz.der
            elif not raiz.der:
                return raiz.izq

            temp = self.minimo(raiz.der)
            raiz.valor = temp.valor
            raiz.der = self.eliminar(raiz.der, temp.valor)

        return raiz


# ---------------- AVL ----------------
class AVL(ABB):

    def altura(self, nodo):
        return nodo.altura if nodo else 0

    def balance(self, nodo):
        return self.altura(nodo.izq) - self.altura(nodo.der)

    def rotar_derecha(self, y):
        x = y.izq
        T2 = x.der

        x.der = y
        y.izq = T2

        y.altura = 1 + max(self.altura(y.izq), self.altura(y.der))
        x.altura = 1 + max(self.altura(x.izq), self.altura(x.der))

        return x

    def rotar_izquierda(self, x):
        y = x.der
        T2 = y.izq

        y.izq = x
        x.der = T2

        x.altura = 1 + max(self.altura(x.izq), self.altura(x.der))
        y.altura = 1 + max(self.altura(y.izq), self.altura(y.der))

        return y

    def insertar(self, raiz, valor):
        raiz = super().insertar(raiz, valor)

        raiz.altura = 1 + max(self.altura(raiz.izq), self.altura(raiz.der))
        balance = self.balance(raiz)

        # Rotaciones
        if balance > 1 and valor < raiz.izq.valor:
            return self.rotar_derecha(raiz)

        if balance < -1 and valor > raiz.der.valor:
            return self.rotar_izquierda(raiz)

        if balance > 1 and valor > raiz.izq.valor:
            raiz.izq = self.rotar_izquierda(raiz.izq)
            return self.rotar_derecha(raiz)

        if balance < -1 and valor < raiz.der.valor:
            raiz.der = self.rotar_derecha(raiz.der)
            return self.rotar_izquierda(raiz)

        return raiz

    def eliminar(self, raiz, valor):
        raiz = super().eliminar(raiz, valor)

        if not raiz:
            return raiz

        raiz.altura = 1 + max(self.altura(raiz.izq), self.altura(raiz.der))
        balance = self.balance(raiz)

        # Rebalanceo
        if balance > 1 and self.balance(raiz.izq) >= 0:
            return self.rotar_derecha(raiz)

        if balance > 1 and self.balance(raiz.izq) < 0:
            raiz.izq = self.rotar_izquierda(raiz.izq)
            return self.rotar_derecha(raiz)

        if balance < -1 and self.balance(raiz.der) <= 0:
            return self.rotar_izquierda(raiz)

        if balance < -1 and self.balance(raiz.der) > 0:
            raiz.der = self.rotar_derecha(raiz.der)
            return self.rotar_izquierda(raiz)

        return raiz


# ---------------- CSV ----------------
def cargar_csv(ruta):
    datos = []
    with open(ruta, newline='') as archivo:
        reader = csv.reader(archivo)
        for fila in reader:
            for valor in fila:
                datos.append(int(valor))
    return datos


# ---------------- GRAPHVIZ ----------------
def generar_dot(raiz):
    dot = "digraph AVL {\n"

    def recorrer(nodo):
        nonlocal dot
        if nodo:
            if nodo.izq:
                dot += f"{nodo.valor} -> {nodo.izq.valor};\n"
                recorrer(nodo.izq)
            if nodo.der:
                dot += f"{nodo.valor} -> {nodo.der.valor};\n"
                recorrer(nodo.der)

    recorrer(raiz)
    dot += "}"
    return dot


def visualizar_arbol(raiz):
    if not raiz:
        print("Árbol vacío")
        return

    dot = generar_dot(raiz)
    Source(dot).render("arbol_avl", format="png", view=True)
    print("Imagen generada: arbol_avl.png")


# ---------------- MENU ----------------
def menu():
    print("\n--- ÁRBOL AVL ---")
    print("1. Insertar")
    print("2. Buscar")
    print("3. Eliminar")
    print("4. Cargar CSV")
    print("5. Visualizar Graphviz")
    print("6. Salir")


def main():
    arbol = AVL()
    raiz = None

    while True:
        menu()
        op = input("Seleccione una opción: ")

        if op == "1":
            valor = int(input("Ingrese número: "))
            raiz = arbol.insertar(raiz, valor)

        elif op == "2":
            valor = int(input("Buscar: "))
            res = arbol.buscar(raiz, valor)
            print("Encontrado" if res else "No encontrado")

        elif op == "3":
            valor = int(input("Eliminar: "))
            raiz = arbol.eliminar(raiz, valor)

        elif op == "4":
            ruta = input("Ruta CSV: ")
            datos = cargar_csv(ruta)
            for d in datos:
                raiz = arbol.insertar(raiz, d)

        elif op == "5":
            visualizar_arbol(raiz)

        elif op == "6":
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    main()