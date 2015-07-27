default:
	rm -rf dist/bundleid
	mkdir -p dist/bundleid/

	# run bundleid on itself.
	./bundleid -f ini > dist/bundleid/bundleid.ini

	cp bundleid dist/bundleid/
	cd dist && zip -r bundleid.zip bundleid
