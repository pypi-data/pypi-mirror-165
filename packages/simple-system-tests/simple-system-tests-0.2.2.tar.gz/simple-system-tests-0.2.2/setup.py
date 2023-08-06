import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="simple-system-tests",
    version="0.2.2",
    author="Christian Koehler",
    author_email="christian_koehler87@gmx.de",
    packages=["simple_system_tests"],
    description="Simple System Tests Environment.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisKoeh/simple-system-tests",
    license='MIT',
    python_requires='>=3.7',
    install_requires=[]
)
