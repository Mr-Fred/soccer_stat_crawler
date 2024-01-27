import read_ytube_data
import get_today_game

class Betting:
    """
        Class for deciding on what team to place bet. Will extract the list of today's game and the list of teams
        of the top two scorers in their respective league.
        If team of top two scorers is in list of today's games then return team name to place bet on'
        Else return None

        Attributes:
            tournament_data: dict, key: tournament_name, value: tournament_stats
            teams: list, List of teams playing today

        Methods:
            get_top_two_scorers_team_name: returns list of top two scorers team names of that league
            get_bet_team_name: returns team name to place bet on
    """

    def __init__(self):
        # self.tournament_data = tournament_data
        # self.teams = teams
        self.top_two_scorers_team_name = []

    def get_top_two_scorers_team_name(self, tournament_data):
        """
            Take tournament dict and extract team name of top two scorers in each tournament.
            Returns list of top two scorers team names of each league
        """
        i = 0
        for league, league_stats in tournament_data.items():
            league_name = league
            for player_data in league_stats.values():
                team_name = player_data['Team Name']
                self.top_two_scorers_team_name.append(team_name)
                i += 1
                if i >= 2:
                    break
            i = 0
        return self.top_two_scorers_team_name

    def get_bet_team_name(self, teams):
        """
            Take top_two_scorers_team_name and today_game_team_name, and return a list of teams that exist in both list
            :param: self.top_two_scorers_team_name, self.teams
            :return: bet_team_name
        """
        bet_team_name = []
        for team in self.top_two_scorers_team_name:
            if team in teams:
                bet_team_name.append(team)
        return bet_team_name

    def main(self):
        tournament_data = read_ytube_data.main()
        teams = get_today_game.get_today_game()
        self.get_top_two_scorers_team_name(tournament_data)
        teams_list = self.get_bet_team_name(teams)
        return teams_list

if __name__ == "__main__":
    bet = Betting()
    teams = bet.main()
    print(teams)