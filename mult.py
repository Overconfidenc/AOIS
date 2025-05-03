def decimal_to_binary(n):
    if n == 0:
        return '0'
    binary = ''
    n_abs = abs(n)
    while n_abs > 0:
        binary = str(n_abs % 2) + binary
        n_abs = n_abs // 2
    return binary

def binary_to_decimal(binary_str):
    decimal = 0
    for i, bit in enumerate(reversed(binary_str)):
        decimal += int(bit) * (1 << i)
    return decimal

def decimal_to_direct(n, bits):
    sign = '0' if n >= 0 else '1'
    abs_n = abs(n)
    bin_abs = decimal_to_binary(abs_n)
    if len(bin_abs) > bits - 1:
        bin_abs = bin_abs[-(bits-1):]
    else:
        bin_abs = bin_abs.zfill(bits - 1)
    return sign + bin_abs

def decimal_to_inverse(n, bits):
    direct = decimal_to_direct(n, bits)
    if n >= 0:
        return direct
    inverse = direct[0]
    for bit in direct[1:]:
        inverse += '0' if bit == '1' else '1'
    return inverse

def decimal_to_twos_complement(n, bits):
    mask = 1 << bits
    twos = (n + mask) & (mask - 1)
    twos_bin = decimal_to_binary(twos)
    return twos_bin.zfill(bits)

def twos_complement_to_decimal(binary_str):
    bits = len(binary_str)
    decimal = 0
    for i in range(bits):
        bit = int(binary_str[i])
        if i == 0:
            decimal += -bit * (1 << (bits - 1))
        else:
            decimal += bit * (1 << (bits - 1 - i))
    return decimal

def binary_addition(a_bin, b_bin):
    max_len = max(len(a_bin), len(b_bin))
    a = a_bin.zfill(max_len)
    b = b_bin.zfill(max_len)
    carry = 0
    result = []
    for i in range(max_len - 1, -1, -1):
        sum_bits = int(a[i]) + int(b[i]) + carry
        result.append(str(sum_bits % 2))
        carry = sum_bits // 2
    if carry:
        result.append('1')
    return ''.join(reversed(result))

def add_twos_complement(a_dec, b_dec, bits):
    a_bin = decimal_to_twos_complement(a_dec, bits)
    b_bin = decimal_to_twos_complement(b_dec, bits)
    sum_bin = binary_addition(a_bin, b_bin)
    sum_bin = sum_bin[-bits:] if len(sum_bin) > bits else sum_bin
    sum_dec = twos_complement_to_decimal(sum_bin)
    return sum_bin, sum_dec

def subtract_twos_complement(a_dec, b_dec, bits):
    return add_twos_complement(a_dec, -b_dec, bits)

def binary_multiplication(a_bin, b_bin):
    result = '0'
    a = a_bin.lstrip('0') or '0'
    b = b_bin.lstrip('0') or '0'
    for i in range(len(b)):
        bit = b[len(b) - 1 - i]
        if bit == '1':
            temp = a + '0' * i
            result = binary_addition(result, temp)
    return result

def multiply_direct(a_dec, b_dec, bits: int):
    sign = 0 if (a_dec >= 0) == (b_dec >= 0) else 1
    a_abs = abs(a_dec)
    b_abs = abs(b_dec)
    a_bin = decimal_to_binary(a_abs)
    b_bin = decimal_to_binary(b_abs)
    product_bin = binary_multiplication(a_bin, b_bin)
    product_dec = binary_to_decimal(product_bin)
    # Convert product_dec to binary and take the least significant bits to fit in bits-1
    product_bin = decimal_to_binary(abs(product_dec))
    # Ensure the magnitude fits in bits-1 bits
    if len(product_bin) > bits - 1:
        product_bin = product_bin[-(bits-1):]  # Truncate to fit
    else:
        product_bin = product_bin.zfill(bits - 1)  # Pad with zeros
    # Apply sign to decimal result
    if sign:
        product_dec = -product_dec
    # Form direct code: sign bit + magnitude
    direct_code = ('0' if sign == 0 else '1') + product_bin
    return direct_code, product_dec

def binary_division(dividend, divisor, precision=5):
    if divisor == 0:
        raise ValueError("Division by zero")
    int_part = dividend // divisor
    remainder = dividend % divisor
    int_bin = decimal_to_binary(int_part) if int_part != 0 else '0'
    frac_bin = []
    current = remainder
    for _ in range(precision):
        current *= 2
        if current >= divisor:
            frac_bin.append('1')
            current -= divisor
        else:
            frac_bin.append('0')
    frac_str = ''.join(frac_bin)
    binary = f"{int_bin}.{frac_str}"
    decimal = int_part + sum(int(bit) * (1.0 / (2 ** (i + 1))) for i, bit in enumerate(frac_str))
    return binary, decimal

