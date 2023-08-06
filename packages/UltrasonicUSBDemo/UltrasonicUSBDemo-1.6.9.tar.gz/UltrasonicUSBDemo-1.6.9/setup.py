#setup.py
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UltrasonicUSBDemo", # Replace with your own username
    version="1.6.9",
    author="Roanoke Electronic Controls, Inc.",
    author_email="info@roanokecontrols.com",
    description="Demonstrates communication with different USB ultrasonic devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RoanokeControls/PkgUltrasonicUSBDemo",
    packages=setuptools.find_packages(),
    package_data={
        "UltrasonicUSBDemo": ["image/*","fs000x.xml","fs0002.xml"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyQt5',
        'pyserial',
     ],
    python_requires='>=3.6',
)
