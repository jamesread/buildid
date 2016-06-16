#!groovy

properties(
	[
		[
			$class: 'jenkins.model.BuildDiscarderProperty', strategy: [$class: 'LogRotator', numToKeepStr: '10', artifactNumToKeepStr: '10']
		]
	]
)

stage "Build"

node {
	checkout scm
	sh "buildid -n"
	sh "make"

	stash includes: 'dist/*.zip', name: 'binzip'
}

stage "Package & Publish"

def buildRpm(dist) {
	env.WORKSPACE = pwd() 

	unstash "binzip"

	sh 'rm -rf SOURCES RPMS SRPMS BUILDROOT BUILD SPECS'
	sh 'mv dist SOURCES'
	sh 'mkdir -p SPECS'
	sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/.buildid.rpmmacro" -d SPECS/'
	
	sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ${env.WORKSPACE}' --define 'dist ${dist}'"

	archive 'RPMS/noarch/*.rpm'
}

parallel (
	rpmFedora: { node { ws("${pwd()}/rpmFedora") {
		buildRpm("fc23")
	}}}, 

	rpmEl6: { node { ws("${pwd()}/rpmEl6") {
		buildRpm("el6")
	}}}, 
	
	rpmEl7: { node { ws("${pwd()}/rpmEl7") {
		buildRpm("el7")
	}}}, 

	failFast: true
)

node { 
	(manager.build.getArtifacts()).each {
		println "Artifact: ${it}"
	}
}
