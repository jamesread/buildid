VERSION:=$(shell ./buildid/app.py -k version.formatted.short)

default: clean tests
	rm -rf dist/buildid-$(VERSION)/
	mkdir -p dist/buildid-$(VERSION)/

	cp .buildid dist/buildid-$(VERSION)/buildid
	cp README.md dist/buildid-$(VERSION)/

	mkdir -p dist/buildid-$(VERSION)/var
	cp var/buildid.spec dist/buildid-$(VERSION)/var/

	mkdir -p dist/buildid-$(VERSION)/doc
	cp doc/buildid.1.gz dist/buildid-$(VERSION)/doc/

	mkdir -p dist/buildid-$(VERSION)/app
	cp buildid/*.py dist/buildid-$(VERSION)/app/
	cd dist && zip -r buildid.zip buildid-$(VERSION)

tests:
	py.test

rpm:
	rpmbuild -ba var/buildid.spec

clean:
	rm -rf dist

.PHONY: clean default tests
