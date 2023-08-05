from pathlib import Path

from vr_configuration.shims.path.path_ensuring import ensure_path

ROOT_PATH: Path = Path(__file__).parent.parent

DATA_PATH: Path = ROOT_PATH / 'data'
ensure_path(path=DATA_PATH)

CONFIG_PATH: Path = DATA_PATH / 'config'
ensure_path(path=CONFIG_PATH)
