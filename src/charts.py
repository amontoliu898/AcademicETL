from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class BarChart(FigureCanvasQTAgg):
    def __init__(self, data, title):
        self.figure = Figure(figsize=(6, 3))
        super().__init__(self.figure)
        self.draw_chart(data, title)

    def draw_chart(self, data, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if data:
            names = [row[0] for row in data]
            values = [row[1] for row in data]

            ax.bar(names, values)
            ax.set_ylim(0, 10)
            ax.set_ylabel("Nota media")
            ax.set_title(title)
            ax.tick_params(axis="x", rotation=25)
        else:
            ax.text(0.5, 0.5, "Sin datos", ha="center", va="center")

        self.figure.tight_layout()
        self.draw()