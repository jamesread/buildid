#!groovy

properties(
	[
		[
			$class: 'jenkins.model.BuildDiscarderProperty', strategy: [$class: 'LogRotator', numToKeepStr: '10', artifactNumToKeepStr: '10'],
			$class: 'CopyArtifactPermissionProperty', projectNames: '*'
		]
	]
)

def buildRpm(dist) {
	deleteDir()

	unstash 'binaries'

	env.WORKSPACE = pwd() 

	sh "find ${env.WORKSPACE}"

	sh 'mkdir -p SPECS SOURCES'
	sh "cp dist/buildid*.zip SOURCES/buildid.zip"

	sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/.buildid.rpmmacro" -d SPECS/'
	sh "find ${env.WORKSPACE}"
	
	sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ${env.WORKSPACE}' --define 'dist ${dist}'"

	archive 'RPMS/noarch/*.rpm'
	stash includes: "RPMS/noarch/*.rpm", name: "${dist}"
}



node {
	stage "Build"

	deleteDir()
	checkout scm
	sh "make"
	stash includes: "dist/*.zip", name: "binaries"
}

stage "Package & Publish"

node {
	buildRpm("el7")
}

node {
	buildRpm("el6")
}

node { 
	buildRpm("fc24")
}

