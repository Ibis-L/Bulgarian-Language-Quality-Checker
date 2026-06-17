import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.0.0"

REPO_NAME = "Bulgarian Language Quality Checker"
AUTHOR_USER_NAME = "Ibis-L"
SRC_REPO = "Bulgarian Language Quality Checker"
AUTHOR_EMAIL = "lovepreet7gr@gmail.com"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Python package for Bulgarian language quality checking",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Fixed typo: was long_description_content
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    packages=setuptools.find_packages(exclude=["tests", "research"]) 
)