def divide_direct(a_dec, b_dec, precision=5):
    if b_dec == 0:
        raise ValueError("Division by zero")
    sign = 0 if (a_dec >= 0) == (b_dec >= 0) else 1
    a_abs = abs(a_dec)
    b_abs = abs(b_dec)
    int_part = a_abs // b_abs
    remainder = a_abs % b_abs
    int_bin = decimal_to_binary(int_part) if int_part != 0 else '0'
    frac_bin = []
    current = remainder
    for _ in range(precision):
        current *= 2
        if current >= b_abs:
            frac_bin.append('1')
            current -= b_abs
        else:
            frac_bin.append('0')
    frac_str = ''.join(frac_bin)
    binary = ('1' if sign else '0') + f"{int_bin}.{frac_str}"
    decimal = (int_part + sum(int(bit) * (1.0 / (2 ** (i + 1))) for i, bit in enumerate(frac_str)))
    if sign:
        decimal = -decimal
    return binary, decimal

def float_to_ieee754(f):
    if f == 0.0:
        return '0' * 32
    sign = '0' if f >= 0 else '1'
    f_abs = abs(f)
    int_part = int(f_abs)
    frac_part = f_abs - int_part

    int_bin = decimal_to_binary(int_part)
    frac_bin = []
    while frac_part > 0 and len(frac_bin) < 23:
        frac_part *= 2
        if frac_part >= 1:
            frac_bin.append('1')
            frac_part -= 1
        else:
            frac_bin.append('0')
    full_bin = int_bin + '.' + ''.join(frac_bin)

    if '.' in full_bin:
        dot_pos = full_bin.index('.')
        first_one = full_bin.find('1')
        if first_one == -1:
            exponent = 0
            mantissa = '0' * 23
        else:
            if first_one < dot_pos:
                shift = dot_pos - first_one - 1
                exponent = shift + 127
                mantissa = (full_bin[first_one + 1:dot_pos] + full_bin[dot_pos + 1:]).ljust(23, '0')[:23]
            else:
                shift = first_one - dot_pos
                exponent = -shift + 127
                mantissa = full_bin[first_one + 1:].ljust(23, '0')[:23]
    else:
        shift = len(int_bin) - 1
        exponent = shift + 127
        mantissa = (int_bin[1:] + '0' * 23)[:23]
    exponent_bin = decimal_to_binary(exponent).zfill(8)[-8:]
    ieee754 = sign + exponent_bin + mantissa.ljust(23, '0')[:23]
    return ieee754.ljust(32, '0')[:32]

def ieee754_to_float(ieee_bin):
    if len(ieee_bin) != 32:
        return 0.0
    sign = -1 if ieee_bin[0] == '1' else 1
    exponent_bin = ieee_bin[1:9]
    mantissa_bin = ieee_bin[9:32]
    exponent = binary_to_decimal(exponent_bin) - 127
    if exponent_bin == '00000000':
        return 0.0
    mantissa = 1.0 if exponent != -127 else 0.0
    for i, bit in enumerate(mantissa_bin):
        mantissa += int(bit) * (1.0 / (2 ** (i + 1)))
    return sign * mantissa * (2 ** exponent)

def add_ieee754_bin(a_bin, b_bin):
    a = ieee754_to_float(a_bin)
    b = ieee754_to_float(b_bin)
    sum_float = a + b
    sum_bin = float_to_ieee754(sum_float)
    return sum_bin, sum_float

num = 5
bits = 8
print(f"Число {num}:")
print(f"Прямой код: {decimal_to_direct(num, bits)}")
print(f"Обратный код: {decimal_to_inverse(num, bits)}")
print(f"Дополнительный код: {decimal_to_twos_complement(num, bits)}")

a, b = 5, -3
sum_bin, sum_dec = add_twos_complement(a, b, bits)
print(f"\nCлoжeниe {a} и {b} в дополнительном коде:")
print(f"Двоичный: {sum_bin}, Десятичный: {sum_dec}")

a, b = 5, 3
mul_bin, mul_dec = multiply_direct(a, b, bits)
print(f"\nУмнoжeниe {a} и {b} в прямом коде:")
print(f"Двоичный: {mul_bin}, Десятичный: {mul_dec}")

a, b = 10, 3
div_bin, div_dec = divide_direct(a, b)
print(f"\nДеление {a} на {b} в прямом коде:")
print(f"Двоичный: {div_bin}, Десятичный: {div_dec:.5f}")

a_float, b_float = 1.5, 17.5
a_ieee = float_to_ieee754(a_float)
b_ieee = float_to_ieee754(b_float)
sum_ieee, sum_float = add_ieee754_bin(a_ieee, b_ieee)
print(f"\nСложение {a_float} и {b_float} в IEEE-754:")
print(f"Двоичный: {sum_ieee}, Десятичный: {sum_float}")