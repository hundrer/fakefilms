from random import randint
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter import filedialog as fd
from llama_cpp import Llama
from os import system
from interpreter import FilmPlayer
path = None
def select_file():
    filetypes = (
        ('.gguf files', '*.gguf'),
        ('All files (not recommended)', '*.*')
    )
    path = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    with open("filename.conf", "w") as file:
        file.write(path)
    print(path)
def start():
    global path
    try:
        file = open('filename.conf', 'r')
        path = file.read()
        if path == "":
            showerror(title="Путь пустой", message="Вы нажали на \"Отмена\" в файловом диалоге. Попробуйте еще раз указать путь.")
            return
    except FileNotFoundError:
        showerror(title="Путь не указан", message="Укажите путь")
        return
    p = editor.get("1.0", "end")
    generation_window = tk.Toplevel(root)
    generation_window.title("Подождите!")
    generation_window.geometry("300x75")
    generation_window.iconbitmap(r'Fakefilms_icon.ico')
    generation_window.resizable(False, False)
    text = Label(generation_window, text="Нейросеть генерирует код. \n Это может занять несколько минут.\nПомни, нейросеть может ошибаться, поэтому\nесли ничего нет, то вини нейросеть")
    text.grid()
    generation_window.update()
    instruction = """даю тебе инструкцию по моему языку программирования, с помощью которого ты будешь делать фильмы
    используй ТОЛЬКО эти функции, другие НИКОГДА не используй, иначе программа выдаст ошибку

    title (название) - стереть всё и изменить заголовок
    пример: title test

    sleep (секунды) - подождать указанное число секунды
    пример: sleep 1 - ждать 1 секунду

    rem (комментарий) - ничего не делает, это комментарий
    пример: rem ывафыовафоыврывр ичо

    spawn - спавнит объекты, это более сложная функция
    первым аргументом будет название (название может быть как на латинице, так и на киррилице)
    вторым аргументом будет rectangle (прямоугольник) или oval (овал)
    третим будет x первой точки
    четвертым будет y первой точки
    пятым будет x второй точки
    шестым будет y второй точки
    и седьмым будет название цвета на английском языке (например blue) или html код цвета (например #010101)
    и главное! НЕ НАЗЫВАЙ объект background, это может привести к конфликту.
    пример:
    spawn прямоугольник rectangle 100 100 200 200 green
    
    следуй строго только эти аргументам, иначе будет ошибка если не напишешь название например

    edit - редактирует объекты, тоже сложная функция
    первым аргументом будет название существующего объекта
    вторым аргументом будет color, nickname или action
    если он будет color, то третим аргументом будет название цвета на английском языке (например blue) или html код цвета (например #010101)
    если еще background будет первым аргументом, то изменится цвет фона

    если он будет nickname (надпись сверху, служит публичным именем) или action (надпись снизу, служит действию или разговору), то третим аргументом будет текст
    пример:
    edit прямоугольник color red
    edit прямоугольник nickname ичо
    edit background color red

    move - перемещает объекты, менее сложная функция
    первым аргументом будет название существующего объекта
    вторым аргументом будет на сколько x переместиться
    третим аргументом будет на сколько y переместиться
    пример:
    move прямоугольник 10 0 (перемещает на 10 пикселей направо)

    delete (название существующего объекта) - удаляет объекты

    если эта функция не одна из функций перечисленная выше, то интерпретатор выдаст ошибку

    пример полного кода:

    sleep 1
    title ичо
    rem комментарий
    sleep 1
    title Да Венерский Он Всегда И Будет Переобувщик.
    sleep 1
    spawn лох rectangle 300 300 500 500 white

    edit лох color blue
    edit лох nickname Венерский ичо.
    edit лох action // ичокает

    sleep 1
    delete лох

    Всего доступной площади 1280 пикселей по x и 720 по y

    Максимальное время sleep - 1 секунда

    ПОМНИ! TITLE УДАЛЯЕТ ВСЕ ОБЪЕКТЫ, ЕСЛИ ТЫ ПОПЫТАЕШЬСЯ ВЗЯТЬ НАПРИМЕР КУБ, ТО ИНТЕРПРЕТАТОР ВЫДАСТ KEYERROR

    ЕЩЕ НИЧЕГО НЕ ВЫВОДИ КРОМЕ КОДА
    
    Названия должны содержать только одно слово (например Венерский) или пробелы в названии должны быть заменены на _ (например Венерский_ичо)
    удачи с созданием фильмов!"""
    try:
        llm = Llama(model_path=path, n_ctx=2048, verbose=True)
        a = llm.create_chat_completion(
            messages=[{"role": "user", "content": instruction}, {"role": "user", "content": f"Сгенерируй фильм с помощью этого языка программирования по следующему сценарию (ПОЖАЛУЙСТА, НЕ ЗАБЫВАЙ УКАЗЫВАТЬ НАЗВАНИЯ ПОСЛЕ SPAWN, ТОЛЬКО ПОТОМ УКАЗЫВАЙ RECTANGLE ИЛИ OVAL):{p}"}],
            temperature=0.7,
        )
        print(a["choices"][0]["message"]["content"])

    except Exception as e:
        showerror(title="Ошибка от Python во время генерации", message=e)
        return
    try:
        text["text"] = "Готово!\nОткрывается окно показа..."
        generation_window.update()
        num = randint(1, 100000)
        with open(f"{num}.🖕", "w", errors="ignore", encoding="utf-8") as file:
            file.write(a["choices"][0]["message"]["content"])
    except Exception as e:
        showerror(title="Ошибка, возможно системная, во время записи файла", message=e)
        return
    # system(f"python interpreter.py {num}.🖕")
    film_player_window = tk.Toplevel(root)
    film_player = FilmPlayer(film_player_window)
    try:
        with open(f"{num}.🖕", "r", errors="ignore", encoding="utf-8") as file:
            film_player.process_line(index=0, content=file.readlines())
    except:
        showwarning(title="Произошла парашка", message="Нейросеть должна исправить код")
        try:
            llm = Llama(model_path=path, n_ctx=2048, verbose=True)
            text["text"] = "Код исправляется.\nЭто может занять несколько минут."
            generation_window.update()
            a = llm.create_chat_completion(
                messages=[{"role": "user", "content": instruction}, {"role": "user",
                                                                       "content": f"Исправь ошибки в этом коде по инструкции выше, укажи названия после spawn и перед rectangle или oval. Код следующий: {a["choices"][0]["message"]["content"]}"}],
                temperature=0.7,
            )
            text["text"] = "Готово!\nОткрывается окно показа..."
            generation_window.update()
            with open(f"{num}.🖕", "w", errors="ignore", encoding="utf-8") as file:
                file.write(a["choices"][0]["message"]["content"])
            with open(f"{num}.🖕", "r", errors="ignore", encoding="utf-8") as file:
                film_player.process_line(index=0, content=file.readlines())
        except Exception as e:
            showerror(title="Провал.", message=e)
            return
root = Tk()
root.iconbitmap(r'Fakefilms_icon.ico')
root.title("Fakefilms")
root.geometry("400x300")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.resizable(False, False)
editor = Text()
editor.grid()
btn = ttk.Button(text="Сгенерировать", command=start)
btn.grid(row=1, column=0, sticky='sw')
btn = ttk.Button(text="Задать путь к gguf файлу", command=select_file)
btn.grid(row=1, column=0, sticky='se')
root.mainloop()