from enum import Enum

class TestType(str, Enum):
    TESTEM = "testem"
    PRINTONE = "printone"
    TESTCASE = "testcase"

TEST_LIST = [t.value for t in TestType]
