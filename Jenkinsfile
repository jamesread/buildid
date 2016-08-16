#!groovy

properties(
	[
		[
			$class: 'jenkins.model.BuildDiscarderProperty', strategy: [$class: 'LogRotator', numToKeepStr: '10', artifactNumToKeepStr: '10']
		]
	]
)

def buildRpm(dist) {
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

	checkout scm
	sh "buildid/app.py -n"
	sh "make"

	stage "Package & Publish"

	docker.image("centos:7").inside {
		sh "cat /etc/os-release"
		sh "ls; pwd; env"
	}

	docker.image("centos:6").inside {
		sh "cat /etc/redhat-release"
		sh "ls; pwd; env"
	}

	docker.image("fedora:23").inside {
		sh "cat /etc/os-release"
		sh "ls; pwd; env"
	}

	buildRpm("fc23")
	buildRpm("el6")
	buildRpm("el7")	

	for (Object artifact : currentBuild.rawBuild.getArtifacts()) {
			println "Artifact: ${artifact}"
	}
}

