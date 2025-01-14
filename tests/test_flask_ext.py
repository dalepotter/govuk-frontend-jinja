
import pytest

flask = pytest.importorskip("flask", reason="requires Flask")

import govuk_frontend_jinja
from govuk_frontend_jinja.flask_ext import Environment, init_govuk_frontend

@pytest.fixture
def app():
    return flask.Flask("test_flask_ext")


def test_environment_takes_app_as_first_argument(app):
    env = Environment(app)
    assert env.app == app


def test_init_govuk_frontend(app):
    init_govuk_frontend(app)
    env = app.jinja_env

    assert (
        env.undefined
        ==
        govuk_frontend_jinja.templates.NunjucksUndefined
    )
    assert (
        "govuk_frontend_jinja.templates.NunjucksExtension"
        in
        env.extensions
    )


def test_render_template(app, loader):
    init_govuk_frontend(app)
    app.jinja_loader = loader

    with app.app_context():
        flask.render_template("template.njk")
