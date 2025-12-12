from tailorfish.core import hello


def test_hello() -> None:
    assert hello("Al-Baraa") == "Tailorfish says hi to Al-Baraa"
