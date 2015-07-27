# bundleid
**Version numbers suck.** Identify bundles of stuff instead. 

A **bundle of stuff** can be a checked out source code repository or even a 
released package like a .RPM or .ZIP

# What can buildid do?

## Developers fixing bugs want to know precisely where running code came from

```
user@host: bundleid 
COMMIT=dacab494b5b355e4a1a0e856c672b3cbd421ab0a
BRANCH=new-feat-2
BUILDDATE=2015-07-27
```

## Sysadmins want to know what changed compared to an installed package

If your stuff came from an **RPM**, no point in replicating working functionality.
```
user@host: ./bundleid --changes
foo was installed via an RPM, use \`rpm -qv foo\` to verify it.
```

But if you released a **zip** file, this is how it would work;

```
user@host: bundleid --changes
ORIGINAL_PACKAGE=foo-1.0.3-windows.zip
CHANGED_FILES: etc/foo/configuration.ini (M), /etc/foo/bar (N)
```

## Developers need version numbers for packages in a CI build

You can run `buildid` from a Jenkins job, for example.

```
user@host: bundleid
COMMIT=dacab494b5b355e4a1a0e856c672b3cbd421ab0a
BRANCH=new-feat-2
TYPE=nightly
VERSION_STRING_SIMPLE=1.0.0
```

# FAQ 

## How does this work?

bundleid generates a bunch of facts about your bundle by looking at files in the
current directory, it can output these facts in various formats, with a 
properties file being the default. 

You can define various presets too, in a configuration file .bundleid.cfg

In keep track of bundles, a .bundleid file is generated at build time. 

## I want a .bundleid file in different formats

Use the `-f` flag to specify `properties`, `json` or `yaml`. 
