"""
Day 9: Production Prompt Templating Engine
Supports parameterized variable interpolation, required slot validation, and versioning.
"""

import json
import re
from typing import Dict, Any, List, Set, Optional


class PromptTemplate:
    """
    Manages structured, parameterized prompt templates with variable validation.
    """

    def __init__(
        self,
        name: str,
        template_str: str,
        version: str = "1.0.0",
        description: str = "",
        defaults: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.template_str = template_str
        self.version = version
        self.description = description
        self.defaults = defaults or {}
        self.slots = self._extract_slots(template_str)

    @staticmethod
    def _extract_slots(text: str) -> Set[str]:
        """Finds all {variable_name} placeholder slots in the template."""
        # Finds single braces like {variable} but ignores escaped double braces {{ ... }}
        pattern = r"(?<!\{)\{([a-zA-Z_][a-zA-Z0-9_]*)\}(?!\})"
        return set(re.findall(pattern, text))

    def render(self, **kwargs) -> str:
        """Renders the template with provided arguments, falling back to defaults."""
        merged = {**self.defaults, **kwargs}
        missing = [slot for slot in self.slots if slot not in merged]
        if missing:
            raise KeyError(f"Missing required template parameters for '{self.name}': {missing}")
        return self.template_str.format(**merged)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "slots": list(self.slots),
            "defaults": self.defaults,
            "template": self.template_str
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromptTemplate":
        return cls(
            name=data["name"],
            template_str=data["template"],
            version=data.get("version", "1.0.0"),
            description=data.get("description", ""),
            defaults=data.get("defaults", {})
        )


class TemplateRegistry:
    """Central repository storing versioned prompt templates."""

    def __init__(self):
        self._templates: Dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate) -> None:
        key = f"{template.name}:{template.version}"
        self._templates[key] = template

    def get(self, name: str, version: Optional[str] = None) -> PromptTemplate:
        if version:
            key = f"{name}:{version}"
            if key in self._templates:
                return self._templates[key]
            raise KeyError(f"Template '{name}' with version '{version}' not found.")
        
        # Match latest version
        matches = [t for k, t in self._templates.items() if t.name == name]
        if not matches:
            raise KeyError(f"No template named '{name}' found.")
        return matches[-1]

    def list_templates(self) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self._templates.values()]


def demonstrate():
    raw_prompt = """
You are a {role}.
Summarize the text below in {word_limit} words or fewer.
Target Tone: {tone}.

<source_text>
{document}
</source_text>
"""
    tmpl = PromptTemplate(
        name="executive_summarizer",
        template_str=raw_prompt,
        version="1.0.0",
        description="Standard summarizer template with customizable role and tone.",
        defaults={"role": "Senior Market Intelligence Analyst", "word_limit": 150, "tone": "Objective and Authoritative"}
    )

    rendered = tmpl.render(document="Q3 revenue grew by 24% year-over-year driven by cloud adoption.")
    print("=" * 60)
    print("DAY 9: PROMPT TEMPLATE ENGINE DEMONSTRATION")
    print("=" * 60)
    print("Slots Identified:", tmpl.slots)
    print("\nRendered Prompt:")
    print(rendered)


if __name__ == "__main__":
    demonstrate()
