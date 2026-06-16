def get_matching_proposal_email(display_name: str, drop_title: str) -> str:
    return f"""
    Hello {display_name},
    
    Exciting news! We have found a candidate matching Circle for the Drop "{drop_title}".
    
    Please log into FirstCircle within the next 2 hours to accept or skip this group.
    Remember, matching proposals are blind - you will see shared interests and reliability scores, but profiles remain anonymized until everyone accepts!
    
    Best,
    The FirstCircle Team
    """

def get_confirmed_circle_email(display_name: str, circle_title: str, event_time: str, location: str) -> str:
    return f"""
    Hello {display_name},
    
    It's a Match! Everyone has accepted the proposal for "{circle_title}".
    
    Event Details:
    * Time: {event_time}
    * Location: {location}
    
    Go to your dashboard to unlock group chat and coordinate meetups!
    
    Best,
    The FirstCircle Team
    """
