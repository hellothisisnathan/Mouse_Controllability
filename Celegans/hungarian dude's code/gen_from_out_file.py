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

    plt.xlabel(xlabel, fontsize = 60, y = 1.1, labelpad = 10)
    plt.ylabel(ylabel, fontsize = 60, rotation = 90, labelpad = 40)
    plt.xticks(index, labels, fontsize=40, rotation=60)
    plt.title(title, y = 1.02)

    plt.legend(handles = patches, bbox_to_anchor=(1.01, 1), loc='upper left',
               borderaxespad=0.)
    plt.savefig(file_name, dpi = dpi)
    plt.close(fig)

#title = "First reached\n" + sensor + ", input: " + str(inp) + "\nMax ticks: " \
#    + str(sim.TICKS)
#bar_plot('Muscles', 'Ticks', title, muscles,
#     [first_reached_values, first_fired_values],
#     OUTPUT_IMAGE, 400, ["First reached", "First fired", ""], False, True, [])
#
# first reach figure END

# avg, stdev of muscle values

INP_AVG = "./figures/sensor_muscles_alt/AVM_1500_avg.out"
INP_FR = "./figures/sensor_muscles/AVM_2000_avg.out"

OUT_AVG = "./figures/avm_1500_avg_6.png"
OUT_FR = "./figures/avm_2000_fr_1.png"
#muscles = ["MVL23", "MVR22", "MVL22", "MVR21", "MVL21", "MVR23", "MVR24"]
muscles = []

indices = {}
with open(INP_AVG, 'r') as f:
    lines = f.readlines()
splitted_lines = list(map(lambda x: x.strip().split(','), lines))
print(splitted_lines[2][69])

for muscle in muscles:
    indices[muscle] = splitted_lines[1].index(muscle)
counter = 0
for avg_fired in splitted_lines[2]:
    if float(avg_fired) > 0:
        indices[splitted_lines[1][counter]] = counter
        muscles.append(splitted_lines[1][counter])
    counter += 1

print(indices.items())

fired_mean_list = []
reached_mean_list = []
all_mean_list = []

fired_err_list = []
reached_err_list = []
all_err_list = []
for muscle in muscles:
    fired_mean_list.append(float(splitted_lines[2][indices[muscle]]))
    reached_mean_list.append(float(splitted_lines[4][indices[muscle]]))
    all_mean_list.append(float(splitted_lines[6][indices[muscle]]))

    fired_err_list.append(float(splitted_lines[3][indices[muscle]]))
    reached_err_list.append(float(splitted_lines[5][indices[muscle]]))
    all_err_list.append(float(splitted_lines[7][indices[muscle]]))

print(fired_mean_list)
print(reached_mean_list)
print(all_mean_list)

title = "Average values\n" + "AVM" + ", input: " + str(2000) + "\nMax ticks: " \
    + str(120)


bar_plot('Muscles', 'Muscle value', title, muscles,
     [fired_mean_list, reached_mean_list, all_mean_list],
     OUT_AVG, 200, ["Avg while fired", "Avg while reached", "Avg"],
     True, False, [fired_err_list, reached_err_list, all_err_list])
# avg, stdev of muscle values END
