from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open("dagster_snowflake/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version["__version__"]


if __name__ == "__main__":
    ver = get_version()
    # dont pin dev installs to avoid pip dep resolver issues
    pin = "" if ver == "0+dev" else f"=={ver}"
    setup(
        name="dagster-snowflake",
        version=ver,
        author="Elementl",
        author_email="hello@elementl.com",
        license="Apache-2.0",
        description="Package for Snowflake Dagster framework components.",
        url="https://github.com/dagster-io/dagster/tree/master/python_modules/libraries/dagster-snowflake",
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ],
        packages=find_packages(exclude=["dagster_snowflake_tests*"]),
        install_requires=["dagster==0.15.9", "snowflake-connector-python>=2.1.0"],
        extras_require={"snowflake.sqlalchemy": ["sqlalchemy", "snowflake-sqlalchemy"]},
        zip_safe=False,
    )
