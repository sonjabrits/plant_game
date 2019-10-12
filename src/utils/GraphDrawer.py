from graphviz import Digraph

class GraphDrawer:
    def __init__(self):
        self.dot = Digraph(comment='Garden family tree')

    def add_node(self, p):
        self.dot.node(str(p.id), label=p.name)

    def add_edge(self, p, parent):
        self.dot.edge(str(parent.id), str(p.id))

    def update_node(self, p):
        self.dot.node(str(p.id), label=p.name, style='filled', fillcolor='lightgray')

    def render_graph(self):
        self.dot.render('family_tree.gv', view=False)
