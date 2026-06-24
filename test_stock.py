from stock_solution import Stock, Item

def test_summary_multiple_items():
    stock = Stock()

    stock.add_item(Item("Coke"))
    stock.add_item(Item("Coke"))
    stock.add_item(Item("Mama"))

    assert stock.get_summary() == {
        "Coke": 2,
        "Mama": 1
    }


def test_summary_after_removal():
    stock = Stock()

    stock.add_item(Item("Coke"))
    stock.add_item(Item("Coke"))
    stock.remove_item_by_name("Coke")

    assert stock.get_summary() == {
        "Coke": 1
    }


def test_summary_empty_stock():
    stock = Stock()

    assert stock.get_summary() == {}


def test_summary_remove_below_zero_does_not_break():
    stock = Stock()

    stock.add_item(Item("Mama"))
    stock.remove_item_by_name("Mama")
    stock.remove_item_by_name("Mama")

    assert stock.get_summary() == {
        "Mama": 0
    }
