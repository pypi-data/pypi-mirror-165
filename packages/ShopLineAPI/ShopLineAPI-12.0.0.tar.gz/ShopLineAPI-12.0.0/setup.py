from setuptools import setup

NAME = "ShopLineAPI"
exec(open("shopline/version.py").read())
DESCRIPTION = "ShopLine API for Python"
LONG_DESCRIPTION = """\
The ShopLine library allows python developers to programmatically
access the admin section of stores using an ActiveResource like
interface similar the ruby ShopLine API gem. The library makes HTTP
requests to ShopLine in order to list, create, update, or delete
resources (e.g. Order, Product, Collection)."""

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="HerbLee",
    author_email="herb2sy@gmail.com",
    url="https://github.com/HerbLee/shopline_python_api",
    packages=["shopline", "shopline/resources", "shopline/utils"],
    scripts=["scripts/shopline_api.py"],
    license="MIT License",
    install_requires=[
        "pyactiveresource>=2.2.2",
        "PyJWT >= 2.0.0",
        "PyYAML",
        "six",
    ],
    test_suite="test",
    tests_require=[
        "mock>=1.0.1",
    ],
    platforms="Any",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
