import os

# Java 11 run check style tool to compute cyclomatic complexity metric of each unit test case
JAVA_11_HOME = "/usr/lib/jvm/java-11-openjdk-amd64/bin/java"
# Java 8 run HalsteadMetricsCMD jar file to compute halstead software metrics of each java test program file
JAVA_8_HOME = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

CHECKSTYLE_CONFIG_FILE = os.path.join(CUR_DIR, "cyclomatic_check.xml")
CHECKSTYLE_CMD = JAVA_11_HOME +  " -jar checkstyle-10.12.3-all.jar -c"

HALSTEAD_CMD = JAVA_8_HOME +  ' -jar HalsteadMetricsCMD.jar'
HALSTEAD_OUTPUT_TYPE = 'html'
HALSTEAD_SKIP_FUC = [] # specify name of java test program file you would like to ignore
HALSTEAD_LOG_DIR = os.path.join(CUR_DIR, "halsteadResult/")

# name and location of open source projects
HCOMMON = "hadoop-common"
HDFS = "hadoop-hdfs"
HBASE = "hbase-server"
ALLUXIO = "alluxio-core"
ZOOKEEPER = "zookeeper-server"
ALLAPPS = [HCOMMON, HDFS, HBASE, ZOOKEEPER, ALLUXIO]
ALLAPPS_AB = ["HCommon", "HDFS", "HBase", "ZooKeeper", "Alluxio"]
# change this to your folder where you clone the ctest projects(this is default one if you follow README)
PROJECT_DIR = os.path.join(CUR_DIR, "app/")
HCOMMON_TEST_DIR = os.path.join(PROJECT_DIR, 'ctest-hadoop/hadoop-common-project/hadoop-common/src/test/java/org/apache/hadoop/')
HDFS_TEST_DIR = os.path.join(PROJECT_DIR, 'ctest-hadoop/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop')
ALLUXIO_TEST_DIR = os.path.join(PROJECT_DIR, 'ctest-alluxio/core/')
HBASE_TEST_DIR = os.path.join(PROJECT_DIR, 'ctest-hbase/hbase-server/src/test/java/org/apache/hadoop/hbase/')
ZOOKEEPER_TEST_DIR = os.path.join(PROJECT_DIR, 'ctest-zookeeper/zookeeper-server/src/test/java/org/apache/zookeeper/')

# configure which project to run
PROJECT_NAME = HCOMMON
TEST_DIR = HCOMMON_TEST_DIR

COMPLEXITY_TSV_FILE = os.path.join(CUR_DIR, f"testInfo/cyclomaticComplexity/{PROJECT_NAME}/{PROJECT_NAME}.tsv")
CTEST_COMPLEXITY_TSV_FILE = os.path.join(CUR_DIR, f"testInfo/cyclomaticComplexity/{PROJECT_NAME}/{PROJECT_NAME}-ctest.tsv")
CLASS_INFO_FILE = os.path.join(CUR_DIR, f"testInfo/general/{PROJECT_NAME}/{PROJECT_NAME}.json")
HALSTEAD_FILE = os.path.join(CUR_DIR, "testInfo/halsteadMetric/{}/{}.tsv").format(PROJECT_NAME, PROJECT_NAME)
HALSTEAD_SIMPLE_FILE = os.path.join(CUR_DIR, "testInfo/halsteadMetric/{}/{}-simple.tsv").format(PROJECT_NAME, PROJECT_NAME)
HALSTEAD_INHERIT_FILE = os.path.join(CUR_DIR, "testInfo/halsteadMetric/{}/{}-inherit.tsv").format(PROJECT_NAME, PROJECT_NAME)

# Optional precomputed file, used when there is dependency between current module and previous computed module. ex. test files in hadoop-hdfs have dependencies on hadoop-common 
LOAD_COMPLEXITY_FILE = None
LOAD_CLASSINFO_FILE = None
# LOAD_COMPLEXITY_FILE = os.path.join(CUR_DIR, f"testInfo/cyclomaticComplexity/{HCOMMON}/{HCOMMON}.tsv")
# LOAD_CLASSINFO_FILE = os.path.join(CUR_DIR, f"testInfo/general/{HCOMMON}/{HCOMMON}.json")
