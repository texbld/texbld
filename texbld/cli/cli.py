import argparse
from texbld.cli.project import add_build_args, add_run_args

from texbld.cli.scaffold import add_scaffold_args

parser = argparse.ArgumentParser(prog="texbld", description="A dockerized build tool for paper compilation")
subparsers = parser.add_subparsers()

add_scaffold_args(subparsers.add_parser('generate', aliases=['g']))
add_build_args(subparsers.add_parser('build', aliases=['b']))
add_run_args(subparsers.add_parser('run', aliases=['r']))
