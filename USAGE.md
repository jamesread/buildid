# Ant

<project>
	...
	<exec executable = "buildid">
		<arg value = "-n">
	</exec>
	<loadproperties srcFile = ".buildid.ini" />
	...
	<echo>Version ${version.formatted.short}</echo>
	...
</project>

# Gradle

Cannot quite figure out the best way to do this with Gradle yet. ;( Here is 
what I have so far... 

```

def generateBuildId() {
	"buildid -n".exec()

	Properties buildInfo = new Properties()
	buildid.load(new File(".buildid.ini").newReader());

	return buildid
}

Properties buildid = generateBuildId()
version = buildid.get("version.formatted.gnu");
```
