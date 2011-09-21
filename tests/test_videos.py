import RTC
bill_id = 'hr2-112'
RTC.apikey = 'c448541518f24d79b652ccc57b384815'
leg_name = 'Mr. Poe of TX'
def test_by_bill():
    results = RTC.Videos.get_by_bill(bill_id)
    assert len(results) != 0, 'We expect at least one video to be returned'
        
def test_by_legislator_name():
    
    results = RTC.Videos.get_legislator_name(leg_name)
    assert len(results) != 0, 'We expect at least one video to be returned'
    for r in results:
        assert leg_name in r['legislator_names'], 'Expecited name to be in legislator_names %s' % leg_name
        
