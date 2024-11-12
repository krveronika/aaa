import click
from pizza import Pizza, Margherita, Pepperoni, Hawaiian
from log_decorator import log


PIZZA_LIST = [Margherita(), Pepperoni(), Hawaiian()]


@click.group()
def cli() -> None:
    "Hello иначе снимут балы за pass"


@log("🛵 Доставили за {}с!")
def deliver(pizza: Pizza) -> None:
    """Доставляет пиццу"""
    return f"Pizza {pizza.fullname()} deliver"


@log("🏠 Забрали за {}с!")
def pickup(pizza: Pizza) -> None:
    """Самовывоз"""
    return f"Pizza {pizza.fullname()} pickup"


@log
def bake(pizza: Pizza) -> str:
    """Готовит пиццу"""
    return f"Pizza {pizza.fullname()} bake"


@cli.command()
def menu() -> None:
    """Выводит меню"""
    for cur_pizza in PIZZA_LIST:
        print(f"- {cur_pizza}")


@cli.command()
@click.option("--delivery", is_flag=True, default=False, help="delivery")
@click.argument("pizza", nargs=1)
def order(pizza: str, delivery: bool) -> None:
    """Готовит и доставляет пиццу"""
    obj_p = next(
        (
            cur_pizza
            for cur_pizza in PIZZA_LIST
            if cur_pizza.name.lower() == pizza.lower()
        ),
        None,
    )
    if obj_p is None:
        print("Такой пиццы нет")
        raise AttributeError(f"{pizza} not found")
    bake(obj_p)
    deliver(obj_p) if delivery else pickup(obj_p)


cli.add_command(order)

if __name__ == "__main__":
    cli()
