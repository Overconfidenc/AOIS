def decimal_to_binary(number: int):
    binary = []
    while number > 0:
        binary.append(str(number % 2))
        number = number // 2
    return ''.join(binary)[::-1].zfill(1)

def summarize_binary(number1: str, number2: str):
    max_length = max(len(number1), len(number2)) + 2
    number1 = number1.zfill(max_length)
    number2 = number2.zfill(max_length)
    binlist1 = list(number1)
    binlist2 = list(number2)
    binresult = []
    extra = 0
    for i in range(max_length - 1, -1, -1):
        subtotal = int(binlist1[i]) + int(binlist2[i]) + extra
        binresult.append(str(subtotal % 2))
        extra = subtotal // 2
    return ''.join(binresult)[::-1].lstrip('0')