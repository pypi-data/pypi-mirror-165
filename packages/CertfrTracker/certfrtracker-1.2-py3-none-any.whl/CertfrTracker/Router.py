from datetime import date

import requests

import CertfrTracker.NVD as NVD
import CertfrTracker.scrapper as scrapper
from CertfrTracker.sqlite import Sqlite
from CertfrTracker.version_parser import systems_filter


class Report:
    """
    Plain object returned by Router class as list of Report.
    It contains all information about each alert.
    """

    def __init__(self, alert_id: str, techno: str, version: str, status: str, score: float, publish_date: str,
                 update_date: str, description: str, source: str, details: str) -> None:
        self.alert_id = alert_id  # id of the Alert           | String | CVE-2022-1234,
        # CERTFR-2022-ALE-004, CERTFR-2022-AVI-004
        self.techno = techno  # Name of the Techno        | String | ex: Apache, Postgresql, Openjdk
        self.version = version  # Version of the Techno     | String | ex: 1.2.3, 1.2, 1.2.3-beta
        self.status = status  # Nature of Alert           | String | Open or Applicable
        self.score = score  # CVSS or NVD Score         | Float  | between 1 and 10
        self.publish_date = publish_date  # Publish Date              | String | ex: "2020-06-21
        self.update_date = update_date  # Update Date               | String | ex: "2020-06-21
        self.description = description  # Alert Description         | String
        # self.source = | String | ex: url
        self.source = source  # url of the alert | string
        self.details = details


class Router:
    """
    This class creates and updates the database to the certfr.
    It also compares the technos and versions you give as argument to the database and returns it as a list of Report
    """

    def __init__(self, verbose=False, db_file="CertfrTracker.db"):
        self.verbose = verbose
        self.sqliteCon = Sqlite(db_file)
        self.sqliteCon.create_data_base()

    def __del__(self):
        self.sqliteCon.close_connection()

    def get_certfr_data(self, feed_type):
        """
        Updates the database by scrapping the certfr.
        :param feed_type: str - "NextAlert" or "NextAvis"
        """
        lastScrap = self.sqliteCon.get_next_scrap(feed_type)  # get lastScrap from database

        if feed_type == "NextAvis":
            url = 'https://www.cert.ssi.gouv.fr/avis/'
            Begin_Year = 2015 if lastScrap == 'Null' else int(lastScrap[7:11])
        else:
            url = 'https://www.cert.ssi.gouv.fr/alerte/'
            Begin_Year = 2014 if lastScrap == 'Null' else int(lastScrap[7:11])

        Begin_Alert = 1 if lastScrap == 'Null' else int(lastScrap[-3:])
        NextScrap = ""
        Actual_Year = date.today().year

        for year in range(Begin_Year, Actual_Year + 1):
            if year != Begin_Year:
                Begin_Alert = 1
            for count in range(Begin_Alert, 1000):
                # Download from URL.
                alert_id = 'CERTFR-' + str(year) + '-' + feed_type.upper()[4:7] + '-' + str(count).zfill(3)
                r = requests.get(url + alert_id)

                # return the next alert to begin with for next run
                if r.status_code == 404 and year == Actual_Year:
                    NextScrap = alert_id
                    break

                # go to next year once the actual is done
                if r.status_code == 404:
                    break

                # Save to database.
                self.alerts_to_database(alert_id, url + alert_id, r.content)

                if self.verbose:
                    print(alert_id)

            # return the next alert to begin with for next run
            if NextScrap != "":
                break

        self.sqliteCon.set_next_scrap(feed_type, NextScrap)  # set NextScrap to database

    def alerts_to_database(self, filename, source, text):
        """
        Scraps the html file in argument and insert it into the database.
        :param filename: str - CERTFR-AAAA-(ALE or AVI)-NNN
        :param source: str - URL of the alert
        :param text: str - html content returned by the certfr
        """
        systems_affectes = scrapper.systems_parser(text)
        _date = scrapper.date_parser(text)
        summary = scrapper.header_summary_parser(text)
        documentation_texte, documentation_liens = scrapper.documentation_parser(text)

        # NVD score
        CVE = NVD.checkForCVE(documentation_liens, documentation_texte)
        if self.verbose:
            print("traitement NVD de", filename)
            print(CVE)
        link = "https://services.nvd.nist.gov/rest/json/cve/1.0/" + CVE if CVE != "" else ""
        score = NVD.getNVDScore(link) if link != "" else 0.0

        # get details link
        details = scrapper.define_details(score, CVE, documentation_liens)

        self.sqliteCon.add_new_alert(filename, _date, systems_affectes, summary, score, source, details)

    def compare_inventory_with_alerts(self, technos: [str], versions: [str], dates: [str]) -> [Report]:
        """
        returns a list of Report by comparing the inventory in entry with the database.
        :param technos: [str]
        :param versions: [str]
        :param dates: [str]
        :return: [Report]
        """
        reports = []

        for techno, version, _date, in zip(technos, versions, dates):
            reports += self.compare_one_techno_with_alerts(techno, version, _date)

        return reports

    def compare_one_techno_with_alerts(self, techno: str, version: str, _date: str) -> [Report]:
        """
        returns a list of Report by comparing the single techno in entry with the database.
        :param techno: str
        :param version: str
        :param _date: str
        :return: [Report]
        """
        reports = []
        techno = techno.lower()
        if _date == "":
            _date = "01-01-2014"

        for alert in self.sqliteCon.get_alerts_newer_than(_date):
            for line in self.sqliteCon.get_one_row_from_alerts('SystèmesAffectés', alert).split("|"):
                result = systems_filter(techno, version, line, self.verbose)
                if result is not None:
                    score_nvd = self.sqliteCon.get_one_row_from_alerts('ScoreNVD', alert)
                    summary = self.sqliteCon.get_one_row_from_alerts('Résumé', alert)
                    release_date = self.sqliteCon.get_one_row_from_alerts('Date', alert)
                    source = self.sqliteCon.get_one_row_from_alerts('Source', alert)
                    details = self.sqliteCon.get_one_row_from_alerts('Details', alert)

                    report = Report(alert_id=alert, techno=techno, version=version, status=result,
                                    score=float(score_nvd), update_date=release_date, publish_date=release_date,
                                    description=summary, source=source, details=details)

                    reports.append(report)

        # to remove duplicated from list
        no_duplicates = []

        for report in reports:
            token = True
            for no_duplicate in no_duplicates:
                if report.alert_id == no_duplicate.alert_id:
                    token = False

            if token:
                no_duplicates.append(report)

        return no_duplicates
