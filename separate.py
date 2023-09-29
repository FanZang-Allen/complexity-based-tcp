#ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/hadoop-common/hadoop-common-testcase.tsv'
#ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/hadoop-hdfs/hadoop-hdfs-testcase.tsv'
#ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/alluxio-core/alluxio-core-testcase.tsv'
#ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/hbase-server/hbase-server-testcase.tsv'
ctest_tsv = '/home/fanzang2/project/ctest-prio-ae/testInfo/execTime/zookeeper-server/zookeeper-server-testcase.tsv'
all_test_file = '/home/fanzang2/project/complexity-based-tcp/zookeeper-server.tsv'
output_file = '/home/fanzang2/project/complexity-based-tcp/zookeeper-server-direct.tsv'
missing_file = '/home/fanzang2/project/complexity-based-tcp/zookeeper-server-inherit.tsv'
used_method = []
with open(ctest_tsv, 'r') as tsv_file:
    for line in tsv_file:
        used_method.append(line.strip().split('\t')[0])
used_method = set(used_method)
record = {}
for i in used_method:
    record[i] = 0
with open(output_file, 'a') as out_file:    
    with open(all_test_file, 'r') as tsv_file:
        for line in tsv_file:
            fields = line.strip().split('\t')
            if fields and fields[0] in used_method:
                out_file.write(line)
                record[fields[0]] = 1
             
with open(missing_file, 'a') as out_file:    
    for i in record:
        if record[i] == 0:
            out_file.write(i+'\n')
