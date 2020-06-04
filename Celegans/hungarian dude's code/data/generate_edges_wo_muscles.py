import csv

inp = []
css = {}
ejs = {}

with open('NeuronConnectOrig.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader, None)
    inp = [row for row in reader]


for row in inp:
    #print(row)
    if row[2] == "EJ":
        if (row[0], row[1]) in ejs:
            ejs[(row[0], row[1])] += int(row[3])
        else:
            ejs[(row[0], row[1])] = int(row[3])
    if (row[2] == "S" or row[2] == "Sp"):
        if (row[0], row[1]) in css:
            css[(row[0], row[1])] += int(row[3])
        else:
            css[(row[0], row[1])] = int(row[3])

#EJs are back and forth connections
for ej in ejs:
    if (ej[1], ej[0]) not in ejs:
        print(ej)

with open('edges_wo_muscles.csv', 'a') as f:
    f.write("Neuron 1,Neuron 2,Type,Nbr\n")
    for key,value in ejs.items():
        to_write = key[0] + ";" + key[1] + ";EJ;" + str(value) + "\n"
        f.write(to_write)

    for key,value in css.items():
        to_write = key[0] + ";" + key[1] + ";CS;" + str(value) + "\n"
        f.write(to_write)
