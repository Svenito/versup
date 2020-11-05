default_conf = {
    "force": False,  # Force the command without prompting the user
    "silent": False,  # Minimize the amount of logs
    "files": {},  # A map of `relativeFilePath: [regex, replacement, regexFlags?] | [regex, replacement, regexFlags?][]`
    "version": {
        "enabled": True,  # Bump the version number
        "initial": "0.0.0",  # Initial version
        "increments": [
            "major",
            "minor",
            "patch",
            "prerelease",
            "prepatch",
            "preminor",
            "premajor",
        ],  # List of available increments to pick from
    },
    "changelog": {
        "enabled": True,  # Enable changelog auto-updates
        "create": False,  # Create the changelog file if it doesn"t exist
        "open": True,  # Open the changelog file after bumping
        "file": "CHANGELOG.md",  # Name of the changelog file
        "version": "### Version [version]",  # Template for the version line
        "commit": "- [message]",  # Template for the commit line
        "separator": "\n",  # Template for the separator between versions sections
    },
    "commit": {
        "enabled": True,  # Commit the changes automatically
        "message": "Update version to [version]",  # Template for the commit message
        "mainbranch": "master",  # name of the main development or release branch
    },
    "tag": {
        "enabled": True,  # Tag the bump commit
        "name": "v[version]",  # Template for the name of the tag in the tag message
    },
    "tokens": {
        "date": {
            "format": "%Y-%m-%d"  # Python datetime format to use when generating the `[date]` token
        },
        "version_date": {
            "format": "%Y-%m-%d"  # Python datetime format to use when generating the `[version_date]` token
        },
    },
    "scripts": {
        "prebump": "",  # Script to execute before bumping the version
        "postbump": "",  # Script to execute after bumping the version
        "prechangelog": "",  # Script to execute before updating the changelog
        "postchangelog": "",  # Script to execute after updating the changelog
        "precommit": "",  # Script to execute before committing
        "postcommit": "",  # Script to execute after committing
        "pretag": "",  # Script to execute before tagging
        "posttag": "",  # Script to execute after tagging
    },
}
