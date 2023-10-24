import subprocess
import re
import os
import fnmatch
import csv
import json

# using checkstyle tool to walk through test file to calculate cyclomatic complexity of each test method

exe_command = 'java -jar checkstyle-10.12.3-all.jar -c'
cyclo_config_file = '/home/fanzang2/project/complexity-based-tcp/cyclomatic_check.xml'
#test_directory = '/home/fanzang2/project/app/ctest-hadoop/hadoop-common-project/hadoop-common/src/test/java/org/apache/hadoop/'
test_directory = '/home/fanzang2/project/app/ctest-hadoop/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop'
#test_directory = '/home/fanzang2/project/app/ctest-alluxio/core/'
#test_directory = '/home/fanzang2/project/app/ctest-hbase/hbase-server/src/test/java/org/apache/hadoop/hbase/'
#test_directory = '/home/fanzang2/project/app/ctest-zookeeper/zookeeper-server/src/test/java/org/apache/zookeeper/'
project_name = 'hadoop-hdfs'
complexity_info = {}
complexity_tsv_file_path = project_name + '.tsv'
test_class_info = {}
test_class_info_json_path = project_name + '.json'
load_complexity_info = None
load_class_info = None


def extract_java_files(directory: str):
    # extract all java test file from given directory
    pattern = '*.java'
    java_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                java_files.append(os.path.join(root, filename))
    return java_files


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


def extract_class_name(java_file_path, package_name):
    class_name = java_file_path.split('/')[-1][:-5]
    parent_class_with_package = None

    with open(java_file_path, 'r') as file:
        java_code = file.read()
        class_pattern = re.compile(r'class\s+'+ class_name + '\s+extends\s+([\w.]+)')
        class_match = class_pattern.search(java_code)

        if class_match:
            parent_class = class_match.group().split(' ')[-1]
        else:
            return class_name, parent_class_with_package
        import_pattern = re.compile(r'import\s+([\w.]+)' + parent_class + ';')
        import_match = import_pattern.search(java_code)
        if import_match:
            parent_class_with_package = import_match.group().split(' ')[1][:-1]
        else:
            parent_class_with_package = package_name + '.' + parent_class
    return class_name, parent_class_with_package


def process_checkstyle_output(checkstyle_output):
    package_name = checkstyle_output[0].split(':')[-1].split("'")[1]
    method_complexity_list = []
    method_name_list = []
    i = 0
    while i + 1 < len(checkstyle_output):
        if checkstyle_output[i].endswith('[CyclomaticComplexity]') and checkstyle_output[i + 1].endswith('[MethodLength]'):
            curr = checkstyle_output[i].split(':')
            method_complexity_list.append(int(curr[-1].split(' ')[4]))
            curr = checkstyle_output[i + 1].split(':')
            method_name_list.append(curr[-1].split(' ')[2])
            i += 2
        else:
            i += 1
    return package_name, method_name_list, method_complexity_list



def extract_method_complexity(java_file_path):
    command = exe_command + ' ' + cyclo_config_file + ' ' + java_file_path
    result = subprocess.run(command, shell=True, cwd='./', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout.splitlines()
    checkstyle_output = output[1:-1]
    package_name, method_name_list, method_complexity_list = process_checkstyle_output(checkstyle_output)
    class_name, parent_class_with_package = extract_class_name(java_file_path, package_name)
    test_class_name = package_name + '.' + class_name
    test_class_info[test_class_name] = {"parent":parent_class_with_package, "methods":method_name_list}
    for i in range(len(method_name_list)):
        complexity_info[test_class_name +'#'+ method_name_list[i]] = method_complexity_list[i]


def extract_inherit_method_complexity():
    for name, info in test_class_info.items():
        parent_class = info["parent"]
        while parent_class != None:
            if parent_class not in test_class_info:
                break
            parent_methods = test_class_info[parent_class]["methods"]
            for m in parent_methods:
                complete_name = parent_class + '#' + m
                if m not in info["methods"]:
                    if complete_name in complexity_info:
                        complexity_info[name +'#'+ m] = complexity_info[complete_name]
#                    elif load_complexity_info != None and complete_name in load_complexity_info:
#                        complexity_info[complete_name] = load_complexity_info[complete_name]
#                        complexity_info[name +'#'+ m] = complexity_info[complete_name]
            parent_class = test_class_info[parent_class]["parent"]



def load_calculated_info(complexity_path, info_path):
    with open(info_path, 'r') as file:
        load_class_info = json.load(file)
#    missing_class = []
#    for name, info in test_class_info.items():
#        parent_class = info["parent"]
#        if parent_class not in test_class_info and parent_class in load_class_info:
#            missing_class.append(parent_class)
#    for m in missing_class:
#        test_class_info[m] = load_class_info[m]
    test_class_info.update(load_class_info)
    load_complexity_info = {}
    with open(complexity_path, 'r') as tsv_file:
        for line in tsv_file:
            method, metric = line.strip().split('\t')
            load_complexity_info[method] = metric
    complexity_info.update(load_complexity_info)

java_files = extract_java_files(test_directory)
for i in range(len(java_files)):
    extract_method_complexity(java_files[i])
    print(f"Complete java file:{java_files[i]}, index: {i}")

load_calculated_info('/home/fanzang2/project/complexity-based-tcp/hadoop-common.tsv', '/home/fanzang2/project/complexity-based-tcp/hadoop-common.json')

with open(test_class_info_json_path, 'w') as json_file:
    json.dump(test_class_info, json_file)

#print(len(complexity_info))
extract_inherit_method_complexity()
#print(len(complexity_info))
with open(complexity_tsv_file_path, 'a', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for key, value in complexity_info.items():
        writer.writerow([key, value])

