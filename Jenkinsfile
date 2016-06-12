properties(
	[
		[
			$class: 'jenkins.model.BuildDiscarderProperty', strategy: [$class: 'LogRotator', numToKeepStr: '10', artifactNumToKeepStr: '10']
		]
	]
)

stage "Package"

node {
	checkout scm
	sh "buildid -n"
	sh "make"

	stash includes: 'dist/*.zip', name: 'binzip'
}

stage "Depoy"

parallel (
	rpmfedora: { node { ws "rpmFedora" {
		writeFile file: 'README.txt', text: "Fedora"
		unstash "binzip"
		sleep 10
	}}}, 

	rpmel6: { node { ws "rpmEl6" {
		writeFile file: 'README.txt', text: "EL6"
		unstash "binzip"
		sleep 10
	}}}, 
	
	rpmel7: { node { ws "rpmEl7" {
			writeFile file: 'README.txt', text: "EL7"
			unstash "binzip"
			sleep 10
	}}},

	failFast: true
)
