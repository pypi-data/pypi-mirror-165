from setuptools import setup, find_packages
import pathlib
import subprocess
from setuptools.command.develop import develop
from setuptools.command.install import install
import sys
import os


class PostDevelopCommand(develop):

    def run(self):
        # print("Here: ", os.path.join(
        #     os.path.dirname(sys.executable), "Scripts"))
        # print("Here: ", os.name)
        # print("Here: ", os.pathsep)
        # print("Here: ", os.environ["PATH"])
        # pathToFile = os.path.dirname(__file__)
        # print("Here: ", pathToFile)
        # os.environ["PATH"] += os.pathsep + os.path.join(
        #     os.path.dirname(sys.executable), "test")

        # path = ""
        # os.system(path)
        # print("Done!")
        develop.run(self)
        # if os.name == "posix":
        #     print("Installed on Linux or Mac")
        #     path = "export PATH=$PATH" + os.pathsep + pathToFile
        # if os.name == "nt":
        #     print("Installed on Windows")
        #     oldPath = os.environ["PATH"]
        #     print("Here: ", oldPath)
        #     path = "set PATH=%PATH%" + os.pathsep + pathToFile
        # print("Here: ", path)
        # subprocess.run(path, shell=True, check=True)


class PostInstallCommand(install):

    def run(self):
        # install.run(self)
        if os.name == "posix":
            if sys.platform == "linux" or sys.platform == "linux2":
                print("Installing python3-tk")
                os.system("sudo apt-get install python3-tk")

        install.run(self)


here = pathlib.Path(__file__).parent.resolve()
long_decription = (here / "README.md").read_text(encoding="utf-8")
packagesToInstall = ["requests >= 2.28.1"]

if os.name == "posix":
    if sys.platform != "linux" or sys.platform != "linux2":
        packagesToInstall.append("tk")
    # else:
    #     packagesToInstall.append("python3-tk")

if os.name == "nt":
    packagesToInstall.append("tk")

setup(
    name="Codelock-CLI-demo",
    version="1.0.3",
    description="A cli for codelock development server",
    author="Codelock",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="codelock, cli",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    extras_require={
        "dev": ["shutil", "requests", "tk"]
    },
    install_requires=packagesToInstall,
    entry_points={
        "console_scripts": [
            "codelock=codelock:run"
        ]
    },
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand
    },
)
