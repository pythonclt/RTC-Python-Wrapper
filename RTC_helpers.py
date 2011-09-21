"""
Simple file to hold help and __doc__ string text related to the
RTC python library.
"""

BILL_HELPER = """
Example http query:
     bills.json...bill_id=hr-3-112&sections=passage_votes.voted_at

    fields ===>
        bill_id, bill_type, number, session, chamber, short_title,
        official_title, popular_title, titles, summary, sponsor_id, sponsor,
        cosponsor_ids, cosponsors, committee_ids, committees, amendment_ids,
        amendments, amendments_count, keywords, actions, last_action,
        last_action_at, passage_votes, passage_votes_count,
        last_passage_vote_at, related_bills, introduced_at,
        senate_passage_result, senate_passage_result_at, house_passage_result,
        house_passage_result_at, awaiting_signature, awaiting_signiture_since,
        vetoed, vetoed_at, senate_override_result, senate_override_result_at,
        house_override_result, house_override_result_at, enacted, enacted_at
    actions ===>
        ::text-> describes action
        ::acted_at-> timestamp,
        ::type-> type of action such as 'action, vote2, signed'
    passage_votes ===>
        ::result-> pass or fail
        ::voted_at-> when vote occurred
        ::passage_type-> what this vote signifies (eg: "vote", "pingpong")
        ::text-> describes vote
        ::how-> How the vote was taken. Can be "roll" if it was a roll call
                vote, or one of several forms indicating a voice vote or
                unanimous consent.
        ::roll_id-> If the vote was a roll call vote, associated roll call ID.
        ::chamber->Chamber the vote took place in. Either "house" or "senate".
    committees ==>  A hash, keyed by committee ID, relating some basic
                    information about the committee to what roles the committee
                    had in relation to the bill.
        ::activity-> An array of activities this committee has in relation to
                     this bill.
        ::committee-> Basic information about the committee.
        """
BILL_DEFAULT_SECTIONS = ('bill_type',
                         'last_action',
                         'number',
                         'sponsor_id',
                         'vetoed',
                         'cosponsors_count',
                         'enacted',
                         'last_action_at',
                         'senate_result_at',
                         'short_title',
                         'amendments_count',
                         'code',
                         'house_result_at',
                         'last_vote_at',
                         'passage_vote_count',
                         'session',
                         'official_title',
                         'introduced_at',
                         'sponsor',
                         'awaiting_signature',
                         'enacted_at',
                         'house_result',
                         'senate_result',
                         'summary',
                         'cosponsor_ids',
                         'popular_title',
                         'amendment_ids',
                         'bill_id',
                         'chamber',
                         'keywords')

VIDEO_HELPER = """
        EXAMPLE:

         """
AMENDMENTS_HELPER = """
Example http query:
    amendments.json...amendment_id=s626-112

    fields ===>
        sponsor_id, number, actions, last_action_at, sponsor_type, session,
        amendment_id, sponsor, title, district, nickname, bioguide_id,
        last_name, name_suffix,  govtrack_id, party, first_name, chamber,
        state, bill, abbreviated, awaiting_signature, bill_id, bill_type,
        chamber, code, cosponsors_count, enacted, house_passage_result,
        house_passage_result_at, introduced_at, last_action_at,
        last_passage_vote_at, last_version_on, number, official_title,
        passage_votes_count, popular_title, session, short_title,
        sponsor_id, vetoed
    sponsor ===>
        ::title->
        ::district->
        ::nickname->
        ::bioguide_id->
        ::last_name->
        ::name_suffix->
        ::govtrack_id->
        ::party->
        ::first_name->
        ::chamber->
        ::state->
    bill ===>
        ::abbreviated->
        ::awaiting_signature->
        ::bill_id->
        ::bill_type->
        ::chamber->
        ::code->
        ::cosponsors_count->
        ::enacted->
        ::house_passage_result->
        ::house_passage_result_at->
        ::introduced_at->
        ::last_action_at->
        ::last_passage_vote_at->
        ::last_version_on->
        ::number->
        ::official_title->
        ::passage_votes_count->
        ::popular_title->
        ::session->
        ::short_title->
        ::sponsor_id->
        ::vetoed->
        """

AMENDMENT_DEFAULT_SECTIONS = ( 'sponsor_id',
                               'number',
                               'actions',
                               'last_action_at',
                               'sponsor_type',
                               'session',
                               'amendment_id',
                               'sponsor',
                               'offered_at',
                               'bill_id',
                               'state',
                               'chamber',
                               'purpose')
