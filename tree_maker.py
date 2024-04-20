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
        node_dict[value] = node

        # Ebeveyn düğümü bul ve çocuk olarak ekle
        if parent_values:
            parent_value = parent_values[-1]  # En son ebeveyni al
            parent_node = node_dict.get(parent_value)
            if parent_node:
                node.parent = parent_node
                parent_node.add_child(node)

    # Kök düğümü bul
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

data =  """
        2	|	2	|		|
        7	|	7	|	2;	|
        5	|	5	|	2;	|
        12	|	12	|	2; 7;	|
        10	|	10	|	2; 7;	|
        6	|	6	|	2; 7;	|
        9	|	9	|	2; 5;	|
        15	|	15	|	2; 7; 6;	|
        11	|	11	|	2; 7; 6;	|
        4	|	4	|	2; 5; 9;	|
        """

root_node = parse_taxonomy_data(data)
print_tree(root_node)