import unittest
import math
from main import calculate_trig_function

class TestTrigonometricCalculator(unittest.TestCase):

    def test_1(self):
        result = calculate_trig_function('sin', 30, 'degrees', 4)
        self.assertEqual(result, 0.5)

    def test_2(self):
        result = calculate_trig_function('sin', -30, 'degrees', 4)
        self.assertEqual(result, -0.5)

    def test_3(self):
        result = calculate_trig_function('cos', 90, 'degrees', 4)
        self.assertEqual(result, 0)

    def test_4(self):
        result = calculate_trig_function('tan', 45, 'degrees', 4)
        self.assertEqual(result, 1)

    def test_5(self):
        result = calculate_trig_function('tan', 90, 'degrees', 4)
        self.assertTrue(isinstance(result, str))
        self.assertTrue('Ошибка' in result)

    def test_6(self):
        result = calculate_trig_function('asin', 2, 'radians', 4)
        self.assertTrue(isinstance(result, str))
        self.assertTrue('Ошибка' in result)

    def test_7(self):
        result = calculate_trig_function('cot', 45, 'degrees', 4)
        self.assertEqual(result, 1)

    def test_8(self):
        result = calculate_trig_function('atan', 1, 'degrees', 4)
        self.assertEqual(result, 45)

    def test_9(self):
        result = calculate_trig_function('atan', -1, 'degrees', 4)
        self.assertEqual(result, -45)

    def test_10(self):
        result = calculate_trig_function('acot', 1, 'degrees', 4)
        self.assertEqual(result, 45)

    def test_11(self):
        result = calculate_trig_function('sin', 30, 'degrees', 0)
        self.assertEqual(result, 0)

    def test_12(self):
        result = calculate_trig_function('sin', '0,5', 'radians', 4)
        self.assertAlmostEqual(result, math.sin(0.5), places=4)

    def test_13(self):
        result = calculate_trig_function('sin', 0.5, 'radians', 4)
        self.assertAlmostEqual(result, math.sin(0.5), places=4)

    def test_14(self):
        result = calculate_trig_function('sin', 'abc', 'radians', 4)
        self.assertTrue(isinstance(result, str))
        self.assertTrue('Ошибка' in result)

    def test_15(self):
        result = calculate_trig_function('sin', 720, 'degrees', 4)
        self.assertAlmostEqual(result, 0, places=4)

if __name__ == '__main__':
    unittest.main()