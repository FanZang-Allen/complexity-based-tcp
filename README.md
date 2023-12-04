
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
