from enum import Enum

class TestType(str, Enum):
    TESTEM = "testEM"

TEST_LIST = [t.value for t in TestType]
