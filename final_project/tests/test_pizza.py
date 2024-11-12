import pytest
from pizza import Pizza, Hawaiian, Pepperoni, Margherita, PizzaSize


class TestPizza:
    @pytest.mark.parametrize(
        "name, size",
        [
            ("base", PizzaSize.XL),
            ("my_pizza", PizzaSize.L),
        ],
    )
    def test_pizza_init(self, name, size):
        """Тестирование инициализации пиццы."""
        pizza_xl = Pizza(name=name, size=size)
        assert pizza_xl.size == size
        assert pizza_xl.name == name

    def test_size_error(self):
        with pytest.raises(TypeError):
            Pizza(name="base", size="M")

    def test_add_to_recipe(self):
        my_pizza = Pizza("Моя пицца", PizzaSize.L)
        my_pizza.add_to_recipe("Томаты")
        classical = Margherita()
        with2cheese = Margherita()
        with2cheese.add_to_recipe("cheese")
        assert classical.name == "Margherita"
        assert with2cheese.name == "Margherita"
        assert classical._recipe == Margherita._ingredients
        assert len(classical._recipe) < len(with2cheese._recipe)
        assert with2cheese >= classical
        assert my_pizza.dict() == {"Моя пицца": "Томаты"}

    def test_order(self):
        big_recipe = Hawaiian(size=PizzaSize.XL)
        big = Pepperoni(size=PizzaSize.XL)
        small = Pepperoni(size=PizzaSize.L)
        like_small = Pepperoni(size=PizzaSize.L)
        for ing in big._recipe:
            big_recipe.add_to_recipe(ing)
        assert small < big
        assert big_recipe > big
        assert like_small == small

    def test_eq_same_object(self):
        # Тестирование равенства двух одинаковых объектов
        pizza1 = Pizza("Маргарита", PizzaSize.L)
        pizza1.add_to_recipe("Томаты")
        pizza2 = Pizza("Маргарита", PizzaSize.L)
        pizza2.add_to_recipe("Томаты")
        assert pizza1 == pizza2
