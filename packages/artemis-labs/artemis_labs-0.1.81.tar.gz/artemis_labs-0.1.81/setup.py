import setuptools
import os

with open('setup_config.txt') as f:
    config = f.read()
    package_version = config.split('=')[1]

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

setuptools.setup(
    name="artemis_labs",
    version=package_version,
    author="Artemis Labs",
    author_email="austinmccoy@artemisar.com",
    description="Artemis Labs",
    packages= setuptools.find_packages('src'),
    package_dir={'': 'src'},
    package_data={'artemis_labs': ['htdocs/**/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points ={
        'console_scripts': [
            'artemis_labs = artemis_labs.artemis_labs_base:main'
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        'imageio',
        'websockets',
        'numpy',
        'matplotlib',
        'seaborn',
        'pandas',
        'licensing'
    ]
)
