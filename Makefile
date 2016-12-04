db.sqlite3:
	python3 manage.py migrate --run-syncdb


.PHONY: deploy
deploy:
	rm -f db.sqlite3
	python3 manage.py migrate --run-syncdb


.PHONY: test
test:
	DJANGO_SETTINGS_MODULE=ivreg.settings py.test -vvx --tb=native tests
