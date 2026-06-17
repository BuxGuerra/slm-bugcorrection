from solution import count_passing


def test_includes_threshold():
    assert count_passing([60, 70, 59], 60) == 2


def test_all_pass():
    assert count_passing([90, 80, 100], 50) == 3


def test_exact_only():
    assert count_passing([60, 60, 60], 60) == 3


def test_none_pass():
    assert count_passing([10, 20, 30], 50) == 0
