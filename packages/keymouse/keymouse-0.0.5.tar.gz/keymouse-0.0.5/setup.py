from setuptools import setup, find_packages


setup(
    name="keymouse",
    version="0.0.5",
    license="MIT",
    author="Roman Smolnyk",
    author_email="poma23324@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://gitlab.com/roman-smolnyk/keymouse",
    keywords="Key Mouse",
    install_requires=[
        "pynput",
        "pyautogui",
        "pylayout",
    ],
    description="Python module to work with keyboard and mouse"
)
