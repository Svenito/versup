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
            "premajor",
            "preminor",
            "prepatch",
            "prerelease",
            "custom",
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
        "message": "[Bumper] Set version to [version]",  # Template for the commit message
    },
    "tag": {
        "enabled": True,  # Tag the bump commit
        "name": "v[version]",  # Template for the name of the tag
    },
    "release": {
        "enabled": False,  # Release to any enabled release providers
        "github": {
            "enabled": False,  # Make a GitHub release
            "open": True,  # Open the release/draft page
            "draft": True,  # Mark it as a draft
            "prerelease": False,  # Mark it as a prerelease
            "files": [],  # Globs of files to attach to the release
            "token": "",  # GitHub OAuth token with `public_repo` priviledge
            "owner": "",  # GitHub repository owner
            "repo": "",  # GitHub repository name
        },
    },
    "tokens": {
        "date": {
            "format": "YYYY-MM-DD"  # Moment.js format to use when generating the `[date]` token
        },
        "version_date": {
            "format": "YYYY-MM-DD"  # Moment.js format to use when generating the `[version_date]` token
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
        "prerelease": "",  # Script to execute before releasing
        "postrelease": "",  # Script to execute after releasing
    },
}
