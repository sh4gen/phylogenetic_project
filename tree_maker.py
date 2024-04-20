from graphviz import Digraph
class Node:
    def __init__(self, value: str, info: str = "", parent=None) -> None:
        self.value = value
        self.info = info
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def parse_taxonomy_data(data):
    node_dict = {}
    lines = data.strip().split('\n')

    for line in lines:
        parts = line.strip().split('|')
        value = parts[0].strip()
        info = parts[1].strip()
        
        parent_values = parts[2].strip().split(';')
        parent_values = [pv.strip() for pv in parent_values if pv.strip()]
    
        node = Node(value, info)
        node_dict[info] = node

        if parent_values:
            parent_value = parent_values[-1]
            parent_node = node_dict.get(parent_value)
            if parent_node:
                node.parent = parent_node
                parent_node.add_child(node)

    root = None
    for node in node_dict.values():
        if node.parent is None:
            root = node
            break

    return root

def print_tree(node, depth=0):
    if node is None:
        return
    print("  " * depth + node.info)
    for child in node.children:
        print_tree(child, depth + 1)

def generate_dot(node, dot, parent_id=None):
    if node is None:
        return
    
    node_id = node.value
    dot.node(node_id, node.info)
    
    if parent_id:
        dot.edge(parent_id, node_id)

    for child in node.children:
        generate_dot(child, dot, node_id)

with open('ver.txt') as f:
    data = f.read()

root_node = parse_taxonomy_data(data)
print_tree(root_node)

dot = Digraph(comment='Taxonomy Tree', graph_attr={'size': '1920,1080'})
generate_dot(root_node, dot)
dot.render('taxonomy_tree', format='png', cleanup=True)