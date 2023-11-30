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
            result += (6 - len(bin(int(instruction[2]))[3:])) * "1" + bin(
                int(instruction[2])
            )[3:]
    else:
        instruction = instruction[1].split(",")
        result += "0000"
        result += convert_register(instruction[0])
        result += convert_register(instruction[1])
        result += convert_register(instruction[2])
        result += "00"
    return result


l = read_file("input.txt")
print(convert_ADD(l[1]))


# It returns the length of the bit representation of the number.
def find_max(num):
    val = 1
    num=-num
    length=0
    while val<num:
        val*=2
        length+=1
    return length+1


def convert_int(negative_string):
    result=0
    length = len(negative_string)
    for i in range(len(negative_string)):
        if i==0:
            result=-pow(2, length-i-1)
        elif negative_string[i]=="1":
            result+=pow(2, length-i-1)
    return result

# Negative decimal to binary converter
# For each iteration, current state of the binary number is calculated.
# Corresponding bits are swapped through 0 and 1 for each iteration.
def generate_negative(num):
    length=find_max(num)
    bit_representation="1"+"0"*(length-1)
    bit_representation=list(bit_representation)
    i=1
    result=convert_int(bit_representation)
    for i in range(len(bit_representation)):
        if convert_int(bit_representation)<num:
            bit_representation[i]="1"
        elif convert_int(bit_representation)>num:
            bit_representation[i-1]="0"
            bit_representation[i]="1"
    return "".join(bit_representation)



print(generate_negative(-25))

    
