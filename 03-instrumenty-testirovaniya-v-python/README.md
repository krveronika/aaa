Для запусков вначале надо сделать следующие шаги:
1. Откройте терминал.
2. Перейдите в папку проекта 03-instrumenty-testirovaniya-v-python.

# Issue-01
## Запуск doctest

Чтобы запустить док-тесты, выполните команду:

```bash
python -m doctest -v morse.py 
```
Эта команда запустит все док-тесты, определенные в комментариях к функции `encode`. 
Флаг `-v` включает режим подробного вывода, позволяющий увидеть результаты каждого теста.

# Issue-02
## Запуск pytest
3. Выполните команду:
```bash
pytest -v test_morse.py
```
   
Этот скрипт запустит все тесты, определенные в файле `test_morse.py`.

# Issue-03
## Запуск unittest
3. Выполните команду:

```bash
python -m unittest test_one_hot_encoder_03.py 
```

# Issue-04
## Запуск pytest
3. Выполните команду:

```bash
pytest -v test_one_hot_encoder_04.py::TestOneHotEncoder
```

# Issue-05
## Запуск pytest
3. Выполните команду:

```bash
python -m pytest -v test_what_is_year_now.py --cov=letters_counter
```

Для запуска расчета отчета о покрытии:

```bash
coverage run -m pytest test_what_is_year_now.py && coverage html --omit="*/site-packages/*"
```
 Не разобралась как это сократить можно. Но все равно прикольно
