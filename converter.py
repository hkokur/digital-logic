import os


def read_file(path: str) -> list:
    with open(path, "r") as f:
        lines_list = f.readlines()
        lines_list = [line.strip() for line in lines_list]
        return lines_list


def convert_register(register: str) -> str:
    register = register.replace("R", "")
    register = bin(int(register))[2:]
    register = register.zfill(4)
    return register


def convert_ADD(instruction: str) -> str:
    instruction = instruction.split(" ")
    result = ""
    if "I" in instruction[0]:
        instruction = instruction[1].split(",")
        result += "0001"
        result += convert_register(instruction[0])
        result += convert_register(instruction[1])
        # negative value problems
        if int(instruction[2]) >= 0:
            result += bin(int(instruction[2]))[2:].zfill(6)
        else:
            # negative value
            result += (6 - len(bin(int(instruction[2]))[2:])) * "1" + bin(
                int(instruction[2])
            )[2:]
    else:
        instruction = instruction[1].split(",")
        result += "0000"
        result += convert_register(instruction[0])
        result += convert_register(instruction[1])
        result += convert_register(instruction[2])
        result += "00"
    return result


l = read_file("input.txt")
convert_ADD(l[0])
