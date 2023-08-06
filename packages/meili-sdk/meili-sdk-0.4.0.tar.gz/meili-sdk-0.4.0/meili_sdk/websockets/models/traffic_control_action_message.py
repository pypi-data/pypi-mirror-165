import typing as t

from meili_sdk.models.base import BaseModel

__all__ = (
    "SlowDownMessage",
    "PathReroutingMessage",
)


class SlowDownMessage(BaseModel):
    goal_id: t.Optional[str] = None
    max_vel_x: float
    max_vel_theta: float


class PathReroutingMessage(BaseModel):
    path: t.List[t.List]
    rotation_angles: t.List
