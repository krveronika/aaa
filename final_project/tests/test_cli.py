from pizza import Pepperoni
import cli
from click.testing import CliRunner
import pytest


def test_deliver(capsys):
    cli.deliver(Pepperoni())
    out, err = capsys.readouterr()
    assert "🛵 Доставили за" in out


def test_pickup(capsys):
    cli.pickup(Pepperoni())
    out, err = capsys.readouterr()
    assert "🏠 Забрали за" in out


def test_without_log_pickup():
    out = cli.pickup.__wrapped__(Pepperoni())
    assert out == "Pizza Pepperoni 🍕 pickup"


def test_bake(capsys):
    cli.bake(Pepperoni())
    out, err = capsys.readouterr()
    assert "bake - " in out


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_menu(runner):
    result = runner.invoke(cli.menu)
    assert result.exit_code == 0


def test_cli_order_arg(runner):
    result = runner.invoke(cli.order, "Pepperoni")
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "pizza, delivery, expected_output",
    [
        ("Margherita", True, "Доставили за "),
        ("Pepperoni", False, "Забрали за"),
    ],
)
def test_order(runner, pizza, delivery, expected_output):
    args = (["--delivery"] if delivery else []) + [pizza]
    result = runner.invoke(cli.order, args)
    assert result.exit_code == 0
    assert "bake - " in result.output
    assert expected_output in result.output
