try:
    import unittest2 as unittest
except:
    import unittest

import RTC
from fake_request import alter_response

class TestBills(unittest.TestCase):
    def setUp(self):
        RTC.API_KEY = 'c448541518f24d79b652ccc57b384815'

    def test_multiple_bill_id(self):
        json_path = 'Bills/by_id.json'
        collection = RTC.Bill
        TestBill = alter_response(json_path, collection)

        self.bill_id = 'hr2-112'
        self.bills = TestBill.get_mult_bills([self.bill_id], sections='')
        for i in self.bills:
            self.assertEqual(i['bill_id'], self.bill_id)


if __name__ == '__main__':
    unittest.main()
