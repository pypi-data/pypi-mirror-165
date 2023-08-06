import matplotlib.pyplot as plt
import math
import io
import numpy as np
import cv2
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.patches import Rectangle


def plot_image(
        xs,
        ys,
        names,
        figsize=(12, 12)
):



def hist_image(
        xs,
        bins,
        names,
        figsize=(12, 12)
):
    ...

def legend_image(
        labels,
        colors,
        fig_size=(6.4, 4.8),
        dpi=100,
        pad=20
):
    handles = [Rectangle((0, 0), 1, 1, color=tuple([_ / 255 for _ in color])) for color in colors]
    #     stage 1
    fig = plt.figure(dpi=dpi, fig_size=fig_size)
    canvas = FigureCanvas(fig)
    legend = fig.legend(handles, labels, loc='upper center')
    canvas.draw()
    w, h = legend.get_window_extent().width, legend.get_window_extent().height
    plt.close(fig)
    #     stage 2
    fig = plt.figure(figsize=((w + pad) / 100, (h + pad) / 100), dpi=dpi)
    canvas = FigureCanvas(fig)
    fig.legend(handles, labels, loc='upper center')
    canvas.draw()
    image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    return image
