import logging
import sys
from setuptools import (
    setup,
    find_packages,
)

from seetm.shared.constants import (
    PACKAGE_VERSION,
    PACKAGE_NAME_PYPI,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if sys.version_info < (3, 7) or sys.version_info >= (3, 9):
    sys.exit('SEETM requires Python 3.7 or 3.8')

requirements = None
long_description = None

try:
    with open("README.md", mode="r", encoding="utf8") as readme_file:
        long_description = readme_file.read()

    with open("requirements.txt", mode="r", encoding="utf8") as requirements_file:
        requirements = requirements_file.readlines()
    requirements = [str.strip(req) for req in requirements]

except Exception as e:
    long_description = "not provided"
    logger.error(f"couldn't retrieve the long "
                 f"package description. {e}")

setup(
    name=PACKAGE_NAME_PYPI,
    version=PACKAGE_VERSION,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # Include special files required
        # for the server env
        "": [
            "data/*",
            "seetm_components/*",
            "seetm_eval/*",
            "seetm_eval/results/*",
            "seetm_exports/*",
            "seetm_exports/tokenizer/*",
            "seetm_exports/rule_based/*",
            "seetm_exports/ipa/*",
            "seetm_maps/*",
            "frontend/*",
            "frontend/res/*",
            "frontend/res/images/*",
            "frontend/res/scripts/*",
            "frontend/res/styles/*",
            "frontend/static/*",
            "frontend/static/css/*",
            "frontend/static/js/*",
            "frontend/static/media/*",
            "static/*",
            "templates/*",
            "*.env",
            "*.md",
            "*.js",
            "*.css",
            "*.png",
            "*.py",
            "__init__.py",
            "*.yml",
        ],
    },
    description="Converts English tokens into the "
                "equivalent Sinhala representation "
                "using IPA (International Phonetic "
                "Alphabet)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dinushiTJ/seetm",
    author="Dinushi Jayasinghe",
    author_email="dinushitj@gmail.com",
    license='Apache License 2.0',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    install_requires=requirements or [
        "eng-to-ipa~=0.0.2",
        "gensim~=4.1.2",
    ],
    entry_points={'console_scripts': ['seetm = seetm.seetm:run_seetm_cli']}
)
