import tkinter as tk
from tkinter import colorchooser
from point import Point
from triangle import Triangle

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho 1 - Computação Gráfica")
        self.points = []
        self.triangulos = []
        self.selectedTriangle = None

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

        self.botao_preencher = tk.Button(self.toolbar, text="Preencher", command=self.fillPoly)
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
        if hasattr(self, 'adding_points') and self.adding_points:
            x, y = event.x, event.y
            color = colorchooser.askcolor()[1]  # Obtemos a cor em hexadecimal
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
                outline="black",
                fill="",
                width=2,
                tags=triangle.id,
            )

            for point in points:
                color = Point.rgb_to_hex(point.cor)
                self.canvas.create_oval(
                    point.x - 5, point.y - 5, point.x + 5, point.y + 5, fill=color
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
        self.botao_preencher.config(state=tk.DISABLED)
        self.botao_pintar.config(state=tk.DISABLED)
        self.botao_pintar_pontos.config(state=tk.DISABLED)

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
        self.botao_novo.config(state=tk.NORMAL)
        self.botao_remover.config(state=tk.NORMAL)
        self.botao_preencher.config(state=tk.NORMAL)
        self.botao_pintar.config(state=tk.NORMAL)
        self.botao_pintar_pontos.config(state=tk.NORMAL)

    def paintPoints(self):
        if hasattr(self, 'selectedTriangle'):
            for i, point in enumerate(self.selectedTriangle.points):
                cor = colorchooser.askcolor(initialcolor=Point.rgb_to_hex(point.cor))[1]
                self.selectedTriangle.points[i].cor = Point.hex_to_rgb(cor)  # Atualiza a cor do ponto

                self.canvas.create_oval(
                    point.x - 5, point.y - 5, point.x + 5, point.y + 5, fill=cor
                )

    def fillPoly(self):
        points = self.selectedTriangle.points
        vertices = [(p.xy(), p.cor) for p in points]
        self.rasterize_triangle(vertices[0][0], vertices[1][0], vertices[2][0], vertices[0][1], vertices[1][1], vertices[2][1], self.canvas)
        self.canvas.update()
    
    def rasterize_triangle(self, v1, v2, v3, c1, c2, c3, canvas):
        vertices = sorted([(v1, c1), (v2, c2), (v3, c3)], key=lambda v: v[0][1])
        
        v1, c1 = vertices[0]
        v2, c2 = vertices[1]
        v3, c3 = vertices[2]
        
        dc12 = [((c2[i] - c1[i]) / (v2[1] - v1[1])) for i in range(3)]
        dc13 = [((c3[i] - c1[i]) / (v3[1] - v1[1])) for i in range(3)]
        dc23 = [((c3[i] - c2[i]) / (v3[1] - v2[1])) for i in range(3)]
        
        dx12 = ((v2[0] - v1[0]) / (v2[1] - v1[1]))
        dx13 = ((v3[0] - v1[0]) / (v3[1] - v1[1]))
        dx23 = ((v3[0] - v2[0]) / (v3[1] - v2[1]))

        c12_r, c12_g, c12_b = c1
        c13_r, c13_g, c13_b = c1
        c23_r, c23_g, c23_b = c2

        c12_x = v1[0]
        c13_x = v1[0]
        c23_x = v2[0]
        
        for y in range(v1[1], v3[1]):
            if y < v2[1]:
                self.draw_scanline(c12_x, c13_x, [c12_r, c12_g, c12_b], [c13_r, c13_g, c13_b], y, canvas)
                c12_r += dc12[0]   
                c12_g += dc12[1]   
                c12_b += dc12[2]    
                c12_x += dx12
                c13_x += dx13
            else:
                self.draw_scanline(c23_x, c13_x, [c23_r, c23_g, c23_b], [c13_r, c13_g, c13_b], y, canvas)
                c23_r += dc23[0]   
                c23_g += dc23[1]   
                c23_b += dc23[2]   
                c23_x += dx23
                c13_x += dx13
                
            c13_r += dc13[0]      
            c13_g += dc13[1]      
            c13_b += dc13[2]      

    def draw_scanline(self, x1, x2, c1, c2, y, canvas):
        if x1 > x2:
            x1, x2 = x2, x1  
            c1, c2 = c2, c1 

        dc_r = (c2[0] - c1[0]) / (x2 - x1) if x2 != x1 else 0   
        dc_g = (c2[1] - c1[1]) / (x2 - x1) if x2 != x1 else 0 
        dc_b = (c2[2] - c1[2]) / (x2 - x1) if x2 != x1 else 0  
        
        c_r, c_g, c_b = c1

        for x in range(int(x1), int(x2)):
            self.set_pixel_color(x, y, [c_r, c_g, c_b], canvas) 
            c_r += dc_r   
            c_g += dc_g   
            c_b += dc_b    

    def set_pixel_color(self, x, y, color, canvas):
        color = '#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2]))
        canvas.create_line(x, y, x+1, y, fill=color)

    def sair(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()