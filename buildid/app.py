#!/usr/bin/python

import argparse
import ConfigParser as configparser

argparser = argparse.ArgumentParser();
argparser.add_argument("-n", "--newBuild", action = 'store_true');
argparser.add_argument("--format", "-f", default = "ini", choices = ["ini"]);
argparser.add_argument("--platform", default = None)
argparser.add_argument("-d", "--debug", action = 'store_true')
argparser.add_argument("-k", "--key", help = "print the value of just one key")
argparser.add_argument("-K", "--keySearch", help = "print the values where the key matches this search term")
argparser.add_argument("-w", "--filename", default = ".buildid")
argparser.add_argument("-q", "--quiet", action = 'store_true')
argparser.add_argument("-p", "--plain", action = "store_true")
argparser.add_argument("-u", "--update", action = "store_true")
args = argparser.parse_args()

if __name__ == "__main__":
	from classes import BuildIdFileHandlerIni, printInfo, getVersionFromReaders, saveVersion, buildProperties

	fileHandlers = {
		"ini": BuildIdFileHandlerIni(),
	}

	configDefaults = {
		"title": "Untitled Project"
	}

	cfgparser = configparser.ConfigParser(defaults = configDefaults)
	cfgparser.add_section("project")
	cfgparser.read("buildid.cfg");


	for section in cfgparser.sections():
		if cfgparser.has_option(section, "type") and cfgparser.has_option(section, "translator"):
			typeOfThing = cfgparser.get(section, "type")

			translatorConfig = dict()
			
			for cfg in cfgparser.items(section):
				translatorConfig[cfg[0]] = cfg[1]

			inst = parseVersionTranslator(translatorConfig)

			if isinstance(inst, VersionReader):
				versionReaders.append(inst)

			if isinstance(inst, VersionWriter):
				versionWriters.append(inst)


	if args.debug:
		printDebug("Readers:" + str(versionReaders))
		printDebug("Writers:" + str(versionWriters))	

	properties = dict()
	properties["project.title"] = cfgparser.get("project", "title")

	handler = fileHandlers[args.format]

	if args.newBuild:
		version = getVersionFromReaders()

		saveVersion(version)

		handler.write(buildProperties(version));

		printInfo("Wrote file: " + handler.getFilename() + ". View the file or just run `buildid` again to see all the properties.");

	else:
		if not handler.fileExists():
			printInfo("There is no buildid file. Use -n to create a new build.")
		else:
			properties = handler.read()

			if args.key:
				if args.key in properties:
					print(properties[args.key])
				else: 
					print(args.key + " was not found.");
			elif args.keySearch:
				for key in properties:
					if args.keySearch in key:
						print(handler.toStringSingle(key))
			else:
				if not args.quiet:
					printInfo("Printing buildid from file: " + handler.getFilename())
					printInfo("You can output a single property with -k <property-name>")
					printInfo("or see all these properties again without this message with -q");
					print("")

				print(handler.toString())