import setuptools

# Load README
with open('README.md', 'r', encoding='utf8') as file:
    long_description = file.read()

# Define package metadata
setuptools.setup(
    name='goatpie',
    version='0.1.2',
    author='Martin Folkers',
    author_email='webmaster@refbw.de',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://codeberg.org/refbw/goatpie',
    license='MIT',
    project_urls={
        'Issues': 'https://codeberg.org/refbw/goatpie/issues',
    },
    entry_points='''
        [console_scripts]
        goatpie=goatpie.cli:cli
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'arrow',
        'click',
        'pandas',
        'plotext',
        'requests',
        'rich',
        'textual',
    ],
    python_requires='>=3.7',
)
