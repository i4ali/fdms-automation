"""
@package  pages.projects

Project page object to encapsulate all functionality related to the FDMS projects page. This includes the
locators, functions to be performed on the page
"""

from bs4 import BeautifulSoup

from pages.base.base_page import BasePage
from pages.projects.projectedit_page import ProjectEditPage
from pages.projects.projecteditdata_page import ProjectEditDataPage
from pages.projects.projectdetails_page import ProjectDetailsPage
from pages.clients.client_page import ClientPage
from pages.navigation.navigation_page import NavigationPage
from pages.acreage.acreage_planner import AcreagePlanner
import globalconfig


class ProjectPage(BasePage):

    urlcontains = 'projects'
    new_project_button_xpath = "//button[text()='New Project']"
    project_successfully_created_toast_xpath = "//*[contains(text(), 'Project successfully created')]"
    project_title_xpath = "//h1[contains(text(), 'Projects')]"
    page_header_xpath = "//h1[text()='Projects']"
    pagination_menu_css = "div[class='ui pagination menu']"
    project_table_xpath = "//table[@id='test-data-table']//tbody"
    project_table_id = 'test-data-table'
    project_table_head_xpath = "//table[@id='test-data-table']//thead/tr"
    searchbox_xpath = "//input[@placeholder='Search']"
    searchbox_text_attribute = "value"
    searbox_text_dropdown_xpath = "//*[@id='container']//div[@class='results transition visible']//div[@class='title']"
    project_name_table_header = "PROJECT NAME"
    basin_table_header = "BASIN"
    delete_project_link_text = "Delete Project"
    view_project_link_text = "View Project"
    delete_project_ok_button_xpath = '//button[text()="OK"]'
    project_successfully_deleted_toast_xpath = "//*[contains(text(), 'Project successfully deleted')]"

    def __init__(self):
        super().__init__()
        self.navigation = NavigationPage()
        self.project_edit_page = ProjectEditPage()
        self.client_page = ClientPage()
        self.projectdata_edit_page = ProjectEditDataPage()
        self.acreage_planner_page = AcreagePlanner()
        self.projectdetail_page = ProjectDetailsPage()

    def add_new_project(self, projectname, companyname, basin):
        """
        clicks new project on project page to create new project and enter
        all field information
        """
        self.navigation.navigate_to_clients()
        self.client_page.add_new_client(companyname)
        self.navigation.navigate_to_projects()
        self.click_new_project()
        self.project_edit_page.enter_project_name(projectname)
        self.project_edit_page.select_company_name(companyname)
        self.project_edit_page.select_basin(basin)
        self.project_edit_page.click_create_project()

    def is_at(self):
        """
        To be used by test functions. Redirects to project page if not
        already there
        :return:True if successful
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        return self._is_at()

    def _is_at(self):
        """
        Internal function to check if currently at project page
        :return: Boolean
        """
        return self.isat(self.page_header_xpath, "xpath")

    def project_exists(self, projectname):
        """
        Check the project table to see if project by projectname exists
        :param projectname: project name to search
        :return: Boolean
        """
        #TODO this might not work when pagination exceeds
        if not self._is_at():
            self.navigation.navigate_to_projects()
        return self.driver.is_element_present(projectname, "link")

    def project_success_message_pops(self):
        """
        Check to see if the success message pops after project created
        :return: Boolean
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        return self.driver.is_element_present(self.project_successfully_created_toast_xpath, "xpath")

    def get_toast_message(self):
        """
        Find the toast element and return its message
        :return: text of the toast message
        """
        # TODO grab toast message element and return its text
        pass

    def click_new_project(self):
        """
        Click the new project button on the project page
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        self.driver.click_element(self.new_project_button_xpath, "xpath")
        return ProjectEditPage()

    def page_refresh(self):
        """
        Refresh the page
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        self.driver.refresh()

    def pagination_menu_exists(self):
        """
        Verify that the pagination menu exists
        :return: Boolean
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        return self.driver.is_element_present(self.pagination_menu_css, "css")

    def get_table_entries_count(self):
        """
        Return the count of rows in the table
        :return: count of rows in the table
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        table_entries = self.driver.get_child_elements(self.project_table_xpath, "tr", "xpath", "tag")
        return len(table_entries)

    def search_project_in_searchbox(self, projectname):
        """
        Enters parameter into searchbox
        :param projectname: projectname to search in searchbox
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        self.driver.get_element(self.searchbox_xpath, "xpath").send_keys(projectname)

    def get_text_from_searchbox_dropdown(self):
        """
        As the data is entered into search box, the dropdown shows with
        the relevant entry. This function should return that entry
        :return: text from searchbox dropdown
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        return self.driver.get_text(self.searbox_text_dropdown_xpath, "xpath")

    def get_table_header(self):
        """
        Retrieves a list of table headers from the project table
        :return: list of table headers
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        header_elements = self.driver.get_child_elements(self.project_table_head_xpath, "th", "xpath", "tag")
        header_elements_text = []
        for element in header_elements:
            header_elements_text.append(self.driver.get_text(element=element))
        return header_elements_text

    def get_table_data(self):
        """
        Retrieves a list of lists for e.g. [[],[]] where each sublist is a row from the project table containing text
        of the elements
        :return: list of lists
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        table_data = []
        soup = BeautifulSoup(self.driver.get_page_source(), 'html.parser')
        table = soup.find('table', attrs={'id': self.project_table_id})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            table_data.append([ele for ele in cols])
        return table_data

    def get_basin_for_a_project_from_table(self, projectname):
        """
        For a given projectname retrieves the basin name from the project table
        :param projectname: name of the project to get basin name for
        :return: basin name
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        table_header = self.get_table_header()
        project_name_position_inside_header = table_header.index(self.project_name_table_header)
        basin_position_inside_header = table_header.index(self.basin_table_header)
        table_data = self.get_table_data()
        for row in table_data:
            if row[project_name_position_inside_header] == projectname:
                return row[basin_position_inside_header]

    def go_to_project(self, projectname):
        """
        Find the project in the project table and click on it
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        # self.driver.get_element(projectname, "link").click()
        self.driver.click_element(projectname, "link")

    def delete_project(self, projectname):
        """
        Find the project in the project table and delete it
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        table_headers = self.get_table_header()
        project_header_index = table_headers.index(self.project_name_table_header)
        data_rows = self.get_table_data()
        for data_row in data_rows:
            if projectname == data_row[project_header_index]:
                project_data_row = data_rows.index(data_row)
                project_row_xpath = self.project_table_xpath+'/tr[{0}]'.format(project_data_row+1)
                data_elements_of_project = self.driver.get_child_elements(project_row_xpath, "td", "xpath", "tag")
                project_icon_data_element = data_elements_of_project[-1]
                project_icon_element = self.driver.get_child_elements_given_parent_element(project_icon_data_element, "i", "tag")
                project_icon_element[0].click()
                delete_project_element = self.driver.get_child_elements_given_parent_element(project_icon_data_element, self.delete_project_link_text, "link")
                delete_project_element[0].click()
                self.driver.click_element(self.delete_project_ok_button_xpath, "xpath")
                break

    def project_delete_success_message_pops(self):
        """
        Check to see if the success message pops after project deleted
        :return: Boolean
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        return self.driver.is_element_present(self.project_successfully_deleted_toast_xpath, "xpath")

    def click_view_project(self, projectname):
        """
        Click on view project from the project table
        :param projectname: projectname of the project to view project for
        """
        if not self._is_at():
            self.navigation.navigate_to_projects()
        table_headers = self.get_table_header()
        project_header_index = table_headers.index(self.project_name_table_header)
        data_rows = self.get_table_data()
        for data_row in data_rows:
            if projectname == data_row[project_header_index]:
                project_data_row = data_rows.index(data_row)
                project_row_xpath = self.project_table_xpath + '/tr[{0}]'.format(project_data_row + 1)
                data_elements_of_project = self.driver.get_child_elements(project_row_xpath, "td", "xpath", "tag")
                project_icon_data_element = data_elements_of_project[-1]
                project_icon_element = self.driver.get_child_elements_given_parent_element(project_icon_data_element, "i", "tag")
                project_icon_element[0].click()
                view_project_element = self.driver.get_child_elements_given_parent_element(project_icon_data_element, self.view_project_link_text, "link")
                view_project_element[0].click()
                break







