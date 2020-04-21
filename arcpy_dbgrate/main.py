import click
import logging
from importlib import import_module
from os.path import join
from sys import path
from os import getcwd, environ
from dbgrate.main import cli 

# modify the local path so we can import our env.py
WORKING_DIR = getcwd()
path.append(WORKING_DIR)

@cli.command()
def create_models():
    from arcpy_dbgrate.create_models import create_models as _create_models
    _create_models()

@cli.command()
def generate_migration():
    from arcpy_dbgrate.compare_models import generate_migration as _generate_migration
    _generate_migration()

if __name__ == '__main__':
    logging.info('arcpy: Current working directory is {}'.format(WORKING_DIR))

    # create cli with context
    cli()
