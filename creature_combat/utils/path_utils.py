from pathlib import Path

_PATH_UTILS = Path(__file__).resolve()
_ROOT = _PATH_UTILS.parent.parent
_CREATUREDEX_PATH = _ROOT.parent / "creaturedex_data"

_MOVE_LIST_PATH = _ROOT.parent / "move_data"