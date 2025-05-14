from pathlib import Path

def load_prompt(template_name: str) -> str:
    path = Path("prompts") / f"{template_name}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Missing prompt template: {path}")
    return path.read_text()


def fill_prompt(template: str, **kwargs) -> str:
    return template.format(**kwargs)