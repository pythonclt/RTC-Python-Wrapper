try:
    import unittest2 as unittest
except:
    import unittest
import RTC
from fake_request import alter_response

class TestCommitteeHearings(unittest.TestCase):
    def setUp(self):
        RTC.apikey = 'c448541518f24d79b652ccc57b384815'

    def test_committeehearings_search(self):
        json_path = 'CommitteeHearings/search.json'
        collection = RTC.CommitteeHearings
        TestCommitteeHearings = alter_response(json_path, collection)
        self.query = 'examine'
        self.committeehearings = TestCommitteeHearings.search(self.query, sections='')
        #self.documents = RTC.CommitteeHearings.search(self.query, sections='')
        assert len(self.committeehearings) != 0, 'There should be at least 1 result'
        #check that they all contain "examine"
        for i in self.committeehearings:
            assert self.query in i['description']
