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


def get_operation(instruction: str):
    return instruction.split(" ")[0]


def get_registers(instruction: str):
    return instruction.split(" ")[1].split(",")


# It returns the length of the bit representation of the number.
def find_max(num):
    val = 1
    num = -num
    length = 0
    while val < num:
        val *= 2
        length += 1
    return length + 1


def convert_int(negative_string):
    result = 0
    length = len(negative_string)
    for i in range(len(negative_string)):
        if i == 0:
            result = -pow(2, length - i - 1)
        elif negative_string[i] == "1":
            result += pow(2, length - i - 1)
    return result


# Negative decimal to binary converter
# For each iteration, current state of the binary number is calculated.
# Corresponding bits are swapped through 0 and 1 for each iteration.
def generate_negative(num):
    length = find_max(num)
    bit_representation = "1" + "0" * (length - 1)
    bit_representation = list(bit_representation)
    i = 1
    result = convert_int(bit_representation)
    for i in range(len(bit_representation)):
        if convert_int(bit_representation) < num:
            bit_representation[i] = "1"
        elif convert_int(bit_representation) > num:
            bit_representation[i - 1] = "0"
            bit_representation[i] = "1"
    return "".join(bit_representation)


def convert_imm(immediate):
    immediate_length = 6
    result = ""
    if int(immediate) >= 0:
        result += bin(int(immediate))[2:].zfill(6)
    else:
        # negative value
        result += (
            immediate_length - len(generate_negative(int(immediate)))
        ) * "1" + generate_negative(int(immediate))
    return result


def convert_ADD_ADDI_AND_ANDI_NAND_NOR(instruction):
    # get the operation
    operation = get_operation(instruction)
    result = ""
    if operation == "ADD":
        result += "0000"
    elif operation == "ADDI":
        result += "0001"
    elif operation == "AND":
        result += "0010"
    elif operation == "ANDI":
        result += "0011"
    elif operation == "NAND":
        result += "0100"
    elif operation == "NOR":
        result += "0101"

    if "I" in operation:
        registers = get_registers(instruction)
        result += convert_register(registers[0])
        result += convert_register(registers[1])
        result += convert_imm(registers[2])
    else:
        registers = get_registers(instruction)
        result += convert_register(registers[0])
        result += convert_register(registers[1])
        result += convert_register(registers[2])
        result += "00"
    # check the size
    return result


def convert_JUMP():
    pass


def convert_ST():
    pass


def convert_CMP():
    pass


def convert_JE():
    pass


def convert_JA():
    pass


def convert_JB():
    pass


l = read_file("input.txt")
print(convert_ADD_ADDI_AND_ANDI_NAND_NOR(l[1]))
