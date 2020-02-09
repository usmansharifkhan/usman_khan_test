


class VersionComparator:
    def __init__(self, version):
        if not isinstance(version, str):
            raise TypeError("version needs to be a string")

        splitted_version_string = version.split(".")

        if len(splitted_version_string) != 2:
            raise ValueError("Malformed version string, one one dot is accepted ")
        self._version_string = version
        self._former = splitted_version_string[0]
        self._latter = splitted_version_string[1]

    def get_former(self):
        return self._former

    def get_latter(self):
        return self._latter

    def get_version_str(self):
        return self._version_string

    def compare(self, version_object):
        if self._former > version_object.get_former():
            return '{} is greater than {}'.format(self._version_string, version_object.get_version_str())
        elif self._former < version_object.get_former():
            return '{} is less than {}'.format(self._version_string, version_object.get_version_str())
        else:
            if self._latter > version_object.get_latter():
                return '{} is greater than {}'.format(self._version_string, version_object.get_version_str())
            elif self._latter < version_object.get_latter():
                return '{} is less than {}'.format(self._version_string, version_object.get_version_str())
            else:
                return '{} is equal to {}'.format(self._version_string, version_object.get_version_str())