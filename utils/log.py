#! /usr/bin/python

from dataclasses import dataclass, field
import json


@dataclass
class Log:
    file_name: str
    log: list = field(default_factory=list)

    def add_entry(self, conf, alphas):
        self.log.append((conf, alphas))

    def save(self):
        with open(self.file_name, "w") as fp:
            json.dump(self.log, fp)
