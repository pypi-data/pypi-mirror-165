# coding: utf-8

from dataclasses import dataclass

@dataclass
class IOSConfig:
    apple_id: str = None
    app_identifier: str = None
    team_id: str = None
    project_name: str = None
    project_dir: str = None
