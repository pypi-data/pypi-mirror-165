from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="DZDBuffy",
    description="Versioning Caching kinda-Proxy for decoupling external responses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.connect.dzd-ev.de/dzdpythonmodules/buffy",
    author="Tim Bleimehl",
    author_email="tim.bleimehl@helmholtz-muenchen.de",
    license="MIT",
    packages=["buffy", "buffy.buffypyclient", "buffy.buffyserver"],
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "requests",
        "redis",
        "croniter",
        "DZDConfigs",
        # "tqdm",
        "getversion",
        "Click",
    ],
    extras_require={
        "test": ["shittywebserver"],
        "docs": [
            "mkdocs",
            "mkdocstrings[python]",
            "mkdocs-autorefs",
            "mkdocs-material",
            "mkdocs-render-swagger-plugin",
        ],
    },
    python_requires=">=3.9",
    zip_safe=False,
    include_package_data=True,
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        # "local_scheme": "node-and-timestamp"
        "local_scheme": "no-local-version",
        "write_to": "version.py",
    },
    setup_requires=["setuptools_scm"],
    entry_points={
        "console_scripts": [
            "buffy-server=buffy.buffyserver.main:start_buffy_server_cli",
            "buffy-server-build-api-doc=buffy.buffyserver.main:build_api_doc",
        ],
    },
)
