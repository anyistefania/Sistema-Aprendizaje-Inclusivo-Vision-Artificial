"""
Setup para el Sistema de Aprendizaje Inclusivo con Visión Artificial
"""

from setuptools import setup, find_packages

with open("docs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sistema-aprendizaje-inclusivo",
    version="2.0.0",
    author="Semillero de Investigación",
    description="Sistema de Aprendizaje Inclusivo con Visión Artificial para Educación Especial",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anyistefania/Sistema-Aprendizaje-Inclusivo-Vision-Artificial",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "pyttsx3>=2.90",
        "imutils>=0.5.4",
        "Pillow>=8.0.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "aprendizaje-inclusivo=src.presentation.cli.main_menu:main",
        ],
    },
)
