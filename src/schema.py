from dataclasses import dataclass


@dataclass
class RuleChunk:
    rule_name: str
    url: str
    content: str
    subsection: str | None
