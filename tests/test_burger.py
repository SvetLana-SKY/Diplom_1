import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.bun import Bun


class TestBurger:



    def test_set_buns_correct_set_bun(self):
        bun = Bun(name="Classic Bun", price=100.0)
        burger = Burger()
        burger.set_buns(bun)
        assert burger.bun is bun

    def test_add_ingredient_adds_ingredient(self):
        ingredient_mock = Mock()
        burger = Burger()
        burger.add_ingredient(ingredient_mock)
        assert ingredient_mock in burger.ingredients 
        assert len(burger.ingredients) == 1


    def test_remove_ingredient_removes_item_by_index(self):
        ingredient_mock = Mock()
        burger = Burger()
        burger.add_ingredient(ingredient_mock)

        burger.remove_ingredient(0)
        assert ingredient_mock not in burger.ingredients 
        assert len(burger.ingredients) == 0

    def test_move_ingredient_swaps_positions_correctly(self):
        first = Mock()
        second = Mock()
        burger = Burger()
        burger.add_ingredient(first)
        burger.add_ingredient(second)

        burger.move_ingredient(0, 2)

        assert burger.ingredients[0] is second
        assert burger.ingredients[1] is first


    @pytest.mark.parametrize("bun_price, ingr_prices, expected_total",[
            (100.0, [50.0, 30.0], 280.0),      
            (80.0, [], 160.0),                 
            (50.0, [10.0], 110.0),   ] )  


    def test_get_price_calculate_total_price_right(self, bun_price, ingr_prices, expected_total):
        burger = Burger()

        bun = Mock()
        bun.get_price.return_value = bun_price
        burger.set_buns(bun) 
        
        for price in ingr_prices:
            ingredient = Mock()
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        total = burger.get_price()

        assert total == expected_total



    def test_get_receipt_formats_correctly_with_ingredients(self):
        
        bun = Mock()
        bun.get_name.return_value = "Classic Bun"
        bun.get_price.return_value = 100.0

        ingr1 = Mock()
        ingr1.get_type.return_value = "Sauce"
        ingr1.get_name.return_value = "Chili"
        ingr1.get_price.return_value = 50.0


        ingr2 = Mock()
        ingr2.get_type.return_value = "Vegetable"
        ingr2.get_name.return_value = "Tomato"
        ingr2.get_price.return_value = 30.0

        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingr1)
        burger.add_ingredient(ingr2)

        
        receipt = burger.get_receipt()
        lines = receipt.splitlines()


        assert lines[0] == "(==== Classic Bun ====)"
        assert lines[1] == "= sauce Chili ="
        assert lines[2] == "= vegetable Tomato ="
        assert lines[3] == "(==== Classic Bun ====)"
        assert lines[4] == ""                 
        assert lines[5] == f"Price: {burger.get_price()}"


