from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from itertools import chain


# chrome_driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])

# Initialize the Chrome web driver
browser = webdriver.Chrome(options=options)  # Use ChromeOptions object

wait = WebDriverWait(browser, timeout=5)


def get_today_game():
    team_list = []
    url = "https://www.whoscored.com"
    browser.get(url)
    # Switch to the first window
    # browser.switch_to.window(browser.window_handles[0])

    # Find
    all_tournaments = wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                  'Tournaments-module_tournaments__JNs0A')))
    tournaments = all_tournaments.find_elements(By.CLASS_NAME, 'Accordion-module_accordion__UuHD0')

    for tournament in tournaments:
        # expanded = games.find_element(By.CLASS_NAME, 'Accordion-module_headerExtra__AZJhC')
        # expanded.click()
        games = tournament.find_element(By.CLASS_NAME, 'Accordion-module_childrenOpened__Ghom6')
        games_per_tournament = games.get_attribute('innerText')
        pattern = r'[A-Z][a-zA-Z]*(?: [A-Z][a-zA-Z]*)*'
        team_names = re.findall(pattern, games_per_tournament)
        # for match in matches:
        #     print(match.strip())
        team_list.append(team_names)
    team_playing_today = list(chain.from_iterable(team_list))
    return team_playing_today

if __name__ == '__main__':
    get_today_game()
