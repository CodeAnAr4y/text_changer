import tkinter.filedialog
from nltk.corpus import stopwords
from pymystem3 import Mystem
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import *
from nltk.corpus import wordnet
from random import randint

def information():
  messagebox.askquestion('Подсказки для Даши', '1. Текст необходимо вводить в окно "Ваш текст"\nТолько ENGLISH!\n'
                            '2. Используйте кнопку "Найти синонимы и антонимы" для нахождения синонимов и антонимов. '
                         'Результат будет выведен в окно Морфем\n'
                            '3. Используйте кнопку "Сгенерировать идентичный текст" '
                         'для генерации равносильного, по мнению умнейшей библиотеки весом в несколько ГБ - nltk, текста '
                         'и вывода его в окно "Предложение аналогичного текста"\n'
                            '4. Используйте кнопку "Подсказки" для отображения окна подсказок\n'
                            '5. Используйте копку "Загрузить из файла" чтобы получить готовый текст и вставить его в окно с текстом\n'
                            '6. Используйте копку "Сохранить в файл" чтобы сохранить вами написанный текст и сгенерированный программой в файл формата .txt\n'
                            '7. Используйте кнопку "Очистить окно морфем" для удаления всех слов с предложенными антонимами и синонимами из данного окна\n', type='ok')

mystem = Mystem()
stopwords = stopwords.words("english")
not_words = [',', '.', '!', '?', '-', '+', '=']

def clear_morph():
    tree.delete(*tree.get_children())

def process_text():
    text2.delete(1.0, 'end')
    syns = []
    ants = []
    sentence = []
    words = text.get(1.0, END).split()
    for i in words:
        for syn in wordnet.synsets(i):
            for l in syn.lemmas():
                syns.append(l.name())
                if l.antonyms():
                    ants.append(l.antonyms()[0].name())
        rand = randint(0, len(syns))
        if not syns:
            sentence.append(i)
        else:
            sentence.append(syns[rand-1])
        syns.clear()
    # print(sentence)
    text2.insert(1.0, sentence)

def synonyms_antonyms():
    input = text.get(1.0, END).split()
    # print(input)

    for i in input:
        synonyms = []
        antonyms = []

        for syn in wordnet.synsets(i):
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
        syns = str(set(synonyms))
        ants = str(set(antonyms))
        tree.insert('', tk.END, values=(i, syns, ants))

def open_file():
    file = tkinter.filedialog.askopenfilename(defaultextension='.txt')
    f = open(file, 'r')
    data = f.read()
    text.insert(1.0, data)
    f.close()

def save():
    file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    res1 = text.get(1.0, END)
    res2 = text2.get(1.0, END)
    file.write('YOUR TEXT:\n' + res1 + '\n\n' + 'GENERATED TEXT:\n' + res2)
    file.close()

root = tk.Tk()
root.title('Dictionary')
pict = tk.PhotoImage(file='icon.png')
root.iconphoto(False, pict)

f_top = LabelFrame(root, text='Поля полей')
f_but = LabelFrame(root, text='Кнопки')
f_bot = LabelFrame(root, text='Морфемы')
frame1 = Frame(f_top)
frame2 = Frame(f_top)
frame1.pack()
frame2.pack()

your_text = Label(frame1, text='Ваш текст', width=40)
your_text.pack(side=LEFT)
your_text = Label(frame1, text='Предложение аналогичного текста')
your_text.pack(side=RIGHT)
text = Text(frame2, width=40, height=10, wrap=WORD)
text.pack(side=LEFT)
text2 = Text(frame2, width=40, height=10, wrap=WORD)
text2.pack(side=LEFT)


frame = Frame()
frame.pack()

open_file = Button(f_but, text="Загрузить из файла", command=open_file)
open_file.pack(side=LEFT)
process = Button(f_but, text="Найти синонимы и антонимы", command=synonyms_antonyms)
process.pack(side=LEFT)

generate = Button(f_but, text='Сгенерировать идентичный текст', command=process_text)
generate.pack(side=LEFT)

clear_tree = Button(f_but, text="Очистить окно морфем", command=clear_morph)
clear_tree.pack(side=LEFT)

tree = ttk.Treeview(f_bot)
tree.pack(side=BOTTOM)
tree["columns"]=("zero","one","two")

tree.heading("zero", text="Слово",anchor=tk.W)
tree.heading("one", text="Синоним",anchor=tk.W)
tree.heading("two", text="Антоним",anchor=tk.W)

help = Button(f_but, text="Подсказки", command=information)
help.pack(side=LEFT)
save = Button(f_but, text="Сохранить в файл", command=save)
save.pack(side=LEFT)


f_top.pack(ipady=5, pady=5)
f_but.pack(ipady=5, pady=5, ipadx=5)
f_bot.pack(ipady=5, pady=5)

root.mainloop()
