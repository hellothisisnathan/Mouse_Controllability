import csv

inp = []
css = {}
ejs = {}

with open('NeuronFixedPoints.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader, None)
    inp = [row for row in reader if row[1][0] != "S"]

with open('edges_to_muscles.csv', 'a') as f:
    f.write("Neuron,Muscle,Nbr\n")
    for row in inp:
        to_write = row[0] + ";" + row[1] + ";NMJ;" + str(float(row[3])) + "\n"
        f.write(to_write)
