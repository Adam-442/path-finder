let selected = 'player';
// POST body data.
let player_coord = null;
let rows = 6;
let columns = 8;
let tree_coords = [];
let gold_coords = [];
let selected_algorithm = 'BFS';
let playback_speed = 1.00;

const compareArrays = (a, b) => {
    return JSON.stringify(a) === JSON.stringify(b);
};

const clearPlayerCoords = (row, column) => {
    if (player_coord && player_coord[0] === row && player_coord[1] === column) player_coord = null;
}

// change size <-- reserve what is placed <-- hover logic <-- clicking logic

async function sendRequest(input_data, method = selected_algorithm) {
    const response = await fetch(`http://0.0.0.0:4422/api/grid/${method}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: input_data
    });
    const jsonData = await response.json();
    return jsonData;
}

async function solve() {
    if (player_coord === null || gold_coords.length === 0) return;

    // await sendRequest();
    const data = JSON.stringify({
        'initial_state': player_coord,
        'N': columns,
        'M': rows,
        'wall_coords': tree_coords,
        'food_coords': gold_coords
    });
    await sendRequest(data).then(solution => {
        toggleButtons();
        highlight_search_journey(solution);
    });

    // let solution_test = {"goal_journey":[[2,2],[1,2],[2,1],[1,1],[1,3],[3,1],[1,4],[4,1],[1,5],
    // [2,4],[4,2],[5,1],[1,6],[2,5],[3,4],[4,3],[5,2],[1,7],[2,6],[3,3]],
    // "goal_path":[[2,2],[1,2],[1,3],[1,4],[2,4],[3,4],[3,3]]}
    
    // highlight_search_journey(solution_test.goal_journey);

    // animatePlayer([[2, 2], [2, 3], [3, 3], [3, 4], [4, 4], [4, 3], [4, 2], [4, 1], [3, 1]])
}

function toggleButtons() {
    let buttons = document.getElementsByClassName('button');
    Array.from(buttons).forEach(button => {
        button.classList.toggle('disable');
    });
    let inputs = document.getElementsByClassName('size_input');
    Array.from(inputs).forEach(input => {
        input.classList.toggle('disable');
    });
}

function highlight_search_journey(solution) {
    // journey = solution.goal_journey.slice();
    let time_gap = parseInt(500/playback_speed);
    console.log(solution.goal_journey);
    journey = solution.goal_journey.slice().filter(( t={}, a=> !(t[a]=a in t) ));
    console.log(...journey);
    const searchInterval = setInterval(()=> {
        if (journey.length === 0) {
            clearInterval(searchInterval);
            highlight_goal_path(solution.goal_path);
        } else {
            search_coord = journey.shift();
            let cell = document.getElementById(`img_${search_coord[0]}x${search_coord[1]}`).parentElement;
            cell.classList.add('search');
        }
    }, time_gap);
}

function highlight_goal_path(goal_path) {
    let time_gap = parseInt(500/playback_speed);
    path = goal_path.slice();
    const searchInterval = setInterval(()=> {
        if (path.length === 0) {
            clearInterval(searchInterval);
            animatePlayer(goal_path);
        } else {
            coord = path.shift();
            let cell = document.getElementById(`img_${coord[0]}x${coord[1]}`).parentElement;
            cell.classList.remove('search');
            cell.classList.add('search_correct');
        }
    }, time_gap);
}

function animatePlayer(path_states = []) {
    // let time_gap = parseInt(400);
    // let inner_time_gap = parseInt(350);
    let move_direction = null;
    const animationInterval = setInterval(()=> {
        if (path_states.length === 0) {
            clearInterval(animationInterval);
            toggleButtons();
            clearSearchHighlights();
        } else {
            if (player_coord[0] - path_states[0][0] === 1) {
                move_direction = 'move_up';
            } else if (player_coord[0] - path_states[0][0] === -1) {
                move_direction = 'move_down';
            } else if (player_coord[1] - path_states[0][1] === 1) {
                move_direction = 'move_left';
            } else if (player_coord[1] - path_states[0][1] === -1) {
                move_direction = 'move_right';
            }

            let old_player = document.getElementById(`img_${player_coord[0]}x${player_coord[1]}`);
            old_player.classList.add(move_direction);

            setTimeout(()=> {
                old_player.style.display = null
                old_player.classList.remove(move_direction);
        
                player_coord = path_states.shift();

                // remove coord from gold coords if it exists there
                gold_coords = gold_coords.filter(el => !compareArrays(el, [player_coord[0], player_coord[1]]))
    
                let new_player = document.getElementById(`img_${player_coord[0]}x${player_coord[1]}`);
                new_player.src = `./vectors/player.svg`;
                new_player.style.display = 'inline-block';
            }, 375) // the animation in CSS takes 0.45s
        }
    }, 425);
}

function clearSearchHighlights() {
    setTimeout(() => {
        for (let r = 1; r <= rows; r++) {
            for (let c = 1; c <= columns; c++) {
                let cell = document.getElementById(`img_${r}x${c}`).parentElement;
                cell.classList.remove('search', 'search_correct');
            }
        }
    }, 3000);
}

// FILL THE TABLES BY CODE (when page first loads)
changeSize();

function selectItem(item) {
    selected = item;
    document.querySelector(':root').style.setProperty(`--selected`, `url('./vectors/${item}.svg')`);
}

function placeItem(row, column) {
    let img = document.getElementById(`img_${row}x${column}`);
    if (selected === 'Xframe') {
        // no need to delete src, just hide it and remove it from the arrays
        img.style.display = null;
        tree_coords = tree_coords.filter(el => !compareArrays(el, [row, column]))
        gold_coords = gold_coords.filter(el => !compareArrays(el, [row, column]))
        clearPlayerCoords(row, column);
    } else {
        // change cell image and make sure its visible
        img.src = `./vectors/${selected}.svg`;
        img.style.display = 'inline-block';

        if (selected === 'tree') {
            // Add coord if its not in tree_coords array
            if (!tree_coords.filter(el => compareArrays(el, [row, column])).length) tree_coords.push([row, column]);
            // remove coord from gold_coords if its included
            gold_coords = gold_coords.filter(el => !compareArrays(el, [row, column]))
            // clear the player coords if the tree is in replacing his current place
            clearPlayerCoords(row, column);
        } else if (selected === 'gold') {
            // Add coord if its not in gold_coords array
            if (!gold_coords.filter(el => compareArrays(el, [row, column])).length) gold_coords.push([row, column]);
            // remove coord from tree_coords if its included
            tree_coords = tree_coords.filter(el => !compareArrays(el, [row, column]))
            // clear the player coords if the gold is in replacing his current place
            clearPlayerCoords(row, column);
        } else {
            // Remove/Clear Previous PLayer position first
            if (player_coord != null) {
                let old_player = document.getElementById(`img_${player_coord[0]}x${player_coord[1]}`);
                old_player.style.display = null;
            }
            // Add/Update the player coords in the array
            player_coord = [row, column];
            // remove coord from tree and gold coords if it exists there
            tree_coords = tree_coords.filter(el => !compareArrays(el, [row, column]))
            gold_coords = gold_coords.filter(el => !compareArrays(el, [row, column]))
        }
    }
}

function changeSize() {
    rows = Number(document.getElementById("rows_input").value);
    columns = Number(document.getElementById("columns_input").value);
    // 1. Reset Table
    let res = ``;
    // 2. Start Adding empty rows
    for (let i = 1; i <= rows; i++) {
        res += `<tr>`
        // 3. Start Adding empty columns inside each row
        for (let j = 1; j <= columns; j++) {
            res += `<td class="cells"><img src="" alt="" id="img_${i}x${j}" onmousedown="return placeItem(${i}, ${j})"></td>`            
        }
        res += `</tr>`
    }
    document.getElementById('game_table').innerHTML = res;
}

function changeAlgorithm(algorithm_short, algorithm_name) {
    selected_algorithm = algorithm_short;
    document.getElementById('algorithm_button').innerText = algorithm_name;
}

function changeSpeed(speed, speed_display_name) {
    playback_speed = speed;
    document.querySelector(':root').style.setProperty(`--speed`, speed);
    document.getElementById('speed_button').innerText = speed_display_name;
}