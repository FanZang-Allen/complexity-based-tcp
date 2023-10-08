import csv

project_name = ['hadoop-common', 'hadoop-hdfs', 'alluxio-core', 'hbase-server', 'zookeeper-server']
ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/hadoop-common/hadoop-common-testcase.tsv'
#ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/hadoop-hdfs/hadoop-hdfs-testcase.tsv'
#ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/alluxio-core/alluxio-core-testcase.tsv'
#ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/hbase-server/hbase-server-testcase.tsv'
#ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/zookeeper-server/zookeeper-server-testcase.tsv'
all_test_file = '/home/fanzang2/project/complexity-based-tcp/hadoop-common.tsv'
output_file = '/home/fanzang2/project/complexity-based-tcp/hadoop-common-direct.tsv'
missing_file = '/home/fanzang2/project/complexity-based-tcp/hadoop-common-inherit.tsv'



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



extract_ctest_cyclomatic(project_name[1])

