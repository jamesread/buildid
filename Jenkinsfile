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
	rpmFedora: {
		node {
			writeFile file: 'README.txt', text: "Fedora"
			unstash "binzip"
			sleep 10
		}
	}, rpmEl6: {
		node {
			writeFile file: 'README.txt', text: "EL6"
			unstash "binzip"
			sleep 10
		}
	}, rpmEl7: {
		node {
			writeFile file: 'README.txt', text: "EL7"
			unstash "binzip"
			sleep 10
		}
	}, 
	failFast: true
)
