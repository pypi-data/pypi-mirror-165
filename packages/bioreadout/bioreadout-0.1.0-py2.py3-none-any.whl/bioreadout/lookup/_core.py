from typing import Literal  # noqa

readoutS = Literal["scRNA-seq", "RNA-seq", "flow-cytometry", "image"]
READOUT_PLATFORMS = Literal["Chromium (10x)", "Visium (10x)"]
