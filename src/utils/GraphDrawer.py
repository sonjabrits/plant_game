from src.Garden import *
from graphviz import Digraph

class GraphDrawer:
    def __init__(self):
        pass

    def draw_family_graph(self, garden):
        dot = Digraph(comment='Garden family tree')
        p = garden.plants[0]
        self.gotochild(dot, p)
        dot.render('family_tree.gv', view=False)

    def gotochild(self, dot, p):
        dot.node(str(p.id), label=p.name)
        if p.children:
            for c in p.children:
                dot.node(str(c.id), label=c.name)
                dot.edge(str(p.id), str(c.id))
                self.gotochild(dot, c)