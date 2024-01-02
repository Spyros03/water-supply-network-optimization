"""
This is a module that uses EPANET_2.3 to solve the hydraulic network. Through the EPANET_2.3 files.
"""


import HydroNetwork as hn
import common
import struct
import os


def create_inp_file(network):
    """Parses a "HydroNetwork" object into a .inp file to be used with EPANET_2.3"""
    file = open("./network_file.inp", 'w')
    file.write('[TITLE]\n\n\n')
    file.write('[JUNCTIONS]\n')
    file.write(';ID              	Elev        	Demand      	Pattern         \n')
    for node in network.get_nodes():
        if not isinstance(node, hn.HydroJunction):
            continue
        file.write(' {}               	{}           	{}           	                	;\n'.format(
            node.get_id(), node.get_elevation(), node.get_demand()))
    file.write('\n')
    file.write('[RESERVOIRS]\n')
    file.write(';ID              	Head        	Pattern         \n')
    for node in network.get_nodes():
        if not isinstance(node, hn.HydroReservoir):
            continue
        file.write(' {}              	{}           	                	;\n'.format(node.get_id(), node.head))
    file.write('\n')
    file.write('[PIPES]\n')
    file.write(';ID              	Node1           	Node2           	Length      	Diameter    	Roughness'
               '   	MinorLoss   	Status\n')
    for pipe in network.get_pipes():
        file.write(' {}               	{}               	{}               	{}        	{}          	{}    '
                   '     	0           	Open  	;\n'
                   .format(pipe.get_id(), pipe.get_start_node().get_id(), pipe.get_end_node().get_id(),
                           pipe.get_length(), pipe.get_pipe_diameter(), pipe.get_pipe_roughness()))
    file.write('\n')
    file.write('[REPORT]\n')
    file.write(' Status             	YES\n')
    file.write(' Summary            	NO\n')
    file.write(' Page               	0\n')
    file.write(' NODES 			ALL\n')
    file.write(' LINKS 			ALL\n')
    file.write('\n')
    file.write('[OPTIONS]\n')
    file.write(' Units              	LPS\n')
    file.write(' Headloss           	D-W\n')
    file.write(' Specific Gravity   	1\n')
    file.write(' Viscosity          	1\n')
    file.write(' Trials             	40\n')
    file.write(' Accuracy           	0.001\n')
    file.write(' CHECKFREQ          	2\n')
    file.write(' MAXCHECK           	10\n')
    file.write(' DAMPLIMIT          	0\n')
    file.write(' Unbalanced         	Continue 10\n')
    file.write(' Pattern            	1\n')
    file.write(' Demand Multiplier  	1.0\n')
    file.write(' Emitter Exponent   	0.5\n')
    file.write(' Quality            	None mg/L\n')
    file.write(' Diffusivity        	1\n')
    file.write(' Tolerance          	0.01\n')
    file.write('\n[END]\n')
    file.close()


def parse_out_file(network):
    """Parses the binary .out file output after execution EPANET_2.3 into the "HydroNetwork" object."""
    n_nodes = len(common.nodes)
    n_links = len(common.pipes)
    with open('output.out', 'rb') as file:
        file.seek(884 + 36 * n_nodes + 52 * n_links + 4 + 8)
        dynamic_results_data = file.read(16*n_nodes + 32*n_links)
        output_data = struct.unpack('f' * 4 * n_nodes + 'f' * 8 * n_links, dynamic_results_data)
    for index, node in enumerate(network.get_nodes()):
        if isinstance(node, hn.HydroReservoir):
            continue
        node.set_actual_pressure(output_data[n_nodes + n_nodes + index])
    for index, pipe in enumerate(network.get_pipes()):
        pipe.set_discharge(output_data[4*n_nodes + index])
        pipe.set_velocity(output_data[4*n_nodes + n_links + index])
        pipe.set_headloss(output_data[4*n_nodes + n_links + n_links + index])


def epanet_solver(network):
    """Solves the network using EPANET_2.3"""
    create_inp_file(network)
    if common.os_name == "Windows":
        os.chdir('epanet_windows')
        ret = os.system('runepanet.exe ../network_file.inp ../report.rpt ../output.out')
        if ret == 100:
            raise hn.HydroError("The network is invalid.")
        os.chdir('..')
    else:
        ret = os.system('./epanet_linux/runepanet.sh network_file.inp report.rpt output.out')
        if (ret >> 8) == 100:
            raise hn.HydroError("The network is invalid.")
    parse_out_file(network)


if __name__ == '__main__':
    """Module test case."""
    from HydroOptimizationIO import hydro_read_csv
    hydro_read_csv()
    network = hn.HydroNetwork(common.nodes, common.pipes)
    create_inp_file(network)
    parse_out_file(network)
    for node in network.get_nodes():
        if isinstance(node, hn.HydroReservoir):
            continue
        print(node.get_actual_pressure())
    for pipe in network.get_pipes():
        print(pipe.discharge, pipe.velocity, pipe.headloss)
