try:
    import unittest2 as unittest
except:
    import unittest
import RTC
from fake_request import alter_response

class TestDocuments(unittest.TestCase):
    def setUp(self):
        RTC.apikey = 'c448541518f24d79b652ccc57b384815'

    def test_documents_get_by_date(self):
        json_path = 'Documents/by_date.json'
        collection = RTC.Documents
        TestDocument = alter_response(json_path, collection)
        
        self.date = '2011-03-14'
        self.documents = TestDocument.get_by_date(self.date, sections='')
        assert len(self.documents) != 0, 'There should be at least 1 documents'
        import re #using regex because 'posted_at' field has timestamp format
        for i in self.documents:
            assert re.match(self.date, i['posted_at']), 'timestamp field for document should contain requested date'

