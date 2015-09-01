#!/usr/bin/python

import time
import re
import platform
from socket import gethostname
import os
import subprocess
import abc
from lxml import etree

import app

args = app.args
properties = dict()

try:
	from colorama import init as coloramainit, Fore, Style

	coloramainit()
except:
	pass

class VersionIdentifier:
	major = 0
	minor = 0
	revision = 0
	release = ""

	def getFormattedShort(self):
		return str(self.major) + "." + str(self.minor) + "." + str(self.revision)

	def getFormattedGnu(self):
		if isEmpty(self.release):
			rel = ''
		else:
			rel = '-' + str(self.release)

		return str(self.major) + "." + str(self.minor) + "." + str(self.revision) + rel

	def getFormattedWin(self):
		if isEmpty(self.release):
			rel = '.0';
		else:
			rel = '.' + str(self.release)

		return str(self.major) + "." + str(self.minor) + "." + str(self.revision) + rel

	def getFormattedPlatform(self):
		return self.getFormattedGnu()

	def __cmp__(self, othr):
		if not isinstance(othr, VersionIdentifier):
			return False 

		return cmp(
			(self.major, self.minor, self.revision),
			(othr.major, othr.minor, othr.revision)
		)

def parseVersionTranslator(config):
	translator = config["translator"].lower()

	if translator == "plainfile":
		return VersionTranslatorPlainFile(config)

	if translator == "rpmspec":
		return VersionTranslatorRpmSpec(config)

	printWarn("Translator not supported: " + translator)

class VersionTranslator:
	def __init__(self, config = None):
		self.config = config

	def name(self):
		return self.__class__.__name__

	def __str__(self):
		return self.name()

class VersionReader(VersionTranslator):
	def isReadable(self):
		return True

	@abc.abstractmethod
	def read(self):
		pass

class VersionWriter(VersionTranslator):
	@abc.abstractmethod
	def write(self):
		pass

class VersionTranslatorRpmSpec(VersionReader):
	def read(self):
		return VersionIdentifier()

class VersionTranslatorPlainFile(VersionReader, VersionWriter):
	def read(self):
		version = VersionIdentifier()
	
		try:
			versionFile = open('VERSION', 'r')
			content = versionFile.read()
			versionFile.close()

			version = parseVersion(content)
		except IOError as e:
			pass
		except Exception as e:
			print(e)

		return version

	def write(self, version):
		f = open("VERSION", "w")
		f.write(version.getFormattedGnu())
		f.close()

	def isReadable(self):
		return os.path.exists("VERSION")

class VersionTranslatorPomFile(VersionReader):
	def isReadble(self):
		return os.path.exists("pom.xml")

	def read(self):
		version = VersionIdentifier()

		try:
			version = reallyCheekyXpath("pom.xml", "//project/version/text()")[0]
			version = parseVersion(version)
		except:
			pass

		return version

def parseVersion(versionString):
	version = VersionIdentifier()

	m = re.search("(\d+)\.(\d+)\.(\d+)[\.-]*(\d*)", versionString)

	if m != None:
		version.major = int(m.group(1))
		version.minor = int(m.group(2))
		version.revision = int(m.group(3))
		version.release = m.group(4)
	elif args.debug:
		print("VERSION file did not match regex.")

	return version

def reallyCheekyXpath(filename, xpath):
	f = open(filename, "r")
	xml = f.read()
	f.close()

	# aherm
	xml = re.sub('xmlns=".+"', "", xml)

	pomTree = etree.fromstring(xml)
	res = pomTree.xpath(xpath)

	return res

versionReaders = [ VersionTranslatorPlainFile(), VersionTranslatorPomFile() ]
versionWriters = [ VersionTranslatorPlainFile() ]

def printWarn(message):
	printPrefix("WARN", message, 3)

def printInfo(message):
	printPrefix("INFO", message, 4)

def printDebug(message):
	printPrefix("DEBG", message, 1)

def printPrefix(prefix, message, color = None):
	startColor = ""
	endColor = ""

	if hasColors():
		if color == 1:
			startColor = Style.BRIGHT + Fore.RED
			endColor = Style.RESET_ALL

		if color == 3:
			startColor = Style.BRIGHT + Fore.MAGENTA
			endColor = Style.RESET_ALL

		if color == 4: 
			startColor = Style.BRIGHT + Fore.BLUE
			endColor = Style.RESET_ALL

	print("[" + startColor + prefix + endColor + "] " + str(message));

