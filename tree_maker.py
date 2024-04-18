class Node:
    def __init__(self, value : str, parent = None) -> None:
        self.value = value
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
        
        parent_values = []
        for value in parts[2].split(";"):
            stripped_values = value.strip()
            if stripped_values:
                parent_values.append(stripped_values)

        node = Node(value)
        node_dict[value] = node

        for parent_value in parent_values[:-1]:
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
    print("  " * depth + node.value)
    for child in node.children:
        print_tree(child, depth + 1)

data =  "2	|	2	|		|\n7	|	7	|	2;	|"
root_node = parse_taxonomy_data(data)
print(root_node.value)