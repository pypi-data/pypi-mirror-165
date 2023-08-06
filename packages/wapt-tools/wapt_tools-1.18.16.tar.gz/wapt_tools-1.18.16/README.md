# WAPT tools

WAPT modules to ease version upgrades.

## How to release

Version number should be based on [Semantic Versionning](https://semver.org/).

After commiting all code to the repository, you should bump version number in wapttools/vers.py.

Depending on the change size:

  * Minor changes, bugs fix: only update the last number (PATCH)
  * Major changes, a new command is added: update the middle number (MINOR)
  * Major breaking changes: update the first number (MAJOR)

Then commit the code,tag the commit with the version number and push all (with the tag):
```
git add wapttools/vers.py
git commit -m "New version v1.17.17"
git tag -a v1.17.17 -m "v1.17.17"
git push
git push --tags
```

An helper script is executing these commands: ./release.sh
