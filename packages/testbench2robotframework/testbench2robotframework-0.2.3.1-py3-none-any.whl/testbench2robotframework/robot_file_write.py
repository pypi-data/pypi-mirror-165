import os


def get_node_path(nodes, node, root_key):
    path = node.baseInformation.name
    current_key = node.baseInformation.parentKey
    while current_key != root_key:
        parent_node = get_node_by_key(current_key, nodes)
        path = "\\".join([parent_node.baseInformation.name, path])
        current_key = parent_node.baseInformation.parentKey
    os.mkdir("\\".join([os.getcwd(), "Generated", path]))


def get_node_by_key(key, nodes):
    for node in nodes:
        if node.baseInformation.key == key:
            return node


def write_robot_files(test_theme_tree):
    root_key = test_theme_tree.root.baseInformation.key
    os.mkdir("\\".join([os.getcwd(), "Generated"]))
    nodes = test_theme_tree.nodes
    for node in nodes:
        if node.elementType == "TestTheme":
            get_node_path(test_theme_tree.nodes, node, root_key)
