import time
import re
import platform
from socket import gethostname
import os
import subprocess
import abc
import logging

from lxml import etree

class BuildId(dict):
    projectTitle = "untitled project"
    version = None

    def __init__(self):
        super().__init__()

        self["timestamp"] = str(int(time.time()))

        self["buildhost.platform"] = platform.platform()
        self["buildhost.system"] = platform.system()
        self["buildhost.release"] = platform.release()
        self["buildhost.version"] = platform.version()
        self["buildhost.hostname"] = gethostname()

        if is_in_jenkins():
            self['jenkins.url'] = os.environ['JENKINS_URL']
            self['jenkins.buildid'] = os.environ['BUILD_ID']
            self['jenkins.buildnumber'] = os.environ['BUILD_NUMBER']
            self['jenkins.buildurl'] = os.environ['BUILD_URL']
            self['jenkins.job_name'] = os.environ['JOB_NAME']
            self['jenkins.node'] = os.environ['NODE_NAME']

        if is_git():
            self["git.branch"] = get_git_branch()
            self["git.revision"] = get_git_revision()
            self["git.revision.short"] = get_git_revision()[0:7]

    def set_version(self, version):
        self.version = version

        self["tag"] = self.get_package_tag(self.version)
        self["version.major"] = self.version.major
        self["version.minor"] = self.version.minor
        self["version.release"] = self.version.release
        self["version.revision"] = self.version.revision
        self["version.formatted.gnu"] = self.version.get_formatted_gnu()
        self["version.formatted.short"] = self.version.get_formatted_short()
        self["version.formatted.win"] = self.version.get_formatted_win()

    def get_source_tag(self):
        if is_release_build() and is_everything_commited():
            return get_commit_tag()

        return self['timestamp']

    def get_package_tag(self, version):
        return version.get_formatted_platform() + "-" + self.get_source_tag()


class VersionIdentifier:
    major = 0
    minor = 0
    revision = 0
    release = ""

    def __init__(self, major = 0, minor = 0, revision = 0, release = ""):
        self.major = major
        self.minor = minor
        self.revision = revision
        self.release = release

    def get_formatted_short(self):
        return str(self.major) + "." + str(self.minor) + "." + str(self.revision)

    def get_formatted_gnu(self):
        if is_none_or_empty_string(self.release):
            rel = ''
        else:
            rel = '-' + str(self.release)

        return str(self.major) + "." + str(self.minor) + "." + str(self.revision) + rel

    def get_formatted_win(self):
        if is_none_or_empty_string(self.release):
            rel = '.0'
        else:
            rel = '.' + str(self.release)

        return str(self.major) + "." + str(self.minor) + "." + str(self.revision) + rel

    def get_formatted_platform(self):
        return self.get_formatted_gnu()

    def __eq__(self, othr):
        if isinstance(othr, VersionIdentifier):
            return (self.major, self.minor, self.release) == (othr.major, othr.minor, othr.release)

        return False

    def __str__(self):
        return self.get_formatted_gnu()

    def __repr__(self):
        return self.__str__()

def parse_version_translator(config):
    translator = config["translator"].lower()

    if translator == "plainfile":
        return VersionTranslatorPlainFile(config)

    if translator == "rpmspec":
        return VersionTranslatorRpmSpec(config)

    logging.warning("Translator not supported: %s", translator)

    return None

class VersionTranslator:
    def __init__(self, config = None):
        self.config = config

    def name(self):
        return self.__class__.__name__.replace("VersionTranslator", "")

    def __str__(self):
        return self.name()

class VersionReader(VersionTranslator):
    def is_readable(self):
        return True

    @abc.abstractmethod
    def read(self):
        pass

    @abc.abstractmethod
    def get_source(self):
        return "???"

class VersionWriter(VersionTranslator):
    @abc.abstractmethod
    def write(self, version):
        pass

class VersionTranslatorRpmSpec(VersionReader):
    def get_source(self):
        return self.config['filename']

    def read(self):
        version = regex_file(self.config["filename"], r"Version\:[ \t]+([\d\.\-]+)")
        version = parse_version(version)

        return version

class VersionTranslatorPlainFile(VersionReader, VersionWriter):
    def get_source(self):
        return 'VERSION'

    def read(self):
        version = VersionIdentifier()

        try:
            version_file = open('VERSION', 'r')
            content = version_file.read()
            version_file.close()

            version = parse_version(content)
        except IOError as e:
            print(e)

        return version

    def write(self, version):
        f = open("VERSION", "w")
        f.write(version.get_formatted_gnu())
        f.close()

    def is_readable(self):
        return os.path.exists("VERSION")

class VersionTranslatorPomFile(VersionReader):
    def is_readable(self):
        return os.path.exists("pom.xml")

    def get_source(self):
        return 'pom.xml'

    def read(self):
        version = VersionIdentifier()

        try:
            version = get_xpath_value_from_file("pom.xml", "//project/version/text()")[0]
            version = parse_version(version)
        except IOError:
            pass

        return version

