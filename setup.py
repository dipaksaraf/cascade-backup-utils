"""Setup script for cascade-backup-utils."""

from setuptools import setup, find_packages

setup(
    name="cascade-backup-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyautogui>=0.9.54",
        "pyperclip>=1.8.2",
        "Pillow>=10.0.0",
    ],
    python_requires=">=3.8",
)
