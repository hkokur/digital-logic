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


def convert_imm(immediate, width):
    immediate_width = width
    result = ""
    if int(immediate) >= 0:
        result += bin(int(immediate))[2:].zfill(width)
    else:
        # negative value
        result += (
            immediate_width - len(generate_negative(int(immediate)))
        ) * "1" + generate_negative(int(immediate))
    return result


def convert_ADD_ADDI_AND_ANDI_NAND_NOR(instruction: str) -> str:
    # get the operation
    operation = get_operation(instruction)
    result = ""
    # set the operation opcodes
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
        result += convert_imm(registers[2], 6)
    else:
        registers = get_registers(instruction)
        result += convert_register(registers[0])
        result += convert_register(registers[1])
        result += convert_register(registers[2])
        result += "00"
    # check the size
    return result


def convert_JE_JA_JB_JAE_JBE(instruction: str) -> str:
    operation = get_operation(instruction)
    result = ""
    # set the operation opcdoes
    if operation == "JE":
        result += "1010"
    elif operation == "JA":
        result += "1011"
    elif operation == "JB":
        result += "1100"
    elif operation == "JAE":
        result += "1101"
    elif operation == "JBE":
        result += "1110"

    value = get_registers(instruction)[0]
    result += convert_imm(value, 10)
    result += "0000"
    return result


def convert_LD_ST(instruction: str) -> str:
    operation = get_operation(instruction)
    result = ""
    if operation == "LD":
        result += "0111"
    elif operation == "ST":
        result += "1000"

    registers = get_registers(instruction)
    result += convert_register(registers[0])
    result += convert_imm(registers[1], 10)
    return result


def convert_JUMP(instruction: str) -> str:
    result = "0110"
    registers = get_registers(instruction)
    result += convert_imm(registers[0], 10)
    result += "0000"
    return result


def convert_CMP(instruction: str) -> str:
    result = "1001"
    registers = get_registers(instruction)
    # can it be immediate value??
    result += convert_register(registers[0])
    result += convert_register(registers[1])
    result += "000000"
    return result


output_file = open("output.txt", "w")
output_file.write("v2.0 raw\n")

for line in read_file("input.txt"):
    line_result = ""
    if line.startswith("A") or line.startswith("N"):
        line_result = convert_ADD_ADDI_AND_ANDI_NAND_NOR(line)
    elif line.startswith("J") and not line.startswith("JUMP"):
        line_result = convert_JE_JA_JB_JAE_JBE(line)
    elif line.startswith("L") or line.startswith("S"):
        line_result = convert_LD_ST(line)
    elif line.startswith("JUMP"):
        line_result = convert_JUMP(line)
    elif line.startswith("C"):
        line_result = convert_CMP(line)
    double_zero = "00"
    line_result = line_result + double_zero
    hex_result = ""
    for i in range(0, len(line_result), 4):
        partial = line_result[i : i + 4]
        hex_result += hex(int(partial, 2))[2:]
    output_file.write(hex_result + "\n")
