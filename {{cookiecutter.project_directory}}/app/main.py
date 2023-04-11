try:
    from app import create_app
except ModuleNotFoundError:
    import sys
    from pathlib import Path

    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]  # app folder
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))  # add ROOT to PATH

    from app import create_app


app = create_app()
