import networkx as nx


class World:
    def __init__(self, locations: nx.Graph):
        self.locations = locations
        for location in self.locations:
            location.world = self

    def tick(self):
        for location in self.locations:
            location.do_turns()
