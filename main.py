from tree import Tree
from graph import Graph, Node, Arc

node_mail = Node('Mail', 2)
node_ts = Node('ts', 4)
node_103 = Node('103', 0)
node_b3 = Node('b3', 4)
node_b1 = Node('b1', 6)
node_c2 = Node('c2', 9)
node_c1 = Node('c1', 10)
node_c3 = Node('c3', 9)
node_b2 = Node('b2', 6)
node_b4 = Node('b4', 7)
node_109 = Node('109', 13)
node_111 = Node('111', 15)
node_119 = Node('119', 10)
node_storage = Node('storage', 16)
node_123 = Node('123', 13)
node_123r = Node('123r', 15)
node_125 = Node('125', 12)

g1 = Graph(
    [node_mail, node_ts, node_103, node_b3, node_b1, node_c2, node_c1, node_c3, node_b2, node_b4, node_109, node_111, node_119, node_storage, node_123, node_123r, node_125],
    [
        Arc(8, node_103, node_ts),
        Arc(12, node_103, node_109),
        Arc(4, node_103, node_b3),
        Arc(6, node_ts, node_mail),
        Arc(4, node_b3, node_b1),
        Arc(7, node_b3, node_b4),
        Arc(3, node_b1, node_c2),
        Arc(6, node_b1, node_b2),
        Arc(6, node_c2, node_c3),
        Arc(4, node_c2, node_c1),
        Arc(8, node_c1, node_c3),
        Arc(3, node_b2, node_b4),
        Arc(7, node_b4, node_109),
        Arc(4, node_109, node_111),
        Arc(16, node_109, node_119),
        Arc(7, node_119, node_storage),
        Arc(9, node_119, node_123),
        Arc(4, node_123, node_123r),
        Arc(4, node_123, node_125),
        Arc(2, node_b3, node_b2)
    ]
)

path = g1.find_path(node_103, node_123r)
# print(path)
for node in path.get('path'):
    print(node[0].value)

# print(g1.a_star(node_103, node_123r))

