import csv
import os
import math
import json
project_name = ['hadoop-common', 'hadoop-hdfs', 'alluxio-core', 'hbase-server', 'zookeeper-server']
halstead_mp = {}


def extract_ctest_cyclomatic(proj_name):
    ctest_tsv = f"/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/{proj_name}/{proj_name}-testcase.tsv"
    all_test_file = f"/home/fanzang2/project/complexity-based-tcp/{proj_name}.tsv"
    output_file = f"/home/fanzang2/project/complexity-based-tcp/{proj_name}-ctest.tsv"
    used_method = []
    labeled_method = {}
    find = {}
    with open(ctest_tsv, 'r') as tsv_file:
        for line in tsv_file:
            method = line.strip().split('\t')[0]
            find[method] = 0
            if method[-1] == ']':
                name = method.split('[')[0]
                if name not in labeled_method:
                    labeled_method[name] = []
                labeled_method[name].append(method)
            else:
                used_method.append(method)
    used_method = set(used_method)
    all_methods = {}
    with open(output_file, 'a', newline='') as out_file:
        with open(all_test_file, 'r') as tsv_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            for line in tsv_file:
                fields = line.strip().split('\t')
                if fields:
                    all_methods[fields[0].split('#')[1]] = fields[1]
                    if fields[0] in used_method:
                        #out_file.write(line)
                        tsv_writer.writerow([fields[0], fields[1]])
                        find[fields[0]] = 1
                    elif fields[0] in labeled_method:
                        for m in labeled_method[fields[0]]:
                            tsv_writer.writerow([m, fields[1]])
                            find[m] = 1
    with open(output_file, 'a', newline='') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        for key,value in find.items():
            if value == 0:
                if key.split('#')[1] in all_methods:
                    tsv_writer.writerow([key, all_methods[key.split('#')[1]]])
                else:
                    print('Ctest: ' + key + ' not found')

def calculate_halstead_metric(N1, N2, n1, n2):
    N = N1 + N2  # Program Length
    n = n1 + n2  # Program Vocabulary
    V = N * math.log2(n) # Program Volume
    D = (n1 / 2) * (N2 / n2) # Program Difficulty
    E = D * V # Program Effort
    return [N1, N2, n1, n2, N, n, V, D, E]

def load_halstead_mp():
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    global halstead_mp
    for proj_name in project_name:
        halstead_file = os.path.join(CUR_DIR, "testInfo/halsteadMetric/{}/{}.tsv").format(proj_name, proj_name)
        halstead_data = [x.strip("\n").split("\t") for x in open(halstead_file)]
        for class_info in halstead_data:
            for i in range(1, len(class_info)):
                if not class_info[i].endswith(".0"):
                    class_info[i] += "00.0"   # the tool fail to calculate metric for this file due to memory constraint
            class_name = class_info[0]
            N1, N2, n1, n2 = [float(x) for x in class_info[1:]] # Total operator, Total operand, Unique operator, Unique operand
            halstead_mp[class_name] = calculate_halstead_metric(N1, N2, n1, n2)

def extract_ctest_halstead(proj_name):
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    ctest_file = os.path.join(CUR_DIR, "testInfo/cyclomaticComplexity/{}/{}-ctest.tsv").format(proj_name, proj_name)
    ctest_name = [x.strip("\n").split("\t")[0] for x in open(ctest_file)]
    inherit_info_file = os.path.join(CUR_DIR, "testInfo/general/{}/{}.json").format(proj_name, proj_name)
    with open(inherit_info_file, 'r') as file:
        inherit_info = json.load(file)
    ctest_halstead_simple = {}
    ctest_halstead_inherit = {}

    for ctest in ctest_name:
        ctest_class = ctest.split("#")[0]
        ctest_halstead_simple[ctest] = halstead_mp[ctest_class]
    
    for ctest in ctest_name:
        ctest_class = ctest.split("#")[0]
        N1, N2, n1, n2 = halstead_mp[ctest_class][:4]
        parent_class = inherit_info[ctest_class]['parent']
        while parent_class != None and parent_class in halstead_mp:
            pN1, pN2, pn1, pn2 = halstead_mp[parent_class][:4]
            N1 += pN1
            N2 += pN2
            n1 += pn1
            n2 += pn2
            if parent_class not in inherit_info:
                break
            parent_class = inherit_info[parent_class]['parent']
        ctest_halstead_inherit[ctest] = calculate_halstead_metric(N1, N2, n1, n2)
    
    ctest_simple_file = os.path.join(CUR_DIR, "testInfo/halsteadMetric/{}/{}-ctest-simple.tsv").format(proj_name, proj_name)
    ctest_inherit_file = os.path.join(CUR_DIR, "testInfo/halsteadMetric/{}/{}-ctest-inherit.tsv").format(proj_name, proj_name)

    with open(ctest_simple_file, 'w') as f:
        for name, info in ctest_halstead_simple.items():
            f.write(name + "\t" + "\t".join([str(x) for x in info]) + "\n")
    

    with open(ctest_inherit_file, 'w') as f:
        for name, info in ctest_halstead_inherit.items():
            f.write(name + "\t" + "\t".join([str(x) for x in info]) + "\n")


if __name__ == "__main__":
    #extract_ctest_cyclomatic(project_name[1])
    load_halstead_mp()
    extract_ctest_halstead(project_name[4])