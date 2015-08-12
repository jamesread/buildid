# Gradle

```
"buildid -n".exec();
Properties buildid = new Properties();
buildid.load(new File(".buildid.ini").newReader())

version = buildid.get("version.formatted.gnu");
gitRevision = buildid.get("git.revision")
```
