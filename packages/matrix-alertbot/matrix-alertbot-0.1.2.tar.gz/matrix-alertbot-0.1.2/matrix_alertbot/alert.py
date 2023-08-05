from __future__ import annotations

import logging
from typing import Dict, Optional

from jinja2 import (
    BaseLoader,
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
)

logger = logging.getLogger(__name__)


class Alert:
    EMOJIS = {"critical": "🔥", "warning": "⚠️", "resolved": "🥦"}
    COLORS = {"critical": "dc3545", "warning": "ffc107", "resolved": "33cc33"}

    def __init__(
        self,
        fingerprint: str,
        url: str,
        labels: Dict[str, str],
        annotations: Dict[str, str],
        firing: bool = True,
    ):
        self.fingerprint = fingerprint
        self.url = url
        self.firing = firing

        self.labels = labels
        self.annotations = annotations
        self.description = annotations["description"]

        if self.firing:
            self.status = self.labels["severity"]
        else:
            self.status = "resolved"

    @staticmethod
    def from_dict(data: Dict) -> Alert:
        return Alert(
            fingerprint=data["fingerprint"],
            url=data["generatorURL"],
            firing=data["status"] == "firing",
            labels=data["labels"],
            annotations=data["annotations"],
        )

    @property
    def emoji(self) -> str:
        return self.EMOJIS[self.status]

    @property
    def color(self) -> str:
        return self.COLORS[self.status]


class AlertRenderer:
    def __init__(self, template_dir: Optional[str] = None) -> None:
        loader: BaseLoader = PackageLoader("matrix_alertbot", "resources/templates")
        if template_dir is not None:
            loader = ChoiceLoader([FileSystemLoader(template_dir), loader])
        env = Environment(loader=loader, autoescape=True)

        self.html_template = env.get_template("alert.html.j2")
        self.text_template = env.get_template("alert.txt.j2")

    def render(self, alert: Alert, html: bool = True) -> str:
        if html:
            template = self.html_template
        else:
            template = self.text_template
        return template.render(vars(alert), color=alert.color, emoji=alert.emoji)
