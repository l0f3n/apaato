# scraper.py

# Import selenium for webscraping
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Import Generator for annotations
from typing import Generator

import re

# Import digits for parsing
# from string import digits

# Import framework
from accommodation import Accommodation


# TODO: find their api and use that instead
# TODO: makes this asynchronous

def fetch_all_accommodations() -> Generator[Accommodation, None, None]:
    """ Goes to studentbostader.se and gathers the information about all the
    currently listed accommodations """

    # Initialize headless driver
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=options)

    start_page = "https://www.studentbostader.se/sv/sok-bostad/" + \
                 "lediga-bostader?pagination=0&paginationantal=1000"
    driver.get(start_page)

    driver.set_page_load_timeout(10)

    # Finds all listed accommodations and their links
    accommodations = driver.find_elements_by_class_name('noLinkcolor')[1:]
    accommodation_links = [a.get_attribute('href') for a in accommodations]

    yield len(accommodation_links)

    for link in accommodation_links:
        yield fetch_accommodation(driver, link)

    driver.quit()


def fetch_accommodation(driver: webdriver, link: str) -> Accommodation:
    """ Gets information about a single accommodation from link using
    webdriver """

    def address() -> str:
        return driver.find_element_by_class_name("adress").text

    def last_application_date():
        text = driver.find_element_by_class_name("IntresseMeddelande").text
        return text[25:35]

    def object_information() -> dict:
        xpath = "//div[@class='objektinformation']/table/tbody/tr"
        elems = driver.find_elements_by_xpath(xpath)

        tuple_elems = [elem.text.split(' ', 1) for elem in elems]

        dict_ = {}

#        area = tuple_elems[0][1]
#        dict_['area'] = area
#
        size = tuple_elems[1][1]
        dict_['size'] = size
#
#        space = float(''.join(
#                       c for c in tuple_elems[2][1] if c in digits+'.'))
#        dict_['space'] = space
#
#        rent = int(''.join(c for c in tuple_elems[3][1] if c in digits))
#        dict_['rent'] = rent
#
#        floor = tuple_elems[4][1][0]
#        dict_['floor'] = floor
#
#        has_elevator = tuple_elems[5][1] == 'Ja'
#        dict_['elevator'] = has_elevator
#
#        date = int(''.join(c for c in tuple_elems[6][1] if c in digits))
#        dict_['available_date'] = date
#
        return dict_

    def number_of_applicants(text: str) -> int:
        try:
            return int(text[text.index('v')+2:text.index('v')+4])
        except ValueError:
            return 0

    def top_queue_points(text: str) -> list:

        # Pattern will match a dot followed by one or more spaces or digits
        # example: . 1 230, . 233, . 73
        queue_points_pattern = re.compile(r'\.([\d ]+)')

        # Create a list of all the matches without the leading dot
        matches = queue_points_pattern.findall(text)

        # Remove whitespace and convert all matches to ints, right pad the list
        # with zeros to make it length 5
        queue_points_list = [int(matches[i].replace(' ', ''))
                             if i < len(matches) else 0 for i in range(5)]

        return queue_points_list


#    def furnished() -> bool:
#        """ Returns whether the accommodation is furnished or not """
#
#        try:
#            xpath = "//div[@class='PropertyItem Egenskap-1015']/span"
#            driver.find_element_by_xpath(xpath)
#        except NoSuchElementException:
#            return False
#        else:
#            return True

    # Make sure that the link does not timeout
    while True:
        try:
            driver.get(link)
        except TimeoutException:
            continue
        else:
            break

    # Get text about the current accommodation
    interest_text = driver.find_element_by_xpath("//div[@class='col']/p").text

    accommodation_properties = {
            'address': address(),
            'link': link,
            'date': last_application_date(),
            **object_information(),
            # 'furnished': furnished(),
            'applicants': number_of_applicants(interest_text),
            'queue_points_list': top_queue_points(interest_text)
            }

    return Accommodation(**accommodation_properties)
