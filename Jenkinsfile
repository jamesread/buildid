node {
	stage "Package"
	checkout scm
	sh "buildid -n"
	sh "make"

	checkpoint "packaged-pre-deploy"

	stage "Deploy"
	echo "Test"
}
