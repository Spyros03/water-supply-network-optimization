"""
This module contains classes that describe a simple water supply network in correlation with the EPANET_2.3 structs
that is used for the hydraulic calculations.
"""


import EpanetSolver as Es


class HydroError(Exception):
    """Exception for hydraulic related issues."""
    pass


class HydroNode:
    """Base class for water supply network node."""
    def __init__(self, idd: int):
        self.idd = idd

    def get_id(self):
        return self.idd

    def copy(self):
        pass


class HydroReservoir(HydroNode):
    """A class that describes a water supply reservoir in correlation with the EPANET_2.3 Reservoir struct."""
    def __init__(self, idd: int, head: float = 0):
        super().__init__(idd)
        self.head = head

    def get_head(self) -> float:
        return self.head

    def copy(self):
        return HydroReservoir(self.idd, self.head)


class HydroJunction(HydroNode):
    """A class that describes a junction of a water supply network in correlation with EPANET_2.3 Junction struct."""
    def __init__(self, idd: int, elevation: float, demand: float, head_demand: float = 0):
        super().__init__(idd)
        self.elevation = elevation
        self.demand = demand
        self.head_demand = head_demand
        self.actual_head = None

    def has_enough_head(self) -> bool:
        if self.actual_head is None:
            raise HydroError('Actual head is has not been set yet.')
        return self.actual_head >= self.head_demand

    def get_elevation(self) -> float:
        return self.elevation

    def get_demand(self) -> float:
        return self.demand

    def get_head_demand(self) -> float:
        return self.head_demand

    def get_actual_head(self) -> float:
        if self.actual_head is None:
            raise HydroError("Head has not been set yet.")
        return self.actual_head

    def set_actual_head(self, actual_head):
        self.actual_head = actual_head

    def copy(self):
        return HydroJunction(self.idd, self.elevation, self.demand, self.head_demand)


class HydroPipe:
    """A class that describes a water supply network pipe in correlation with EPANET_2.3 Pipe struct."""
    def __init__(self, idd: int, start_node: HydroNode, end_node: HydroNode, length: float,
                 pipe_diameter: float = 60.0, pipe_roughness: float = 1):
        self.idd = idd
        self.start_node = start_node.copy()
        self.end_node = end_node.copy()
        if pipe_diameter < 0:
            raise HydroError("Pipe roughness cannot be negative.")
        self.pipe_diameter = pipe_diameter
        if pipe_roughness < 0:
            raise HydroError("Pipe roughness cannot be negative.")
        self.pipe_roughness = pipe_roughness
        self.length = length
        self.discharge = None
        self.velocity = None
        self.headloss = None

    def get_id(self) -> int:
        return self.idd

    def get_start_node(self) -> HydroNode:
        return self.start_node

    def get_end_node(self) -> HydroNode:
        return self.end_node

    def get_pipe_diameter(self) -> float:
        return self.pipe_diameter

    def get_pipe_roughness(self) -> float:
        return self.pipe_roughness

    def get_length(self) -> float:
        return self.length

    def set_diameter(self, pipe_diameter: float):
        self.pipe_diameter = pipe_diameter

    def set_discharge(self, discharge: float):
        self.discharge = discharge

    def set_velocity(self, velocity: float):
        self.velocity = velocity

    def set_headloss(self, headloss: float):
        self.headloss = headloss

    def copy(self):
        return HydroPipe(self.idd, self.start_node, self.end_node, self.pipe_diameter,
                         self.pipe_roughness)


class HydroNetwork:
    """A class that describes a water supply network."""
    def __init__(self, nodes, pipes: list[HydroPipe]):
        self.nodes = []
        self.pipes = []
        for node in nodes:
            self.nodes.append(node.copy())
        for pipe in pipes:
            self.pipes.append(pipe.copy())
        self.pipes = pipes

    def set_pipe_diameters(self, diameters):
        for i in range(len(diameters)):
            self.pipes[i].set_diameter(diameters[i])

    def solve_network(self):
        Es.epanet_solver(self)

    def get_nodes(self):
        return self.nodes

    def get_pipes(self) -> list[HydroPipe]:
        return self.pipes
