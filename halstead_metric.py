import subprocess
import os
import re
import csv
import shutil
test_directory_list = ['/home/fanzang2/project/app/ctest-hadoop/hadoop-common-project/hadoop-common/src/test/java/org/apache/hadoop/', 
                       '/home/fanzang2/project/app/ctest-hadoop/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/',
                       '/home/fanzang2/project/app/ctest-alluxio/core/',
                       '/home/fanzang2/project/app/ctest-hbase/hbase-server/src/test/java/org/apache/hadoop/hbase/',
                       '/home/fanzang2/project/app/ctest-zookeeper/zookeeper-server/src/test/java/org/apache/zookeeper/']

project_name_list = ['hadoop-common', 'hadoop-hdfs', 'alluxio-core', 'hbase-server', 'zookeeper-server']
output_folder = '/home/fanzang2/project/complexity-based-tcp/halsteadResult/'

halstead_metric_result = {}

def extract_package_name(java_file_path):
    # extract package name of a java file
    with open(java_file_path, 'r') as java_file:
        content = java_file.read()
        package_match = re.search(r'^\s*package\s+([^;]+);', content, re.MULTILINE)
        if package_match:
            return package_match.group(1).strip() + '.' + java_file_path.split('/')[-1][:-5]
        else:
            return None

def extract_sub_directory(directory):
    subdirectories = ['']
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            subdirectory = os.path.relpath(os.path.join(root, dir_name), directory)
            subdirectories.append(subdirectory)
    return subdirectories


def create_halstead_result_directory(subdirectories, project_name):
    for d in subdirectories:
        target_directory = output_folder + project_name + '/' + d
        os.makedirs(target_directory, exist_ok=True)


def parse_output_html(package_name, output_file):
    html_content = None
    halstead_metric_result[package_name] = []
    search_text_list = ['No of Distinct Operators(n1)', 'No of Distinct Operands(n2)', 'Total No of Operators(N1)', 'Toatl No of Operands(N2)']
    with open(output_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    for search_text in search_text_list:
        start_pos = html_content.find(search_text)
        if start_pos != -1:
            end_pos = html_content.find('</td>', start_pos)
        if end_pos != -1:
            value = html_content[start_pos:end_pos].split('>')[-1].strip()
            halstead_metric_result[package_name].append(value)
    
def count_lines(filename):
    with open(filename, 'r') as file:
        return sum(1 for line in file)

def extract_metric(directory, subdirectories, project_name):
    global halstead_metric_result
    command_head = 'java -jar HalsteadMetricsCMD.jar'
    output_type = 'html'
    skip_function = ['MultiThreadedUpdater.java']
    for index, sub in enumerate(subdirectories):
        #if index < 11:
        #    continue
        test_dir = directory + sub
        output_dir = output_folder + project_name + '/' + sub + '/'
        if sub == '':
            output_dir = output_folder + project_name + '/'
        command = command_head + ' ' + test_dir + ' ' + output_dir + ' ' + output_type
        #print(command)
        long_file = []
        for filename in os.listdir(test_dir):
            #print(filename)
            if filename.endswith(".java"):
                length = count_lines(test_dir +'/' +  filename)
                if length > 500 or filename in skip_function:
                    new_name = os.path.join(test_dir, filename[:-1])
                    package_name = extract_package_name(test_dir + '/' + filename)
                    halstead_metric_result[package_name] = [str(length), str(length),str(length),str(length)]
                    print(f"change file {filename} name to {new_name}")
                    shutil.move(os.path.join(test_dir, filename), new_name)

        result = subprocess.run(command, shell=True, cwd='./', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Complete halstead metric calculation of java files in {test_dir} with index {index}")
        for filename in os.listdir(test_dir):
            if filename.endswith(".java"):
                package_name = extract_package_name(test_dir + '/' + filename)
                #print(package_name)
                output_file = output_dir + filename.split('.')[0] + '.html'
                #print(output_file)
                parse_output_html(package_name, output_file)
            if filename.endswith(".jav"):
                shutil.move(os.path.join(test_dir, filename), os.path.join(test_dir, filename + 'a'))
                print(f"change file {filename} name back to {os.path.join(test_dir, filename + 'a')}")
        store_result(project_name)
        halstead_metric_result = {}
        #break

def store_result(project_name):
    file_name = project_name + '.tsv'
    with open(file_name, 'a', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        for key, value in halstead_metric_result.items():
            writer.writerow([key] + value)

subdirectories = extract_sub_directory(test_directory_list[4])

create_halstead_result_directory(subdirectories, project_name_list[4])

extract_metric(test_directory_list[4], subdirectories, project_name_list[4])