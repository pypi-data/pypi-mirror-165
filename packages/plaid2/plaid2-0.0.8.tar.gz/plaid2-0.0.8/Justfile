set dotenv-load

version level:
    git diff-index --exit-code HEAD > /dev/null || ! echo You have untracked changes. Commit your changes before bumping the version.
    toml set -i pyproject.toml project.version $(semver bump {{level}} $(toml get -r pyproject.toml project.version))
    VERSION=$(toml get pyproject.toml project.version -r) && \
        git commit -am "Bump version {{level}} to $VERSION" && \
        git tag v$VERSION && \
        git push origin v$VERSION
    git push

publish:
   FLIT_USERNAME="__token__" \
   FLIT_PASSWORD=$PYPI_API_TOKEN \
   flit publish

check:
    mypy --allow-redefinition --strict plaid2/

test:
    pytest --ignore=__pypackages__

lint:
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=__pypackages__
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=__pypackages__
