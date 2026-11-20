import os

from dugout.loader import load_players, load_team, load_teams
from dugout.models import League
from dugout.rules import MAX_CREDITS

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def show_pool(players):
    """Print how many players there are per franchise and per role."""
    by_franchise = {}
    by_role = {}
    for player in players.values():
        by_franchise[player.franchise] = by_franchise.get(player.franchise, 0) + 1
        by_role[player.role] = by_role.get(player.role, 0) + 1

    print(f"Player pool: {len(players)} players")
    print("Players by franchise:")
    for franchise in sorted(by_franchise):
        print(f"  {franchise}: {by_franchise[franchise]}")
    print("Players by role:")
    for role in sorted(by_role):
        print(f"  {role}: {by_role[role]}")


def show_team(team):
    print(f"\nTeam {team.team_name} by {team.owner}:")
    for player in team.players:
        print(f"  {player}")
    print(f"Total credits: {team.total_credits()}")
    print(f"Captain: {team.captain.name}, Vice-captain: {team.vice_captain.name}")


def show_verdict(team):
    """Print LEGAL or the list of problems. Returns True if the team is legal."""
    errors = team.check_rules()
    if errors:
        print("ILLEGAL:")
        for error in errors:
            print(f"  - {error}")
        return False
    print("LEGAL")
    return True


def show_league_table(league, reverse=False):
    for team in league.rank_teams(reverse=reverse):
        verdict = "ILLEGAL" if team.check_rules() else "LEGAL"
        print(f"{team.team_name:<20}{team.owner:<12}{team.total_credits():>6}   {verdict}")


def main():
    players = load_players(os.path.join(DATA_DIR, "players.csv"))
    show_pool(players)

    teams = load_teams(os.path.join(DATA_DIR, "sample_teams.csv"), players)
    legal = []
    illegal = []
    for team in teams:
        show_team(team)
        if show_verdict(team):
            legal.append(team)
        else:
            illegal.append(team)

    print(f"\nSummary: {len(legal)} legal, {len(illegal)} illegal out of {len(teams)} teams")
    print("Legal teams:")
    for team in legal:
        print(f"  {team.team_name}")
    print("Illegal teams:")
    for team in illegal:
        print(f"  {team.team_name}")

    print("\n--- My team ---")
    my_team = load_team(os.path.join(DATA_DIR, "my_team.csv"), players)
    show_team(my_team)
    print(f"Credits left: {MAX_CREDITS - my_team.total_credits()}")
    show_verdict(my_team)

    league = League("Dugout League")
    for team in teams:
        league.add_team(team)
    league.add_team(my_team)

    print("\n--- League table (cheapest first) ---")
    show_league_table(league)
    print("\n--- League table (most expensive first) ---")
    show_league_table(league, reverse=True)


if __name__ == "__main__":
    main()
