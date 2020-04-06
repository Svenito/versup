import versup.gitops as gitops
import pytest


class MockGit:
    @staticmethod
    def tag(*args, **kwargs):
        return "2.5.1\n2.5.0\n2.4.0\n2.3.0\n2.2.0\n2.1.1\n2.1.0\n2.0.7\n2.0.6\n2.0.5\n2.0.3\n2.0.1\n2.0.0"


class MockRepo:
    git = MockGit()

    @staticmethod
    def is_dirty():
        return True


@pytest.fixture
def mock_repo(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockRepo()

    monkeypatch.setattr(gitops, "get_repo", mock_get)


def test_get_latest_tag(mock_repo):
    assert gitops.get_latest_tag() == "2.5.1"
