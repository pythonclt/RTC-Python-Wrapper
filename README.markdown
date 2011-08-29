RTC Python Library
==================
UPDATE 06-18-2011
------
Added a classmethod to query multiple bills in one request. This is very
efficient for cases that require iterations through a list of bill_ids.
Usage: 
<pre><code>
bill_list = ['hr1-112', 'hr2-112']
\#note: setting sections='', will request all sections for each bill
bills = RTC.get_mult_bills(bill_list, sections='') 
</pre></code>
See RTCtest.py for a full example.



Requirements
------------
python >= 2.6
unittest2

Example Usage
-------------
You can specify the sections you want to pull from the RESTful API.
<pre><code>
sections = ('bill_id', 'sponsor', 'committees')
bill = Bill.get_bill(bill_id='hr3-112', sections=sections)
print bill.sponsor_id
</pre></code>

Otherwise, it uses the default that's specified in the library.

<pre><code>
bill = RTC.Bill.get_bill(bill_id)
print bill.sponsor_id, bill.vetoed, bill.last_action.text
</pre></code>

See RTCtest.py for more examples usage.

Development Notes for Contributers
----------------------------------
- dict2obj is a function that coverts the json converted dictionary into a usable object. Since much of the RTC API's fields are not guaranteed, this may help avoid the extra coding for keyErrors.  Additionally, it is convenient to use dot notation instead of dictionaries.

###How to create class methods for collections
This is the basic structure:
<pre><code>
class Bill(rtc): #name of collection (eg: bills, videos, floor, updates)
    """  __doc_\_ string goes here """
    __help_\_ = RTC_helpers.BILL_HELPER #string created and imported from RTC_helpers.py   
    ...
    @classmethod
    def actions(cls, bill_id, sections=('actions',)): 
        """doc string goes here"""        
        #'sections' parameter above specifies what default sections to pull from a collection
        func = "bills"  #the collection were using (eg: bills.json)
        params = {'bill_id': bill_id}
        result = super(Bill, cls).get(func, params, sections)
        bill = result.bills[0]
        return [i for i in bill.actions]
</pre></code>
When writing a classmethod you can skip creating the obj and just return a dictionary instead.  Just specify 'make_obj=False' when declaring the classmethod parameters. 

<pre><code>
    ...
    @classmethod
    def titles(cls, bill_id, sections=('titles',), make_obj=False):
        ...
        response = super(Bill, cls).get(func, params, sections, make_obj) #remember to declare make_obj
        ...
    ...
</pre></code>
### Other comments
- It'd be helpful to enter helper text into the RTC_helpers.py after writing a new classmethod
- It'd be helpful to write a test function in RTCtest.py after writing a new classmethod
