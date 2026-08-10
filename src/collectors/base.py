from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path

from src.config import Config, DATA_DIR
from src.models import Listing

logger = logging.getLogger(__name__)


class BaseCollector(ABC):

    def __init__(self, config: Config):
        self.config = config
        self._usage_file = DATA_DIR / "api_usage.json"

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def collect(self) -> list[Listing]:
        pass

    def check_budget(self) -> bool:
        collector_config = self.config.collectors.get(self.name)
        if not collector_config or not collector_config.max_calls_per_month:
            return True

        usage = self._load_usage()
        current_month = datetime.now(timezone.utc).strftime("%Y-%m")

        if usage.get("month") != current_month:
            usage = {"month": current_month, "calls": {}}
            self._save_usage(usage)

        calls_used = usage["calls"].get(self.name, 0)
        remaining = collector_config.max_calls_per_month - calls_used

        if remaining <= 0:
            logger.warning(f"{self.name}: monthly API budget exhausted ({calls_used} calls used)")
            return False

        return True

    def record_api_call(self):
        usage = self._load_usage()
        current_month = datetime.now(timezone.utc).strftime("%Y-%m")

        if usage.get("month") != current_month:
            usage = {"month": current_month, "calls": {}}

        usage["calls"][self.name] = usage["calls"].get(self.name, 0) + 1
        self._save_usage(usage)

    def _load_usage(self) -> dict:
        if self._usage_file.exists():
            with open(self._usage_file) as f:
                return json.load(f)
        return {"month": None, "calls": {}}

    def _save_usage(self, usage: dict):
        with open(self._usage_file, "w") as f:
            json.dump(usage, f, indent=2)
