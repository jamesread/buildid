#!groovy

properties(
	[
		[
			$class: 'jenkins.model.BuildDiscarderProperty', strategy: [$class: 'LogRotator', numToKeepStr: '10', artifactNumToKeepStr: '10']
		]
	]
)

def buildRpm(dist) {
	deleteDir()

	unstash 'binaries'

	env.WORKSPACE = pwd() 

	sh 'rm -rf SOURCES RPMS SRPMS BUILDROOT BUILD SPECS'
	sh 'mkdir -p SPECS SOURCES'
	sh 'cp dist/buildid.zip SOURCES/'

	sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/.buildid.rpmmacro" -d SPECS/'
	
	sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ${env.WORKSPACE}' --define 'dist ${dist}'"

	archive 'RPMS/noarch/*.rpm'
}



node {
	stage "Build"

	deleteDir()
	checkout scm
	sh "buildid/app.py -n"
	sh "make"
	stash includes: "dist/*.zip", name "binaries"
}

stage "Package & Publish"

parallel 
centos7: { node {
	buildRpm("el7")
}},
centos6: { node {
	buildRpm("el6")
}}
fc24: { node { 
	buildRpm("fc24")
}}

node {
	for (Object artifact : currentBuild.rawBuild.getArtifacts()) {
			println "Artifact: ${artifact}"
	}
}

