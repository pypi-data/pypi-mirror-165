from setuptools import setup


with open('README.md') as f:
    long_description = f.read()
    description = long_description.split('\n')[2]


setup(
    name='magicli',
    version='0.2.0',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    py_modules=[
        'magicli',
    ],
    install_requires=[
        'pargv'
    ],
    extras_require={
        'dev':[
            'pytest',
        ]
    },
    keywords=[
        'python',
        'cli'
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: OS Independent",
    ]
)
