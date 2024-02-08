from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from problem import *
from search_algorithms import *

app = Flask(__name__)
CORS(app)

def astar_wrapper(p):
    return astar_search(p, h=p.h)

def greedy_wrapper(p):
    return greedy_search(p, h=p.h)

algorithms = {
    'DFS': depth_first_search,
    'BFS': breadth_first_search,
    'UCS': uniform_cost_search,
    'Astar': astar_wrapper,
    'Greedy': greedy_wrapper,
}

@app.route('/')
def empty():
    return redirect(url_for('home'))

@app.route('/api')
def home():
    return 'Home Route - a.k.a backend is working'

@app.route('/api/grid/<searcher>', methods=['POST'])
def grid_problem(searcher):
    content = request.get_json(silent=False)
    
    walls = [(coord[0], coord[1]) for coord in content['wall_coords']]
    foods = [(coord[0], coord[1]) for coord in content['food_coords']]
    
    grid_problem = GridProblem(initial_state=tuple(content['initial_state']), 
                                       N=content['N'], M=content['M'], 
                                       wall_coords=walls,
                                       food_coords=foods)
    goal = algorithms[searcher](grid_problem)

    states = get_path_states(goal['node'])
    path_states = [state[0] for state in states]
    
    data = {'goal_path':path_states, 'goal_journey':goal['journey']}
    response = jsonify(data)
    return response

@app.route('/api/route/<searcher>', methods=['GET']) # Change method to 'POST' later..
def route_problem(searcher):
    # route problem example
    example_map_graph = { 
    ('A', 'B'): 1,
    ('A', 'C'): 1,
    ('A', 'D'): 1,
    ('B', 'A'): 1,
    ('B', 'C'): 1,
    ('B', 'E'): 1,
    ('C', 'B'): 1
    }

    example_coords = {
    'A': (1,2),
    'B': (0,1), 
    'C': (1,1),
    'D': (2,1),
    'E': (0,0),
    }

    route_problem = RouteProblem(initial_state='A', goal_state='E', 
                                         map_graph=example_map_graph, 
                                         map_coords=example_coords)
    
    goal = algorithms[searcher](route_problem)
    
    states = get_path_states(goal['node'])
    path_states = [state[0] for state in states]
    
    data = {'goal_path':path_states, 'goal_journey':goal['journey']}
    response = jsonify(data)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=4422, host='0.0.0.0')