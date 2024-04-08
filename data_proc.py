from scapy.all import *
import csv
import pandas as pd
from variable import variable
from model import NeuralNetwork
import matplotlib.pyplot as plt
from time import localtime, strftime

class DataProcessor:
    def __init__(self):
        self.headers = ['udp.srcport', 'udp.dstport', 'tcp.srcport', 'tcp.dstport', 'tcp.ack', 'tcp.urgent_pointer',
                        'tcp.window_size_value', 'tcp.reserved', 'ip.len', 'ip.id', 'ip.tos', 'ip.frag', 'ip.src',
                        'ip.dst']
        self.prepareset_path = os.getcwd() + '\\prepareset.csv'
        pass

    def dump_parser(self, mode, selected_iface, dump_path):

        if mode == 1:
            pcap = rdpcap(dump_path)
        else:
            pcap = sniff(count=1, iface=selected_iface)

        with open(self.prepareset_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
            for pkt in pcap:
                if UDP in pkt:
                    u1 = pkt['UDP'].sport
                    u2 = pkt['UDP'].dport
                else:
                    u1 = -1
                    u2 = -1
                if TCP in pkt:
                    t1 = pkt['TCP'].sport
                    t2 = pkt['TCP'].dport
                    t3 = pkt['TCP'].ack
                    t4 = pkt['TCP'].urgptr
                    t5 = pkt['TCP'].window
                    t6 = pkt['TCP'].reserved
                else:
                    t1 = -1
                    t2 = -1
                    t3 = -1
                    t4 = -1
                    t5 = -1
                    t6 = -1
                if IP in pkt:
                    i1 = pkt['IP'].len
                    i2 = pkt['IP'].id
                    i3 = pkt['IP'].tos
                    i4 = pkt['IP'].frag
                    i5 = pkt['IP'].src
                    i6 = pkt['IP'].dst
                else:
                    i1 = -1
                    i2 = -1
                    i3 = -1
                    i4 = -1
                    i5 = -1
                    i6 = -1
                rows = [u1, u2, t1, t2, t3, t4, t5, t6, i1, i2, i3, i4, i5, i6]
                writer.writerow(rows)

    def import_to_(self, file_type, out_path):
        if file_type == 0:
            os.replace(self.prepareset_path, out_path)
        else:
            df = pd.read_csv(self.prepareset_path)
            df.to_excel(out_path, index=False)
        pass

    def calc(self, inputs, output):

        nn = NeuralNetwork()
        input_batch = pd.read_csv(inputs)
        input_batch.dropna(subset=['ip.src'], inplace=True)
        input_batch.dropna(subset=['ip.dst'], inplace=True)
        outputs = nn.calculate_batch_output(input_batch.values)
        convert = pd.DataFrame(outputs)
        input_batch['probability'] = convert
        input_batch['probability'] = input_batch['probability'].round()
        input_batch.to_excel(output)
        self.plot(input_batch)

    def plot(self, df):
        if variable.mean_diag is not True:
            return None
        else:
            sum_prob_prob = df['probability'].sum()
            sum_all = df.shape[0]
            x = ['Всего пакетов', 'Пакетов с вложениями']
            y = [sum_all, sum_prob_prob]
            fig, ax = plt.subplots()
            ax.bar(x, y)
            ax.set_facecolor('seashell')
            plt.title("Результаты анализа")
            self.add_value_labels(ax)
            if variable.mean_diag:
                plt.show()
            if variable.save_diag:
                plt.savefig(variable.path_of_save + '/' + strftime("%Y-%m-%d_%H-%M-%S", localtime()) + '.png')

    def add_value_labels(self, ax, spacing=5):
        """Add labels to the end of each bar in a bar chart.

        Arguments:
            ax (matplotlib.axes.Axes): The matplotlib object containing the axes
                of the plot to annotate.
            spacing (int): The distance between the labels and the bars.
        """

        # For each bar: Place a label
        for rect in ax.patches:
            # Get X and Y placement of label from rect.
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2

            # Number of points between bar and label. Change to your liking.
            space = spacing
            # Vertical alignment for positive values
            va = 'bottom'

            # If value of bar is negative: Place label below bar
            if y_value < 0:
                # Invert space to place label below
                space *= -1
                # Vertically align label at top
                va = 'top'

            # Use Y value as label and format number with one decimal place
            label = "{:.1f}".format(y_value)

            # Create annotation
            ax.annotate(
                label,  # Use `label` as label
                (x_value, y_value),  # Place label at end of the bar
                xytext=(0, space),  # Vertically shift label by `space`
                textcoords="offset points",  # Interpret `xytext` as offset in points
                ha='center',  # Horizontally center label
                va=va)  # Vertically align label differently for
            # positive and negative values.