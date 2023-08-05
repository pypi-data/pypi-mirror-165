from setuptools import setup, find_packages
import codecs


def read_file(path: str) -> list[str]:
    with codecs.open(path, 'r', 'utf-8') as f:
        return [l.strip() for l in f.readlines()]


README_PATH = 'README.md'
VERSION = '0.5.0'
DESCRIPTION = 'a Python midi utility'
LONG_DESCRIPTION = '\n'.join(read_file(README_PATH))
setup(
    name="midi-simplifier",
    version=VERSION,
    author="danielnachumdev (Daniel Nachum)",
    author_email="<danielnachumdev@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "arhicve/"]),
    install_requires=["mido"],
    keywords=['midi', 'python', 'note', 'chord', 'scale'],
    classifiers=[
        # "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
# python .\setup.py sdist
# powershell: twine upload dist/...
