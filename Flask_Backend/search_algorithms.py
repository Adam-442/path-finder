from node import Node
from problem import *
import heapq

def expand(problem, node):
    s = node.state
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s2)
        yield Node(s2, node, action, cost)

def get_path_actions(node):
    actionList = []
    if (node != None) and (node.parent_node != None):
        while (node.parent_node != None):
            actionList.append(node.action_from_parent)
            node = node.parent_node
    return actionList[::-1]

def get_path_states(node):
    stateList = []
    if node != None:
        stateList.append(node.state)
        while (node.parent_node != None):
            node = node.parent_node
            stateList.append(node.state)
    return stateList[::-1]

class PriorityQueue:
    def __init__(self, items=(), priority_function=(lambda x: x)):
        self.priority_function = priority_function
        self.pqueue = []
        # add the items to the PQ
        for item in items:
            self.add(item)
    
    """
    #Add item to PQ with priority-value given by call to priority_function
    """
    def add(self, item):
        pair = (self.priority_function(item), item)
        heapq.heappush(self.pqueue, pair)
    
    """
    pop and return item from PQ with min priority-value
    """
    def pop(self):
        return heapq.heappop(self.pqueue)[1]
    
    """
    gets number of items in PQ
    """
    def __len__(self):
        return len(self.pqueue)

def best_first_search(problem, f):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue(items=[node], priority_function=f)
    reached = {problem.initial_state:node}
    visited_nodes = []
    while frontier:
        node = frontier.pop()
        visited_nodes.append(node.state[0])
        if problem.is_goal(node.state):
            return {'node': node, 'journey': visited_nodes}
        for child in expand(problem, node):
            s = child.state
            if (s not in reached) or (child.path_cost < reached[s].path_cost):
                reached[s] = child
                frontier.add(child)
    return None

def best_first_search_treelike(problem, f):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue(items=[node], priority_function=f)
    visited_nodes = []
    while frontier:
        node = frontier.pop()
        visited_nodes.append(node.state[0])
        if problem.is_goal(node.state):
            return {'node': node, 'journey': visited_nodes}
        for child in expand(problem, node):
            frontier.add(child)
    return None

def breadth_first_search(problem, treelike = False):
    if not treelike:
        return best_first_search(problem, (lambda node: node.depth))
    return best_first_search_treelike(problem, (lambda node: node.depth))

def depth_first_search(problem, treelike = False):
    if not treelike:
        return best_first_search(problem, (lambda node: -node.depth))
    return best_first_search_treelike(problem, (lambda node: -node.depth))
    
def uniform_cost_search(problem, treelike = False):
    if not treelike:
        return best_first_search(problem, (lambda node: node.path_cost))
    return best_first_search_treelike(problem, (lambda node: node.path_cost))

def greedy_search(problem, h, treelike = False):
    if not treelike:
        return best_first_search(problem, h)
    return best_first_search_treelike(problem, h)

def astar_search(problem, h, treelike = False):
    if not treelike:
        return best_first_search(problem, (lambda node: node.path_cost + h(node)))
    return best_first_search_treelike(problem, (lambda node: node.path_cost + h(node)))