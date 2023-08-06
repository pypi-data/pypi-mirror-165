from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import os


# todo: Find font file in different operation system.

def hasChinese(input_str):
    for char in input_str:
        if "\u4e00" <= char <= u"\u9fff": return True


class FigureBase:
    def __init__(self):
        self._base_data = None
        self._fig_list = []
        self._font_size = 10
        self._font_dict = {"TimesNewRoman" : FontProperties(family="Times New Roman", size=self._font_size)}
        self._legend_list = []
        self._x_limit = None
        self._y_limit = None
        # Make plt canvas.
        plt.figure()

    def _choose_font(self, text):
        if hasChinese(text):
            return self._font_dict["TimesNewRoman"]
        else:
            return self._font_dict["TimesNewRoman"]


class Figure(FigureBase):
    def __init__(self):
        FigureBase.__init__(self)

    def add_legend(self, loc="best"):
        """
        Add legend for figure.
        :param loc: str | Legend location. (best, upper+l/r/c, lower+l/r/c, right, center+l/r, center)
        :return:
        """
        plt.legend(self._fig_list, self._legend_list, loc=loc)

    def add_line_data(self, data, linewidth=1, color="black", legend=""):
        """
        One line each time.
        :param data:
        :return:
        """
        fig, = plt.plot(self._base_data, data, linewidth=linewidth, c=color)
        self._fig_list.append(fig)
        self._legend_list.append(legend)

    def add_point_data(self, data, marker="o", color="w", edgecolor="red", size=35, legend=""):
        fig = plt.scatter(self._base_data, data, marker=marker, color=color, edgecolor=edgecolor, s=size)
        self._fig_list.append(fig)
        self._legend_list.append(legend)

    def save(self, filename="unknown", dpi=1000):
        plt.savefig(filename, dpi=dpi)

    def set_base_data(self, base_data):
        self._base_data = base_data
        self._x_limit = [base_data.min(), base_data.max()]

    def set_title(self, title):
        plt.title(title, fontproperties=self._choose_font(title))

    def set_x_label(self, text):
        plt.xlabel(text, fontproperties=self._choose_font(text))

    def set_x_limit(self, range):
        self._x_limit = []
        self._x_limit.append(range[0])
        self._x_limit.append(range[1])

    def set_y_label(self, text):
        plt.ylabel(text, fontproperties=self._choose_font(text))

    def set_y_limit(self, range):
        self._y_limit = []
        self._y_limit.append(range[0])
        self._y_limit.append(range[1])

    def show(self):
        if self._x_limit is not None : plt.xlim(self._x_limit)
        if self._y_limit is not None : plt.ylim(self._y_limit)
        plt.show()
