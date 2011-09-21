"""
Python library for interacting with the Sunlight Labs
Real Time Congress API.
"""

__author__ = "Matt Johnson"
__copyright__ = "Copyright 2011, RTC Python Library Project"
__credits__ = ["James Turk - helped with getting us started"]
__license__ = "BSD"
__maintainer__ = "Matt Johnson"
__email__ = "johnson.matthew.h@gmail.com"
__status__ = "Development"

import sys
import json
import datetime
from pprint import pprint

if sys.version_info[0] == 3:
    from urllib.parse import urlencode, urljoin
    from urllib.request import urlopen
    from urllib.error import HTTPError
else:
    from urllib import urlencode
    from urlparse import urljoin
    from urllib2 import HTTPError, urlopen

import RTC_helpers  # includes class doc strings etc.


apikey = None

#apikey backwards-compatibility for previous development users
API_KEY = None


def dict2obj(d):
    """ convenient conversion endpointtion found on stackoverflow.com
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


class BaseClient(object):
    def __init__(self):
        pass

    @classmethod
    def _apicall(self, endpoint, sections='', make_obj=False, **kwargs):
        if not apikey:
            raise Exception('API key must be set')


        kwargs['apikey'] = apikey
        if not(sections == ''):
            kwargs['sections'] = ','.join([arg for arg in sections])

        url = "{0}?{1}".format(urljoin(self.base_url, endpoint),
                               urlencode(kwargs, doseq=True))
        print url
        try:
            response = urlopen(url).read().decode('utf-8')
            if make_obj == True:
                generated_obj = dict2obj(json.loads(response))  # creates nested objects
                return SunlightApiObject(generated_obj.__dict__)
            else:
                return json.loads(response)

        except HTTPError as e:
            raise
        except (ValueError, KeyError) as e:
            raise




class Error(Exception):
    """Class place holder for errors"""

class RTC_Client(BaseClient):
    base_url = 'http://api.realtimecongress.org/api/v1/'

class Bill(RTC_Client):
    """
        Usage:
            sections = ('bill_id', 'sponsor', 'committees')
            result = Bill.get_bill(bill_id='hr3-112', sections=sections)
        Help on search fields and sub-field details: $print Bill.__help__
    """
    __help__ = RTC_helpers.BILL_HELPER

    @classmethod
    def bill_check(cls, bill_id, make_obj=False, sections=('bill_id',),):
    # check if bill exists
        """
           checks to see if bill exists
           usage: exists = RTC.Bill.bill_check(bill_id)
           returns True if exists.
        """
        endpoint = "bills.json"
        params = {'bill_id': bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)

        try:
            bill = result['bills[0]']['bill_id']
            exists = True
        except IndexError:
            exists = False
        return exists


    @classmethod
    def get_bill(cls, bill_id, make_obj=False, sections=RTC_helpers.BILL_DEFAULT_SECTIONS):
        endpoint = "bills.json"
        params = {'bill_id': bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill = result['bills'][0]
        return bill

    @classmethod
    def get_mult_bills(cls, bill_ids, make_obj=False,
                       sections=RTC_helpers.BILL_DEFAULT_SECTIONS):
        """
        USE THIS IF REQUESTING MULTIPLE BILLS
        More efficient
        bills = RTC.get_mult_bills(bill_ids=('hr1-112', 's1-112'))
        """
        endpoint = "bills.json"

        #builds string like 'hr1-112|hr2-112|hr2-112' for params
        bills = "|".join(bill_ids)

        params = {'bill_id__in': bills}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill_list = result['bills']
        return bill_list

    @classmethod
    def actions(cls, bill_id, make_obj=False, sections=('actions',)):
        """
        list of actions
            Attributes of each action: text, acted_at, and type
        """

        endpoint = "bills.json"
        params = {'bill_id': bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill = result['bills'][0]
        return [i for i in bill.actions]

    @classmethod
    def passage_votes(cls, bill_id, make_obj=False, sections=('passage_votes',)):
        """
        list of passage votes
        Attributes of each passage_vote: result, passage_type, voted_at, text,
                                         how, roll_id, chamber
        """
        endpoint = "bills.json"
        params = {'bill_id': bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill = result['bills'][0]
        return [i for i in bill.passage_votes]

    @classmethod
    def committees(cls, bill_id, make_obj=False, sections=('committees', 'committee_ids')):
        """
        returns a list of committee details & committee-specific
        activities related a bill
        Attributes of committee:
                activity (list)
                committee: name, committee_id, chamber
        """

        endpoint = "bills.json"
        params = {'bill_id': bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill = result['bills'][0]
        return bill['committees']  # FIXME: TERRIBLE BUG HERE!!

    #FIXME: committee_ids are not indexed on some bill objects
    @classmethod
    def committee_ids(cls, bill_id, make_obj=False, sections=('committee_ids',)):
        """ list of the committee ids """
        endpoint = "bills.json"
        params = {'bill_id': bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill = result['bills'][0]
        return committee_ids  # Committee ids are not returning!!!

    @classmethod
    def titles(cls, bill_id, make_obj=False, sections=('titles',),):
        """
        list of bill's titles
            Attributes of each title: title, type, *type_as*
        """
        endpoint = "bills.json"
        params = {"bill_id": bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill = result['bills'][0]
        for title in bill['titles']:
            value = title['as']
            title['type_as'] = value  # avoid keyword conflicts
        modified_result = dict2obj(bill['titles'])
        return modified_result

    @classmethod
    def related_bills(cls, bill_id, sections=('related_bills',),
                      make_obj=False):
        """
        returns list of related bills
        """
        endpoint = "bills.json"
        params = {"bill_id": bill_id}
        response = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        try:
            related_bills = response['bills'][0]['related_bills']
            bill_list = []
            for i in related_bills:
                for value in related_bills[i]:
                    bill_list.append(value)
        except AttributeError:
            bill_list = []
        return bill_list

    @classmethod
    def amendments(cls, bill_id, make_obj=False, sections=('amendments',)):
        """
        list of amendments
            Attributes of each amendment:
                sponsor_id, number, last_action_at, session,
                amendment_id, offered_at, description, state, purpose,
                chamber, bill_id
        """
        endpoint = "bills.json"
        params = {"bill_id": bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill = result['bills'][0]
        return [i for i in bill.amendments]

    @classmethod
    def cosponsors(cls, bill_id, make_obj=False, sections=('cosponsors',)):
        """
        list of cosponsors
            Attributes of each cosponsor:
                title, nickname, district, bioguide_id, govtrack_id,
                last_name, name_suffix, party, first_name, state,
                chamber
        """
        endpoint = "bills.json"
        params = {"bill_id": bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill = result['bills'][0]
        return [i for i in bill.cosponsors]


class Votes(RTC_Client):
    @classmethod
    def get_by_bill(cls, bill_id, make_obj=False, sections=''):
        endpoint = "votes.json"
        params = {'bill_id': bill_id}
        result = super(Votes, cls)._apicall(endpoint, sections, make_obj, **params)
        return result

class FloorUpdates(RTC_Client):
    @classmethod
    def search(cls, query, make_obj=False, sections=''):
        endpoint = "floor_updates.json"
        params = {'search':query}
        result = super(FloorUpdates, cls)._apicall(endpoint, sections, make_obj, **params)
        return result['floor_updates']
    @classmethod
    def get_by_date(cls, legislative_day, make_obj=False, sections=''):
        endpoint = "floor_updates.json"
        params = {'legislative_day':legislative_day}
        result = super(FloorUpdates, cls)._apicall(endpoint, sections, make_obj, **params)
        return result['floor_updates'] 
  
    @classmethod   	
    def get_mult_dates(cls, legislative_days, make_obj=False, sections=''):
        """
        Example: 
            date_list = ["08-29-2011", "08-30-2011"]	
            floor_updates = RTC.FloorUpdates.get_mult_dates(date_list)
        """
        endpoint = "floor_updates.json"
        query_string = "|".join(legislative_days)
        params = {'legislative_day__in':query_string}
        result = super(FloorUpdates, cls)._apicall(endpoint, sections, make_obj, **params)
        return result.floor_updates

    @classmethod
    def get_todays(cls, make_obj=True, sections=''):
        import datetime
        now = datetime.datetime.now()
        legislative_day = now.strftime("%Y-%m-%d")	
        endpoint = "floor_updates.json"
        params = {'legislative_day': legislative_day}
        result = super(FloorUpdates, cls)._apicall(endpoint, sections, make_obj, **params)
        return result['floor_updates']
        
class Videos(RTC_Client):
    """ Currently only supports house type videos """
    __help__ = RTC_helpers.VIDEO_HELPER

    def __str__(self):
        return self.clip_id

    @classmethod
    def get_by_bill(cls, bill_id, make_obj=False, sections=('clip_urls', 'duration',
                                             'legislative_day', 'clip_id',
                                             'video_id', 'bills', 'clips')):
        endpoint = "videos.json"
        params = {'clips.bills': bill_id}
        results = super(Videos, cls)._apicall(endpoint, sections, make_obj, **params)
        ### Only include clips from each video that contain bill_id ###
        clips = []
        for v in results['videos']:
            print(v)
            if v.has_key('bills') and bill_id in v['bills']:
                for clip in v['clips']: 
                    clips.append(clip)
            v['clips'] = clips
        #################################################
        return clips

    @classmethod
    def get_legislator_name(cls, name, make_obj=False, sections=('clip_urls', 'duration',
                                                           'legislative_day', 'clip_id',
                                                           'video_id', 'bills', 'clips')):
        endpoint = "videos.json"
        params = {'clips.legislator_names': name}
        results = super(Videos, cls)._apicall(endpoint, sections, make_obj, **params)
        ### Only include clips from each video that contain bill_id ###
        clips = []
        for v in results['videos']:
            for clip in v['clips']: 
                if clip.has_key('legislator_names') and name in clip['legislator_names']:
                    clips.append(clip)
            v['clips'] = clips
        #################################################
        return clips

    @classmethod
    def get_legislator_name(cls, bioguide_id, make_obj=False, sections=('clip_urls', 'duration',
                                                           'legislative_day', 'clip_id',
                                                           'video_id', 'bills', 'clips')):
        endpoint = "videos.json"
        params = {'clips.bioguide_ids': name}
        results = super(Videos, cls)._apicall(endpoint, sections, make_obj, **params)
        ### Only include clips from each video that contain bill_id ###
        clips = []
        for v in results['videos']:
            for clip in v['clips']: 
                if clip.has_key('legislator_names') and name in clip['legislator_names']:
                    clips.append(clip)
            v['clips'] = clips
        #################################################
        return clips
class Amendments(RTC_Client):
    """ 
    Represents the amendments collection, which holds all amendments 
    to bills and resolutions offered in Congress.

    Amendments IDs are a combination of the chamber, the amendment number, and the 
    session of Congress an amendment was offered in. They are of the format:

    [chamber][number]-[session]

    For example, Senate amendment no. 4850 from the 111th Congress would be "s4850-111".
    
    All fields are guaranteed.

    """

    @classmethod
    def get_amendment(cls, amendment_id, make_obj=False, sections=RTC_helpers.AMENDMENTS_DEFAULT_SECTIONS):
        endpoint = "amendments.json"
        params = {'amendment_id': amendment_id}
        result = super(Amendments, cls)._apicall(endpoint, sections, make_obj, **params)
        amendment = result.amendments[0]
        return amendment 

    @classmethod
    def get_mult_amendments(cls, amendment_ids, make_obj=False,
                       sections=RTC_helpers.AMENDMENT_DEFAULT_SECTIONS):
        endpoint = "amendments.json"

        amendments = "|".join(amendment_ids)
        
        params = {'amendment_id__in': amendments}
        result = super(Amendments, cls)._apicall(endpoint, sections, make_obj, **params)
        amendment_list = result.amendments
        return amendment_list
