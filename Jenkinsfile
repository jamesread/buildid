node {
	stage "Package"
	checkout scm
	sh "buildid -n"
	sh "make"

	stage "Deploy"
	echo "Test"
}
