from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.5'
DESCRIPTION = 'Descarga de audios SurveyToGo'
LONG_DESCRIPTION = 'Programa para descargar y ordenar audios de encuestas de plataforma SurveyToGo'

# Setting up
setup(
    name="imasensurvey",
    version=VERSION,
    author="Matias Canales",
    author_email="<matias.canales@alum.udep.edu.pe>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pandas","pytest-shutil","pathlib"],
    keywords=['python', 'imasen'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)