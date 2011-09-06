"""
Python library for interacting with the Sunlight Labs
Real Time Congress API.
"""

__author__ = "Matt Johnson"
__copyright__ = "Copyright 2011, RTC Python Library Project"
__credits__ = ["James Turk - used his previous code as a guide"]
__license__ = "BSD"
__maintainer__ = "Matt Johnson"
__email__ = "johnson.matthew.h@gmail.com"
__status__ = "Development"


from pprint import pprint
import sys
import warnings
if sys.version_info[0] == 3:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import HTTPError
else:
    from urllib import urlencode
    from urllib2 import urlopen
    from urllib2 import HTTPError

try:
    import json
except ImportError:
    import simplejson as json

import RTC_helpers  # includes class doc strings etc.

API_KEY = None


def dict2obj(d):
    """ convenient conversion function found on stackoverflow.com
    posted by Roberto Liffredo"""
    if isinstance(d, dict):
        n = {}
        for item in d:
            if isinstance(d[item], dict):
                n[item] = dict2obj(d[item])
            elif isinstance(d[item], (list, tuple)):
                n[item] = [dict2obj(elem) for elem in d[item]]
            else:
                n[item] = d[item]
        return type('dict2obj', (object,), n)
        # create new object from dict or nested dictionary
    elif isinstance(d, (list, tuple,)):
        l = []
        for item in d:
            l.append(dict2obj(item))
        return l
    else:
        return d


class SunlightApiObject(object):
    def __init__(self, d):
        self.__dict__.update(d)

    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]

    def __repr__(self):
        pretty_dictionary = pprint(self.__dict__)
        return '%s(%r)' % (self.__class__.__name__, pretty_dictionary)


class Error(Exception):
    """Class place holder for errors"""


class rtc(object):
    @classmethod
    def get(self, func, params={}, sections='', make_obj=True):
        if API_KEY is None:
            raise Error("An API key is required")
        url = 'http://api.realtimecongress.org/api/v1/%s.json?apikey=%s&%s' %\
            (func, API_KEY, urlencode(params))
        # add the sections parameter to the url if passed as an argument
        if not(sections == ''):
            urlized_sections = ','.join([arg for arg in sections])
            url += '&sections=' + urlized_sections
        print url  # temporary - used for debugging purposes
        try:
            response = unicode(urlopen(url).read(), 'utf8').decode()
            dictionary = json.loads(response)
            if make_obj == True:
                generated_obj = dict2obj(dictionary)  # creates nested objects
                result = SunlightApiObject(generated_obj.__dict__)
            else:
                result = SunlightApiObject(dictionary)
            return result

        except HTTPError, e:
            raise Error(e.read())
        except (ValueError, KeyError), e:
            raise Error('Invalid Response')


