import os

JAVA_11_HOME = "/usr/lib/jvm/java-11-openjdk-amd64/bin/java"
JAVA_8_HOME = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
CHECKSTYLE_CONFIG_FILE = os.path.join(CUR_DIR, "cyclomatic_check.xml")
CHECKSTYLE_CMD = JAVA_11_HOME +  " -jar checkstyle-10.12.3-all.jar -c"

HALSTEAD_CMD = JAVA_8_HOME +  ' -jar HalsteadMetricsCMD.jar'
HALSTEAD_OUTPUT_TYPE = 'html'
HALSTEAD_SKIP_FUC = []
HALSTEAD_LOG_DIR = os.path.join(CUR_DIR, "halsteadResult/")

HCOMMON = "hadoop-common"
HDFS = "hadoop-hdfs"
HBASE = "hbase-server"
ALLUXIO = "alluxio-core"
ZOOKEEPER = "zookeeper-server"
ALLAPPS = [HCOMMON, HDFS, HBASE, ZOOKEEPER, ALLUXIO]
ALLAPPS_AB = ["HCommon", "HDFS", "HBase", "ZooKeeper", "Alluxio"]

HCOMMON_TEST_DIR = '/home/fanzang2/project/app/ctest-hadoop/hadoop-common-project/hadoop-common/src/test/java/org/apache/hadoop/'
HDFS_TEST_DIR = '/home/fanzang2/project/app/ctest-hadoop/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop'
ALLUXIO_TEST_DIR = '/home/fanzang2/project/app/ctest-alluxio/core/'
HBASE_TEST_DIR = '/home/fanzang2/project/app/ctest-hbase/hbase-server/src/test/java/org/apache/hadoop/hbase/'
ZOOKEEPER_TEST_DIR = '/home/fanzang2/project/app/ctest-zookeeper/zookeeper-server/src/test/java/org/apache/zookeeper/'

# configure which project to run
PROJECT_NAME = HCOMMON
TEST_DIR = HCOMMON_TEST_DIR

COMPLEXITY_TSV_FILE = os.path.join(CUR_DIR, f"testInfo/cyclomaticComplexity/{PROJECT_NAME}/{PROJECT_NAME}.tsv")
CTEST_COMPLEXITY_TSV_FILE = os.path.join(CUR_DIR, f"testInfo/cyclomaticComplexity/{PROJECT_NAME}/{PROJECT_NAME}-ctest.tsv")
CLASS_INFO_FILE = os.path.join(CUR_DIR, f"testInfo/general/{PROJECT_NAME}/{PROJECT_NAME}.json")
HALSTEAD_FILE = os.path.join(CUR_DIR, "testInfo/halsteadMetric/{}/{}.tsv").format(PROJECT_NAME, PROJECT_NAME)
HALSTEAD_SIMPLE_FILE = os.path.join(CUR_DIR, "testInfo/halsteadMetric/{}/{}-simple.tsv").format(PROJECT_NAME, PROJECT_NAME)
HALSTEAD_INHERIT_FILE = os.path.join(CUR_DIR, "testInfo/halsteadMetric/{}/{}-inherit.tsv").format(PROJECT_NAME, PROJECT_NAME)

# Optional precomputed file
LOAD_COMPLEXITY_FILE = None
LOAD_CLASSINFO_FILE = None
# LOAD_COMPLEXITY_FILE = os.path.join(CUR_DIR, f"testInfo/cyclomaticComplexity/{HCOMMON}/{HCOMMON}.tsv")
# LOAD_CLASSINFO_FILE = os.path.join(CUR_DIR, f"testInfo/general/{HCOMMON}/{HCOMMON}.json")
