"""
This module does the file IO between the user given network data and the solution given via the optimization.
"""


import tkinter.filedialog as dialog
from HydroNetwork import HydroJunction, HydroPipe, HydroReservoir
import common
import csv

valid_labels = ['junction_id', 'junction_elevation', 'junction_demand', 'junction_pressure_demand', 'pipe_id',
                'pipe_st_node', 'pipe_end_node', 'pipe_length', 'reservoir_id', 'reservoir_head']


def hydro_read_csv():
    """Gets the data from a csv file."""
    csvfilename = dialog.askopenfilename(defaultextension='.csv')
    with open(csvfilename, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        data = []
        for index, row in enumerate(csvreader):
            label = row[0]
            if valid_labels[index] != label:
                raise IOError("Invalid data.")
            data.append(row[1::])
    for j in range(len(data[8])):
        common.nodes.append(HydroReservoir(int(data[8][j]), float(data[9][j])))
    for j in range(len(data[0])):
        common.nodes.append(HydroJunction(int(data[0][j]), float(data[1][j]), float(data[2][j]), float(data[3][j])))
    common.nodes.sort(key=lambda x: x.get_id(), reverse=False)
    for j in range(len(data[4])):
        common.pipes.append(HydroPipe(int(data[4][j]), common.nodes[int(data[5][j])-1], common.nodes[int(data[6][j])-1],
                                      float(data[7][j])))
    common.pipes.sort(key=lambda x: x.get_id(), reverse=False)


def hydro_write_csv(network):
    """Returns the data in a csv file."""
    diameters = ['optimized_diameters']
    for pipe in network.get_pipes():
        diameters.append(pipe.get_pipe_diameter())
    csvfilename = dialog.askopenfilename(defaultextension='.csv')
    with open(csvfilename, 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(diameters)
