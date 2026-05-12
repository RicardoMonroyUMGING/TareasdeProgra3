import csv
import os
from graphviz import Digraph

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Grado mínimo
        self.leaf = leaf
        self.keys = []
        self.child = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    # --- Operaciones de Búsqueda ---
    def search(self, k, x=None):
        if x is None: x = self.root
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            return x
        if x.leaf:
            return None
        return self.search(k, x.child[i])

    # --- Operaciones de Inserción ---
    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode(self.t, False)
            self.root = new_root
            new_root.child.insert(0, root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.child[i], k)

    def _split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(t, y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t]

    # --- Operaciones de Eliminación (Simplificada para estabilidad) ---
    def delete(self, k):
        self._delete(self.root, k)
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.child[0]

    def _delete(self, x, k):
        t = self.t
        if k in x.keys:
            if x.leaf:
                x.keys.remove(k)
            else:
                # Caso complejo: El nodo no es hoja (requiere buscar predecesor/sucesor)
                idx = x.keys.index(k)
                x.keys[idx] = self._get_predecessor(x, idx)
        else:
            if x.leaf: return # No encontrado
            # Lógica de descenso y rebalanceo...
            # Para fines académicos, aquí se implementa la búsqueda recursiva
            for i, key in enumerate(x.keys):
                if k < key:
                    self._delete(x.child[i], k)
                    return
            self._delete(x.child[-1], k)

    def _get_predecessor(self, x, i):
        curr = x.child[i]
        while not curr.leaf:
            curr = curr.child[-1]
        return curr.keys.pop(-1)

    # --- Utilidades: CSV y Gráficos ---
    def load_csv(self, filename):
        if not os.path.exists(filename):
            print(f"Error: El archivo {filename} no existe.")
            return
        with open(filename, mode='r') as f:
            reader = csv.reader(f)
            count = 0
            for row in reader:
                for item in row:
                    try:
                        self.insert(int(item.strip()))
                        count += 1
                    except ValueError: continue
            print(f"Se cargaron {count} claves exitosamente.")

    def plot(self, name="btree_graph"):
        dot = Digraph(format='png')
        dot.attr('node', shape='record', style='filled', fillcolor='lightblue')
        
        def add_nodes(node):
            node_id = str(id(node))
            label = " | ".join(map(str, node.keys))
            dot.node(node_id, f"{{ {label} }}")
            if not node.leaf:
                for i, child in enumerate(node.child):
                    child_id = add_nodes(child)
                    dot.edge(node_id, child_id)
            return node_id

        add_nodes(self.root)
        dot.render(name, view=True, cleanup=True)

# --- Interfaz de Consola ---
def menu():
    print("\n--- CONFIGURACIÓN INICIAL ---")
    t = int(input("Ingrese el grado mínimo del Árbol B (t >= 2): "))
    tree = BTree(t)

    while True:
        print(f"\n[Árbol B Grado {t}]")
        print("1. Insertar clave")
        print("2. Buscar clave")
        print("3. Eliminar clave")
        print("4. Cargar CSV masivo")
        print("5. Generar gráfico (Graphviz)")
        print("6. Salir")
        op = input("Seleccione una opción: ")

        if op == "1":
            val = int(input("Clave a insertar: "))
            tree.insert(val)
        elif op == "2":
            val = int(input("Clave a buscar: "))
            res = tree.search(val)
            print("Encontrada" if res else "No encontrada")
        elif op == "3":
            val = int(input("Clave a eliminar: "))
            tree.delete(val)
        elif op == "4":
            path = input("Nombre del archivo CSV (ej. datos1.csv): ")
            tree.load_csv(path)
        elif op == "5":
            tree.plot()
        elif op == "6":
            break

if __name__ == "__main__":
    menu()