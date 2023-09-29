import subprocess
import re
import os
import fnmatch
import csv

# using checkstyle tool to walk through test file to calculate cyclomatic complexity of each test method

exe_command = 'java -jar checkstyle-10.12.3-all.jar -c'
cyclo_config_file = '/home/fanzang2/project/complexity-based-tcp/cyclomatic_check.xml'
len_config_file = '/home/fanzang2/project/complexity-based-tcp/method_len.xml'
#test_directory = '/home/fanzang2/project/app/ctest-hadoop/hadoop-common-project/hadoop-common/src/test/java/org/apache/hadoop/'
#test_directory = '/home/fanzang2/project/app/ctest-hadoop/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/'
#test_directory = '/home/fanzang2/project/app/ctest-alluxio/core/'
test_directory = '/home/fanzang2/project/app/ctest-hbase/hbase-server/src/test/java/org/apache/hadoop/hbase/'
#test_directory = '/home/fanzang2/project/zookeeper/zookeeper-server/src/test/java/org/apache/zookeeper/'
package_name_start = 'org'
tsv_file_path = 'hbase-server.tsv'

def extract_java_files(directory: str):
    # extract all java test file from given directory
    pattern = '*.java'
    java_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                java_files.append(os.path.join(root, filename))
    return java_files


def extract_method_name(java_file_path):
    command = exe_command + ' ' + len_config_file + ' ' + java_file_path
    result = subprocess.run(command, shell=True, cwd='./', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout.splitlines()
    name_list = []
    for i in range(1, len(output) - 1):
        curr = output[i].split(':')
        name_list.append(curr[-1].split(' ')[2])
    return name_list


def extract_method_names(java_file_path, starting_line_numbers):
    # extract names of test method given the start line
    method_names = []

    with open(java_file_path, 'r') as java_file:
        lines = java_file.readlines()

    for line_number in starting_line_numbers:
        if line_number >= len(lines):
            continue
        line = lines[line_number - 1].strip()
        # if start line is @Override or @Test
        find = False
        while len(line) > 0 and line[0] == '@':
            match = re.match(r'^@\w+\s*\(\w+\)', line)
            if match:
                line = line[len(match.group()):]
                print(line)
            match = re.search(r'\w+\s*\(', line)
            if match:
                method_names.append(match.group().split('(')[0])
                find = True
                break
            line_number += 1
            line = lines[line_number - 1].strip()
        if find == True:
            continue
        match = re.search(r'\w+\s*\(', line)
        if match:
            method_names.append(match.group().split('(')[0])
        else:
            method_names.append('NuLL')
            print(f"fail to find method in {java_file_path} with line_number: {line_number}")

    return method_names


def extract_package_name(java_file_path):
    # extract package name of a java file
    with open(java_file_path, 'r') as java_file:
        content = java_file.read()
        package_match = re.search(r'^\s*package\s+([^;]+);', content, re.MULTILINE)
        if package_match:
            return package_match.group(1).strip() + '.' + java_file_path.split('/')[-1][:-5]
        else:
            return '' 



def extract_method_complexity(java_file_path):
    command = exe_command + ' ' + cyclo_config_file + ' ' + java_file_path
    result = subprocess.run(command, shell=True, cwd='./', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout.splitlines()
    # method_start_lines = []
    complexity_list = []
    for i in range(1, len(output) - 1):
        curr = output[i].split(':')
        #method_start_lines.append(int(curr[1]))
        complexity_list.append(int(curr[-1].split(' ')[4]))
    #method_names = extract_method_names(java_file_path, method_start_lines)
    method_names = extract_method_name(java_file_path)
    package_name = extract_package_name(java_file_path)
    if package_name == '':
        package_name = java_file_path[java_file_path.find(package_name_start):].replace('/', '.')[:-5]
    for i in range(len(method_names)):
        if method_names[i] == 'NuLL':
            continue
        method_names[i] = package_name + '#' + method_names[i]
    result_dict = {}
    for i in range(len(method_names)):
        if method_names[i] == 'NuLL':
            continue
        result_dict[method_names[i]] = complexity_list[i]
    return result_dict


java_files = extract_java_files(test_directory)
with open(tsv_file_path, 'a', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for i in range(len(java_files)):
        result_dict = extract_method_complexity(java_files[i])
        for key, value in result_dict.items():
            writer.writerow([key, value])
        print(f"Complete java file:{java_files[i]}, index: {i}")
