from enum import Flag
from enum import auto
from typing import List
from typing import TypedDict


class AppType(Flag):
    SPA = auto()
    NATIVE = auto()
    NON_INTERACTIVE = auto()
    REGULAR_WEB = auto()


class User(TypedDict):
    created_at: str
    email: str
    email_verified: bool
    given_name: str
    family_name: str
    identities: dict
    video_upload_limits: dict
    locale: str
    name: str
    nickname: str
    picture: str
    updated_at: str
    user_id: str
    last_login: str
    last_ip: str
    logins_count: str
    install_type: str
    installed: str
    # Sample value: "{first} {last}"
    name_format: str
    picture: str
    picture_large: str
    short_name: str


class UserList(TypedDict):
    start: int
    limit: int
    length: int
    total: int
    users: List[User]
