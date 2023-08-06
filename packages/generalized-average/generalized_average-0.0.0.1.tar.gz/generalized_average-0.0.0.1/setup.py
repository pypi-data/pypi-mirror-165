import setuptools
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
name="generalized_average",
version="0.0.0.1",
author ="Uri Itai Alexander Molak &  Natan Katz",
include_package_data=True,
description="Calcalating different of averages for DL pooling tasks",
long_description=long_description,
long_description_content_type='text/markdown',
  packages=["generalized_average"]
)