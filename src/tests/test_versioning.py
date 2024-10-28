import pytest

from versup import versioning


def test_get_new_version_explicit():
    assert "1.6.88" == versioning.get_new_version("1.2.3", "1.6.88", [], False)


def test_get_new_version_explicit_raise():
    with pytest.raises(Exception):
        versioning.get_new_version("1.4.2", "1.pies.88", [], False)


def test_get_new_version_increment_raise():
    with pytest.raises(Exception):
        versioning.get_new_version("1.4.2", "minor", ["major"], False)

    assert "1.5.0" == versioning.get_new_version("1.4.2", "minor", ["minor"], False)


def test_patch_increment():
    assert "1.0.1" == versioning.bump_version("1.0.0", "patch")


def test_minor_increment():
    assert "1.1.0" == versioning.bump_version("1.0.0", "minor")


def test_major_increment():
    assert "2.0.0" == versioning.bump_version("1.0.0", "major")


def test_prepatch_increment():
    assert "1.0.1-rc.1" == versioning.bump_version("1.0.0", "prepatch")


def test_preminor_increment():
    assert "1.1.0-rc.1" == versioning.bump_version("1.0.0", "preminor")
    assert "1.3.0-rc.1" == versioning.bump_version("1.2.4", "preminor")


def test_premajor_increment():
    assert "2.0.0-rc.1" == versioning.bump_version("1.0.0", "premajor")
    assert "2.0.0-rc.1" == versioning.bump_version("1.3.4", "premajor")


def test_prerelease():
    assert "1.0.1-rc.1" == versioning.bump_version("1.0.0", "prerelease")
    assert "1.0.1-rc.2" == versioning.bump_version("1.0.1-rc.1", "prerelease")
    assert "1.0.1-rc.3" == versioning.bump_version("1.0.1-rc.2", "prerelease")


def test_drop_prerelease():
    assert "1.0.1" == versioning.bump_version("1.0.1-rc.1", "patch")
    assert "1.1.0" == versioning.bump_version("1.0.1-rc.1", "minor")
    assert "2.0.0" == versioning.bump_version("1.0.1-rc.1", "major")


def test_release():
    assert "1.0.1" == versioning.bump_version("1.0.1-rc.1", "release")
    assert "2.0.1" == versioning.bump_version("2.0.1-rc.5", "release")

    with pytest.raises(Exception):
        versioning.bump_version("2.0.1", "release")
