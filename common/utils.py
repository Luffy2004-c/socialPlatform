import re
from typing import Any


def parse_string(input_string: str) -> list[Any]:
    """
    用于解析输入字符串中的#标签
    """
    pattern = r"#(\w+)"
    results = re.findall(pattern, input_string)
    return results


if __name__ == "__main__":
    input_string = "这是一个# 测试#,例子"
    print(parse_string(input_string))
