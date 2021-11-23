PROG = "readelf"

correct_coverage = open("%s.cor.gcov" % PROG, "r")
correct_coverage.readline()
correct_coverage.readline()
correct_coverage.readline()
correct_runs = float(correct_coverage.readline().strip().split(":")[-1])

incorrect_coverage = open("%s.incor.gcov" % PROG, "r")
incorrect_coverage.readline()
incorrect_coverage.readline()
incorrect_coverage.readline()
incorrect_runs = float(incorrect_coverage.readline().strip().split(":")[-1])

vals = {}

for line in correct_coverage.readlines():
    if "-" in line.split(":")[0]:
        continue
    linenum = line.split(":")[1]
    vals[linenum] = {}
    try:
        vals[linenum]["cor"] = float(line.split(":")[0])/correct_runs
    except:
        vals[linenum]["cor"] = 0

for line in incorrect_coverage.readlines():
    if "-" in line.split(":")[0]:
        continue
    linenum = line.split(":")[1]
    try:
        vals[linenum]["incor"] = float(line.split(":")[0])/incorrect_runs
    except:
        vals[linenum]["incor"] = 0

correct_coverage.close()
incorrect_coverage.close()

output = open("%s.csv" % PROG, "w")

output.write("line_num,correct,incorrect\n")

for key in sorted(vals.keys()):
    output.write("%s,%d,%d\n" % (key,vals[key]["cor"],vals[key]["incor"]))
    print "%s,%d,%d" % (key,vals[key]["cor"],vals[key]["incor"])

output.close()

print correct_runs, incorrect_runs
