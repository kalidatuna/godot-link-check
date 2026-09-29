from setuptools import find_packages, setup

setup(
    name="godot-link-check",
    version="0.1.0",
    description="Offline checks for external resources and IDs in Godot text scenes",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={"console_scripts": ["godot-link-check=godot_link_check.cli:main"]},
)
