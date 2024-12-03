# ============
# Main targets
# ============


# -------------
# Configuration
# -------------

$(eval venvpath     := .venv)
$(eval pip          := $(venvpath)/bin/pip)
$(eval python       := $(venvpath)/bin/python)
$(eval pytest       := $(venvpath)/bin/pytest)
$(eval bumpversion  := $(venvpath)/bin/bumpversion)


# Setup Python virtualenv
setup-virtualenv:
	@test -e $(python) || python3 -m venv $(venvpath)
	@test -e $(pytest) || $(pip) install --quiet --editable=.[test]


# ----
# Test
# ----
test: setup-virtualenv
	$(pytest)

format-js:
	brew install prettier || true
	prettier --write grafanimate


# -------
# Release
# -------

# Release this piece of software
# Synopsis:
#   make release bump=minor  (major,minor,patch)
release: bumpversion push package pypi-upload


# -------------
# Documentation
# -------------

# Build the documentation
docs-html: install-doctools
	touch doc/index.rst
	export SPHINXBUILD="`pwd`/$(sphinx)"; cd doc; make html


# ===============
# Utility targets
# ===============
bumpversion: install-releasetools
	@$(bumpversion) $(bump)

push:
	git push && git push --tags

package:
	@$(python) -m build

pypi-upload: install-releasetools
	twine upload --skip-existing --verbose dist/*{.tar.gz,.whl}

install-doctools: setup-virtualenv
	@$(pip) install --quiet --upgrade '.[docs]'

install-releasetools: setup-virtualenv
	@$(pip) install --quiet --upgrade '.[release]'


# ==========================================
#            ptrace.hiveeyes.org
# ==========================================

# Don't commit media assets (screenshots, etc.) to the repository.
# Instead, upload them to https://ptrace.hiveeyes.org/
ptrace_target := root@ptrace.hiveeyes.org:/var/www/ptrace.hiveeyes.org/htdocs/
ptrace_http   := https://ptrace.hiveeyes.org/
ptrace: check-ptrace-options
	$(eval prefix         := $(shell gdate --iso-8601))
	$(eval name           := $(shell basename '$(source)'))
	$(eval file_name      := $(prefix)_$(name))
	$(eval file_escaped   := $(shell printf %q "$(file_name)"))
	$(eval file_url       := $(shell /bin/echo -n "$(file_name)" | python -c "import sys, urllib; print urllib.quote(sys.stdin.read())"))

	$(eval upload_command := scp -P 2707 '$(source)' '$(ptrace_target)$(file_escaped)')
	$(eval media_url      := $(ptrace_http)$(file_url))

	@# debugging
	@#echo "name:         $(name)"
	@#echo "file_name:    $(file_name)"
	@#echo "file_escaped: $(file_escaped)"
	@#echo "file_url:     $(file_url)"
	@#echo "command:      $(upload_command)"

	$(upload_command)

	@echo "Access URL:    $(media_url)"

check-ptrace-options:
	@if test "$(source)" = ""; then \
		echo "ERROR: 'source' not set"; \
		exit 1; \
	fi



# -------
# Project
# -------

grafana-start:
	grafana-server --config=/usr/local/etc/grafana/grafana.ini --homepath /usr/local/share/grafana cfg:default.paths.logs=/usr/local/var/log/grafana cfg:default.paths.data=/usr/local/var/lib/grafana cfg:default.paths.plugins=/usr/local/var/lib/grafana/plugins
