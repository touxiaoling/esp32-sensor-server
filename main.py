import uvicorn
import os
from pathlib import Path
import shutil
import jurigged


def init_prometheus():
    PROMETHEUS_MULTIPROC_DIR = os.getenv("PROMETHEUS_MULTIPROC_DIR")

    if not PROMETHEUS_MULTIPROC_DIR:
        return

    multiproc_dir = Path(PROMETHEUS_MULTIPROC_DIR)
    if multiproc_dir.exists():
        shutil.rmtree(multiproc_dir)
    multiproc_dir.mkdir()


if __name__ == "__main__":
    jurigged.watch()
    init_prometheus()
    uvicorn.run(app="app:app", host="0.0.0.0", port=8084)
