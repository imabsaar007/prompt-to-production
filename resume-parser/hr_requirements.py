import json
from pathlib import Path

from models import HRRequirements


def load_hr_requirements(file_path: str) -> HRRequirements:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return HRRequirements.model_validate(data)


if __name__ == "__main__":
    requirements = load_hr_requirements("hr_requirements.json")
    print(requirements.model_dump_json(indent=2))