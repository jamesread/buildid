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
		writeFile file: 'README.txt', text: "Fedora"
		unstash "binzip"

		echo "${WORKSPACE}"

		sh 'rm -rf SOURCES'
		sh 'mv dist SOURCES'
		sh 'mkdir -p SPECS'
		sh 'unzip -jo SOURCES/buildid.zip "buildid-*/var/buildid.spec" "buildid-*/buildid" -d SPECS/'
		sh 'buildid -f rpmmacro > SPECS/buildid.rpmmacro'
		sh "rpmbuild -ba SPECS/buildid.spec --define '_topdir ${WORKSPACE}' "
	}}}, 

	rpmEl6: { node { ws {
		writeFile file: 'README.txt', text: "EL6"
		unstash "binzip"
		sleep 10
	}}}, 
	
	rpmEl7: { node { ws {
		writeFile file: 'README.txt', text: "EL7"
		unstash "binzip"
		sleep 10
	}}}, 

	failFast: true
)
