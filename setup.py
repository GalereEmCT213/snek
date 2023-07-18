from setuptools import setup
import versioneer


if __name__ == "__main__":
    setup(
        version=versioneer.get_version(), # type: ignore
        cmdclass=versioneer.get_cmdclass(), # type: ignore
    )