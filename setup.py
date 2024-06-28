
"""
setup.

# NOTES
# ----------------------------------------------------------------------------|


Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import setuptools
import os


# define some useful vars
repo_name = "st-dash-template"
package_name = "st_dash_template"
dir_path = os.path.dirname(os.path.abspath(__file__))
requirements_path = os.path.join(dir_path, "requirements.txt")
test_requirements_path = os.path.join(dir_path, "test_requirements.txt")


# create long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_requirements(path):
    """Get the requirements in right format.

    Args:
        path (str: Path to requirements file

    Returns:
        reqs (list): list of strings defining dependencies
    """
    reqs = open(path).read().splitlines()
    for idx, req in enumerate(reqs):
        if "git+https://" in req:
            pkg_name = req.split('/')[-1].split('.')[0]
            reqs[idx] = f'{pkg_name} @ {req}'.replace(
                "${GITHUB_TOKEN}", os.environ["GITHUB_TOKEN"])

    return reqs


def package_files(directory):
    """Package necessary files.

    Args:
        directory (str): Directory name

    Returns:
        paths (list): list of files to package
    """
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


# main setup
setuptools.setup(
    name=repo_name,
    version=os.environ.get("VERSION"),
    install_requires=get_requirements(requirements_path),
    extras_require={"test": get_requirements(test_requirements_path)},
    author="Samuel Thorpe",
    description=f"Repository housing {repo_name} tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/samuelgthorpe/{repo_name}",
    classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent"],
    packages=[package_name],
    python_requires=">=3.10",
    package_data={'': package_files(package_name)},
    include_package_data=False,
    entry_points={
        'console_scripts': [
            f'{repo_name} = {package_name}.main:main',
        ],
    },
)