def parse_version(version_string):
    version = VersionIdentifier()

    version_regex = r"(\d+)\.(\d+)\.(\d+)[\.-]*(\d*)"
    matches = re.search(version_regex, version_string)

    if matches is not None:
        version.major = int(matches.group(1))
        version.minor = int(matches.group(2))
        version.revision = int(matches.group(3))
        version.release = matches.group(4)
    else:
        logging.info("VERSION file did not match regex.")

    return version

def regex_file(filename, regex):
    f = open(filename, "r")
    content = f.read()
    f.close()

    m = re.findall(regex, content, re.MULTILINE)

    if m is not None and len(m) > 0:
        return m[0]

    return ""

def get_xpath_value_from_file(filename, xpath):
    f = open(filename, "r")
    xml = f.read()
    f.close()

    # aherm
    xml = re.sub('xmlns=".+"', "", xml)

    pom_tree = etree.fromstring(xml)
    res = pom_tree.xpath(xpath)

    return res

class BuildIdFileHandler:
    def get_filename(self):
        alts = list()
        alts.append(".buildid")
        alts.append("SPECS/.buildid")
        alts.append("SPECS/buildid")

        for filename in alts:
            if os.path.exists(filename):
                return filename

        return self.get_default_filename()

    def get_default_filename(self):
        return ".buildid"

    def file_exists(self):
        return os.path.exists(self.get_filename())

    def to_string(self, properties):
        raise NotImplementedError()

    def read(self, properties):
        raise NotImplementedError()

    def write(self, properties = None, filename = None):
        if filename is None:
            filename = self.get_filename()

        handle = open(filename, "w")
        handle.write(self.to_string(properties))
        handle.close()

class BuildIdFileHandlerIni(BuildIdFileHandler):
    def get_default_filename(self):
        return ".buildid"

    def to_string(self, properties):
        buf = ""
        for key in sorted(properties):
            buf += self.to_string_single(properties, key) + "\n"

        return buf.strip()

    def to_string_single(self, properties, key):
        return key + "=" + str(properties[key])

    def read(self, properties):
        content = open(self.get_filename(), 'r').readlines()

        for line in content:
            key, value = line.strip().split("=")

            properties[key] = value

        return properties

class BuildIdFileHandlerRpmMacros(BuildIdFileHandler):
    def to_string(self, properties):
        buf = ""

        for key in sorted(properties):
            buf += "%define " + key.replace(".", "_") + " " + str(properties[key]) + "\n"

        return buf.strip()

    def read(self, properties):
        pass

class VersionHelpers():
    versionReaders = [ VersionTranslatorPlainFile(), VersionTranslatorPomFile() ]
    versionWriters = [ VersionTranslatorPlainFile() ]

    def parse_version_translators_from_config(self, cfgparser):
        for section in cfgparser.sections():
            if cfgparser.has_option(section, "type") and cfgparser.has_option(section, "translator"):
                translatorConfig = dict()

                for cfg in cfgparser.items(section):
                    translatorConfig[cfg[0]] = cfg[1]

                inst = parse_version_translator(translatorConfig)

                if isinstance(inst, VersionReader):
                    self.versionReaders.append(inst)

                if isinstance(inst, VersionWriter):
                    self.versionWriters.append(inst)

    def get_version_from_readers(self):
        versions = []

        for reader in self.versionReaders:
            if reader.is_readable():
                versionFromReader = reader.read()

                versions.append(versionFromReader)

                logging.info("Reading version using: " + reader.name() + " (" + reader.get_source() + ") = " + versionFromReader.get_formatted_gnu() )

        tmp = None
        for version in versions:
            if tmp is None:
                tmp = version
                continue

            if tmp != version:
                logging.warning("All version readers are not consistant! Using the first: %s", versions[0].get_formatted_gnu())
                logging.warning("Or re-run buildid with -u to update version sources")

                break

        if len(versions) == 0:
            return VersionIdentifier()

        return versions[0] # first one only at the mo

    def write_all_version_writers(self, version):
        for writer in self.versionWriters:
            writer.write(version)

def run_command(cmd):
    process = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE)
    output = "".join(str(process.stdout.readlines())).strip()

    return output

def check_git_ignore():
    if not os.path.exists(".gitignore"):
        return

    gitIgnoreFile = open(".gitignore", 'r')

    content = gitIgnoreFile.read()

    if "buildid" not in content:
        logging.warning("You should ignore your buildid in .gitignore.")

    gitIgnoreFile.close()


def is_git():
    check_git_ignore()

    return os.path.exists(".git")

def is_in_jenkins():
    return "JENKINS_URL" in os.environ

def get_git_revision():
    return run_command("git rev-parse HEAD")

def get_git_branch():
    return run_command("git branch | awk '{print $2}'")

def is_none_or_empty_string(value):
    if value is None:
        return True

    if value == 0:
        return True

    if value == '':
        return True

    return False

def get_commit_tag():
    if is_git():
        return get_git_revision()

    return '00000'

def is_release_build():
    return False

def is_everything_commited():
    return False

def get_file_handlers():
    return {
        "ini": BuildIdFileHandlerIni(),
    }
