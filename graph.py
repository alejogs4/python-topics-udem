# Graph is an ordered pair or Arc-edges(E) and nodes-vertices(V) G = (V, E)
# ordered pair (a, b) !== (b, a) if a !== b
# unordered {a, b} == {b, a}
# edges(arc) could be either directed or indirected
# Breadth First Search is using queue
from queue import Queue, PriorityQueue
from functools import reduce
import graphutils


class Arc:
    def __init__(self, weigth, initial_node, final_node):
        assert weigth > 0, "Weigth must be greather than 0"
        self.weigth = weigth
        self.initial_node = initial_node
        self.final_node = final_node


class Node:
    def __init__(self, value, heuristic=0):
        self.value = value
        self.heuristic = heuristic

    def __gt__(self, other):
        if isinstance(other, tuple):
            return self.value > other[1].value
        return self.value > other.value

    def __eq__(self, other):
        if isinstance(other, bool):
            return self.value == other
        if isinstance(other, tuple):
            return self.value == other[1].value
        return self.value == other.value


class Graph:
    def __init__(self, nodes, arcs):
        self.nodes = graphutils.init_edged_list(nodes, arcs)
        self.nodes_length = len(nodes)

    def deep_first_search(self, initial_node, callback):
        visited_nodes = graphutils.init_visited_nodes(self.nodes.keys())

        def deep_first_search_alg(initial_node, callback):
            if visited_nodes[initial_node.value] == True:
                return
            callback(initial_node.value)
            visited_nodes[initial_node.value] = True
            neighboors = self.nodes[initial_node.value]

            for neighboor in neighboors:
                deep_first_search_alg(neighboor[0], callback)

        deep_first_search_alg(initial_node, callback)

    def breadth_first_search(self, initial_node, goal_node=None):
        visited_nodes = graphutils.init_visited_nodes(self.nodes.keys())
        queue = Queue(self.nodes_length)
        queue.put(initial_node)
        visited_nodes[initial_node.value] = True
        graph_nodes = []

        while not queue.empty():
            front = queue.get()
            neighboors = self.nodes[front.value]

            for neighboor in neighboors:
                if visited_nodes[neighboor[0].value] == False:
                    graph_nodes.append(neighboor[0])
                    visited_nodes[neighboor[0].value] = True
                    queue.put(neighboor[0])

                    if goal_node is not None and neighboor[0].value == goal_node.value:
                        return graph_nodes

        return graph_nodes

    def dijkstra(self, initial_node):
        visited_nodes = graphutils.init_visited_nodes(self.nodes.keys())
        previous = graphutils.init_visited_nodes(self.nodes.keys())

        # Dijkstra distance
        distance = {}
        for node in self.nodes.keys():
            distance[node] = 1e1000

        distance[initial_node.value] = 0
        queue = Queue()
        queue.put((initial_node, 0))

        while not queue.empty():
            current_node = queue.get()
            visited_nodes[current_node[0].value] = True
            for neighboor in self.neighboors(current_node[0]):
                if visited_nodes[neighboor[0].value] == True:
                    continue
                new_distance = distance[current_node[0].value] + neighboor[1]
                if new_distance < distance[neighboor[0].value]:
                    previous[neighboor[0].value] = current_node
                    distance[neighboor[0].value] = new_distance
                    queue.put((neighboor[0], new_distance))

        # print(previous)
        return {'distance': distance, 'previous': previous}

    def a_star(self, initial_node, final):
        previous = graphutils.init_visited_nodes(self.nodes.keys())

        priority_queue = PriorityQueue()
        priority_queue.put((initial_node, initial_node.heuristic))

        graph_score = graphutils.init_map_to_infinity(self.nodes.keys())
        graph_score[initial_node.value] = 0

        f_score = graphutils.init_map_to_infinity(self.nodes.keys())
        f_score[initial_node.value] = initial_node.heuristic

        while not priority_queue.empty():
            current_node = priority_queue.get()
            if current_node[0].value == final.value:
                break
            for neighboor in self.neighboors(current_node[0]):
                probable_graph_score = graph_score[current_node[0].value] + neighboor[1]

                if probable_graph_score < graph_score[neighboor[0].value]:
                    previous[neighboor[0].value] = current_node
                    graph_score[neighboor[0].value] = probable_graph_score
                    f_score[neighboor[0].value] = graph_score[neighboor[0].value] + neighboor[0].heuristic

                    if not any((neighboor[0].heuristic, neighboor[0]) in element for element in priority_queue.queue):
                        priority_queue.put((neighboor[0], f_score[neighboor[0].value]))
        return {'distance': f_score, 'previous': previous}
    '''
    Find out if it's posible to reach to target node since initial node in a given maximun depth
    '''
    def iterative_search(self, initial_node, target_node, depth):
        def limited_search(root, final_node, limit):
            if root.value == final_node.value:
                return True

            if limit <= 0:
                return False

            for neighboor in self.neighboors(root):
                if limited_search(neighboor[0], final_node, limit - 1) == True:
                    return True
            return False

        for i in range(depth):
            if limited_search(initial_node, target_node, i) == True:
                return True
        return False

    def find_path(self, initial_node, final_node):
        dijkstra = self.a_star(initial_node, final_node)
        path = []

        if (dijkstra.get('previous')[final_node.value] == False):
            return {'path': path, 'distance': 10e2000}

        queue = Queue()
        queue.put(dijkstra.get('previous')[final_node.value])

        while not queue.empty():
            current = queue.get()
            if current is not False:
                path.append(current)
                queue.put(dijkstra.get('previous')[current[0].value])
        # Put last node
        current_distance = reduce(
            lambda acumulated, current, : acumulated + current[1], path, 0)
        path.insert(0, (final_node, abs(dijkstra.get('distance')
                                        [final_node.value] - current_distance)))

        return {
            'path': list(reversed(path)),
            'distance': dijkstra.get('distance')[final_node.value]
        }

    def is_cyclic(self, initial_node):
        unvisited_nodes = graphutils.init_visited_nodes(self.nodes)
        unvisited_nodes[initial_node.value] = True
        queue = Queue()
        queue.put(initial_node)

        while not queue.empty():
            current_node = queue.get()
            unvisited_nodes[current_node.value] = True

            neighboors = self.neighboors(current_node)
            for neighboor in neighboors:
                if unvisited_nodes[neighboor[0].value] == True:
                    return True
                queue.put(neighboor[0])
        return False

    def is_bipartite(self, initial_node):
        unvisited_nodes = graphutils.init_visited_nodes(self.nodes)
        queue = Queue()
        queue.put(initial_node)

        while not queue.empty():
            current_node = queue.get()
            unvisited_nodes[current_node.value] = True
            for neighboor in self.neighboors(current_node):
                if unvisited_nodes[neighboor[0].value] == False:
                    queue.put(neighboor[0])

        return len(list(filter(lambda visited: visited == False, unvisited_nodes.values()))) >= 1

    def neighboors(self, node):
        return self.nodes[node.value]
