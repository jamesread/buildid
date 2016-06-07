stage "Package"

node {
	checkout scm
	sh "buildid -n"
	sh "make"

	stage "Deploy"
	echo "Test"
}

stage "Depoy"

parallel rpmFedora: {
	node {
		writeFile file: 'README.txt', text: "Fedora"
		sleep 10
	}
}, rpmEl6: {
	node {
		writeFile file: 'README.txt', text: "EL6"
		sleep 10
	}
}, rpmEl7: {
	node {
		writeFile file: 'README.txt', text: "EL7"
		sleep 10
	}
}, 
failFast: true
