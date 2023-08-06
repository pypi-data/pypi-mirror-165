import argparse
import logging
from alation.cli.core import auth
# from command_modules import article


def main():

    mainparser = argparse.ArgumentParser(description="Alation CLI")
    mainparser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true")
    subparsers = mainparser.add_subparsers(dest="subcommand")

    def argument(*names_or_flags, **kwargs):
        return names_or_flags, kwargs

    def subcommand(*subparser_args, parent=subparsers):
        def decorator(func):
            parser = parent.add_parser(func.__name__, description=func.__doc__)
            for args, kwargs in subparser_args:
                parser.add_argument(*args, **kwargs)
            parser.set_defaults(func=func)
        return decorator


    @subcommand(
        argument("-i", "--instance",
                 help="name of Alation instance: {this value}.alationcloud.com"),
        argument("-u", "--user", help="Username or email"),
        argument("-p", "--password", help="Password")
    )
    def login(args):
        auth.login(args.instance, args.user, args.password)

    args = mainparser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    if args.subcommand is None:
        mainparser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
    #auth.say("lion")
