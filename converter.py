import os


def read_file(path):
    with open(path, "r") as f:
        lines_list = f.readlines()
        lines_list = [line.strip() for line in lines_list]
        return lines_list


print(read_file("input.txt"))
