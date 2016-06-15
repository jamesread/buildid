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

parallel (
	rpmFedora: { node { ws {
		env.WORKSPACE = pwd() 

		unstash "binzip"

		sh 'rm -rf SOURCES RPMS SRPMS BUILDROOT BUILD SPECS'
		sh 'mv dist SOURCES'
		sh 'mkdir -p SPECS'
		sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/.buildid.rpmmacro" -d SPECS/'
		
		sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ${env.WORKSPACE}' --define 'dist fc23'"

		archive 'RPMS/noarch/*.rpm'
	}}}, 

	rpmEl6: { node { ws {
		env.WORKSPACE = pwd() 

		unstash "binzip"

		sh 'rm -rf SOURCES RPMS SRPMS BUILDROOT BUILD SPECS'
		sh 'mv dist SOURCES'
		sh 'mkdir -p SPECS'
		sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/.buildid.rpmmacro" -d SPECS/'
		sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ${env.WORKSPACE}' --define 'dist el6'"

		archive 'RPMS/noarch/*.rpm'
	}}}, 
	
	rpmEl7: { node { ws {
		env.WORKSPACE = pwd() 

		unstash "binzip"

		sh 'rm -rf SOURCES RPMS SRPMS BUILDROOT BUILD SPECS'
		sh 'mv dist SOURCES'
		sh 'mkdir -p SPECS'
		sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/.buildid.rpmmacro" -d SPECS/'
		sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ${env.WORKSPACE}' --define 'dist el7'"

		archive 'RPMS/noarch/*.rpm'
	}}}, 

	failFast: true
)

node { 
	(manager.build.getArtifacts()).each {
		println "Artifact: ${it}"
	}
}
