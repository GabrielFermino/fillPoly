import tkinter as tk
from tkinter import colorchooser

class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.cor = color

    def xy(self):
        return (self.x, self.y)
    
class Triangle:
    def __init__(self, id):
        self.points = []
        self.id = id
        self.cor = "black"  # Cor padrão para arestas

class Application():
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho 1 - Computação Gráfica")
        self.points = []
        self.triangulos = []

        self.barraMenu = tk.Menu(self.root)
        self.root.config(menu=self.barraMenu)

        self.menuArquivo = tk.Menu(self.barraMenu)

        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.sair)

        self.toolbar = tk.Frame(self.root, bg="gray")
        self.toolbar.pack(side="top", fill="x")

        self.botao_novo = tk.Button(self.toolbar, text="Novo Triângulo", command=self.newTriangle)
        self.botao_novo.pack(side=tk.LEFT)

        self.botao_remover = tk.Button(self.toolbar, text="Remover Triângulo Selecionado", command=self.removeTriangle)
        self.botao_remover.pack(side=tk.LEFT)
        self.botao_remover.config(state=tk.DISABLED)

        self.botao_pintar = tk.Button(self.toolbar, text="Pintar Arestas", command=self.paintEdge)
        self.botao_pintar.pack(side=tk.LEFT)
        self.botao_pintar.config(state=tk.DISABLED)

        self.botao_editar = tk.Button(self.toolbar, text="Editar Pontos do Triângulo Selecionado", command=self.editTriangle)
        self.botao_editar.pack(side=tk.LEFT)
        self.botao_editar.config(state=tk.DISABLED)

        self.botao_parar_edicao = tk.Button(self.toolbar, text="Parar Edição", command=self.stopEdit)
        self.botao_parar_edicao.pack(side=tk.LEFT)
        self.botao_parar_edicao.config(state=tk.DISABLED)

        self.botao_pintar_pontos = tk.Button(self.toolbar, text="Pintar Pontos", command=self.paintPoints)
        self.botao_pintar_pontos.pack(side=tk.LEFT)
        self.botao_pintar_pontos.config(state=tk.DISABLED)

        self.botao_preencher = tk.Button(self.toolbar, text="Preencher", command=lambda: self.fillPoly(self.selectedTriangle))
        self.botao_preencher.pack(side=tk.LEFT)
        self.botao_preencher.config(state=tk.DISABLED)

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.lista_triangulos = tk.Listbox(self.root)
        self.lista_triangulos.pack()
        self.lista_triangulos.bind("<ButtonRelease-1>", self.selectTriangle)

        self.canvas.bind("<Button-1>", self.addPoints)

        self.id_triangle = 1

    def addPoints(self, event):
            if self.adding_points: 
                x, y = event.x, event.y
                color = colorchooser.askcolor()[1]
                self.points.append(Point(x, y, color))

                if len(self.points) == 3:
                    triangle = Triangle(self.id_triangle)
                    self.triangulos.append(triangle)
                    triangle.points = self.points
                    self.id_triangle += 1
                    self.lista_triangulos.insert(tk.END, "Triângulo " + str(triangle.id))

                    self.drawTriangle()
                    self.adding_points = False  

    def drawTriangle(self, event=None):
        self.canvas.delete("all")
        for triangle in self.triangulos:
            points = triangle.points
            self.canvas.create_polygon(
                points[0].xy(),
                points[1].xy(),
                points[2].xy(),
                outline=triangle.cor,
                fill="",
                width=2,
                tags=triangle.id,
            )

            for point in points:
                self.canvas.create_oval(
                    point.x - 5, point.y - 5, point.x + 5, point.y + 5, fill=point.cor
                )
            
    def newTriangle(self):
        self.points = []
        self.adding_points = True  
        self.drawTriangle()

    def selectTriangle(self, event):
        index = self.lista_triangulos.curselection()
        if index:
            self.selectedTriangle = self.triangulos[index[0]]
            self.botao_remover.config(state=tk.NORMAL)
            self.botao_pintar.config(state=tk.NORMAL)
            self.botao_editar.config(state=tk.NORMAL)
            self.botao_preencher.config(state=tk.NORMAL)
            self.botao_pintar_pontos.config(state=tk.NORMAL)

    def removeTriangle(self):
        index = self.lista_triangulos.curselection()
        if index:
            self.canvas.delete(self.selectedTriangle.id)
            self.lista_triangulos.delete(index)
            self.triangulos.remove(self.selectedTriangle)
            self.botao_remover.config(state=tk.DISABLED)
            self.drawTriangle()

    def paintEdge(self):
        index = self.lista_triangulos.curselection()
        if index:
            cor = colorchooser.askcolor()[1]
            self.triangulos[index[0]].cor = cor
            triangle = self.triangulos[index[0]]
            points = triangle.points
            self.canvas.delete(triangle.id)
            self.canvas.create_polygon(
                points[0].xy(),
                points[1].xy(),
                points[2].xy(),
                outline=cor,
                fill="",
                width=2,
                tags=triangle.id,
                )
            
    def editTriangle(self):
        self.canvas.bind("<Button-1>", self.startDragging)
        self.canvas.bind("<B1-Motion>", self.dragPoint)
        self.canvas.bind("<ButtonRelease-1>", self.stopDragging)
        self.botao_parar_edicao.config(state=tk.NORMAL)
        self.botao_editar.config(state=tk.DISABLED)
        self.botao_novo.config(state=tk.DISABLED)
        self.botao_remover.config(state=tk.DISABLED)

    def startDragging(self, event):
        x, y = event.x, event.y
        for point in self.selectedTriangle.points:
            if abs(x - point.x) < 10 and abs(y - point.y) < 10:
                self.draggedPoint = point
                break

    def dragPoint(self, event):
        if self.draggedPoint:
            self.draggedPoint.x = event.x
            self.draggedPoint.y = event.y
            self.drawTriangle()

    def stopDragging(self, event):
        self.draggedPoint = None

    def stopEdit(self):
        self.canvas.bind("<Button-1>", self.addPoints)
        self.botao_parar_edicao.config(state=tk.DISABLED)
        self.botao_editar.config(state=tk.NORMAL)

    def fill_poly(self, triangle):
        vertices = [(point.xy(), point.cor) for point in triangle.points]

        def interpolate_color(color1, color2, color3, t1, t2, t3):
            r = int(t1 * color1[0] + t2 * color2[0] + t3 * color3[0])
            g = int(t1 * color1[1] + t2 * color2[1] + t3 * color3[1])
            b = int(t1 * color1[2] + t2 * color2[2] + t3 * color3[2])

            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))

            return r, g, b

        def hex_to_rgb(hex_color):
            # Convert '#RRGGBB' to (R, G, B)
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return f'#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'

        min_y = min(vertices, key=lambda p: p[0][1])[0][1]
        max_y = max(vertices, key=lambda p: p[0][1])[0][1]

        for y in range(min_y, max_y + 1):
            intersections = []

            for i in range(3):
                x1, y1 = vertices[i][0]
                x2, y2 = vertices[(i + 1) % 3][0]
                if y1 <= y + 1e-6 <= y2 or y2 <= y + 1e-6 <= y1:
                    if y2 - y1 != 0:
                        x = int(x1 + (y + 1e-6 - y1) * (x2 - x1) / (y2 - y1))
                        intersections.append(x)

            intersections.sort()

            for i in range(0, len(intersections), 2):
                x1 = intersections[i]
                x2 = intersections[i + 1] if i + 1 < len(intersections) else intersections[0]

                for x in range(x1, x2 + 1):
                    d = [((vx - x) ** 2 + (vy - y) ** 2) ** 0.5 for ((vx, vy), _) in vertices]
                    total = sum(1 / ((di + 1e-6) ** 2) for di in d)
                    t = [(1 / ((di + 1e-6) ** 2)) / total for di in d]

                    color1 = hex_to_rgb(vertices[0][1])
                    color2 = hex_to_rgb(vertices[1][1])
                    color3 = hex_to_rgb(vertices[2][1])

                    color = interpolate_color(color1, color2, color3, t[0], t[1], t[2])
                    color_hex = rgb_to_hex(color)

                    self.canvas.create_line(x, y, x + 1, y, fill=color_hex)

    def fillPoly(self, triangle):
        self.fill_poly(triangle)

    def paintPoints(self):
        if hasattr(self, 'selectedTriangle'):
            for i, point in enumerate(self.selectedTriangle.points):
                cor = colorchooser.askcolor(initialcolor=point.cor)[1]
                self.selectedTriangle.points[i].cor = cor  # Atualiza a cor do ponto

                self.canvas.create_oval(
                    point.x - 5, point.y - 5, point.x + 5, point.y + 5, fill=cor, outline="black", width=2
                )

    def sair(self):
            self.root.destroy()

        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