def hasColors():
	hasColors = True 

	try: 
		if Fore.BLACK:
			pass
	except:
		hasColors = False

	if args.plain:
		hasColors = False

	return hasColors

class BuildIdFileHandler:
	def getFilename(self):
		if args.filename == ".buildid":
			return self.getDefaultFilename()
		else:
			return args.filename

	def getDefaultFilename(self):
		return args.filename
	
	def fileExists(self):
		return os.path.exists(self.getFilename())

	def toString(self):
		raise NotImplementedError()

	def read(self):
		pass
		#raise NotImplementedError()

	def write(self, properties):
		handle = open(self.getFilename(), "w");
		handle.write(self.toString());
		handle.close()

class BuildIdFileHandlerIni(BuildIdFileHandler):
	def getDefaultFilename(self):
		return ".buildid"

	def toString(self):
		global properties 

		buf = ""
		for key in sorted(properties):
			buf += self.toStringSingle(key) + "\n"

		return buf.strip()

	def toStringSingle(self, key):
		global properties 

		return (key + "=" + str(properties[key]))


	def read(self):
		global properties
		properties = dict()

		content = open(self.getFilename(), 'r').readlines()

		for line in content:
			key, value = line.strip().split("=");
			
			properties[key] = value

		return properties


def getVersionFromReaders():
	versions = []

	for reader in versionReaders:
		if reader.isReadable():
			versionFromReader = reader.read()

			versions.append(versionFromReader)

			printInfo("Reading version using: " + reader.name() + " = " + versionFromReader.getFormattedGnu() )
	
	tmp = None
	for version in versions:
		if tmp == None:
			tmp = version
			continue

		if tmp != version:
			printWarn("All version readers are not consistant! Using the first: " + versions[0].getFormattedGnu());
			printWarn("Or re-run buildid with -u to update version sources")

			break

	return versions[0] # first one only at the mo


def runCommand(cmd):
	process = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE)
	output = "".join(process.stdout.readlines()).strip()

	return output

def checkGitIgnore():
	if not os.path.exists(".gitignore"):
		return 

	gitIgnoreFile = open(".gitignore", 'r');

	content = gitIgnoreFile.read()

	if "buildid" not in content:
		printWarn("You should ignore your buildid in .gitignore.")

	gitIgnoreFile.close()


def isGit():
	checkGitIgnore();
		
	return os.path.exists(".git")

def getGitRevision():
	return runCommand("git rev-parse HEAD")

def getGitBranch():
	return runCommand("git branch | awk '{print $2}'")

def isEmpty(value):
	if value == None:
		return True

	if value == 0:
		return True

	if value == '':
		return True

	return False

def getCommitTag():
	if isGit():
		return getGitRevision()
	else:
		return '00000'

def isReleaseBuild():
	return False

def getSourceTag():
	global properties 

	if isReleaseBuild() and isEverythingCommited():
		return getCommitTag()
	else:
		return properties['timestamp']

def getPackageTag(version):
	return version.getFormattedPlatform() + "-" + getSourceTag()

def isEverythingCommited():
	return False

def saveVersion(version):
	for writer in versionWriters:
		writer.write(version)

def buildProperties(version):
	global properties

	properties["timestamp"] = str(int(time.time()))

	properties["version.major"] = version.major
	properties["version.minor"] = version.minor
	properties["version.release"] = version.release
	properties["version.revision"] = version.revision
	properties["version.formatted.gnu"] = version.getFormattedGnu()
	properties["version.formatted.short"] = version.getFormattedShort()
	properties["version.formatted.win"] = version.getFormattedWin()
	properties["tag"] = getPackageTag(version)
	properties["buildhost.platform"] = platform.platform()
	properties["buildhost.system"] = platform.system()
	properties["buildhost.release"] = platform.release()
	properties["buildhost.version"] = platform.version()
	properties["buildhost.hostname"] = gethostname()

	if isGit():
		properties["git.branch"] = getGitBranch()
		properties["git.revision"] = getGitRevision();
		properties["git.revision.short"] = getGitRevision()[0:7];


	return properties

def getFileHandlers():
	return {
		"ini": BuildIdFileHandlerIni(),
	}

