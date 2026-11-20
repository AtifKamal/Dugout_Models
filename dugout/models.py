from dugout.rules import (
    check_players_count,
    check_budget,
    check_franchise_limit,
    check_roles,
    check_captains,
    check_no_duplicates,
)


class Player:
    """One real cricketer from the PSL player list."""

    def __init__(self, player_id, name, franchise, role, credits):
        self.player_id = player_id
        self.name = name
        self.franchise = franchise
        self.role = role
        self.credits = credits

    @classmethod
    def from_row(cls, row):
        return cls(
            row["player_id"],
            row["name"],
            row["franchise"],
            row["role"],
            float(row["credits"]),
        )

    def __str__(self):
        return f"{self.name} ({self.franchise}, {self.role}, {self.credits} cr)"

    def __repr__(self):
        return f"Player({self.player_id!r}, {self.name!r})"


class FantasyTeam:
    """A fantasy XI picked by one person."""

    def __init__(self, team_name, owner):
        self.team_name = team_name
        self.owner = owner
        self.players = []
        self.captain = None
        self.vice_captain = None

    def add_player(self, player):
        self.players.append(player)

    def set_captain(self, captain, vice_captain):
        self.captain = captain
        self.vice_captain = vice_captain

    def total_credits(self):
        total = 0
        for player in self.players:
            total += player.credits
        return total

    def count_by_role(self):
        counts = {"WK": 0, "BAT": 0, "AR": 0, "BOWL": 0}
        for player in self.players:
            counts[player.role] += 1
        return counts

    def count_by_franchise(self):
        counts = {}
        for player in self.players:
            counts[player.franchise] = counts.get(player.franchise, 0) + 1
        return counts

    def check_rules(self):
        """Returns a list of problems. An empty list means the team is legal."""
        errors = []
        errors.extend(check_players_count(self))
        errors.extend(check_budget(self))
        errors.extend(check_franchise_limit(self))
        errors.extend(check_roles(self))
        errors.extend(check_captains(self))
        errors.extend(check_no_duplicates(self))
        return errors

    def __str__(self):
        return (
            f"{self.team_name} (owner: {self.owner}, "
            f"{len(self.players)} players, {self.total_credits()} cr)"
        )

    def __repr__(self):
        return f"FantasyTeam({self.team_name!r}, {self.owner!r})"


class League:
    """Keeps one team per owner and can list or rank them."""

    def __init__(self, name):
        self.name = name
        self.teams = {}

    def add_team(self, team):
        self.teams[team.owner] = team

    def find_team(self, owner):
        return self.teams.get(owner)

    def legal_teams(self):
        return [team for team in self.teams.values() if not team.check_rules()]

    def rank_teams(self, reverse=False):
        """Teams sorted by total credits, cheapest first unless reverse is set."""
        return sorted(
            self.teams.values(), key=lambda team: team.total_credits(), reverse=reverse
        )
