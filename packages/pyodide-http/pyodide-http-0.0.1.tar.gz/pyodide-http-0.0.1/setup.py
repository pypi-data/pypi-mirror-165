from distutils.core import setup


def setup_package():
    setup(
        name="pyodide-http",
        version="0.0.1",
        author="Koen Vossen",
        author_email="info@koenvossen.nl",
        url="",
        packages=[],
        license="MIT",
        description="Patch reqeusts, urllib and urllib3 to make them work in Pyodide",
        long_description='Patch reqeusts, urllib and urllib3 to make them work in Pyodide',
        long_description_content_type="text/markdown",
        classifiers=[],
        install_requires=[],
        ext_modules=[],
    )


if __name__ == "__main__":
    setup_package()
