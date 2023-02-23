import os
import keyword
import argparse
from tabulate import tabulate

# create ArgumentParser object
parser = argparse.ArgumentParser(description="Python Keyword Counter")

# add arguments
parser.add_argument('-f', '--file', required=True, help='Path of the Python file to be analyzed')

# parse arguments
args = parser.parse_args()

# open the python file in read mode
file = open(args.file, "r")
keyword_counts = {}

for line in file:
    words = line.split()
    for word in words:
        if keyword.iskeyword(word):
            if word in keyword_counts:
                keyword_counts[word] += 1
            else:
                keyword_counts[word] = 1

file.close()

# print the keyword counts in table format
os.system("clear")
print(tabulate(keyword_counts.items(), headers=["Keyword", "Count"], tablefmt="grid"))
