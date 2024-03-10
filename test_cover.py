import re

from cover import getTitle

def test_getTitle():
    assert getTitle("anything-123") == "anything-123"
    assert getTitle("anything+xxx-123") == "xxx-123"
    print(getTitle("050_3xplanet_NHDTA-618"))
    assert getTitle("050_3xplanet_NHDTA-618") == "NHDTA-618"
    assert getTitle("anything-xxx-123") == "xxx-123"
    assert getTitle("abc-456") == "abc-456"
    assert getTitle("no-number") == "no-number"
    assert getTitle("/++++uncen-cute-CWP-117") == "CWP-117"
    assert getTitle("heyzo_hd_0821_full") == "heyzo_hd_0821_full"

    
test_getTitle()