import setuptools
from pixivery import __version__

setuptools.setup(
    name="pixivery",
    version=__version__,
    license="MIT",
    author="VoidAsMad",
    author_email="voidasmad@gmail.com",
    description="픽시브(랭킹, 검색) 크롤링 라이브러리",
    long_description=open("README.md", "rt", encoding="UTF8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VoidAsMad/Pixivery",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)