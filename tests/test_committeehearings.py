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
        #self.committeehearings = RTC.CommitteeHearings.search(self.query, sections='')
        self.assertNotEqual(len(self.committeehearings), 0, 'There should be at least 1 result')
        #check that they all contain "examine"
        for i in self.committeehearings:
            self.assertIn(self.query, i['description'])

    def test_committeehearings_get(self):
        json_path = 'CommitteeHearings/get.json'
        collection = RTC.CommitteeHearings
        TestCommitteeHearings = alter_response(json_path, collection)
        self.date = '2011-10-06'
        self.chamber = 'senate'
        self.committee_id = 'SSEV'
        self.query = 'uranium'
         
        self.committeehearings = TestCommitteeHearings.get(date=self.date, 
        chamber=self.chamber, committee_id=self.committee_id,
        search=self.query)

        self.assertNotEqual(len(self.committeehearings), 0, 'There should be at least 1 result')
        #self.committeehearings = RTC.CommitteeHearings.get(date=self.date, 
        #chamber=self.chamber, committee_id=self.committee_id,
        #search=self.query)
        #check that it contains the keyword arguments
        for i in self.committeehearings:
            self.assertIn(self.date, i['legislative_day'], 'Should have correct legi day')
            self.assertIn(self.chamber, i['chamber'], 'Should have correct chamber')
            self.assertIn(self.committee_id, i['committee_id'], 'Should have correct committee_id')
            self.assertIn(self.query, i['description'], 'Should have correct query in description field')
