VERSION:=$(shell ./buildid/app.py -k version.formatted.short)

default: newbuild clean tests
	rm -rf dist/buildid-$(VERSION)/
	mkdir -p dist/buildid-$(VERSION)/

	cp .buildid dist/buildid-$(VERSION)/buildid
	cp .buildid.rpmmacro dist/buildid-$(VERSION)/

	cp README.md dist/buildid-$(VERSION)/

	mkdir -p dist/buildid-$(VERSION)/var
	cp var/buildid.spec dist/buildid-$(VERSION)/var/

	mkdir -p dist/buildid-$(VERSION)/doc
	cp doc/buildid.1.gz dist/buildid-$(VERSION)/doc/

	mkdir -p dist/buildid-$(VERSION)/app
	cp buildid/*.py dist/buildid-$(VERSION)/app/
	
	cd dist && zip -r buildid.zip buildid-$(VERSION)

newbuild:
	buildid -n 
	buildid -qf rpmmacro > .buildid.rpmmacro

tests:
	py.test tests

test:tests

rpm:
	rpmbuild -ba var/buildid.spec

clean:
	rm -rf dist

.PHONY: clean default tests test
