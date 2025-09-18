from enum import Enum

class TestType(str, Enum):
    TESTEM = "testEM"

    Test_LIST = [t.value for t in (TESTEM)]
