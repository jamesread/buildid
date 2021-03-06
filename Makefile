default: newbuild clean tests
	$(eval VERSION := $(shell ./buildid/app.py -k tag))

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
	
	cd dist && zip -r buildid-$(VERSION).zip buildid-$(VERSION)

newbuild:
	./buildid/app.py -n
	./buildid/app.py -qf rpmmacro > .buildid.rpmmacro

tests:
	py.test tests

test:tests

rpm:
	rpmbuild -ba var/buildid.spec

clean:
	rm -rf dist

.PHONY: clean default tests test
