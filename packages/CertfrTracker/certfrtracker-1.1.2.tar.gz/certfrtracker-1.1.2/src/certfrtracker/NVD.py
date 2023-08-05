from re import search
from requests import get
from json import loads, JSONDecodeError
from logging import warning


def checkForCVE(documentation_links, documentation_text) -> str:
    """
    Returns a string containing either a str or None.
    Searches in the documentation given as argument an occurrence of a CVE.
    :param documentation_links: [str]
    :param documentation_text: [str]
    :return: str
    """
    for link in documentation_links:
        res = search(r'CVE-\d{4}-\d{4}', link)
        if res is not None:
            return res.group(0)

    for line in documentation_text:
        res = search(r'CVE-\d{4}-\d{4}', line)
        if res is not None:
            return res.group(0)

    return ""


def getNVDScore(link) -> float:
    """
    Returns a float containing the severity score of the CVE, established by NVD.
    :param link: str
    :return: float
    """
    r = get(link)
    try:
        json_data = loads(r.text)
    except JSONDecodeError:
        warning("ERREUR JSON NVD !")
        warning("STATUS HTTP :" + str(r.status_code))
        warning("HEADERS REPONSE HTTP : " + str(r.headers))
        return 0.0

    if not PageExists(json_data):
        return 0.0

    parsed_data = json_data["result"]['CVE_Items'][0]['impact']
    try:
        if parsed_data.get('baseMetricV3') is None:
            score = str(parsed_data['baseMetricV2']["cvssV2"]['baseScore'])

            return float(score)
        else:
            parsed_data = parsed_data['baseMetricV3']["cvssV3"]
            BaseScore = str(parsed_data['baseScore']) + " " + parsed_data['baseSeverity']

            return float(BaseScore.split()[0])
    except KeyError:
        return 0.0


def PageExists(json_data) -> bool:
    """
    Returns a boolean depending on the json_data. Since NVD's API doesn't respond with 404 status code when a CVE
    page doesn't exist. We need to inspect the content of the json response.
    :param json_data: str
    :return: int - 1 or 0
    """
    if not json_data.get("message") is None:
        if json_data['message'].startswith("Unable to find vuln"):
            return False

    return True
