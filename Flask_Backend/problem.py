class Problem(object):
    
    def __init__(self, initial_state, goal_state = None):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    def actions(self, state):
        raise NotImplementedError
    
    def result(self, state, action):
        raise NotImplementedError
    
    def is_goal(self, state):
        return (self.goal_state == state)
    
    def action_cost(self, state1, action, state2):
        return 1
    
    def h(self, node):
        return 0
    
class RouteProblem(Problem):
    
    def __init__(self, initial_state, goal_state = None, map_graph = None, map_coords = None):
        super().__init__(initial_state, goal_state)
        self.map_graph = map_graph
        self.map_coords = map_coords
        self.neighbors = {}
        for key in map_graph:
            if key[0] in self.neighbors:
                self.neighbors[key[0]].append(key[1])
            else:
                self.neighbors[key[0]] = [key[1]]
        
    def actions(self, state):
        reachable = []
        if state in self.neighbors: 
            reachable = reachable + (self.neighbors[state])
        return reachable
    
    def result(self, state, action):
        if state in self.neighbors:
            if action in self.neighbors[state]:
                return action
        return state
    
    def action_cost(self, state1, action, state2):
        if (state1, state2) in self.map_graph:
            return self.map_graph[(state1, state2)]  
    
    def h(self, node):
        x2 = (self.map_coords[self.goal_state][0] - self.map_coords[node.state][0])**2
        y2 = (self.map_coords[self.goal_state][1] - self.map_coords[node.state][1])**2
        return (x2+y2)**(1/2)
    
class GridProblem(Problem):
    
    def __init__(self, initial_state, N, M, wall_coords, food_coords):
        self.N = N # number of rows
        self.M = M # number of columns
        self.wall_coords = wall_coords
        self.food_coords = food_coords
        # the tuple = self.food_eaten
        self.initial_state = (initial_state, tuple(False for _ in food_coords))
        
    def actions(self, state):
        x, y = state[0][0], state[0][1]
        legal = []
        if ((y+1 <= self.N) and ((x, y+1) not in self.wall_coords)):
            legal.append((x, y+1)) # up
        if ((y-1 <= self.N) and (y-1 >= 1) and ((x, y-1) not in self.wall_coords)):
            legal.append((x, y-1)) # down
        if ((x+1 <= self.M) and ((x+1, y) not in self.wall_coords)):
            legal.append((x+1, y)) # right
        if ((x-1 <= self.M) and (x-1 >= 1) and ((x-1, y) not in self.wall_coords)):
            legal.append((x-1, y)) # left
        return legal
    
    def result(self, state, action):
        eaten = list(state[1])
        if action in self.food_coords:
            eaten[self.food_coords.index(action)] = True
        return (action, tuple(eaten))

    def is_goal(self, state):
        return all(state[1])
    
    def h(self, node):
        x0, y0 = node.state[0][0], node.state[0][1]
        hs = []
        for i in [j for j, t in enumerate(node.state[1]) if not t]: # list of not yet eaten food
            x1, y1 = self.food_coords[i][0], self.food_coords[i][1]
            hs.append(abs(x1-x0) + abs(y1-y0))
        return min(hs) if hs else 0