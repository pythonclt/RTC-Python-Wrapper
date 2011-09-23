RTC Python Wrapper Library
==========================

This is a Python wrapper for the [Sunlight Foundation's Real Time
Congress API](http://services.sunlightlabs.com/docs/Real_Time_Congress_API/).

Sunlight Labs takes government data and transforms it into services developers can use.  The Real Time Congress (RTC) API is a RESTful API over the artifacts of Congress, in as close to real-time as possible.

**WARNING**: This may create a more transparent government. If you don't want change then stop reading here. 

Requirements
------------
- python >= 2.6

List of Files
-------------
- README.markdown - you're reading it
- requirements.txt - list of required Python packages
- RTC_helpers.py - Simple file to hold help and __doc__ string text related to the RTC python library.
- RTC.py - Python library for interacting with the Sunlight Labs Real Time Congress API.
- tests/ - Folder containing all tests (files that start with 'test_')
  - RTCtest.py - File demonstrating some of the API usage.

Example Usage
-------------
You can specify the sections you want to pull from the RESTful API.
<pre><code>
sections = ('bill_id', 'sponsor', 'committees')
bill = Bill.get_bill(bill_id='hr3-112', sections=sections)
print bill['sponsor_id']
</pre></code>

Otherwise, it uses the default that's specified in the library.

<pre><code>
bill = RTC.Bill.get_bill(bill_id)
print bill['sponsor_id'], bill['vetoed'], bill['last_action']['text']
</pre></code>

See tests/RTCtest.py for more examples usage.

How to contribute
----------------------------------

- Fork the project.
- Read through the outstanding issues, or report new ones
  [here](https://github.com/pythonclt/RTC-Python-Wrapper/issues).
- Write some tests to make sure we don't accidentally break your
  code later. We've created a [test
  example](https://github.com/pythonclt/RTC-Python-Wrapper/blob/master/tests/test_example.py)
  for you.
- Enter helper text into the **RTC_helpers.py** after writing a new
  classmethod to help document what you've done.
- Send us a pull request.

###How to create class methods for collections
This is the basic structure:
<pre><code>
class Bill(RTC_Client): #name of collection (eg: bills, videos, floor, updates)
    """  __doc_\_ string goes here """
    __help_\_ = RTC_helpers.BILL_HELPER #string created and imported from RTC_helpers.py
    ...
    @classmethod
    def get_bill(cls, bill_id, make_obj=False, sections=RTC_helpers.BILL_DEFAULT_SECTIONS):
        endpoint = "bills.json"
        params = {'bill_id': bill_id}
        result = super(Bill, cls)._apicall(endpoint, sections, make_obj, **params)
        bill = result['bills'][0]
        return bill
</pre></code>


### Running tests
Make sure you have the **discover** package installed. It is included in our
**requirements.txt**, which you can install with this command:

<code>
$ pip install -r requirements.txt
</code>

Then, in the project directory you can run all the tests with:

<code>
$ python -m discover
</code>

You can run individual or grouped tests based on patterns:
<code>
$ python -m discover -p 'test_videos.py'
</code>

or 

<code>
$ python -m discover -p '*.py'
</code>

### Development Notes for Contributors
**dict2obj** is a function that coverts the json converted dictionary into a usable object. Since much of the RTC API's fields are not guaranteed, this may help avoid the extra coding for keyErrors.  Additionally, it is convenient to use dot notation instead of dictionaries.

