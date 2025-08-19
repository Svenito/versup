import configparser
import pytest
from unittest.mock import Mock

import versup.gitops as gitops


class MockGit:
    def __init__(self):
        self.tag_return = "2.5.1\n2.5.0\n2.4.0\n2.3.0\n2.2.0\n2.1.1\n2.1.0\n2.0.7\n2.0.6\n2.0.5\n2.0.3\n2.0.1\n2.0.0"
        self.log_return = "5d804e0b826978c184b183ac0820a11b30f8052c||User Name||user@email.com||1586965955||update readme with travis badge\n4539d9c8d682e76924fcca7c73295283f24ffb85||User Name||user@email.com||1586965850||Update version to 1.0.1\na902c9ac29d118d728f887b900268134766ad131||User Name||user@email.com||1586946947||Add conditional to travis deploy task\nc89100943b648712946ef1eb1704be28c5e8461c||User Name||user@email.com||1586946740||Fix up travis again"

    def tag(self, *args, **kwargs):
        return self.tag_return

    def log(self, *args, **kwargs):
        return self.log_return


class MockBranch:
    def __init__(self, name="main"):
        self.name = name


class MockConfigparser:
    def __init__(self, name="testman", email="test@email.com"):
        self.name = name
        self.email = email

    def get_value(self, section, option):
        if section == "user":
            if option == "name":
                return self.name
            elif option == "email":
                return self.email
        raise configparser.NoOptionError(option, section)


class MockIndex:
    def __init__(self):
        self.diff_result = []

    def diff(self, other):
        return self.diff_result

    def add(self, items):
        pass


class MockRepo:
    def __init__(self, branch_name="main", dirty=False):
        self.git = MockGit()
        self.active_branch = MockBranch(branch_name)
        self._dirty = dirty
        self.index = MockIndex()
        self.untracked_files = []
        self.config_values = {}

    def config_reader(self):
        return MockConfigparser()

    def is_dirty(self, untracked_files=False):
        return self._dirty

    def create_tag(self, name, message=None):
        pass


@pytest.fixture
def mock_repo(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockRepo()

    monkeypatch.setattr(gitops, "get_repo", mock_get)


def test_get_username(mock_repo):
    assert gitops.get_username() == "testman"


def test_get_email(mock_repo):
    assert gitops.get_email() == "test@email.com"


def test_get_email_missing_config(monkeypatch):
    class MockRepoNoEmail:
        def config_reader(self):
            return MockConfigparser(email="")

    def mock_get(*args, **kwargs):
        return MockRepoNoEmail()

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    with pytest.raises(gitops.MissingConfig):
        gitops.get_email()


def test_get_current_branch(mock_repo):
    branch = gitops.get_current_branch()
    assert branch == "main"


def test_is_repo_dirty_true(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockRepo(dirty=True)

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    assert gitops.is_repo_dirty() is True


def test_is_repo_dirty_false(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockRepo(dirty=False)

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    assert gitops.is_repo_dirty() is False


def test_get_latest_tag(mock_repo):
    assert gitops.get_latest_tag() == "2.5.1"


def test_get_latest_tag_no_semver_tags(monkeypatch):
    class MockGitNoSemver:
        def tag(self, *args, **kwargs):
            return "v1\nv2\ntest-tag\nrelease-candidate"

    class MockRepoNoSemver:
        def __init__(self):
            self.git = MockGitNoSemver()
            self.active_branch = MockBranch()

    def mock_get(*args, **kwargs):
        return MockRepoNoSemver()

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    with pytest.raises(ValueError, match="No semantic version tags found"):
        gitops.get_latest_tag()


def test_create_new_tag(monkeypatch):
    mock_repo_obj = MockRepo()
    mock_repo_obj.create_tag = Mock()

    def mock_get(*args, **kwargs):
        return mock_repo_obj

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    gitops.create_new_tag("1.0.0", "Release 1.0.0")
    mock_repo_obj.create_tag.assert_called_once_with("1.0.0", message="Release 1.0.0")


def test_get_unstaged_changes(monkeypatch):
    class MockDiff:
        def __init__(self, a_path):
            self.a_path = a_path

    class MockIndexWithChanges:
        def diff(self, other):
            return [MockDiff("file1.txt"), MockDiff("file2.txt")]

    class MockRepoWithChanges:
        def __init__(self):
            self.index = MockIndexWithChanges()
            self.untracked_files = ["file3.txt", "file4.txt"]

    def mock_get(*args, **kwargs):
        return MockRepoWithChanges()

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    changes = gitops.get_unstaged_changes()
    assert len(changes) == 4
    assert "file1.txt" in changes
    assert "file2.txt" in changes
    assert "file3.txt" in changes
    assert "file4.txt" in changes


def test_create_commit(monkeypatch):
    mock_repo_obj = MockRepo()
    mock_repo_obj.index.add = Mock()
    mock_repo_obj.git = Mock()

    def mock_get(*args, **kwargs):
        return mock_repo_obj

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    gitops.create_commit("Test commit message", ["file1.txt", "file2.txt"])
    mock_repo_obj.index.add.assert_called_once()
    mock_repo_obj.git.commit.assert_called_once_with("-m", "Test commit message")


def test_create_commit_no_files(monkeypatch):
    mock_repo_obj = MockRepo()
    mock_repo_obj.index.add = Mock()
    mock_repo_obj.git = Mock()

    def mock_get(*args, **kwargs):
        return mock_repo_obj

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    gitops.create_commit("Test commit message")
    mock_repo_obj.index.add.assert_called_once_with([])
    mock_repo_obj.git.commit.assert_called_once_with("-m", "Test commit message")


def test_get_commit_messages(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockRepo()

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    messages = gitops.get_commit_messages()
    assert len(messages) == 4
    assert messages[0]["author_name"] == "User Name"
    assert messages[0]["hash"] == "5d804e0b826978c184b183ac0820a11b30f8052c"


def test_get_commit_messages_no_tags(monkeypatch):
    class MockGitNoTags:
        def tag(self, *args, **kwargs):
            return ""

        def log(self, *args, **kwargs):
            return "5d804e0b826978c184b183ac0820a11b30f8052c||User Name||user@email.com||1586965955||update readme with travis badge"

    class MockRepoNoTags:
        def __init__(self):
            self.git = MockGitNoTags()
            self.active_branch = MockBranch()

    def mock_get(*args, **kwargs):
        return MockRepoNoTags()

    monkeypatch.setattr(gitops, "get_repo", mock_get)

    messages = gitops.get_commit_messages()
    assert len(messages) == 1
    assert messages[0]["message"] == "update readme with travis badge"


def test_check_current_branch_matches(mock_repo):
    assert gitops.check_current_branch_matches("main") is True
    assert gitops.check_current_branch_matches("testing") is False
