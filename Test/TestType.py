from enum import Enum

class TestType(str, Enum):
    TESTEM = "testem"

TEST_LIST = [t.value for t in TestType]
