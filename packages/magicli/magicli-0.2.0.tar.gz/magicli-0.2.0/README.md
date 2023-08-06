# magiᴄʟɪ✨

Automatically turn functions of file into command line interface.

## Install

```
pip install magicli
```

## Get started

Basic usage example.
By default, every function except for the `main` function is callable through command line arguments.

```python
from magicli import magicli

def main():
    magicli()
```

### Define name of CLI in `setup.py`

In order to define the name of the CLI, it needs to be defined in the `setup.py` file. The following code sets up a sample CLI with the following folder structure.

```bash
hello/
└── setup.py
└── hello.py
```

`setup.py`

```python
from setuptools import setup

setup(
    name='hello',
    version='0.1.0',
    install_requires=[
        'magicli'
    ],
    entry_points={
        'console_scripts':[
            'hello=hello:main'
        ]
    }
)
```

`hello.py`

```python
from magicli import magicli

def main():
    magicli()

def hello(name='World', amount=1):
    for _ in range(int(amount)):
        print(f'Hello {name}!')
```

The script can then be called in the following way.

```bash
hello Name --amount 3
```

This outputs

```bash
Hello Name!
Hello Name!
Hello Name!
```

### Help message

By default, a help message will be created based on the available functions.
For the example above, calling `hello --help` will display this help message.

```bash
Usage:
    hello --name --amount
```
