from graphviz import Digraph
class Node:
    def __init__(self, tax_id: str, scientific_name: str = "", parent=None) -> None:
        self.tax_id = tax_id
        self.scientific_name = scientific_name
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def parse_taxonomy_data(data):
    node_dict = {}
    lines = data.strip().split('\n')

    for line in lines:
        parts = line.strip().split('|')
        tax_id = parts[0].strip()
        scientific_name = parts[1].strip()
        
        lineage = parts[2].strip().split(';')
        lineage = [pv.strip() for pv in lineage if pv.strip()]
    
        node = Node(tax_id, scientific_name)
        node_dict[scientific_name] = node

        if lineage:
            parent_value = lineage[-1]
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
    print("  " * depth + node.scientific_name)
    for child in node.children:
        print_tree(child, depth + 1)

def generate_dot(node, dot, parent_id=None):
    if node is None:
        return
    
    node_id = node.tax_id
    dot.node(node_id, node.scientific_name)
    
    if parent_id:
        dot.edge(parent_id, node_id)

    for child in node.children:
        generate_dot(child, dot, node_id)

with open('primates_taxonomy.txt', encoding='utf-8') as f:
    data = f.read()

root_node = parse_taxonomy_data(data)
print_tree(root_node)

# Dot Section
dot = Digraph(comment='Species Taxonomy', engine='dot', format='svg')
dot.attr(rankdir='LR')
dot.attr('node', shape='ellipse', style='filled', color='lightgrey', fontname='Helvetica')
dot.attr('edge', arrowhead='empty', style='solid')
generate_dot(root_node, dot)
dot.render('Primates_taxonomy_tree')