import versup.template as template


def test_render():
    result = template.render("the new [version]")
    assert result == "the new [version]"
    result = template.render("the new [version]", {"version": "1.2.3"})
    assert result == "the new 1.2.3"
