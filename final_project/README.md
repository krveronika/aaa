# Команды:

# сli
Команда отображает доступное меню.
```bash
python src/cli.py menu
```

Команды для запуска приготовки и доставки заказа
```bash
python src/cli.py order pepperoni -–delivery
```

```bash
python src/cli.py order --delivery pepperoni
```

# pytest 
Сначала добавим путь к директории src, чтобы Python мог находить модули внутри неё. 
Для этого выполните следующую команду перед запуском тестов:
```bash
export PYTHONPATH=$PWD/src
```
Запуск тестов:
```bash
python -m pytest tests
```
