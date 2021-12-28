pkgname := indent-sort

.PHONY: install clean test uninstall

all:

install:
	install -D -m 0755 "indent-sort.py" "$(DESTDIR)/usr/bin/$(pkgname)"

uninstall:
	rm "$(DESTDIR)/usr/bin/$(pkgname)"

test:
	(cd Tests; ./tests.sh)

clean:
	rm -f Tests/*.wrong
