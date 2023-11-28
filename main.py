from complexity_metric import *
from halstead_metric import *
from separate import *
import subprocess, sys


if __name__ == "__main__":

    print(f"start extracting cyclomatic metric for {PROJECT_NAME}")
    compute_cyclomatic_metric()

    print(f"start extracting halstead metric for {PROJECT_NAME}")
    subdirectories = extract_sub_directory(TEST_DIR)
    create_halstead_result_directory(subdirectories, PROJECT_NAME)
    extract_metric(TEST_DIR, subdirectories, PROJECT_NAME)

    halstead_mp = load_halstead_mp()
    extract_test_halstead(halstead_mp, COMPLEXITY_TSV_FILE)

