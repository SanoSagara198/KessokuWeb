from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Metric(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: int = Field(ge=0, le=100)


class StoryBeat(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    title: str
    description: str


class DetailBlock(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    summary: str
    description: str
    bullets: tuple[str, ...]


class Mode(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str
    title: str
    strapline: str
    player_fantasy: str
    description: str
    objective: str
    facts: tuple[str, ...]
    metrics: tuple[Metric, ...]
    loop: tuple[StoryBeat, ...]
    systems: tuple[DetailBlock, ...]


class Alignment(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: Literal["criminal", "police", "vigilante"]
    title: str
    code: str
    fantasy: str
    description: str
    objective: str
    progression: str
    methods: tuple[str, ...]
    consequences: tuple[str, ...]
    accent: str
    metrics: tuple[Metric, ...]
    loop: tuple[StoryBeat, ...]
    systems: tuple[DetailBlock, ...]


class Skill(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    tier: int = Field(ge=1, le=3)
    description: str


class SkillCategory(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str
    title: str
    summary: str
    accent: str
    skills: tuple[Skill, ...]


class DevelopmentUpdate(BaseModel):
    model_config = ConfigDict(frozen=True)

    state: Literal["ACTIVE", "NEXT", "PLANNED"]
    project: str
    title: str
    description: str


class Game(BaseModel):
    model_config = ConfigDict(frozen=True)

    slug: str
    title: str
    category: str
    tagline: str
    pitch: str
    long_description: str
    accent: str
    accent_rgb: tuple[int, int, int]
    status: str
    features: tuple[tuple[str, str], ...]


class WeaponSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str
    name: str
    role: str
    caliber: str
    rpm: int
    mag_size: int
    reload_sec: float
    base_damage: float
    head_mult: float
    optimal_range: int
    max_range: int
    recoil_vert: float
    recoil_horiz: float
    description: str


class DevlogEntry(BaseModel):
    model_config = ConfigDict(frozen=True)

    version: str
    date: str
    category: Literal["NETCODE", "COMBAT", "TRAFFIC AI", "MOBILE UI", "BALANCE"]
    title: str
    summary: str
    highlights: tuple[str, ...]


class ArchetypeResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    title: str
    description: str
    accent: str
    badge: str

