code = open("sbt.c", "w")

num_funcs = (1 << 16) - 15
depth = 3

defs_protos = """#include <string.h>

#define NUM_FUNCS %s
#define START_DEPTH %s

unsigned long globl = 0;

unsigned long func(unsigned long, int);

""" % (num_funcs, depth)

dbt = """
unsigned long dbt(unsigned char * str) {
    unsigned long hash = 5381;
    int c;

    globl = 0;

    while ((c = *str++))
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return func(hash, START_DEPTH);
}

unsigned long dbt_slow(unsigned char * str) {
    unsigned long hash = 5381;
    int c;

    globl = 0;

    while ((c = *str++))
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return func(hash, START_DEPTH);
}
"""

func = """
unsigned long func(unsigned long num, int depth){
    if (depth == 0) return num;
    unsigned long idx = (num << depth) % NUM_FUNCS;
    return funcs[idx](depth-1);
}"""

func_proto = """unsigned long func%s(unsigned long depth){
    unsigned long x = %s;
    memcpy(&globl, &x, sizeof(unsigned long));
    return func(%s,depth) + globl;
};\n"""

array = """unsigned long (*funcs[NUM_FUNCS])(unsigned long) = {
    func0"""




code.write(defs_protos)


for i in range(num_funcs):
    code.write(func_proto % (i,i,i))

code.write("\n\n%s" % array)

for i in range(1,num_funcs):
    code.write(", ")
    if i%10 == 0:
        code.write("\n    ")
    code.write("func%s" % i)
code.write("};\n")

code.write(dbt)

code.write("\n\n")

code.write(func)
