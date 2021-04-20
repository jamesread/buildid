#!/usr/bin/env python3

import os
import logging
import configargparse
from classes import BuildIdFileHandlerIni, BuildIdFileHandlerRpmMacros, VersionHelpers, BuildId # parse_version_translators_from_config

def get_argument_parser():
    argparser = configargparse.ArgumentParser(default_config_files = ['buildid.cfg'])
    argparser.add_argument("-n", "--newBuild", action = 'store_true')
    argparser.add_argument("-f", "--outputFormat", default = "ini", choices = ["ini", "rpmmacro"])
    argparser.add_argument("-F", "--inputFormat", default = "ini", choices = ["ini", "rpmmacro"])
    argparser.add_argument("--platform", default = None)
    argparser.add_argument("-d", "--debug", action = 'store_true')
    argparser.add_argument("-i", "--info", action = 'store_true' )
    argparser.add_argument("-k", "--key", help = "print the value of just one key")
    argparser.add_argument("-K", "--keySearch", help = "print the values where the key matches this search term")
    argparser.add_argument("-w", "--filename", default = None)
    argparser.add_argument("-W", "--writeCopy", default = None)
    argparser.add_argument("-q", "--quiet", action = 'store_true')
    argparser.add_argument("-p", "--plain", action = "store_true")
    argparser.add_argument("-u", "--update", action = "store_true")

    return argparser

def init_logging():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

def get_handler_for_filetype(filetype):
    file_handlers = {
        "ini": BuildIdFileHandlerIni(),
        "rpmmacro": BuildIdFileHandlerRpmMacros(),
    }

    return file_handlers[filetype]

def main_new_build():
    vh = VersionHelpers()

    build = BuildId()
    build.set_version(vh.get_version_from_readers())

    vh.write_all_version_writers(build.version)

    outputHandler = get_handler_for_filetype(args.outputFormat)
    outputHandler.write(build)

    logging.info("Wrote file: %s/%s. View the file or just run `buildid` again to see all the properties.", os.getcwd(), outputHandler.get_filename())
    print("")
    print(outputHandler.to_string(build) + "\n")

def main_current_build():
    inputHandler = get_handler_for_filetype(args.inputFormat)

    if not inputHandler.file_exists():
        logging.info("There is no buildid file. Use -n to create a new build.")

        return

    buildid = BuildId()
    inputHandler.read(buildid)

    outputHandler = get_handler_for_filetype(args.outputFormat)

    if args.key:
        if args.plain:
            key_ending = ""
        else:
            key_ending = "\n"

        if args.key in buildid:
            print(buildid[args.key], end=key_ending)
        else:
            print(args.key + " was not found.", end=key_ending)
    elif args.keySearch:
        for key in buildid:
            if args.keySearch in key:
                print(outputHandler.to_string_single(buildid, key))
    else:
        if not args.quiet:
            logging.info("Printing buildid from file: %s", inputHandler.get_filename())
            logging.info("You can output a single property with -k <property-name>")
            logging.info("or see all these properties again without this message with -q")
            print("")

            if args.writeCopy is not None:
                outputHandler.write(filename = args.writeCopy)
            else:
                print(outputHandler.to_string(buildid))


if __name__ == "__main__":
    init_logging()

    args = get_argument_parser().parse_args()

    if args.newBuild:
        main_new_build()
    else:
        main_current_build()
