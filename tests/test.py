def calculate_total(products):
    total = 0
    for product in products:
        total += product["price"]
    return total


def test_calculate_total_with_empty_list():
    assert calculate_total([]) == 0


def test_calculate_total_with_single_product():
    products = [
        {
            "name": "Notebook", "price": 5
        }
    ]
    assert calculate_total(products) == 5


def test_calculate_total_with_multiple_product():
    products = [
        {
            "name": "Book", "price": 10
        },
        {
            "name": "Pen", "price": 2
        }
    ]
    assert calculate_total(products) == 12


def test_calculate_total_with_negative_price():
    products = [
        {"name": "Notebook", "price": 5},
        {"name": "Pen", "price": -2}
    ]
    assert calculate_total(products) == 3  # 5 - 2 = 3


def test_calculate_total_with_zero_price():
    products = [
        {"name": "Notebook", "price": 5},
        {"name": "Pen", "price": 0}
    ]
    assert calculate_total(products) == 5  # 5 + 0 = 5


def test_calculate_total_with_float_price():
    products = [
        {"name": "Notebook", "price": 5.99},
        {"name": "Pen", "price": 2.50}
    ]
    assert calculate_total(products) == 8.49  # 5.99 + 2.50 = 8.49

def test_calculate_total_with_same_price():
    products = [
        {"name": "Notebook", "price": 10},
        {"name": "Pen", "price": 10}
    ]
    assert calculate_total(products) == 20  # 10 + 10 = 20


if __name__ == "__main__":
    test_calculate_total_with_empty_list()
    test_calculate_total_with_single_product()
    test_calculate_total_with_multiple_product()
    test_calculate_total_with_negative_price()
    test_calculate_total_with_float_price()
    test_calculate_total_with_same_price()
    print("All tests passed")
