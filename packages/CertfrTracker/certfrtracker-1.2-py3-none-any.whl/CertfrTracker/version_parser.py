from re import sub


def systems_filter(techno, json_version, line, verbose):
    """
    Returns a string containing either "Open" or "Applicable" depending on the level of confidence.
    checks if techno and version given in argument matches with the line argument.
    :param techno: str
    :param json_version: str
    :param line: str
    :param verbose: Bool
    :return: str or None
    """
    if verbose:
        print("ligne en traitement :", line)
        print("techno donnée ->", techno, " || version : ->", json_version, end="\n\n")

    cleared_line = sub(r"[^a-zA-Z0-9-.-é-à-è-ê-û-ï-ö-ë]", " ", line.lower())
    if cleared_line[-1:] == ".":  # sometimes the line could finish by a ".", so it can confuse the parsers
        cleared_line = cleared_line[:-1]

    all_check = [
        double_range_plus_extra(cleared_line, techno, json_version),
        perfect_match(cleared_line, techno, json_version),
        double_range_no_x(cleared_line, techno, json_version),
        range_x(cleared_line, techno, json_version),
        double_range_x(cleared_line, techno, json_version),
    ]

    for single_check in all_check:
        if single_check:
            return "Applicable"

    if techno in cleared_line:
        return "Open"


def range_x(cleared_line, techno, json_version) -> bool:
    """
    Returns a Bool by comparing the line with the techno and version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : Apache Log4j versions 2.x (versions obsolètes)
    :param techno: str
    :param json_version: str
    :return: bool
    """
    if ".x" in cleared_line and not all(x in cleared_line for x in ["antérieures", "à"]):
        version = ""
        for word in cleared_line.split():
            if ".x" in word:
                version = word

        # quit function if nothing detected
        if "" == version:
            return False

        if techno in cleared_line:
            dot_number = len(version.split(".")) - 1
            left_of_value = '.'.join(version.split(".")[0:-1])
            json_left_of_value = '.'.join(json_version.split(".")[0:dot_number])

            if left_of_value == json_left_of_value:
                return True
            elif len(version) > len(json_version) and version[0:len(json_version)] == json_version:
                return True
    return False


def double_range_no_x(cleared_line, techno, json_version) -> bool:
    """
    Returns a Bool by comparing the line with the techno and version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : vCenter Server versions 7.0 antérieures à 7.0 U2b
    :param techno: str
    :param json_version: str
    :return: bool
    """
    if (("antérieures à" in cleared_line) or ("à" in cleared_line and not "antérieures à" in cleared_line)) and (
            not ".x" in cleared_line):
        version1 = ""
        version2 = ""
        for word in cleared_line.split():
            if "." in word and version1 == "":
                version1 = word
            if "." in word and version2 == "" and word != version1 and version1 != "":
                version2 = word

        # quit function if nothing detected
        if "" in (version1, version2):
            return False

        if techno in cleared_line:
            json_version_as_array = Private.version_to_int_array(json_version)
            version1_as_array = Private.version_to_int_array(version1)
            version2_as_array = Private.version_to_int_array(version2)

            return Private.double_range_comparator(version1_as_array, version2_as_array, json_version_as_array, 0)
    return False


def double_range_x(cleared_line, techno, json_version) -> bool:
    """
    Returns a Bool by comparing the line with the techno and version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : Cloud Foundation (vCenter Server) versions 3.x antérieures à 3.10.2.1
    :param techno: str
    :param json_version: str
    :return: bool
    """
    if (("antérieures à" in cleared_line) or ("à" in cleared_line and not "antérieures à" in cleared_line)) and (
            ".x" in cleared_line):
        version1 = ""
        version2 = ""
        for word in cleared_line.split():
            if ".x" in word and version1 == "":
                version1 = word
            if "." in word and version2 == "" and word != version1 and version1 != "":
                version2 = word

        # quit function if nothing detected
        if "" in (version1, version2):
            return False

        if techno in cleared_line:
            dot_number = len(version1.split(".")) - 1
            left_of_value = '.'.join(version1.split(".")[0:-1])
            v1_sanitized = left_of_value + (".0" * (len(version2.split(".")) - dot_number))

            json_version_as_array = Private.version_to_int_array(json_version)
            version1_as_array = Private.version_to_int_array(v1_sanitized)
            version2_as_array = Private.version_to_int_array(version2)

            return Private.double_range_comparator(version1_as_array, version2_as_array, json_version_as_array, 0)
    return False


def perfect_match(cleared_line, techno, json_version) -> bool:
    """
    Returns a Bool by comparing the line with the techno and version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : Apache Log4j versions 2.16.0 et 2.12.2 (java 7)
    :param techno: str
    :param json_version: str
    :return: bool
    """
    if all(x + ' ' in cleared_line for x in [techno, json_version]):
        return True
    return False


def double_range_plus_extra(cleared_line, techno, json_version) -> bool:
    """
    Returns a Bool by comparing the line with the techno and version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : apache tomcat versions 8.5.50 à 8.5.81 antérieures à 8.5.82
    :param techno: str
    :param json_version: str
    :return: bool
    """
    split = cleared_line.split(" à ")
    if len(split) == 3 and len(
            cleared_line.split(" antérieures ")) == 2:  # comparing with split() is the fastest way
        if ".x" in cleared_line:
            return double_range_x(" à ".join(split[0:2]), techno, json_version)
        else:
            return double_range_no_x(" à ".join(split[0:2]), techno, json_version)

    return False


class Private:
    """
    Private class inside of module "certfr_version_parser". this class doesn't need to be imported.
    """

    @staticmethod
    def double_range_comparator(version1, version2, json_version, recursion_level) -> bool:
        """
        Return a bool by comparing if version1 <= json_version <= version2 via recursion.
        :param version1: [int]
        :param version2: [int]
        :param json_version: [int]
        :param recursion_level: int
        :return: bool
        """
        if recursion_level in (len(version1), len(version2), len(json_version)):
            return True
        if version1[recursion_level] < json_version[recursion_level] < version2[recursion_level]:
            return True
        elif json_version[recursion_level] in [version1[recursion_level], version2[recursion_level]]:
            return Private.double_range_comparator(version1, version2, json_version, recursion_level + 1)
        else:
            return False

    @staticmethod
    def version_to_int_array(version) -> [int]:
        """
        Return an array of int containing the version given in argument converted.
        :param version: str - eg : "3.4.0"
        :return: [int] - eg : [3, 4, 0]
        """
        version = version.split(".")

        for char in version[-1]:  # if non digit character follows the version
            if not char.isdigit():
                version[-1] = version[-1].split(char)[0]
        version[-1] += "0" if version[-1] == "" else ""

        map_version = map(int, version)
        return list(map_version)
