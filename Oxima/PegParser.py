import sys
from parsimonious.exceptions import ParseError

__peg_parser__ = """
    start = (number / string)*
    number = [0-9]+
    string = "\"" char* "\""
    char = ~"[^\"]"
"""

def parse(text):
    try:
        return parse(start, text)
    except ParseError as e:
        print(f"Error parsing input: {e}", file=sys.stderr)
        return None

result = parse('123 "hello" 456 "world" 789')
if result is not None:
    print(result)
