import argparse
from pyhocon import ConfigFactory


def parse_args():
    parser = argparse.ArgumentParser(description='Spark Application')
    parser.add_argument(
        '-C',
        '--config',
        nargs='+',
        help=(
            'Property of the config that needs to be overridden. Set a number of key-value '
            'pairs(do not put spaces before or after the = sign). Ex: -C fabricName=dev '
            'dbConnection="db.prophecy.io" dbUserName="prophecy"'
        )
    )
    parser.add_argument('-f', '--file', help='Location of the hocon config file. Ex: -f /opt/prophecy/dev.json')
    args = parser.parse_args()

    return args


def parse_config(args):
    if args.file is not None:
        conf = ConfigFactory.parse_file(args.file)
    else:
        conf = ConfigFactory.parse_string('{}')

    # override the file config with explicit value passed
    if args.config is not None:
        for config in args.config:
            c = config.split('=', 1)
            conf.put(c[0], c[1])

    return conf
