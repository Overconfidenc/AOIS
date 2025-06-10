class BinNumber:
    def __init__(self, number_list: list):
        assert len(number_list) == 8, "Число должно быть 8-битным"
        self.number_list = number_list
        self.number = "".join(str(digit) for digit in number_list)
    
    def __repr__(self):
        return f"BinNumber({self.number})"
    
    def translate_to_dex(self):
        """Переводит 8-битное число в десятичное (учитывая доп. код)"""
        if self.number_list[0] == 0:  # Положительное
            return sum(bit * 2**(7-i) for i, bit in enumerate(self.number_list))
        else:  # Отрицательное
            return -(sum((1-bit) * 2**(7-i) for i, bit in enumerate(self.number_list))) - 1
    
    def multiply(self, other: 'BinNumber') -> 'BinNumber':
        """Умножение двух 8-битных чисел в доп. коде"""
        # Определяем знак результата
        sign = self.number_list[0] ^ other.number_list[0]
        
        # Получаем модули чисел
        abs1 = self if self.number_list[0] == 0 else self.invert().add_one()
        abs2 = other if other.number_list[0] == 0 else other.invert().add_one()
        
        # Умножаем модули
        result = [0] * 16  # Временный 16-битный результат
        for i in range(7, -1, -1):
            if abs2.number_list[i] == 1:
                # Складываем со сдвигом
                temp = [0] * 16
                for j in range(7, -1, -1):
                    pos = i + j + 1
                    temp[pos] += abs1.number_list[j]
                    if temp[pos] > 1:
                        temp[pos-1] += temp[pos] // 2
                        temp[pos] = temp[pos] % 2
                # Суммируем с результатом
                carry = 0
                for k in range(15, -1, -1):
                    total = result[k] + temp[k] + carry
                    result[k] = total % 2
                    carry = total // 2
        
        # Берем младшие 8 бит
        final_result = result[8:]
        
        return BinNumber(final_result)
    
    def invert(self) -> 'BinNumber':
        """Инвертирует все биты числа"""
        inverted = [1 if x == 0 else 0 for x in self.number_list]
        return BinNumber(inverted)
    
    def add_one(self) -> 'BinNumber':
        """Добавляет 1 к числу"""
        result = self.number_list.copy()
        carry = 1
        for i in range(7, -1, -1):
            total = result[i] + carry
            result[i] = total % 2
            carry = total // 2
        return BinNumber(result)
    
    @staticmethod
    def invert_bits(bits: list) -> list:
        return [1 if x == 0 else 0 for x in bits]
    
    @staticmethod
    def add_one_to_bits(bits: list) -> list:
        result = bits.copy()
        carry = 1
        for i in range(len(bits)-1, -1, -1):
            total = result[i] + carry
            result[i] = total % 2
            carry = total // 2
        return result


class DexNumber:
    def __init__(self, number: int):
        self.number = number
    
    def translate_to_bin(self) -> BinNumber:
        """Переводит десятичное число в 8-битное двоичное (в доп. коде)"""
        if -128 <= self.number <= 127:
            if self.number >= 0:
                binary = [int(x) for x in f"{self.number:08b}"]
                return BinNumber(binary)
            else:
                abs_bin = [int(x) for x in f"{abs(self.number):08b}"]
                inverted = [1 if x == 0 else 0 for x in abs_bin]
                return BinNumber(inverted).add_one()
        else:
            raise ValueError("Число вне диапазона 8-битного числа (-128..127)")

# Тестирование умножения 5 * (-3)
num1 = DexNumber(6).translate_to_bin()   # 00000101 (5)
num2 = DexNumber(-1).translate_to_bin()  # 11111101 (-3)
result = num1.multiply(num2)             # 11110001 (-15)
print(result.translate_to_dex())         # Выведет -15