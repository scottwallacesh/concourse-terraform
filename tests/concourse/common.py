# stdlib
import tempfile

# =============================================================================
#
# constants
#
# =============================================================================

TEST_TERRAFORM_DIR = '/opt/resource/testdata/terraform'
TEST_ROOT_DIR = '/opt/resource'
RELATIVE_TEST_TERRAFORM_DIR = 'testdata/terraform'


# =============================================================================
#
# test helpers
#
# =============================================================================

# =============================================================================
# create_test_working_dir
# =============================================================================
def create_test_working_dir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory()
