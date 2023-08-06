from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests>=2.22.0"]

setup(
    name="vk_api_lite",
    version="0.0.4",
    author="Chesnokov MA",
    author_email="chesnkov.malex@gmail.com",
    description="Небольшая библиотека для работы с VK API через access_token (wall.post, wall.get, photos.save)",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/vkapilitelib/vk_api_lite",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)