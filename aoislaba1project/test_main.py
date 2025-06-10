import unittest
from mult import*

class TestBinaryConversions(unittest.TestCase):
    def test_decimal_to_binary(self):
        self.assertEqual(decimal_to_binary(0), '0')
        self.assertEqual(decimal_to_binary(5), '101')
        self.assertEqual(decimal_to_binary(10), '1010')
        self.assertEqual(decimal_to_binary(255), '11111111')

    def test_binary_to_decimal(self):
        self.assertEqual(binary_to_decimal('0'), 0)
        self.assertEqual(binary_to_decimal('101'), 5)
        self.assertEqual(binary_to_decimal('1010'), 10)
        self.assertEqual(binary_to_decimal('11111111'), 255)

    def test_decimal_to_direct(self):
        self.assertEqual(decimal_to_direct(5, 8), '00000101')
        self.assertEqual(decimal_to_direct(-5, 8), '10000101')
        self.assertEqual(decimal_to_direct(0, 8), '00000000')

    def test_decimal_to_inverse(self):
        self.assertEqual(decimal_to_inverse(5, 8), '00000101')
        self.assertEqual(decimal_to_inverse(-5, 8), '11111010')
        self.assertEqual(decimal_to_inverse(0, 8), '00000000')

    def test_decimal_to_twos_complement(self):
        self.assertEqual(decimal_to_twos_complement(5, 8), '00000101')
        self.assertEqual(decimal_to_twos_complement(-5, 8), '11111011')
        self.assertEqual(decimal_to_twos_complement(0, 8), '00000000')

class TestBinaryOperations(unittest.TestCase):
    def test_binary_addition(self):
        self.assertEqual(binary_addition('101', '110'), '1011')
        self.assertEqual(binary_addition('111', '1'), '1000')
        self.assertEqual(binary_addition('1', '1'), '10')

    def test_add_twos_complement(self):
        sum_bin, sum_dec = add_twos_complement(5, 3, 8)
        self.assertEqual(sum_bin, '00001000')
        self.assertEqual(sum_dec, 8)

        sum_bin, sum_dec = add_twos_complement(5, -3, 8)
        self.assertEqual(sum_bin, '00000010')
        self.assertEqual(sum_dec, 2)

    def test_subtract_twos_complement(self):
        sub_bin, sub_dec = subtract_twos_complement(5, 3, 8)
        self.assertEqual(sub_bin, '00000010')
        self.assertEqual(sub_dec, 2)

        sub_bin, sub_dec = subtract_twos_complement(5, -3, 8)
        self.assertEqual(sub_bin, '00001000')
        self.assertEqual(sub_dec, 8)

def test_multiply_direct(self):
    # Existing test for positive numbers
    mul_bin, mul_dec = multiply_direct(5, 3, 8)
    self.assertEqual(mul_bin, '00001111')
    self.assertEqual(mul_dec, 15)
    
    # New test for negative number
    mul_bin, mul_dec = multiply_direct(-5, 3, 8)
    self.assertEqual(mul_bin, '10001111')
    self.assertEqual(mul_dec, -15)

class TestFloatingPoint(unittest.TestCase):
    def test_float_to_ieee754(self):
        self.assertEqual(float_to_ieee754(0.0), '0' * 32)
        self.assertEqual(float_to_ieee754(1.0), '00111111100000000000000000000000')
        self.assertEqual(float_to_ieee754(-2.0), '11000000000000000000000000000000')

    def test_ieee754_to_float(self):
        self.assertEqual(ieee754_to_float('0' * 32), 0.0)
        self.assertAlmostEqual(ieee754_to_float('00111111100000000000000000000000'), 1.0)
        self.assertAlmostEqual(ieee754_to_float('11000000000000000000000000000000'), -2.0)

    def test_add_ieee754_bin(self):
        sum_bin, sum_float = add_ieee754_bin(
            '00111111100000000000000000000000', 
            '00111111000000000000000000000000'   
        )
        self.assertAlmostEqual(sum_float, 1.5)
        self.assertEqual(sum_bin, '00111111110000000000000000000000')

if __name__ == '__main__':
    unittest.main()