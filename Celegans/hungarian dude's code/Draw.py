import time
import logging
import curses
from Simulator import Simulator
from curses import wrapper

def get_color(nt):
    nt = nt.split('/')[0]
    ret_val = curses.color_pair(1)
    if nt == "mu":
        ret_val = curses.color_pair(2)
    elif nt == "in":
        ret_val = curses.color_pair(3)
    elif nt == "mo":
        ret_val = curses.color_pair(4)
    return ret_val

def draw_border(stdscr, width, height):
    for i in range(width):
        for j in range(height):
            if i == 0 and j != 0 and j != height - 1:
                stdscr.addstr(j, i, "|")
            elif j == 0 and i != 0 and i != width - 1:
                stdscr.addstr(j, i, "_")
            elif i == width - 1 and j != 0 and j != height - 1:
                stdscr.addstr(j, i, "|")
            elif j == height - 1 and i != 0 and i != width - 1:
                stdscr.addstr(j, i, "*")

def draw_cells(stdscr, nw, y_coords, curr_tick):
    for node in nw.nodes:
        pos = int(nw.neurons[node].position * 100)
        st = "X"
        if nw.neurons[node].last_fired == curr_tick and nw.neurons[node].is_muscle():
            st = "F"
        stdscr.addstr(y_coords[node], pos, st, get_color(nw.neurons[node].type))

def write_info(stdscr, width, height, curr_tick):
    stdscr.addstr(height + 1, 0, "CURRENT TICK: " + str(curr_tick))
    stdscr.addstr(height + 2, 0, "Blue: sensor neuron", curses.color_pair(1))
    stdscr.addstr(height + 3, 0, "Cyan: interneuron", curses.color_pair(3))
    stdscr.addstr(height + 4, 0, "Yellow: motor neuron", curses.color_pair(4))
    stdscr.addstr(height + 5, 0, "Magenta: muscle", curses.color_pair(2))
    pass

def get_y_coords(nw, width):
    x_coords = {}
    y_coords = {}
    pos_in_cols = {}
    for i in range(width):
        pos_in_cols[i] = 0

    for node in nw.nodes:
        pos = int(nw.neurons[node].position * 100)
        x_coords[node] = pos
        y_coords[node] = int(pos_in_cols[pos] + 1)
        pos_in_cols[pos] += 1

    def comp(node):
        tp = nw.neurons[node].type.split('/')[0]
        if tp == "se":
            return 1
        elif tp == "in":
            return 2
        elif tp == "mo":
            return 3
        return 4

    for i in range(width):
        nodes = sorted([node for node in x_coords.keys() if x_coords[node] == i], key = comp)
        k = 1
        for node in nodes:
            y_coords[node] = k
            k += 1

    return y_coords

def main(stdscr):
    # for debugging
    logger = logging.getLogger(__file__)
    hdlr = logging.FileHandler(__file__ + ".log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

    logger.info("begin")
    # clear screen
    stdscr.clear()

    # initializing colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    width = 102
    height = 30

    sim = Simulator()
    nw = sim.nw
    #nw.set_input_data(["OLQDL"], [10000.0])
    y_coords = get_y_coords(sim.nw, width)

    done = False
    while (sim.curr_tick < sim.TICKS and not done):
        stdscr.clear()
        sim.perform_tick()

        draw_border(stdscr, width, height)
        write_info(stdscr, width, height, sim.curr_tick)
        draw_cells(stdscr, nw, y_coords, sim.curr_tick)
        stdscr.refresh()

        done = sim.check_state()
        sim.curr_tick += 1
        time.sleep(0.5)
        if done or sim.curr_tick == sim.TICKS:
            time.sleep(1000)

wrapper(main)
