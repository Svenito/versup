import versup.template as template
import pytest


class TestTemplate:
    def test_render(self):
        result = template.render("the new [version]")
        assert result == "the new [version]"
        result = template.render("the new [version]", {"version": "1.2.3"})
        assert result == "the new 1.2.3"
