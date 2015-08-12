VERSION:=$(shell ./buildid -k version.formatted.short)

default: clean
	rm -rf dist/buildid-$(VERSION)/
	mkdir -p dist/buildid-$(VERSION)/

	cp .buildid.ini dist/buildid-$(VERSION)/buildid.ini
	cp README.md dist/buildid-$(VERSION)/

	mkdir -p dist/buildid-$(VERSION)/var
	cp var/buildid.spec dist/buildid-$(VERSION)/var/

	mkdir -p dist/buildid-$(VERSION)/doc
	cp doc/buildid.1.gz dist/buildid-$(VERSION)/doc/

	cp buildid dist/buildid-$(VERSION)/
	cd dist && zip -r buildid.zip buildid-$(VERSION)

rpm:
	rpmbuild -ba var/buildid.spec

clean:
	rm -rf dist

.PHONY: clean default
