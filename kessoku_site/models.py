from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Metric(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: int = Field(ge=0, le=100)


class Mode(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str
    title: str
    strapline: str
    description: str
    facts: tuple[str, ...]
    metrics: tuple[Metric, ...]


class Alignment(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: Literal["criminal", "police", "vigilante"]
    title: str
    code: str
    description: str
    objective: str
    accent: str
    metrics: tuple[Metric, ...]


class Game(BaseModel):
    model_config = ConfigDict(frozen=True)

    slug: str
    title: str
    category: str
    tagline: str
    pitch: str
    accent: str
    accent_rgb: tuple[int, int, int]
    status: str
    features: tuple[tuple[str, str], ...]
