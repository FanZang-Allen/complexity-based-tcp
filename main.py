from complexity_metric import *
from halstead_metric import *
from separate import *
import subprocess, sys

def switch_jdk_version(jdk_version):
    try:
        # Set the Java version using update-alternatives
        subprocess.run(['sudo', 'update-alternatives', '--set', 'java', f'/path/to/your/jdk{jdk_version}/bin/java'])
        subprocess.run(['sudo', 'update-alternatives', '--set', 'javac', f'/path/to/your/jdk{jdk_version}/bin/javac'])
        print(f'Switched to JDK {jdk_version}')
    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')

if __name__ == "__main__":

    switch_jdk_version(11)
    sys.exit(1)
    print(f"start extracting cyclomatic metric for {PROJECT_NAME}")
    compute_cyclomatic_metric()

    print(f"start extracting halstead metric for {PROJECT_NAME}")
    subdirectories = extract_sub_directory(TEST_DIR)
    create_halstead_result_directory(subdirectories, PROJECT_NAME)
    extract_metric(TEST_DIR, subdirectories, PROJECT_NAME)

    halstead_mp = load_halstead_mp()
    extract_test_halstead(halstead_mp, COMPLEXITY_TSV_FILE)

