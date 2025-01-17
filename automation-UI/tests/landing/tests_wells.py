# """
# @package  tests.wells
#
# Landing page test class to encapsulate test cases related to the wells page for FDMS
# web application.
#
# The file is either run individually through pytest testrunner for e.g. 'pytest tests_wells.py' or is run
# as part of the test_suites file through pytest testrunner for e.g. 'pytest test_suites.py'.
# """
#
# # standard and site-package import
# import unittest
# from ddt import ddt, data, unpack
# from pymongo import MongoClient
# import pytest
# import time
#
# # project import
# from pages.wells.well_page import WellPage
# from pages.wells.welledit_page import WellEditPage
# from utilities.read_data import getCSVData
# from utilities.statustest import StatusTest
# import globalconfig
# from base.DBclient import DBClient
#
#
# @ddt
# class TestWells(unittest.TestCase):
#
#     @pytest.fixture(autouse=True)
#     def object_setup(self):
#         """
#         Instantiates LandingPage, TestStatus instance to be used by the test class
#         The function is run before every test function is called
#         """
#         self.teststatus = StatusTest()
#         self.wellpage = WellPage()
#         self.welleditpage = WellEditPage()
#
#     """Tests"""
#     @pytest.mark.smoketest
#     def test_can_go_to_landing_page(self):
#         """
#         Instanstiates wells page and verifies the page can be reached
#         successfully from the browser
#         """
#         result = self.wellpage.is_at()
#         self.teststatus.mark_final(result, "URL verification")
#
#     @pytest.mark.usefixtures("clear_well_from_db")
#     @data(*getCSVData('tests/testdata/welltestdata.csv'))
#     @unpack
#     def test_add_new_well(self, wellname, apinumber):
#         """
#         Adds a new well to the database
#         :param wellname: name of the well to be entered into the form
#         :param apinumber: api number to be entered into the form
#         """
#         self.wellpage.add_new_well(wellname, apinumber)
#         result = self.wellpage.well_success_message_pops()
#         self.teststatus.mark_final(result, "success toast message")
#
#     @pytest.mark.usefixtures("clear_well_from_db")
#     @data(*getCSVData('tests/testdata/validation/wellnamevalidation.csv'))
#     @unpack
#     def test_wellname_validation(self, wellname, validationmessage):
#         """FDMS-183
#         Validates the wellname field when adding a new well
#         :param wellname: name of the well to be entered into the form
#         :param validationmessage: the expected validation message
#         """
#         self.wellpage.click_new_well()
#         self.welleditpage.enter_well_name(wellname)
#         self.welleditpage.click_create_well()
#         self.teststatus.mark_final(validationmessage == self.welleditpage.get_validation_message_wellname(), "wellname form validation")
#
#     @pytest.mark.usefixtures("clear_well_from_db")
#     @data(*getCSVData('tests/testdata/validation/apinamevalidation.csv'))
#     @unpack
#     def test_apiname_validation(self, apinumber, validationmessage):
#         """FDMS-182
#         Validates the apiname field when adding a new well
#         :param apiname: apiname to be entered into the form
#         :param validationmessage: the expected validation message
#         """
#         self.wellpage.click_new_well()
#         self.welleditpage.enter_api_number(apinumber)
#         self.welleditpage.click_create_well()
#         self.teststatus.mark_final(validationmessage == self.welleditpage.get_validation_message_apiname(), "api name form validation")
#
#
#
#     # @pytest.mark.pagination
#     # @pytest.mark.usefixtures("clear_well_from_db")
#     # def test_well_pagination_limit_exceed_and_entries_to_show_match_number_table_rows(self):
#     #     # insert bulk data such that pagination limit is exceeded
#     #     self.client = DBClient(globalconfig.postgres_conn_URI)
#     #     rows = getCSVData('tests/testdata/pagination/wellpaginationexceed.csv')
#     #     table_entries = 0
#     #     for row in rows:
#     #         self.client.insert_well(row[0], row[1])
#     #         table_entries += 1
#         # verify entries to show matches number of rows in table
#
#
#     # def test_well_pagination_limit_exceed_and_can_navigate_to_nxt_page(self):
#     #     pass
#
#
#
