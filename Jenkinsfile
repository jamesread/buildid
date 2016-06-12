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
	branch("rpmFedora") {
		writeFile file: 'README.txt', text: "Fedora"
		unstash "binzip"
		sleep 10
	}, 

	branch("rpmEl6") {
		writeFile file: 'README.txt', text: "EL6"
		unstash "binzip"
		sleep 10
	}, 
	
	branch("rpmEl7") {
			writeFile file: 'README.txt', text: "EL7"
			unstash "binzip"
			sleep 10
	},

	failFast: true
)

branch(String label, Closure body) {
	label: { node(label) { ws(label) {
		body.call()
	}}}
}
