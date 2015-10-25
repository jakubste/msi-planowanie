import pyhop


def car_price(dist):
    return 10 + 1.5 * dist


def car_time(dist):
    return 1.2 * dist


def taxi_price(dist):
    return 10 + 2.5 * dist


def taxi_time(dist):
    return 15 + 1.2 * dist


def pt_price(dist):
    if dist < 20:
        return 2
    else:
        return 25


def pt_time(dist):
    return 10 + 0.7 * dist


def walk_time(dist):
    return 3 * dist


def ride_car(state, x, y):
    if state.loc['me'] == x and state.loc['car'] == x and \
                    state.cash >= car_price(state.dist[x][y]) and \
                    state.time >= car_time(state.dist[x][y]):
        state.loc['me'] = y
        state.loc['car'] = y
        state.cash -= car_price(state.dist[x][y])
        state.time -= car_time(state.dist[x][y])
        return state
    return False


def ride_public_transport(state, x, y):
    if state.loc['me'] == x and \
                    state.cash >= pt_price(state.dist[x][y]) and \
                    state.time >= pt_time(state.dist[x][y]):
        state.loc['me'] = y
        state.cash -= pt_price(state.dist[x][y])
        state.time -= pt_time(state.dist[x][y])
        return state
    return False


def walk(state, x, y):
    if state.loc['me'] == x and state.dist[x][y] < 20 and \
                    state.time >= walk_time(state.dist[x][y]):
        state.loc['me'] = y
        state.time -= walk_time(state.dist[x][y])
        return state
    return False


def ride_taxi(state, x, y):
    if state.loc['me'] == x and state.loc['taxi'] == x and state.dist[x][y] < 50 and \
                    state.cash >= taxi_price(state.dist[x][y]) and \
                    state.time >= taxi_time(state.dist[x][y]):
        state.loc['me'] = y
        state.loc['taxi'] = y
        state.cash -= taxi_price(state.dist[x][y])
        state.time -= taxi_time(state.dist[x][y])
        return state
    return False


def call_taxi(state, x):
    if state.loc['taxi'] != x and \
                    state.time >= 5:
        state.time -= 5
        state.loc['taxi'] = x
        return state
    return False


pyhop.declare_operators(
    ride_car,
    ride_public_transport,
    walk,
    ride_taxi,
    call_taxi
)


def travel_car(state, x, y):
    return [('ride_car', x, y)]


def travel_taxi_pt(state, x, y):
    return [('call_taxi', x), ('ride_taxi', x, 'train_station'), ('ride_public_transport', 'train_station', y)]


def travel_car_pt(state, x, y):
    return [('ride_car', x, 'train_station'), ('ride_public_transport', 'train_station', y)]


def travel_pt_pt(state, x, y):
    return [('ride_public_transport', x, 'train_station'), ('ride_public_transport', 'train_station', y)]


def travel_walk_pt(state, x, y):
    return [('walk', x, 'train_station'), ('ride_public_transport', 'train_station', y)]


pyhop.declare_methods('travel', travel_car, travel_taxi_pt, travel_car_pt, travel_pt_pt, travel_walk_pt)

state = pyhop.State('state')
state.loc = {
    'me': 'home',
    'car': 'home',
    'taxi': 'anywhere',
}
state.dist = {
    'home': {'train_station': 10, 'target': 100},
    'train_station': {'target': 100},
}


state.cash = 100
state.time = 97

result = pyhop.pyhop(state, [('travel', 'home', 'target')], verbose=3)
