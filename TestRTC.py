try:
    import unittest2 as unittest
except:
    import unittest

import RTC


class SimplisticTest(unittest.TestCase):

    def test(self):
        self.failUnless(True)


class TestPreReqs(unittest.TestCase):

    def setUp(self):
        self.numbers = [23, 55, 4, 32]

    def test_expected(self):
        self.assertEqual(self.numbers[1] - self.numbers[0], self.numbers[3])


class TestRTC(unittest.TestCase):

    def setUp(self):
        RTC.API_KEY = 'c448541518f24d79b652ccc57b384815'
        self.bill_id = 'hr2-112'
        self.bills = RTC.Bill.get_mult_bills([self.bill_id], sections='')

    def test_bill_id(self):
        for i in self.bills:
            self.assertEqual(i.bill_id, self.bill_id)


if __name__ == '__main__':
    unittest.main()
