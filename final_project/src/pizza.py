from enum import Enum, auto
from functools import total_ordering
from typing import TypeVar


P = TypeVar("P", bound="Pizza")


class PizzaSize(Enum):
    """Размеры пиццы."""

    L = auto()
    XL = auto()


@total_ordering
class Pizza:
    """
    Базовый класс для всех видов пицц.

    :param name: Название пиццы.
    :param size: Размер пиццы.
    """

    def __init__(
        self, name: str, size: PizzaSize = PizzaSize.L, emoji: str = None
    ) -> None:
        """
        Конструктор класса Pizza.

        :param name: Название пиццы.
        :param size: Размер пиццы.
        """
        if not isinstance(size, PizzaSize):
            raise TypeError(f"{type(size)} is not PizzaSize")
        self.name: str = name
        self.emoji: str = emoji
        self.size: PizzaSize = size
        self._recipe: list[str] = []

    def add_to_recipe(self, ingredient: str) -> None:
        """
        Добавляет ингредиент в рецепт пиццы.

        :param ingredient: Ингредиент, который добавляется в рецепт.
        """
        self._recipe.append(ingredient)

    def dict(self) -> dict[str, str]:
        """
        Преобразует рецепт пиццы в словарь.

        :return: Словарь, содержащий название пиццы и список ингредиентов.
        """
        recipe_str = ", ".join(self._recipe)
        return {self.name: recipe_str}

    def __eq__(self, other: P) -> bool:
        """
        Определяет равенство двух объектов пиццы.

        :param other: Другой объект пиццы для сравнения.
        :return: True, если обе пиццы равны по размеру, названию и ингредиентам, иначе False.
        """
        if not isinstance(other, Pizza):
            return NotImplemented
        noteq_size: bool = self.size.value != other.size.value
        noteq_name: bool = self.name != other.name
        if noteq_size or noteq_name:
            return False
        return sorted(self._recipe) == sorted(other._recipe)

    def __lt__(self, other: P) -> bool:
        """
        Определяет порядок сортировки двух объектов пиццы.

        :param other: Другой объект пиццы для сравнения.
        :return: True, если текущая пицца меньше другой по размеру или количеству ингредиентов, иначе False
        """
        if self.size.value < other.size.value:
            return True
        return len(self._recipe) < len(other._recipe)

    def fullname(self) -> str:
        """
        Возвращает строковое представление названия пиццы.

        :return: Строку, содержащую название пиццы и эмоджи.
        """
        return self.name if self.emoji is None else f"{self.name} {self.emoji}"

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта пиццы.

        :return: Строку, содержащую название пиццы и список ингредиентов.
        """

        return f"{self.fullname}: {', '.join(self._recipe)}"


class Margherita(Pizza):
    """
    Класс для пиццы Margherita.

    :param name: Название пиццы.
    :param size: Размер пиццы.
    """

    _ingredients: list[str] = ["tomato sauce", "mozzarella", "tomatoes"]
    _emoji: str = "🧀"

    def __init__(self, name: str = "Margherita", size: PizzaSize = PizzaSize.L) -> None:
        """
        Инициализация рецепта пиццы Margherita с указанным именем и размером.

        :param name: Название пиццы.
        :param size: Размер пиццы.
        """
        super().__init__(name, size, self._emoji)
        self._recipe = self._ingredients.copy()


class Pepperoni(Pizza):
    """
    Класс для пиццы Pepperoni.

    :param name: Название пиццы.
    :param size: Размер пиццы.
    """

    _ingredients = ["tomato sauce", "mozzarella", "pepperoni"]
    _emoji: str = "🍕"

    def __init__(self, name="Pepperoni", size: PizzaSize = PizzaSize.L) -> None:
        """
        Инициализация рецепта пиццы Pepperoni с указанным именем и размером.

        :param name: Название пиццы.
        :param size: Размер пиццы.
        """
        super().__init__(name, size, self._emoji)
        self._recipe = self._ingredients.copy()


class Hawaiian(Pizza):
    """
    Класс для пиццы Hawaiian.

    :param name: Название пиццы.
    :param size: Размер пиццы.
    """

    _ingredients = ["tomato sauce", "mozzarella", "chicken", "pineapples"]
    _emoji: str = "🍍"

    def __init__(self, name="Hawaiian", size: PizzaSize = PizzaSize.L) -> None:
        """
        Инициализация рецепта пиццы Hawaiian с указанным именем и размером.

        :param name: Название пиццы.
        :param size: Размер пиццы.
        """
        super().__init__(name, size, self._emoji)
        self._recipe = self._ingredients.copy()


if __name__ == "__main__":
    print(Hawaiian())
