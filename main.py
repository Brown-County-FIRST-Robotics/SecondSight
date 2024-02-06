#!/usr/bin/env python
import logging
import os
import sys
import SecondSight.main
import argparse

parser = argparse.ArgumentParser(prog='./main.py')
parser.add_argument('--loglevel', choices=['DEBUG', 'INFO', 'WARNING'], default='WARNING'
                    , help='Logging level')
parser.add_argument('--compress', action="store_true"
                    , help='Compress')
args = parser.parse_args(sys.argv[1:])

if not os.path.exists('logs/'):
    os.mkdir('logs')
if args.compress:
    SecondSight.main.compress()
    sys.exit()

file_handler = logging.FileHandler(filename=f'logs/{SecondSight.utils.get8601date()}')
stderr_handler = logging.StreamHandler(stream=sys.stderr)
logging.basicConfig(level=getattr(logging, args.loglevel), handlers=[file_handler, stderr_handler])

SecondSight.main.main_cli()
