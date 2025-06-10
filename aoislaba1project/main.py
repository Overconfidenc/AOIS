class BinNumber:
    def __init__(self, number_list: list):
        self.number_list = number_list
        self.number="".join(str(digit) for digit in number_list)
    
    def __repr__(self):
        return (f"{self.number}, {self.number_list}")
    
    def list_in_string(self):
        return "".join(str(digit) for digit in self.number_list)
    
    def string_in_list(self):
        lis=[]
        for digit in self.number:
            lis.append(int(digit))
        return lis
    
    def translate_to_dex(self):
        dexnumber=0
        for digit in range(0,5):
            dexnumber = dexnumber + self.number_list[digit] * 2 ** digit
            print(dexnumber)
        return dexnumber

    
    def in_reverse_code (self):
        if self.number_list[0]==0:
            reversed_code=self
            return reversed_code
        else:
            lis=[]
            lis.append(self.number_list[0])
            for digit in range(1,len(self.number_list)):
                if (self.number_list[digit] == 0):
                    lis.append(1)
                else:
                    lis.append(0)
            reversed_code=BinNumber(lis)
            return reversed_code
    
    def number_plus_one(self):
        lis=self.number_list
        for digit in range(len(lis)-1,-1,-1):
            if lis[digit]==1:
                lis[digit]=0
            else:
                lis[digit]=1
                break
        return lis
        
    
    def in_add_code(self):
        if self.number_list[0]==0:
            add_code=self
            return add_code
        else:
            add_code=self.in_reverse_code()
            add_code.number_list=add_code.number_plus_one()
            add_code.number=add_code.list_in_string()
            return add_code

    @staticmethod    
    def sum_add_code(rty1:"BinNumber",rty2:"BinNumber"):
        rty3=[0] * 8
        carry = 0
    
        for i in range(7, -1, -1):
            total = rty1.number_list[i]+rty2.number_list[i]+carry
            rty3[i] = total % 2
            carry = total // 2
    
        return BinNumber(rty3)

def multiply(rty1:"BinNumber",rty2:"BinNumber"):
    """
    Умножает два числа в дополнительном коде.
    Возвращает результат в дополнительном коде.
    """
    rty3 = [0] * 8
    
    # Определяем знак результата
    sign = rty1.number_list[0] ^ rty2.number_list[0]  # XOR для определения знака
    
    # Работаем с модулями чисел
    if rty1.number_list[0] == 1:
        num1 = BinNumber.sum_add_code([1 if x == 0 else 0 for x in rty1], [0]*7 + [1])
    else:
        num1 = rty1.number_list.copy()
    
    if rty2[0] == 1:
        num2 = BinNumber.sum_add_code([1 if x == 0 else 0 for x in rty2], [0]*7 + [1])
    else:
        num2 = rty2.number_list.copy()
    
    num1.number_list = num1.number_list[1:]  # Убираем знаковый бит
    num2.number_list = num2.number_list[1:]  # Убираем знаковый бит
    
    # Основной цикл умножения
    for i in range(7, 0, -1):
        if num2.number_list[i-1] == 1:
            # Сдвигаем num1 на (7-i) позиций влево
            shifted = num1.number_list.copy()
            shifted.extend([0] * (7-i))
            shifted = shifted[-(7):]  # Берем последние 7 бит
            
            # Складываем с текущим результатом
            temp_result = [0] + rty3[1:]  # Без знакового бита
            sum_res = sum_add_code(temp_result, [0] + shifted)
            rty3 = sum_res
    
    # Добавляем знаковый бит
    rty3[0] = sign
    
    return rty3
    
        
    
class DexNumber:
    def __init__(self, number: int):
        self.number = number

    def __repr__(self):
        return (f"{self.number}")

    @staticmethod
    def input():
        dex_number=DexNumber(int(input("Enter DEX number: ")))
        return dex_number

    def translate_to_bin (self):
        if self.number == 0:
            bin_number=BinNumber([0,0,0,0,0,0])
        else:
            number=self.number
            lis=[]
            while (number/2) !=0:
                lis.append(int(number % 2))
                number=int(number/2)
            while len(lis) < 5:
                lis.append(0)
            if self.number < 0:
                lis.append(1)
            else:
                lis.append(0)
            lis.reverse()
            bin_number=BinNumber(lis)
        return bin_number

a=DexNumber.input()
binnumber=a.translate_to_bin()
dexnumber = binnumber.translate_to_dex()
print(repr(dexnumber))





