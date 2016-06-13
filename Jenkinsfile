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
		unstash "binzip"

		sh 'rm -rf SOURCES RPMS SRPMS BUILDROOT BUILD'
		sh 'mv dist SOURCES'
		sh 'mkdir -p SPECS'
		sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/buildid" -d SPECS/'
		sh 'buildid -f rpmmacro > SPECS/buildid.rpmmacro'
		sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ./' --define 'dist fc23'"

		archive 'RPMS/noarch/*.rpm'
	}}}, 

	rpmEl6: { node { ws {
		unstash "binzip"

		sh 'rm -rf SOURCES RPMS SRPMS BUILDROOT BUILD'
		sh 'mv dist SOURCES'
		sh 'mkdir -p SPECS'
		sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/buildid" -d SPECS/'
		sh 'buildid -f rpmmacro > SPECS/buildid.rpmmacro'
		sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ./' --define 'dist el6'"

		archive 'RPMS/noarch/*.rpm'
	}}}, 
	
	rpmEl7: { node { ws {
		unstash "binzip"

		sh 'rm -rf SOURCES RPMS SRPMS BUILDROOT BUILD'
		sh 'mv dist SOURCES'
		sh 'mkdir -p SPECS'
		sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/buildid" -d SPECS/'
		sh 'buildid -f rpmmacro > SPECS/buildid.rpmmacro'
		sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ./' --define 'dist el7'"

		archive 'RPMS/noarch/*.rpm'
	}}}, 

	failFast: true
)
