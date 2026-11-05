"""Entrada ejecutable desde cualquier directorio; resuelve raíz por código."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from auditoriacfe.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
