import pytest

import versup.gitops as gitops


class MockGit:
    @staticmethod
    def tag(*args, **kwargs):
        return "2.5.1\n2.5.0\n2.4.0\n2.3.0\n2.2.0\n2.1.1\n2.1.0\n2.0.7\n2.0.6\n2.0.5\n2.0.3\n2.0.1\n2.0.0"

    @staticmethod
    def log(*args, **kwargs):
        return "5d804e0b826978c184b183ac0820a11b30f8052c||User Name||user@email.com||1586965955||update readme with travis badge\n4539d9c8d682e76924fcca7c73295283f24ffb85||User Name||user@email.com||1586965850||Update version to 1.0.1\na902c9ac29d118d728f887b900268134766ad131||User Name||user@email.com||1586946947||Add conditional to travis deploy task\nc89100943b648712946ef1eb1704be28c5e8461c||User Name||user@email.com||1586946740||Fix up travis again"


class MockBranch:
    name = "main"


class MockConfigparser:
    def get_value(self, *args, **kwargs):
        if args[0] == "user":
            if args[1] == "name":
                return "testman"


class MockRepo:
    git = MockGit()
    active_branch = MockBranch()

    @staticmethod
    def config_reader():
        return MockConfigparser()

    @staticmethod
    def is_dirty():
        return True


@pytest.fixture
def mock_repo(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockRepo()

    monkeypatch.setattr(gitops, "get_repo", mock_get)


def test_get_username(mock_repo):
    assert gitops.get_username() == "testman"


def test_get_latest_tag(mock_repo):
    assert gitops.get_latest_tag() == "2.5.1"


def test_get_commit_messages(mock_repo):
    messages = gitops.get_commit_messages()

    assert len(messages) == 4
    assert messages[0]["author_name"] == "User Name"


def test_get_current_branch(mock_repo):
    branch = gitops.get_current_branch()

    assert branch == "main"


def test_check_current_branch_matches(mock_repo):
    assert gitops.check_current_branch_matches("main") is True
    assert gitops.check_current_branch_matches("testing") is False
