from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
license = (this_directory / "LICENSE").read_text()

setup(
    name='eazy-django-user',
    # other arguments omitted
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license
)