from setuptools import setup
setup(
    name = 'ares-testbed-cli',
    # Version needs to change every time it is pushed up to PyPI (Python Package Index)
    version = '1.0.0',
    packages = ['otbctl'],
    author = 'Venkata Krishna Lolla',
    author_email = 'venkata.lolla@optum.com',
    maintainer = 'Venkata Krishna Lolla',
    url = 'https://github.optum.com/ecp/optum-testbed-cli',
    install_requires=[
        'python-dotenv', 'requests', 'pyyaml', 'tabulate', 'numpy', 'munch'
    ],
    scripts=['otbctl_directory.sh'],
    entry_points = {
        'console_scripts': [
            'otbctl = otbctl.__main__:main'
        ]
    }
)