class Bill(rtc):
    """
        Usage:
            sections = ('bill_id', 'sponsor', 'committees')
            result = Bill.get_bill(bill_id='hr3-112', sections=sections)
        Help on search fields and sub-field details: $print Bill.__help__
    """
    __help__ = RTC_helpers.BILL_HELPER

    @classmethod
    def bill_check(cls, bill_id, sections=('bill_id',), make_obj=False):
    # check if bill exists
        """
           checks to see if bill exists
           usage: exists = RTC.Bill.bill_check(bill_id)
           returns True if exists.
        """
        func = "bills"
        params = {'bill_id': bill_id}
        result = super(Bill, cls).get(func, params, sections, make_obj)

        try:
            bill = result.bills[0].get('bill_id')
            exists = True
        except IndexError:
            exists = False
        return exists

    @classmethod
    def get_bill(cls, bill_id, sections=RTC_helpers.BILL_DEFAULT_SECTIONS):
        func = "bills"
        params = {'bill_id': bill_id}
        result = super(Bill, cls).get(func, params, sections)
        bill = result.bills[0]
        return bill

    @classmethod
    def get_mult_bills(cls, bill_ids,
                       sections=RTC_helpers.BILL_DEFAULT_SECTIONS):
        """
        USE THIS IF REQUESTING MULTIPLE BILLS
        More efficient
        bills = RTC.get_mult_bills(bill_ids=('hr1-112', 's1-112'))
        """
        func = "bills"

        #builds string like 'hr1-112|hr2-112|hr2-112' for params
        bills = "|".join(bill_ids)
        
        params = {'bill_id__in': bills}
        result = super(Bill, cls).get(func, params, sections)
        bill_list = result.bills
        return bill_list

    @classmethod
    def actions(cls, bill_id, sections=('actions',)):
        """
        list of actions
            Attributes of each action: text, acted_at, and type
        """

        func = "bills"
        params = {'bill_id': bill_id}
        result = super(Bill, cls).get(func, params, sections)
        bill = result.bills[0]
        return [i for i in bill.actions]

    @classmethod
    def passage_votes(cls, bill_id, sections=('passage_votes',)):
        """
        list of passage votes
        Attributes of each passage_vote: result, passage_type, voted_at, text,
                                         how, roll_id, chamber
        """
        func = "bills"
        params = {'bill_id': bill_id}
        result = super(Bill, cls).get(func, params, sections)
        bill = result.bills[0]
        return [i for i in bill.passage_votes]

    @classmethod
    def committees(cls, bill_id, sections=('committees', 'committee_ids')):
        """
        returns a list of committee details & committee-specific
        activities related a bill
        Attributes of committee:
                activity (list)
                committee: name, committee_id, chamber
        """

        func = "bills"
        params = {'bill_id': bill_id}
        result = super(Bill, cls).get(func, params, sections)
        bill = result.bills[0]
        committees = bill.committees
        return bills.committees  # FIXME: TERRIBLE BUG HERE!!

    #FIXME: committee_ids are not indexed on some bill objects
    @classmethod
    def committee_ids(cls, bill_id, sections=('committee_ids',)):
        """ list of the committee ids """
        func = "bills"
        params = {'bill_id': bill_id}
        result = super(Bill, cls).get(func, params, sections)
        bill = result.bills[0]
        return committee_ids  # Committee ids are not returning!!!

    @classmethod
    def titles(cls, bill_id, sections=('titles',), make_obj=False):
        """
        list of bill's titles
            Attributes of each title: title, type, *type_as*
        """
        func = "bills"
        params = {"bill_id": bill_id}
        result = super(Bill, cls).get(func, params, sections, make_obj)
        bill = result.bills[0]
        for title in bill['titles']:
            value = title.get('as')
            title['type_as'] = value  # avoid keyword conflicts
        modified_result = dict2obj(bill['titles'])
        return modified_result

    @classmethod
    def related_bills(cls, bill_id, sections=('related_bills',),
                      make_obj=False):
        """
        returns list of related bills
        """
        func = "bills"
        params = {"bill_id": bill_id}
        response = super(Bill, cls).get(func, params, sections, make_obj)
        try:
            related_bills = response.bills[0].get('related_bills')
            related_types = related_bills.keys()
            bill_list = []
            for i in related_types:
                for value in related_bills[i]:
                    bill_list.append(value)
        except AttributeError:
            bill_list = []
        return bill_list

    @classmethod
    def amendments(cls, bill_id, sections=('amendments',)):
        """
        list of amendments
            Attributes of each amendment:
                sponsor_id, number, last_action_at, session,
                amendment_id, offered_at, description, state, purpose,
                chamber, bill_id
        """
        func = "bills"
        params = {"bill_id": bill_id}
        result = super(Bill, cls).get(func, params, sections)
        bill = result.bills[0]
        return [i for i in bill.amendments]

    @classmethod
    def cosponsors(cls, bill_id, sections=('cosponsors',)):
        """
        list of cosponsors
            Attributes of each cosponsor:
                title, nickname, district, bioguide_id, govtrack_id,
                last_name, name_suffix, party, first_name, state,
                chamber
        """
        func = "bills"
        params = {"bill_id": bill_id}
        result = super(Bill, cls).get(func, params, sections)
        bill = result.bills[0]
        return [i for i in bill.cosponsors]


class Votes(rtc):
    @classmethod
    def get_by_bill(cls, bill_id, sections=''):
        func = "votes"
        params = {'bill_id': bill_id}
        result = super(Votes, cls).get(func, params, sections)
        return result

class FloorUpdates(rtc):
    @classmethod
    def get_by_date(cls, legislative_day, sections=''):
        func = "floor_updates"
        params = {'legislative_day':legislative_day}
        result = super(FloorUpdates, cls).get(func, params, sections)
        return result.floor_updates 
  
    @classmethod   	
    def get_mult_dates(cls, legislative_days, sections=''):
        """
	Example: 
            date_list = ["08-29-2011", "08-30-2011"]	
            floor_updates = RTC.FloorUpdates.get_mult_dates(date_list)
	"""
        func = "floor_updates"
	query_string = "|".join(legislative_days)
	params = {'legislative_day__in':query_string}
	result = super(FloorUpdates, cls).get(func, params, sections)
	return result.floor_updates
    
    @classmethod
    def get_todays(cls, sections=''):
    	import datetime
    	now = datetime.datetime.now()
        legislative_day = now.strftime("%Y-%m-%d")	
        func = "floor_updates"
        params = {'legislative_day': legislative_day}
        result = super(FloorUpdates, cls).get(func, params, sections)
        return result.floor_updates
        
class Videos(rtc):
    """ Currently only supports house type videos """
    __help__ = RTC_helpers.VIDEO_HELPER

    def __str__(self):
        return self.clip_id

    @classmethod
    def get_by_bill(cls, bill_id, sections=('clip_urls', 'duration',
                                             'legislative_day', 'clip_id',
                                             'video_id', 'bills', 'clips')):
        func = "videos"
        params = {'clips.bills': bill_id}
        results = super(Videos, cls).get(func, params, sections)

        ### Only include clips from each video that contain bill_id ###
        clips = []
        for v in results.videos:
            for clip in v.clips:
                if hasattr(clip, 'bills') and bill_id in clip.bills:
                        clips.append(clip)
            v.clips = clips
        #################################################
        return results
