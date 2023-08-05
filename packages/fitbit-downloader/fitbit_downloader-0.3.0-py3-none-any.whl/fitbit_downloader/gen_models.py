import os
from pathlib import Path
from typing import Generator

from fitbit_downloader.ext_subprocess import run_then_show_output
from tests.config import RESPONSES_FOLDER

MODELS_FOLDER = Path(__file__).parent / "models"


def generate_models():
    for path in _get_json_paths():
        model_name = _create_model_name(path)
        print(f"Generating model {model_name} from {path}")
        out_path = MODELS_FOLDER / f"{model_name.lower()}.py"
        _generate_model(path, out_path, model_name)


def _create_model_name(path: Path) -> str:
    base_name = path.with_suffix("").name
    parts = base_name.split("-")
    combined = "".join(part.title() for part in parts)
    return f"{combined}Response"


def _get_json_paths() -> Generator[Path, None, None]:
    for path, folders, files in os.walk(RESPONSES_FOLDER):
        for file in files:
            if file.endswith(".json"):
                full_path = Path(path) / file
                yield full_path


def _generate_model(in_path: Path, out_path: Path, name: str):
    command = f"datamodel-codegen --input {in_path.absolute()} --input-file-type json --output {out_path} --class-name {name}"
    run_then_show_output(command)


def main():
    generate_models()


if __name__ == "__main__":
    main()
