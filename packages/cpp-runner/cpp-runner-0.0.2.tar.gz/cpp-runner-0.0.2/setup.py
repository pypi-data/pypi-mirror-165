import setuptools


setuptools.setup(
    name='cpp-runner',
    version='0.0.2',
    license="MIT",
    entry_points={
        'console_scripts': ['crun=crun.crun:cli'],
    },
    packages=["crun"],
    url="https://github.com/macaquedev/cpp-runner",
    author='Alex Pylypenko',
    author_email="macaquedev@gmail.com",
    description='A simple, small command line utility to run cpp files.',
    long_description=open('README.md').read(),
    long_description_content_type="text/x-rst",
    install_requires=[
        'setuptools',
        'pip'
    ],
    python_requires='>=3.3'
)
