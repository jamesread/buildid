default:
	rm -rf dist/buildid
	mkdir -p dist/buildid/

	# run buildid on itself.
	./buildid -f ini > dist/buildid/buildid.ini

	cp buildid dist/buildid/
	cd dist && zip -r buildid.zip buildid
