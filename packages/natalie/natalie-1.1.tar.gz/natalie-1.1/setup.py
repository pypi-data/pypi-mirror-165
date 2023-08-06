import setuptools

setuptools.setup(
    name='natalie',
    version='1.1',
    packages=setuptools.find_packages(),
    license='GPL-3.0',
    author='jack',
    author_email='kinginjack@gmail.com',
    description='an automation software made for my friend natalie',
    install_requires=['selenium', 'colorama', 'datetime', 'cryptography', 'webdriver-manager', 'termcolor', 'tinydb'],
    python_requires='>=3.8'
)
