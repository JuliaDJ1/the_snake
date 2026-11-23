<div align="center">

# 🐍 Snake

**Классическая «Змейка» на Pygame, написанная в объектно-ориентированном стиле**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5-2E8B57)
![OOP](https://img.shields.io/badge/OOP-inheritance-informational)

</div>

## Об игре

Змейка ползает по полю 32 × 24 клетки, ест яблоки и растёт. Управление — стрелками. Если змейка врезается в собственный хвост, игра начинается заново. Поле «замкнуто»: выйдя за край, змейка появляется с противоположной стороны.

## Что сделано

- Иерархия классов: базовый `GameObject` и наследники `Apple` и `Snake` с переопределением `draw()`.
- Яблоко появляется только в свободной клетке, не на теле змейки.
- Защита от разворота на 180° за один ход, обработка выхода из игры.
- Аннотации типов, docstring-и, константы вынесены в начало модуля, код проходит flake8.

## Стек

Python 3.10+ · Pygame · ООП · type hints · pytest · flake8

## Запуск

```bash
git clone https://github.com/JuliaDJ1/the_snake.git
cd the_snake
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python the_snake.py
```

## Автор

**Вадим Гусейнов** — Python-разработчик (Backend) · [Telegram](https://t.me/eviliing)
