from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class User:
    id: str
    age: Optional[int]
    created: datetime
    email: str
    first_name: str
    gender: Optional[str]
    last_name: str
    phone: str
    icon: str
    code: str
    timezone: str
    username: str
    state: str


@dataclass
class Team:
    id: str
    name: str
    code: str
    icon: str
    created: Optional[datetime]
    member_count: int


@dataclass
class Goal:
    team_id: str
    distance: int
    units: str
    start_date: datetime
    end_date: datetime

    progress: Optional[float] = None


@dataclass
class Member:
    id: str
    first_name: str
    last_name: str
    email: Optional[str]


@dataclass
class MemberStats(Member):
    icon: str
    distance: float

    team_id: str
    rank: int

    units: str = "Kilometers"


@dataclass
class Activity:
    name: str
    type: str
    distance: float
    units: str
    duration: timedelta
    time_completed: datetime

    user_id: str
    user_first_name: str
    user_last_name: str
    user_icon: str
