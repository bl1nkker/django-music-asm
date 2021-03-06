import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(x, y, x_label, y_label):
    plt.switch_backend('agg')
    plt.figure(figsize=(10, 5))
    plt.title('Listenings')
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_bar_plot(x, y, x_label, y_label):
    plt.switch_backend('agg')
    plt.figure(figsize=(10, 5))
    plt.title('Listenings')
    plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    graph = get_graph()
    return graph
