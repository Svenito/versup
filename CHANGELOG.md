### Version 1.6.4
- Fix typo in pyproject.toml

### Version 1.6.3
- Fix mypy error for list type
- Update dependencies
- Remove github workflows
- Update README

### Version 1.6.2
- Update readme
- Update dependencies
- Merge pull request #13 from Svenito/poetry-to-uv
- Modify github action to use uv
- Move versup to src folder

### Version 1.6.1
- Update dependencies
- flake8 to ignore black formatting choices
- Ignore some flake rules
- Add run on test branch
- Remove 3.8 and add 3.11, 3.12

### Version 1.6.0
- Use rich UI
- Update deps

### Version 1.5.9
- Update dependencies and isort/black code

### Version 1.5.8
- Update deps via poetry update

### Version 1.5.7
- Update dependencies for requests patch for CVE-2023-32681
- Change default main branch name to "main"

### Version 1.5.6
- Update setuptools dependency
- Fix some sphinx doc issues
- Create codeql.yml
- Change format to f-strings
- Update certifi for CVE-2022-23491

### Version 1.5.5
- fix for coveralls
- Update dependecies
- convert gitops value to str for mypy
- Update lock file
- Remove py 3.7
- Update black
- Add py 3.10 to workflow list
- Up python req for setuptools

### Version 1.5.4
- Update project details and deps

### Version 1.5.3
- handle exception when gitconfig is missing entries

### Version 1.5.2
- fix incorrect default for create_commit func

### Version 1.5.1
- Remove unused import of sys

### Version 1.5.0
- Warn about unstaged files earlier
- Only commit changed files
- Fix missing fstring in printer
- Edit github action for flake8 lint
- Fix flake8 errors
- remove walrusops
- Some refactoring
- Remove Final from conf_reader
- Add "current" option to show config
- Update docs for changelog
- Fix default value for getting commit messages
- Add install of mypy to action
- Black formatting fixes
- Merge branch 'main' of github.com:Svenito/versup into main
- Add 3.9 to Python list for actions
- Add MyPy type checking
- Add Python 3.9 to actions
- Create python-package.yml
- Update README
- Fix up coveralls run
- Add token to coveralls
- Add token to coveralls
- Clean up unused code
- Add coveralls pip install
- Update python-app.yml
- Create python-app.yml
- Update coveralls badge with main branch

### Version 1.4.0
- Get latest version tag from branch parents

### Version 1.3.0
- Remove semver import and rename class
- Add option to skip file updates
- Remove python 2 support
- Add pre* actions
- Dependency updates

### Version 1.2.0
- No longer write default to home dir

### Version 1.1.4
- Fix the python2 issue with subprocess
- Add information to developer docs

### Version 1.1.3
- Handle empty files field in config

### Version 1.1.2
- Set explicit name for CLI

### Version 1.1.1
- Fix black formatting

### Version 1.1.0
- Add .vscode to .gitignore
- Update docs and README
- Check that current branch matches main branch
- Merge branch 'python2' of github.com:Svenito/versup into python2
- Add description to pyproject.toml
- update the docs with developer guide
- Conditional deploy for travis test
- Fix command_line formattin for newer black
- Another travis config test:
- Add a diff to black to troubleshoot:
- Move black check into travis file
- Fix the unicode issues in the changelog tests
- Make Versup compatiable with Python 2
- Revert "Try different travis config"
- Try different travis config
- update the docs with developer guide
- Conditional deploy for travis test
- Fix command_line formattin for newer black
- Another travis config test:
- Add a diff to black to troubleshoot:
- Move black check into travis file
- Fix the unicode issues in the changelog tests
- Make Versup compatiable with Python 2
- Revert "Try different travis config"
- Try different travis config

### Version 1.0.3
- Add licence badge to readme
- Add Black badge to README
- Add convenient help option (#5)

### Version 1.0.2
- Add some coverage exclusions
- Fix deprecation warning for Semver
- Update dependencies
- Update docs
- Fix black formatting error
- Add Black to the test CI task
- Add some coverage exclusions
- Test coveralls submission
- Change how changelog is opened
- Improve test coverage
- update readme with travis badge

### Version 1.0.0
- Return only actual files updated
- Fix fileupdate matching in dryrun
- Print out file update status
- update poetry.lock

### Version 0.3.2
- Undo original fix for changelog entries
- Fix pyroject toml name

### Version 0.3.1
- Also update package version

### Version 0.3.0
- Fix file update newline character
- Move pycov to dev deps
- Add badges to readme
- Merge branch 'next'
- Update docs
- Merge branch 'changelog-fix' into next
- Merge branch 'dry-run-files' into next
- Fix changelog entries including last tag
- Add dry run to fileupdater
- Remove conf_parses from changelog
- Start writing docs and doc strings
- Rename project from bumper to versup
- Update version to 0.2.0
- Update version to 0.2.0

### Version 0.2.0
- 5be9c34 Fix adding of files
- 998f475 Add changed files to staging
- 3cd3bad Fix bad logic in test_dirty
- 5b806c1 remove changelog
- fd61371 heck dirty state fix
- 0d123e0 Fix commit operation
- eb7298b Handle dirty repo better on dryrun
- c7355ec Format output with newlines
- 54ed752 Create a new file for printer functions
- f068447 Fix merge conflicts
- c9841ae Add dryrun option
- 061ff86 Add pasic print functions for success and error
- ad19fd8 Update readme

