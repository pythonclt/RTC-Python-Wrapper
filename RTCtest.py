#!/usr/bin/python
"""
Simple test file to make sure each function is working.
Must be edited manually.
"""
import RTC
from pprint import *
bill_id = 'hr2-112'
RTC.API_KEY = 'c448541518f24d79b652ccc57b384815'


#bill tests
def bill():
    bill = RTC.Bill.get_bill(bill_id)
    print bill.sponsor_id, bill.vetoed, bill.last_action.text


def mult_bills():
    bills = RTC.Bill.get_mult_bills(['hr1-112', 'hr2-112', 'hr3-112'],
                                    sections='')
    for i in bills:
        for a in i.actions:
            print a.type, a.acted_at, a.text


def bill_actions():
    actions = RTC.Bill.actions(bill_id)
    for a in actions:
        print a.type, a.acted_at, a.text


def bill_passage_votes():
    passage_votes = RTC.Bill.passage_votes(bill_id)
    for i in passage_votes:
        print i.result, i.passage_type, i.voted_at, i.text, i.how, i.roll_id,\
            i.chamber


def bill_committees():  # Does not work!
    committees = RTC.Bill.committees(bill_id)
    for i in committees:
        print i


def bill_titles():
    titles = RTC.Bill.titles(bill_id)
    for i in titles:
        print i.title, i.type, i.type_as


def bill_amendments():
    amendments = RTC.Bill.amendments(bill_id)
    for i in amendments:
        print i.sponsor_id, i.number, i.last_action_at, i.session,\
            i.amendment_id, i.offered_at, i.description. i.state, i.purpose,\
            i.chamber, i.bill_id


def bill_related_bills():
    result = RTC.Bill.related_bills(bill_id)
    print result
    for i in result:
        print i


def bill_cosponsors():
    cosponsors = RTC.Bill.cosponsors(bill_id)
    for i in cosponsors:
        print i.district, i.bioguide_id, i.govtrack_id, i.last_name,\
            i.name_suffix, i.party, i.first_name, i.state, i.chamber,\
            i.title, i.nickname


# votes tests
def votes():
    votes = RTC.Votes.get_by_bill(bill_id)
    print dir(votes)

#floor_updates tests
def floor_updates():
    result = RTC.FloorUpdates.get_by_date('2011-09-02')
    for i in result:
        print "--------------------------------------"       
        print i.chamber, i.timestamp
        # These fields are not guaranteed:  i.bioguide_ids, i.roll_ids, i.bill_ids
        print "EVENTS:"        
        for e in i.events:
            print e
def get_mult_floor_updates():
    date_list = ['2011-09-02', '2011-09-01', '2011-08-31',
		 '2011-08-30', '2011-08-29']
    result = RTC.FloorUpdates.get_mult_dates(date_list)
    for i in result: print i.chamber, i.timestamp   

def todays_floor_updates():
    result = RTC.FloorUpdates.get_todays()
    for i in result: print i.chamber, i.timestamp




# video tests
def video_test():
    result = RTC.Videos.get_by_bill(bill_id)
    for v in result.videos:
        print "=== Legislative_Day:  %s | Video ID: %s  | Duration: %s" %\
            (v.legislative_day, v.clip_id, v.duration)
        print "This is the video URL for the video in the mp4 format: %s" %\
            v.clip_urls.hls
        for clip in v.clips:
            print "* offset: %s | duration: %s | summary: %s  " %\
                (clip.offset, clip.duration, clip.events[0])


todays_floor_updates()  # desired test function goes here
