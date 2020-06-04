from Simulator import Simulator
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import statistics
import matplotlib.patches as mpatches

mpl.rcParams.update({'font.size': 30})

def get_muscle_labels():
    muscles = []
    with open('./config/muscle_list', 'r') as f:
        muscles = [line.split(',')[0] for line in f]
    return muscles

# magic function for bar plots
def bar_plot(xlabel, ylabel, title, labels, values_list, file_name, dpi, patch_labels,
             stdev, avg_to_legend, err_list):
    bars = len(values_list)
    index = np.array([2 * x for x in np.arange(len(labels))])
    fig = plt.figure(figsize = (60, 20), dpi = dpi)
    ax = plt.subplot(111)

    pad = 0
    width = 0
    patch_c = mpatches.Patch(color = 'c',  label = patch_labels[0])
    patch_y = mpatches.Patch(color = 'y',  label = patch_labels[1])
    patch_m = mpatches.Patch(color = 'm',  label = patch_labels[2])

    if bars == 1:
        width = 1
        ax.bar(index, values_list[0], width = width, color = 'c', align = 'center')
        if stdev:
            ax.errorbar(index , values_list[0],
                        err_list[0],
                        linestyle = 'None', marker = '.', ecolor = 'red', color = 'red',
                        capthick = 1, elinewidth = 0.7)
        patches = patch_c
        if avg_to_legend:
            avg_patch_c =  mpatches.Patch(color = 'w',
                                          label = "avg: "
                                                   + str("{:.4f}".format(statistics.mean(values_list[0])))
                                                   + "\nstdev: "
                                                   + str("{:.4f}".format(statistics.stdev(values_list[0]))))
            patches = [patch_c, avg_patch_c]
    elif bars == 2:
        pad = 0.25
        width = 0.5
        ax.bar(index - pad, values_list[0], width = width, color = 'c', align = 'center')
        ax.bar(index + pad, values_list[1], width = width, color = 'y', align = 'center')

        if stdev:
            ax.errorbar(index - pad, values_list[0],
                        err_list[0],
                        linestyle = 'None', marker = '.', ecolor = 'red', color = 'red',
                        capthick = 1, elinewidth = 0.7)
            ax.errorbar(index + pad, values_list[1],
                        err_list[1],
                        linestyle = 'None', marker = '.', ecolor = 'red', color = 'red',
                        capthick = 1, elinewidth = 0.7)

        patches = [patch_c, patch_y]
        if avg_to_legend:
            avg_patch_c =  mpatches.Patch(color = 'w',
                                          label = "avg: "
                                                   + str("{:.4f}".format(statistics.mean(values_list[0])))
                                                   + "\nstdev: "
                                                   + str("{:.4f}".format(statistics.stdev(values_list[0]))))
            avg_patch_y =  mpatches.Patch(color = 'w',
                                          label = "avg: "
                                                   + str("{:.4f}".format(statistics.mean(values_list[1])))
                                                   + "\nstdev: "
                                                   + str("{:.4f}".format(statistics.stdev(values_list[1]))))
            patches = [patch_c, avg_patch_c, patch_y, avg_patch_y]

    elif bars == 3:
        pad = 0.5
        width = 0.5
        ax.bar(index - pad, values_list[0], width = width, color = 'c', align = 'center')
        ax.bar(index, values_list[1], width = width, color = 'y', align = 'center')
        ax.bar(index + pad, values_list[2], width = width, color = 'm', align = 'center')

        if stdev:
            ax.errorbar(index - pad, values_list[0],
                        err_list[0],
                        linestyle = 'None', marker = '.', ecolor = 'red', color = 'red',
                        capthick = 1, elinewidth = 0.5)
            ax.errorbar(index, values_list[1],
                        err_list[1],
                        linestyle = 'None', marker = '.', ecolor = 'red', color = 'red',
                        capthick = 1, elinewidth = 0.5)
            ax.errorbar(index + pad, values_list[2],
                        err_list[2],
                        linestyle = 'None', marker = '.', ecolor = 'red', color = 'red',
                        capthick = 1, elinewidth = 0.5)

        patches = [patch_c, patch_y, patch_m]
        if avg_to_legend:
            avg_patch_c =  mpatches.Patch(color = 'w',
                                          label = "avg: "
                                                   + str("{:.4f}".format(statistics.mean(values_list[0])))
                                                   + "\nstdev: "
                                                   + str("{:.4f}".format(statistics.stdev(values_list[0]))))
            avg_patch_y =  mpatches.Patch(color = 'w',
                                          label = "avg: "
                                                   + str("{:.4f}".format(statistics.mean(values_list[1])))
                                                   + "\nstdev: "
                                                   + str("{:.4f}".format(statistics.stdev(values_list[1]))))
            avg_patch_m =  mpatches.Patch(color = 'w',
                                          label = "avg: "
                                                   + str("{:.4f}".format(statistics.mean(values_list[2])))
                                                   + "\nstdev: "
                                                   + str("{:.4f}".format(statistics.stdev(values_list[2]))))
            patches = [patch_c, avg_patch_c, patch_y, avg_patch_y, patch_m, avg_patch_m]

    plt.xlabel(xlabel, fontsize = 30, y = 1.1)
    plt.ylabel(ylabel, fontsize = 30, rotation = 90, labelpad = 20)
    plt.xticks(index, labels, fontsize=15, rotation=60)
    plt.title(title, y = 1.02)

    plt.legend(handles = patches, bbox_to_anchor=(1.01, 1), loc='upper left',
               borderaxespad=0.)
    plt.savefig(file_name, dpi = dpi)
    plt.close(fig)


start = time.time()

