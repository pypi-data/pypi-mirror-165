from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional
from requests import Session, Response

from .models import Goal, Member, MemberStats, Team, Activity, User


import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RunAcrossAmerica:
    BASE_URL: str = "https://runprod.cockpitmobile.com"

    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202",
            "Origin": "ionic://localhost",
            "is-virtual-client": "true",
            "ios-version": "1.0.74",
        }

        self.session.proxies = {"http": "127.0.0.1:8888", "https": "127.0.0.1:8888"}
        self.session.verify = False

    def _authenticate(self, user_code: str) -> Dict[str, Any]:
        url: str = f"{self.BASE_URL}/authenticate"
        headers: Dict[str, str] = {
            "content-type": "application/json",
        }
        payload: Dict[str, str] = {"email": "", "password": user_code}

        resp: Response = self.session.post(url, json=payload, headers=headers)
        return resp.json()

    def user_id(self, user_code: str) -> str:
        resp: Dict[str, Any] = self._authenticate(user_code)
        return resp.get("user", {}).get("id")

    def user(self, user_id: str) -> User:
        url: str = f"{self.BASE_URL}/users/{user_id}"
        resp: Response = self.session.get(url)
        data = resp.json()

        return User(
            id=data.get("id"),
            age=data.get("age"),
            created=datetime.strptime(
                data.get("creation_date", ""), "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            gender=data.get("gender"),
            phone=data.get("phone"),
            icon=data.get("profile_photo_link"),
            code=data.get("user_setup_passcode"),
            timezone=data.get("user_timezone"),
            username=data.get("username"),
            state=data.get("state"),
        )

    def _parse_team(self, data: Dict[str, Any]) -> Team:
        inner: Dict[str, Any] = data.get("team", {})

        created: Optional[datetime] = None
        if inner.get("creation_time"):
            created = datetime.strptime(inner["creation_time"], "%Y-%m-%dT%H:%M:%S.%fZ")

        return Team(
            id=inner.get("id"),
            name=inner.get("name"),
            code=inner.get("code"),
            icon=inner.get("icon"),
            created=created,
            member_count=int(data.get("memberCount", "0")),
        )

    def all_teams(self) -> Any:
        url: str = f"{self.BASE_URL}/raceteams"
        resp: Response = self.session.get(url)
        data = resp.json()
        for item in data:
            yield self._parse_team(item)

    def teams(self, user_id: str) -> Iterator[Team]:
        url: str = f"{self.BASE_URL}/users/{user_id}/raceteams"
        resp: Response = self.session.get(url)

        data = resp.json()
        for item in data.get("race_teams", []):
            yield self._parse_team(item)

    def goals(self, team_id: str, include_progress: bool = True) -> Goal:
        url: str = f"{self.BASE_URL}/raceteams/{team_id}/goals"
        resp: Response = self.session.get(url)
        data = resp.json().get("team_goal")

        progress: Optional[float] = None
        if include_progress:
            progress = self.goal_progress(team_id)

        return Goal(
            team_id=data.get("race_team_id"),
            distance=data.get("distance"),
            units=data.get("distance_units"),
            start_date=datetime.strptime(
                data.get("start_date", ""), "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            end_date=datetime.strptime(
                data.get("end_date", ""), "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            progress=progress,
        )

    def goal_progress(self, team_id: str) -> float:
        url: str = f"{self.BASE_URL}/raceteams/{team_id}/cumulativedistance"
        resp: Response = self.session.get(url)
        return resp.json().get("distance")

    def members(self, team_id: str) -> Iterator[Member]:
        url: str = f"{self.BASE_URL}/raceteams/{team_id}/members?limit=1000&offset=0"
        resp: Response = self.session.get(url)

        for item in resp.json():
            yield Member(
                id=item.get("user_id"),
                email=item.get("email"),
                first_name=item.get("first_name"),
                last_name=item.get("last_name"),
            )

    def leaderboard(self, team_id: str) -> List[MemberStats]:
        url: str = (
            f"{self.BASE_URL}/teams/{team_id}/goalleaderboard?limit=1000&offset=0"
        )
        resp: Response = self.session.get(url)

        data = resp.json()
        for idx, item in enumerate(data.get("user_distances")):
            yield MemberStats(
                id=item.get("user_id"),
                first_name=item.get("first_name"),
                last_name=item.get("last_name"),
                email=None,
                distance=item.get("sum"),
                icon=item.get("profile_photo_link"),
                team_id=team_id,
                rank=idx + 1,
            )

    def feed(self, team_id: str) -> Iterator[Activity]:
        url: str = f"{self.BASE_URL}/raceteams/{team_id}/feed?limit=1000&offset=0"
        headers: Dict[str, str] = {
            "content-type": "application/json",
        }
        payload: Dict[str, str] = {
            "filters": {
                "feed_type": {
                    "plans": False,
                    "activities": True,
                    "achievements": False,
                },
                "activities": {"all": True, "description_or_selfie_only": None},
            }
        }
        resp: Response = self.session.post(url, json=payload, headers=headers)

        data = resp.json()
        for item in data.get("runs"):
            yield Activity(
                name=item.get("activity_name"),
                type=item.get("activity_type"),
                distance=float(item.get("distance_ran")),
                units=item.get("distance_units"),
                duration=timedelta(milliseconds=int(item.get("run_time"))),
                time_completed=datetime.strptime(
                    item.get("time_completed_at"), "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                user_id=item.get("user_id"),
                user_first_name=item.get("first_name"),
                user_last_name=item.get("last_name"),
                user_icon=item.get("profile_photo_link"),
            )
