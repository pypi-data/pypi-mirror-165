import os

from .helpers import print_header
from .helpers import print_default
from .helpers import print_empty

from .checks import check_flake
from .checks import check_radon
from .checks import check_security_linter
from .checks import check_migrations
from .checks import check_unit_tests
from .checks import check_garpix_page_tests
from .checks import check_lighthouse
from .checks import check_test_coverage
from .checks import check_sentry

import datetime
from .constants import CONFIG_FILE_NAME_FLAKE8, CONFIG_FILE_CONTENT_FLAKE8
from .constants import CONFIG_FILE_NAME_COVERAGE, CONFIG_FILE_CONTENT_COVERAGE
from .constants import CONFIG_FILE_NAME_RADON, CONFIG_FILE_CONTENT_RADON
from .constants import CONFIG_FILE_NAME_BANDIT, CONFIG_FILE_CONTENT_BANDIT
from .constants import CONFIG_FILE_NAME_LIGHTHOUSE, CONFIG_FILE_CONTENT_LIGHTHOUSE


def create_config(directory, config_file_name, config_file_content):
    path = os.path.join(directory, config_file_name)
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            f.write(config_file_content)


def create_configuration_files(directory):
    create_config(directory, CONFIG_FILE_NAME_FLAKE8, CONFIG_FILE_CONTENT_FLAKE8)
    create_config(directory, CONFIG_FILE_NAME_RADON, CONFIG_FILE_CONTENT_RADON)
    create_config(directory, CONFIG_FILE_NAME_BANDIT, CONFIG_FILE_CONTENT_BANDIT)
    create_config(directory, CONFIG_FILE_NAME_COVERAGE, CONFIG_FILE_CONTENT_COVERAGE)
    create_config(directory, CONFIG_FILE_NAME_LIGHTHOUSE, CONFIG_FILE_CONTENT_LIGHTHOUSE)


def run_qa(
        directory, verbose: bool = False, lighthouse: bool = False, clear_reports: bool = False,
        flake: bool = False, radon: bool = False, linter: bool = False, migrations: bool = False, tests: bool = False,
        garpix_page: bool = False, test_coverage: bool = False
):
    # Default run all check without lighthouse
    variables_passed = lighthouse or flake or radon or linter or migrations or tests or garpix_page or test_coverage
    #
    os.chdir(directory)
    create_configuration_files(directory)
    #
    error_count = 0
    start_at = datetime.datetime.now()
    #
    print_header('Input')
    print_default(f'Directory: {directory}\n')
    print_default(f'Start at: {start_at}\n')

    print_header('Checking')

    # flake8 for backend
    error_count += check_flake(directory, verbose, CONFIG_FILE_NAME_FLAKE8, flake, variables_passed)

    # Cyclomatic complexity
    error_count += check_radon(directory, verbose, CONFIG_FILE_NAME_RADON, radon, variables_passed)

    # Security linter
    error_count += check_security_linter(directory, verbose, CONFIG_FILE_NAME_BANDIT, linter, variables_passed)

    # Project migrations
    error_count += check_migrations(directory, verbose, migrations, variables_passed)

    # Unit tests
    error_count += check_unit_tests(directory, verbose, tests, variables_passed, test_coverage)

    # Unit tests garpix_page
    error_count += check_garpix_page_tests(verbose, garpix_page, variables_passed)

    # Test coverage
    coverage_result, coverage_value = check_test_coverage(verbose, test_coverage, variables_passed)
    error_count += coverage_result

    # Lighthouse
    error_count += check_lighthouse(verbose, lighthouse, clear_reports, variables_passed)

    # Sentry SDK
    error_count += check_sentry()

    # *** RESULT ***
    end_at = datetime.datetime.now()
    duration = end_at - start_at

    print_header('Result')
    print_default(f'Problems found: {error_count}\n')
    print_default(f'End at: {end_at}\n')
    print_default(f'Duration: {duration}\n')
    if coverage_value != -1:
        print_default(f'Test coverage: {coverage_value}%\n')
    print_empty()
    if error_count > 0:
        exit(1)
