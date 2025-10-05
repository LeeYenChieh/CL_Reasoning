from enum import Enum

class TestType(str, Enum):
    TESTEM = "testem"
    PRINTONE = "printone"

TEST_LIST = [t.value for t in TestType]
