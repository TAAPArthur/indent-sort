pkgname := indent-sort

install:
	install -D -m 0755 "indent-sort.py" "$(DESTDIR)/usr/bin/$(pkgname)"
test:
	(cd Tests; ./tests.sh)

uninstall:
	rm "$(DESTDIR)/usr/bin/$(pkgname)"
