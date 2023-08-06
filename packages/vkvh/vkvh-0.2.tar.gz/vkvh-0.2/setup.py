import sys
from setuptools import setup, find_packages

with open("vkvh/version.txt") as fp:
   version=fp.read().strip()

setup(
   name="vkvh",
   version=version,
   author="Maria Morozova, Serguei Sokol",
   author_email="sokol@insa-toulouse.fr",
   url="https://forgemia.inra.fr/mathscell/vkvh",
   description="KVH Format Reader/Editor with Graphical User Interface",
   keywords="Key-Value Hierarchy",
   license="GNU General Public License v2 or later (GPLv2+)",
   long_description="Multi-platform GUI for KVH format reader/editor based on wxpython",
   packages=find_packages(),
   include_package_data = True,
   #package_data={"vkvh": ["help/*"]},
   #py_modules=["kvh"],
   python_requires=">=3.6",
   install_requires=['wxpython', 'kvh'],
   entry_points={
         'gui_scripts': [
            'vkvh = vkvh.vkvh:main',
         ],
   },
   classifiers=[
      "Environment :: Console",
      "Environment :: X11 Applications :: GTK",
      "Environment :: Win32 (MS Windows)",
      "Environment :: MacOS X",
      "Intended Audience :: End Users/Desktop",
      "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
      "Operating System :: OS Independent",
      "Programming Language :: Python :: 3",
      "Topic :: Scientific/Engineering",
      "Topic :: Text Processing :: Markup",
      "Topic :: Utilities",
   ],
   project_urls={
      "Source": "https://forgemia.inra.fr/mathscell/vkvh",
      "Tracker": "https://forgemia.inra.fr/mathscell/vkvh/-/issues",
   },
)
