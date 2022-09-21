import project

def test_getDatetest():
    assert project.getDate("TEST", 1658637000000, 1659007800000) == "July, 24 2022 to July, 28 2022"

def test_getDateodi():
    assert project.getDate("ODI", 1660640400000, 1660669200000) == "Tuesday - August, 16 2022"

def test_getDatet20():
    assert project.getDate("T20", 1660640400000, 1660669200000) == "Tuesday - August, 16 2022"