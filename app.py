import random
import threading
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'worms_destructible_objects_v5'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=False, engineio_logger=False)

WIDTH = 800
HEIGHT = 500

WORM_NAMES = [
    "Chcankopán", "Kuleštencl", "Mrdojeb", "Řiťopich", "Zabíječ", "Praselyzér", "Krutopřísňák", 
    "Gringo", "Dežodorant", "Falus", "Nedomrd", "Prasopes", "Bobíček", "Honimír", "Kazimír", 
    "Rakeťák", "Kolmosral", "Uzdichcal", "Lofas", "Bombarďák", "Píčus", "Netáhlo", "Zpíčenec"
]

game_state = {}

def generate_clouds_and_rocks():
    rocks = []
    for _ in range(12):
        rx = random.randint(50, WIDTH - 50)
        ry = random.randint(300, 480)
        rocks.append({"x": rx, "y": ry, "r": random.randint(12, 24)})
        
    clouds = []
    for _ in range(5):
        clouds.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(30, 130),
            "speed": random.uniform(0.1, 0.3),
            "size": random.randint(20, 35)
        })
    tree_positions = [180, 320, 480, 640]
    return rocks, clouds, tree_positions

def get_initial_state(map_name="map1", mode="vs_friend"):
    rocks, clouds, tree_positions = generate_clouds_and_rocks()
    
    worms = {}
    chosen_names = random.sample(WORM_NAMES, 10)
    
    # Bezpečné zóny pro generování okurek (min_x, max_x), aby se neutopily.
    # Uprav tyto hodnoty podle polohy vody na konkrétních mapách.
    SAFE_SPAWN_ZONES = {
        "map1": {"team1": (30, WIDTH//2 - 50), "team2": (WIDTH//2 + 50, WIDTH - 30)},
        "map2": {"team1": (30, 200), "team2": (600, 770)},
        "map3": {"team1": (30, WIDTH//2 - 50), "team2": (WIDTH//2 + 50, WIDTH - 30)},
        "map4": {"team1": (30, WIDTH//2 - 50), "team2": (WIDTH//2 + 50, WIDTH - 30)},
        "map5": {"team1": (30, WIDTH//2 - 50), "team2": (WIDTH//2 + 50, WIDTH - 30)}
    }
    
    safe_zones = SAFE_SPAWN_ZONES.get(map_name, {"team1": (30, WIDTH//2 - 50), "team2": (WIDTH//2 + 50, WIDTH - 30)})
    
    for i in range(5):
        w_id = f"t1_{i}"
        worms[w_id] = {
            "team": "team1", "x": random.randint(*safe_zones["team1"]), "y": 50, 
            "hp": 100, "angle": -0.5, "facing": "right", "color": "#ff3385", 
            "name": chosen_names[i]
        }
    
    for i in range(5):
        w_id = f"t2_{i}"
        worms[w_id] = {
            "team": "team2", "x": random.randint(*safe_zones["team2"]), "y": 50, 
            "hp": 100, "angle": -0.5, "facing": "left", "color": "#00e5ff", 
            "name": chosen_names[i+5]
        }

    crates = []
    for i in range(4):
        crates.append({
            "id": f"c_{i}", "x": random.randint(50, WIDTH - 50), "y": random.randint(-100, 0), "type": "health", "value": 25
        })
       
    mines = []
    for _ in range(2):  # Číslo udává počet vygenerovaných min
        mines.append({
            "id": f"m_{random.randint(1000, 99999)}",
            "x": random.randint(50, WIDTH - 50),
            "y": random.randint(-100, 0),
            "triggered": False
        })

    return {
        "worms": worms,
        "active_team": "team1",
        "active_worm_id": "t1_0",
        "rocks": rocks,
        "clouds": clouds,
        "tree_positions": tree_positions,
        "crates": crates,
        "mines": mines,
        "game_over": False,
        "winner": None,
        "explosion_event": None,
        "map_name": map_name,
        "mode": mode,
        "wind": random.uniform(-1.0, 1.0),
        "team1_ammo": { "frag": 2, "m79": 2, "uzi": 2, "shotgun": 4, "lupara": 4, "plasma": 2, "molotov": 2, "railgun": 2 },
        "team2_ammo": { "frag": 2, "m79": 2, "uzi": 2, "shotgun": 4, "lupara": 4, "plasma": 2, "molotov": 2, "railgun": 2 },
        "weapon_used_this_turn": False,
        "last_active_worm": { "team1": "t1_0", "team2": "t2_0" }
    }

game_state = get_initial_state()

def airdrop_worker():
    while True:
        time.sleep(60)
        try:
            if game_state and not game_state.get("game_over"):
                drop_types = ["health", "frag", "m79", "uzi", "shotgun", "lupara", "plasma", "molotov", "railgun"]
                chosen_type = random.choice(drop_types)
                
                drop_val = 25 if chosen_type == "health" else (2 if chosen_type in ["shotgun", "lupara"] else 1)
                
                crate = {
                    "id": f"ad_{random.randint(1000, 99999)}",
                    "x": random.randint(50, WIDTH - 50),
                    "y": -50,
                    "type": chosen_type,
                    "value": drop_val,
                    "is_airdrop": True,
                    "landed": False
                }
                game_state["crates"].append(crate)
    
                socketio.emit('spawn_airdrop', crate)
                socketio.emit('state_update', game_state)
        except Exception:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('init_state', game_state)

@socketio.on('start_new_game')
def handle_start_game(data):
    global game_state
    m_name = data.get('map_name', 'map1')
    mode = data.get('mode', 'vs_friend')
    game_state = get_initial_state(map_name=m_name, mode=mode)
    emit('init_state', game_state, broadcast=True)

@socketio.on('sync_worm')
def handle_sync_worm(data):
    p_id = data.get('player_id')
    if p_id in game_state["worms"] and not game_state["game_over"]:
        game_state["worms"][p_id]["x"] = data.get('x')
        game_state["worms"][p_id]["y"] = data.get('y')
        game_state["worms"][p_id]["angle"] = data.get('angle')
        game_state["worms"][p_id]["facing"] = data.get('facing')
        game_state["worms"][p_id]["hp"] = data.get('hp', game_state["worms"][p_id]["hp"])
        emit('state_update', game_state, broadcast=True, include_self=False)

@socketio.on('client_shoot')
def handle_client_shoot(data):
    w_id = game_state.get("active_worm_id")
    if not w_id: return
    data['shooter'] = w_id
    
    wpn_type = data.get('type')
    team = game_state["worms"][w_id]["team"]
    ammo_key = f"{team}_ammo"
    
    if wpn_type not in ['bazooka', 'grenade']:
        consume_ammo = data.get('consume_ammo', True)
        
        if consume_ammo:
            is_multi_shot = wpn_type in ['shotgun', 'lupara']
            
            if is_multi_shot or not game_state.get('weapon_used_this_turn'):
                if game_state[ammo_key].get(wpn_type, 0) <= 0:
                    return
                
                game_state[ammo_key][wpn_type] -= 1
                game_state['weapon_used_this_turn'] = True
                emit('state_update', game_state, broadcast=True)
        
    emit('spawn_bullet', data, broadcast=True)

@socketio.on('client_explosion')
def handle_client_explosion(data):
    global game_state
    if game_state["game_over"]: return

    updated_worms = data.get('worms')
    if updated_worms:
        game_state["worms"] = updated_worms

    game_state["rocks"] = data.get('rocks', game_state["rocks"])
    game_state["crates"] = data.get('crates', game_state["crates"])
    game_state["mines"] = data.get('mines', game_state.get("mines", []))

    game_state["explosion_event"] = {
        "x": data.get('ex'),
        "y": data.get('ey'),
        "r": data.get('er')
    }

    t1_alive = any(w["hp"] > 0 for w in game_state["worms"].values() if w["team"] == "team1")
    t2_alive = any(w["hp"] > 0 for w in game_state["worms"].values() if w["team"] == "team2")

    if not t1_alive and not t2_alive:
        game_state["game_over"] = True
        game_state["winner"] = "Remíza"
    elif not t2_alive:
        game_state["game_over"] = True
        game_state["winner"] = "Tým 1"
    elif not t1_alive:
        game_state["game_over"] = True
        game_state["winner"] = "Tým 2"

    emit('state_update', game_state, broadcast=True)
    game_state["explosion_event"] = None 

@socketio.on('collect_crate')
def handle_collect_crate(data):
    crate_id = data.get('crate_id')
    w_id = data.get('worm_id')
    
    crate = next((c for c in game_state["crates"] if c["id"] == crate_id), None)
    if not crate: return
    
    game_state["crates"] = [c for c in game_state["crates"] if c["id"] != crate_id]
    
    if w_id in game_state["worms"]:
        c_type = crate.get('type', 'health')
        if c_type == "health":
            game_state["worms"][w_id]["hp"] += crate.get('value', 25)
        else:
            team = game_state["worms"][w_id]["team"]
            ammo_key = f"{team}_ammo"
            game_state[ammo_key][c_type] = game_state[ammo_key].get(c_type, 0) + crate.get('value', 1)
            
    emit('state_update', game_state, broadcast=True)

@socketio.on('object_sunk')
def handle_object_sunk(data):
    kind = data.get('kind')
    obj_id = data.get('id')
    if kind == 'crate':
        game_state["crates"] = [c for c in game_state["crates"] if c["id"] != obj_id]
    elif kind == 'mine':
        game_state["mines"] = [m for m in game_state.get("mines", []) if m["id"] != obj_id]

@socketio.on('switch_worm')
def handle_switch_worm():
    if game_state["game_over"]: return
    
    team = game_state["active_team"]
    alive_in_team = [w_id for w_id, w in game_state["worms"].items() if w["team"] == team and w["hp"] > 0]
    
    if alive_in_team:
        try:
            curr_idx = alive_in_team.index(game_state["active_worm_id"])
            next_idx = (curr_idx + 1) % len(alive_in_team)
            game_state["active_worm_id"] = alive_in_team[next_idx]
        except ValueError:
            game_state["active_worm_id"] = alive_in_team[0]

        game_state.setdefault("last_active_worm", {})[team] = game_state["active_worm_id"]
        emit('state_update', game_state, broadcast=True)

def find_next_alive_worm(team_name):
    alive = [w_id for w_id, w in game_state["worms"].items() if w["team"] == team_name and w["hp"] > 0]
    if not alive:
        return None

    # Pokud je okurka, se kterou tento tým naposledy hrál, stále naživu, zůstáváme u ní.
    # Jinak (zemřela) spadneme zpět na první živou v pořadí.
    last_worm_id = game_state.get("last_active_worm", {}).get(team_name)
    if last_worm_id in alive:
        return last_worm_id

    return alive[0]

@socketio.on('next_turn')
def handle_next_turn():
    if not game_state["game_over"]:
        game_state["active_team"] = "team2" if game_state["active_team"] == "team1" else "team1"
        game_state["weapon_used_this_turn"] = False
        next_worm = find_next_alive_worm(game_state["active_team"])
        
        game_state["wind"] = random.uniform(-1.0, 1.0)
        
        if next_worm:
            game_state["active_worm_id"] = next_worm
            game_state.setdefault("last_active_worm", {})[game_state["active_team"]] = next_worm

        emit('state_update', game_state, broadcast=True)

@socketio.on('restart_game')
def handle_restart():
    global game_state
    game_state = get_initial_state(map_name=game_state.get('map_name', 'map1'), mode=game_state.get('mode', 'vs_friend'))
    emit('init_state', game_state, broadcast=True)

if __name__ == '__main__':
    threading.Thread(target=airdrop_worker, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
