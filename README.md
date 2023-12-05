
# Complexity Metric Calculation Tool: Test-Case Prioritization for Configuration Testing

This is a complexity metric calculation tool for configuration test prioritization of open source projects in Ctest [dataset](https://github.com/FanZang-Allen/ctest-prio-ae).

## About

The execution time of regression testing in Continuous Integration is usually long in complex system. Test Case Prioritization (TCP)  is one of the leading strategies in speeding up the CI/CD pipeline for developers, which attempts to fnd an optimal execution order of test cases to get the maximum rate of fault
detection. There are already a bunch of researches in exploring effectiveness of metrics like code coverage and historical information in TCP algorithm. However, these metrics all have some pain points: dynamic code coverage analysis is time consuming and TCP algorithm based on historical information is not stable. Hence, some researchers start to investigate effectiveness of other static metrics like complexity metric: [McCabe cyclomatic metric](https://en.wikipedia.org/wiki/Cyclomatic_complexity) and [Halstead software metric](https://en.wikipedia.org/wiki/Halstead_complexity_measures). Although some researches like [Daniel et.al](https://link.springer.com/chapter/10.1007/978-3-031-07297-0_4) show that complexity metrics works well for nomal unit testing, little effort has been made on exploring the performance of complexity based TCP for configuration test. This repository contains a tool which compute the complexity metric of five open source projects, and the collected results are utilized in [Ctest prioritization project](https://github.com/FanZang-Allen/ctest-prio-ae) for evaluation.

## Getting Started

### Requirements

- Python3 >= 3.5.0.
- Java 11: run [checkstyle](https://checkstyle.sourceforge.io/) tool to compute cyclomatic complexity metric of java test cases
- Java 8: run tool developed by [Speckboy Inc.](https://sourceforge.net/projects/halsteadmetricstool/) to compute halstead software metric of java program

### Add Project

Clone the following projects:

- Hadoop: git clone https://github.com/xlab-uiuc/hadoop.git app/ctest-hadoop
- Zookeeper: git clone https://github.com/xlab-uiuc/zookeeper.git app/ctest-zookeeper
- Hbase: git clone https://github.com/xlab-uiuc/hbase.git app/ctest-hbase
- Alluxio: git clone https://github.com/xlab-uiuc/alluxio.git app/ctest-alluxio

### Configuration

Follow the comments in config.py, configure the path to Java 11 and Java 8. You can also change the name of result folder if you want.

### Reproducibility

In config.py, you can specify the project that you want to collect information. You can then reproduce all results in testInfo/ folder:

```Bash
# after configuration
python3 main.py
# you will see progress in terminal
```

### Extension

This tool can be used to collect complexity metric of any java projects. You can clone your own project and then update the config.py to include your project directory. For more details, please refer to comments in config.py

## Collected Test Information

The final collected information for test cases of open source projects stay in testInfo/ folder:

- testInfo/CyclomaticComplexity: This folder contains computed cyclomatic complexity metric for each java test case in format "module#testname metric". The direct tsv file contains metrics that don't consider inheritance relationship between classes. The inherit tsv file consider this relationship. Both are evaluated in Ctesr prioritization folder.
- testInfo/general: This folder contains computed class information in json format. Inheritance relation between classes are included in these files.
- testInfo/HalsteadMetric: This folder contains computed halstead software metric for each java test file in format "testfile total_operator total_operand distinct_operator distinct_operand". These four basic metrics are then used in separate.py to calculate halstead metric like program volume and program length. For more details, please refer to separate.py 

## Contact

For questions about this project or artifact, please contact [Fan Zang](fanzang2@illinois.edu)
