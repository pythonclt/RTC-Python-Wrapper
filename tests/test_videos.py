import RTC
bill_id = 'hr2-112'
RTC.apikey = 'c448541518f24d79b652ccc57b384815'
leg_name = 'Mr. Poe of TX'
def test_by_bill():
    videos = RTC.Videos.get_by_bill(bill_id)
    assert len(videos) != 0, 'We expect at least one video to be returned'
    for v in videos:
        assert bill_id in v['bills'], 'The bill id that is being searched ' +\
                'for should be in list of bills that are returned'

    videos = RTC.Videos.get_by_bill('hrnotabill')
    assert len(videos) == 0, 'not bills should match this bill id'
        
def test_by_legislator_name():
    results = RTC.Videos.get_legislator_name(leg_name)
    assert len(results) != 0, 'We expect at least one video to be returned'
    for r in results:
        for c in r['clips']:
            assert leg_name in c['legislator_names'], 'Expecited name to ' +\
                    'be in legislator_names %s' % leg_name
        
    results = RTC.Videos.get_legislator_name('not a legislator name')
    assert len(results) == 0, 'there should be no legislators with this name'
