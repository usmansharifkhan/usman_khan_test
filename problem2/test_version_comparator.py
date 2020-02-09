
from .version_comparator import VersionComparator


def test_version_comparator():
    version1 = VersionComparator('1.5')
    version2 = VersionComparator('1.7')
    version3 = VersionComparator('2.1')

    assert version1.compare(version2) == "1.5 is less than 1.7"
    assert version2.compare(version1) == "1.7 is greater than 1.5"
    assert version3.compare(version2) == "2.1 is greater than 1.7"
    assert version1.compare(version1) == "1.5 is equal to 1.5"