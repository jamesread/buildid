# buildid
`buildid` is a small utility that runs at build-time and gathers up identity 
properties for a build, and makes it easy to keep that build identity from 
build-time all the way through to run-time. 

The public site is published here; http://jamesread.github.io/buildid/

## What is wrong with just using version numbers?

* What does the number actually tell me?
* Which branch did this build come from?
* Which source commit does a build come from?
* What happens if I forget to increment the version number?
* Version numbers have no meaning in nightly or development builds

## What does this buildid utility do?

### Developers: Where did this running code came from?

```
user@host: buildid 
...
git.commit=dacab494b5b355e4a1a0e856c672b3cbd421ab0a
git.branch=new-feat-2
timestamp=1438623621
...
```

### Sysadmins: What changed compared to an installed package?

If your stuff came from an **RPM**, no point in replicating working functionality.
```
user@host: cd /opt/myproject/
user@host: ./buildid --changes
myproject was installed via an RPM, use \`rpm -qv myproject\` to verify it.
```

But if you released a **zip** file, this is how it would work;

```
user@host: buildid --changes
ORIGINAL_PACKAGE=myproject-1.0.3-windows.zip
CHANGED_FILES: etc/myproject/configuration.ini (M), /etc/myproject/bar (N)
```

### Developers need version numbers for packages in a CI build

You can run `buildid` from a Jenkins job, for example.

```
user@host: buildid
COMMIT=dacab494b5b355e4a1a0e856c672b3cbd421ab0a
BRANCH=new-feat-2
TYPE=nightly
VERSION_STRING_SIMPLE=1.0.0
PACKAGE_NAME-myproject-1.0.0-win
PACKAGE_FILENAME-myproject-1.0.0-win.zip
```

## FAQ 

### Using buildid with Gradle

	plugins {
		id "com.github.jamesread.buildid" version "1.10"
	}

	buildid.newBuild()
	
	println buildid.get("tag")
	println buildid.get("version.formatted.short")
	... etc


### How does this work?

buildid generates a bunch of facts about your build by looking at files in the
current directory, it can output these facts in various formats, with a 
properties file being the default. 

You can define various presets too, in a configuration file `.buildid.cfg`

In keep track of builds, a .buildid file is generated at build time. 

### I want a `.buildid` file in different formats

Use the `-f` flag to specify `properties`, `json` or `yaml`. 

test. 2.