def is_sensor(types):
    is_sens = False
    sp = types.split('/')
    if sp[0] == "se" or len(sp) > 1 and sp[1] == "se":
        is_sens = True
    return is_sens

sensors = []
with open('./config/neuron_list', 'r') as f:
    #sensors = [line.split(',')[0] for line in f if line.strip().split(',')[1].split('/')[0] == "se"]
    sensors = [line.split(',')[0] for line in f if is_sensor(line.strip().split(',')[1])]

PATH = "./figures/sensor_muscles_alt/"

x = np.array([100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000])
#x = np.array([500])
output = ""
counter = 1
muscles = get_muscle_labels()
for sensor in sensors:
    print("sensor: " + sensor + " (" + str(counter) + ")")
    for inp in x:
        print("inp: " + str(inp))
        sim = Simulator()
        nw = sim.nw
        nw.set_input_data([sensor], [inp])
        done = False

        while (sim.curr_tick < sim.TICKS and not done):
            sim.perform_tick()
            done = sim.check_state()
            sim.curr_tick += 1

        first_reached_values = [sim.nw.neurons[muscle].first_reached for muscle in muscles]
        first_fired_values = [sim.nw.neurons[muscle].first_fired for muscle in muscles]
        fired_values_list = [sim.nw.neurons[muscle].fire_values for muscle in muscles]
        reached_values_list = [sim.nw.neurons[muscle].reached_values for muscle in muscles]
        all_values_list = [sim.nw.neurons[muscle].all_values for muscle in muscles]

        # first reach figure
        OUTPUT_FILE = PATH + sensor + "_" + str(inp) + "_fr.out"
        OUTPUT_IMAGE = PATH + sensor + "_" + str(inp) + "_fr.png"
        title = "First reached\n" + sensor + ", input: " + str(inp) + "\nMax ticks: " \
                + str(sim.TICKS)
        bar_plot('Muscles', 'Ticks', title, muscles,
                 [first_reached_values, first_fired_values],
                 OUTPUT_IMAGE, 400, ["First reached", "First fired", ""], False, True, [])

        output = "first line: muscles; second line: first_reached; third line: first_fired\n"
        output += ",".join(muscle for muscle in muscles)
        output += "\n"
        output += ",".join(str(val) for val in first_reached_values)
        output += "\n"
        output += ",".join(str(val) for val in first_fired_values)

        with open(OUTPUT_FILE, 'w') as f:
            f.write(output)
        output = ""
        # first reach figure END

        # avg, stdev of muscle values
        OUTPUT_FILE = PATH + sensor + "_" + str(inp) + "_avg.out"
        OUTPUT_IMAGE = PATH + sensor + "_" + str(inp) + "_avg.png"
        title = "Average values\n" + sensor + ", input: " + str(inp) + "\nMax ticks: " \
                + str(sim.TICKS)

        fired_mean_list = []
        for val_list in fired_values_list:
            if len(val_list) > 0:
                fired_mean_list.append(statistics.mean(val_list))
            else:
                fired_mean_list.append(0)
        fired_err_list = []
        for val_list in fired_values_list:
            if len(val_list) > 1:
                fired_err_list.append(statistics.stdev(val_list))
            else:
                fired_err_list.append(0)
       # fired_mean_list = [statistics.mean(x) for x in fired_values_list if len(x) > 0]
       # fired_err_list = [statistics.stdev(x) for x in fired_values_list if len(x) > 0]

        reached_mean_list = []
        for val_list in reached_values_list:
            if len(val_list) > 0:
                reached_mean_list.append(statistics.mean(val_list))
            else:
                reached_mean_list.append(0)
        reached_err_list = []
        for val_list in reached_values_list:
            if len(val_list) > 1:
                reached_err_list.append(statistics.stdev(val_list))
            else:
                reached_err_list.append(0)
        #reached_mean_list = [statistics.mean(x) for x in reached_values_list if len(x) > 0]
#        reached_err_list = [statistics.stdev(x) for x in reached_values_list if len(x) > 1]

        all_mean_list = []
        for val_list in all_values_list:
            if len(val_list) > 0:
                all_mean_list.append(statistics.mean(val_list))
            else:
                all_mean_list.append(0)
        all_err_list = []
        for val_list in all_values_list:
            if len(val_list) > 1:
                all_err_list.append(statistics.stdev(val_list))
            elif len(val_list) > 0:
                all_err_list.append(0)
        #all_mean_list = [statistics.mean(x) for x in all_values_list if len(x) > 0]
#        all_err_list = [statistics.stdev(x) for x in all_values_list if len(x) > 0]

        bar_plot('Muscles', 'Muscle value', title, muscles,
                 [fired_mean_list, reached_mean_list, all_mean_list],
                 OUTPUT_IMAGE, 400, ["Avg while fired", "Avg while reached", "Avg"],
                 True, False, [fired_err_list, reached_err_list, all_err_list])

        output = "lines: muscles, fired avg, fired sted, reached avg, reached stdev," \
                 + " avg, stdev\n"
        output += ",".join(muscle for muscle in muscles)
        output += "\n"
        output += ",".join(str(val) for val in fired_mean_list)
        output += "\n"
        output += ",".join(str(val) for val in fired_err_list)
        output += "\n"
        output += ",".join(str(val) for val in reached_mean_list)
        output += "\n"
        output += ",".join(str(val) for val in reached_err_list)
        output += "\n"
        output += ",".join(str(val) for val in all_mean_list)
        output += "\n"
        output += ",".join(str(val) for val in all_err_list)
        with open(OUTPUT_FILE, 'w') as f:
            f.write(output)
        output = ""
        counter += 1
        # avg, stdev of muscle values END


print("--- %s seconds ---" % (time.time() - start))
