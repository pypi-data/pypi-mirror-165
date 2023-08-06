import argparse
from typing import List

from run_across_america import (
    RunAcrossAmerica,
    Team,
    Activity,
    Goal,
    Member,
    MemberStats,
    User,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lookup info from `Run Across America`."
    )

    subparsers = parser.add_subparsers(dest="command")

    user_id_parser = subparsers.add_parser(
        "user_id",
        help="Get the `user_id` for the user code.",
    )
    user_id_parser.add_argument(
        "user_code",
        help="User invitation code emailed after sign-up.",
    )

    user_parser = subparsers.add_parser(
        "user",
        help="Get info about a user.",
    )
    user_parser.add_argument("user_id")

    teams_parser = subparsers.add_parser(
        "teams",
        help="Get all the teams known to a user.",
    )
    teams_parser.add_argument("user_id")

    team_goals_parser = subparsers.add_parser(
        "goals",
        help="Get the distance goal for the specified team.",
    )
    team_goals_parser.add_argument("team_id")

    members_parser = subparsers.add_parser(
        "members",
        help="Get all the members of the specified team.",
    )
    members_parser.add_argument("team_id")

    leaderboard_parser = subparsers.add_parser(
        "leaderboard",
        help="Get all current leaderboard of the specified team.",
    )
    leaderboard_parser.add_argument("team_id")

    feed_parser = subparsers.add_parser(
        "feed",
        help="Get the current feed of the specified team.",
    )
    feed_parser.add_argument("team_id")

    args = parser.parse_args()

    client = RunAcrossAmerica()

    if args.command == "user_id":
        user_id: str = client.user_id(args.user_code)
        print(user_id)

    elif args.command == "user":
        user: User = client.user(args.user_id)
        print(user)

    elif args.command == "teams":
        if args.user_id == "-":
            teams: List[Team] = list(client.all_teams())
        else:
            teams: List[Team] = list(client.teams(args.user_id))
        for team in teams:
            print(team)

    elif args.command == "goals":
        goal: Goal = client.goals(args.team_id, include_progress=True)
        print(goal)

    elif args.command == "members":
        members: List[Member] = list(client.members(args.team_id))
        for member in members:
            print(member)

    elif args.command == "leaderboard":
        leaderboard: List[MemberStats] = client.leaderboard(args.team_id)
        for member in leaderboard:
            print(member)

    elif args.command == "feed":
        feed: List[Activity] = list(client.feed(args.team_id))
        for activity in feed:
            print(activity)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
