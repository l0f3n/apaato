#scraper.py

# Import selenium for webscraping
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Import Generator for annotations
from typing import Generator

# Import digits for parsing
# from string import digits

# Import framework
from apartment import Apartment


# TODO: find their api and use that instead
# TODO: makes this asynchronous

def fetch_all_apartments() -> Generator[Apartment, None, None]:
    """ Goes to studentbostader.se and gathers the information about all the
    currently listed apartments """

    # Initialize headless driver
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=options)

    start_page = "https://www.studentbostader.se/sv/sok-bostad/" + \
                 "lediga-bostader?pagination=0&paginationantal=1000"
    driver.get(start_page)

    driver.set_page_load_timeout(10)
    # Finds all listed apartments and their links
    apartments = driver.find_elements_by_class_name('noLinkcolor')[1:]
    apartment_links = [a.get_attribute('href') for a in apartments]

    for link in apartment_links:
        yield fetch_apartment(driver, link)

    driver.quit()


def fetch_apartment(driver: webdriver, link: str) -> Apartment:
    """ Gets information about a single apartment from link using webdriver """

    def top_queue_points(text: str) -> list:
        applicants = number_of_applicants(text)

        try:
            queue_points_in_text = text[text.index(':'):]
        except ValueError:
            visible_queue_points = 0

        queue_points_list = []

        visible_queue_points = min(applicants, 5)
        for _ in range(visible_queue_points):
            begin = queue_points_in_text.index('.') + 2
            try:
                # Get end of queue points
                end = queue_points_in_text[begin:].index('.') - 2 + begin
            except ValueError:
                # If on last person in queue
                queue_points = queue_points_in_text[begin:]
            else:
                # Store queue points
                queue_points = queue_points_in_text[begin:end]
                # Removes queue points just stored from string
                queue_points_in_text = queue_points_in_text[end + 2:]

            # Remove whitespace from queue points and convert to int
            queue_points = int(queue_points.replace(' ', ''))

            queue_points_list.append(queue_points)

        # Make length of list always five to match database
        queue_points_list.extend([0]*(5-visible_queue_points))

        return queue_points_list

    def number_of_applicants(text: str) -> int:
        try:
            return int(text[text.index('v')+2:text.index('v')+4])
        except ValueError:
            return 0

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

    def address() -> str:
        return driver.find_element_by_class_name("adress").text

#    def furnished() -> bool:
#        """ Returns whether the apartment is furnished or not """
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

    # Get text about the current apartment
    text = driver.find_element_by_xpath("//div[@class='col']/p").text

    apartment_properties = {
            'address': address(),
            'link': link,
            **object_information(),
            # 'furnished': furnished(),
            'applicants': number_of_applicants(text),
            'queue_points_list': top_queue_points(text)
            }

    return Apartment(**apartment_properties)
