.PHONY: test
test:
	DJANGO_SETTINGS_MODULE=ivreg.settings py.test -vvx --tb=native tests
