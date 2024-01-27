import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from load_data_to_sheet import write_table_to_google_sheets
import time


class Bot(webdriver.Chrome):

    def __init__(self, **kwargs):
        # Initialize the Chrome web driver
        self.tournament_data = None
        self.top_players_table = None
        self.browser = webdriver.Chrome()  # Use ChromeOptions object
        self.wait = WebDriverWait(self.browser, timeout=15)
        super(Bot, self).__init__()

    def get_popular_tournaments_data(self, site_url):
        """
        Get the data for the most popular tournaments in the world
        :return: A list of dictionaries containing the data for the most popular tournaments in the world
        """

        # Open the main page
        self.browser.get(site_url)
        self.browser.execute_script("window.open('', '_blank');")
        # Wait for all elements to load
        popular_tournaments_list = self.wait.until(EC.presence_of_element_located((By.ID, "popular-tournaments-list")))

        # Extract all the list items (li elements) from the unordered list
        list_items = popular_tournaments_list.find_elements(By.TAG_NAME, "li")

        tournament_data = []
        for item in list_items:

            tournament_url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            # premier_league = extract_league_data(tournament_url)
            if item.find_element(By.TAG_NAME, "a").get_attribute("title") == "Russia":
                tournament_name = "Russia " + item.text.strip()
            else:
                tournament_name = item.text.strip()

            player_stats_url = None

            try:
                # Open the tournament page in a new tab using JavaScript
                self.browser.switch_to.window(self.browser.window_handles[1])
                self.browser.get(tournament_url)

                sub_navigation_div = self.wait.until(EC.presence_of_element_located((By.ID, "sub-navigation")))
                sub_navigation_ul = sub_navigation_div.find_element(By.TAG_NAME, "ul")
                list_items = sub_navigation_ul.find_elements(By.TAG_NAME, "li")

                for li in list_items:
                    if "Player Statistics" == li.text.strip():
                        player_stats_url = li.find_element(By.TAG_NAME, "a").get_attribute("href")
                        break

            except TimeoutException as ex:
                print(f"Error while processing tournament URL: {tournament_url}")
                print(f"Error message: {ex}")

            finally:
                # Close the new tab after processing
                self.browser.switch_to.window(self.browser.window_handles[0])

            self.tournament_data.append({
                'Tournament Name': tournament_name,
                'Tournament URL': tournament_url,
                'Player Stats URL': player_stats_url
            })
        return self.tournament_data

    def extract_table_by_id(self, table_id):
        try:
            statistics_table_summary = self.wait.until(EC.presence_of_element_located((By.ID, table_id)))

            # Extract the table as a pandas DataFrame
            top_players_table = pd.read_html(statistics_table_summary.get_attribute("outerHTML"))

            # Since read_html() returns a list of DataFrames, you need to select the desired DataFrame from the list.
            # In this case, the first (index 0) DataFrame contains the table you want.
            self.top_players_table = top_players_table[0]
            return self.top_players_table

        except TimeoutException as ex:
            print(f"Error while extracting table with ID: {table_id}")
            print(f"Error message: {ex}")
            return None

    def get_statistics_table_summary(self, tournament_data: list):
        for data in self.tournament_data:
            player_stats_url = data['Player Stats URL']
            if player_stats_url:
                try:
                    self.browser.get(player_stats_url)
                    tournament_name = data['Tournament Name']

                    # Extract Player Statistics table
                    player_stats_table_id = 'top-player-stats-summary-grid'
                    player_stats_table = self.extract_table_by_id(player_stats_table_id)

                    # Extract Assist to Goal Scorer table
                    assist_to_goal_scorer_table_id = 'top-player-assist-grid'
                    assist_to_goal_scorer_table = self.extract_table_by_id(assist_to_goal_scorer_table_id)

                    if player_stats_table is not None and assist_to_goal_scorer_table is not None:
                        # Save Player Statistics table to CSV
                        # csv_file_path_player_stats = f"{tournament_name} - Player_Statistics.csv"
                        # player_stats_table.to_csv(csv_file_path_player_stats, index=False)
                        # player_stats_table = pd.read_html(player_stats_table_elm.get_attribute("outerHTML"))
                        # player_stats_table_list = player_stats_table.values.tolist()

                        # csv_file_path_assist_to_goal_scorer = f"{tournament_name} - Assist_to_Goal_Scorer.csv"
                        # assist_to_goal_scorer_table.to_csv(csv_file_path_assist_to_goal_scorer, index=False)
                        # print(f"Assist to Goal Scorer table for {tournament_name} saved as CSV.")
                        # assist_to_goal_scorer_table_list = assist_to_goal_scorer_table.values.tolist()
                        write_table_to_google_sheets(data, player_stats_table, assist_to_goal_scorer_table)
                        print(f"Player Statistics table for {tournament_name} saved in the SpreadSheet.")

                except TimeoutException as ex:
                    print(f"Error while processing player stats URL: {player_stats_url}")
                    print(f"Error message: {ex}")
            time.sleep(2)

    def main(self, site_url):
        # Get the data for popular tournaments
        self.get_popular_tournaments_data(site_url)

        # Process the player stats URLs to extract the data
        if self.tournament_data:
            self.get_statistics_table_summary()
            # Close the browser after processing
            self.browser.quit()


if __name__ == '__main__':
    url = "https://www.whoscored.com"
    bot = Bot()
    bot.main(url)
