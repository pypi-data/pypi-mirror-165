import setuptools, disutils
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
with open("README.md", "r", encoding="utf-8", errors="ignore") as fh:
    long_description = fh.read()
current_directory = Path(__file__).parent.resolve()
version_path = current_directory / "disutils" / "_version.py"
module_spec = spec_from_file_location(version_path.name[:-3], version_path)
version_module = module_from_spec(module_spec)
module_spec.loader.exec_module(version_module)
setuptools.setup(
    name="discord-ext-disutils",
    version=version_module.__version__,
    author="Pranoy Majumdar",
    description="Disutils is a very useful library made to be used with discord.py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">= 3.7",
    include_package_data=True,
    install_requires=["discord.py", "discord-ext-menus"],
)