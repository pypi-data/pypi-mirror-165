import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyuserside',
    version='0.0.5',
    author='Ivan Balakin',
    author_email='nekonekun@gmail.com',
    description='Small module to work with Userside ERP',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nekonekun/pyuserside',
    project_urls={
        'Bug Tracker': 'https://github.com/nekonekun/pyuserside/issues/',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.8',
    install_requires=['requests', 'aiohttp'],
)