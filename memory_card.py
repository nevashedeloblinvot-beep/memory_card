from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QVBoxLayout, QHBoxLayout, QRadioButton,
                             QGroupBox, QButtonGroup)
from PyQt5.QtGui import QFont
from random import shuffle, randint  # choice для случайного выбора вопроса


app = QApplication([])
main_win = QWidget()
main_win.setGeometry(300, 300, 600, 500)
main_win.setWindowTitle("Memory Card - Культурный центр 'Человек мира'")
font = QFont('Arial', 14)
main_win.setFont(font)


# ============ КЛАСС ДЛЯ ХРАНЕНИЯ ВОПРОСОВ ============
class Question:
    def __init__(self, text, right_answer, wrong1, wrong2, wrong3):
        self.text = text                # текст вопроса
        self.right_answer = right_answer  # правильный ответ
        self.wrong_answers = [wrong1, wrong2, wrong3]  # список неправильных ответов


# ============ СОЗДАНИЕ СПИСКА ВОПРОСОВ ============
questions_list = [
    Question("Какой национальности не существует?",
             "Смурфы", "Энцы", "Чулымцы", "Алеуты"),
    Question("Какой язык является официальным в Бразилии?",
             "Португальский", "Испанский", "Французский", "Итальянский"),
    Question("Какое из этих племён существует в реальности?",
             "Чулымцы", "Хоббиты", "Эльфы", "Смурфы"),
    Question("Где находится культурный центр «Человек мира»?",
             "В Москве", "В Санкт-Петербурге", "В Новосибирске", "Во Владивостоке"),
    Question("Какой народ проживает на Аляске?",
             "Алеуты", "Энцы", "Чулымцы", "Смурфы")
]


# ============ ПЕРЕМЕННЫЕ ДЛЯ СТАТИСТИКИ ============
main_win.total = 0      # всего отвеченных вопросов
main_win.count = 0       # количество правильных ответов


# ============ СОЗДАНИЕ ВИДЖЕТОВ ============
lb_Question = QLabel("")  # текст вопроса будет заполняться позже


# Группа для вариантов ответов
RadioGroupBox = QGroupBox("Варианты ответов")


# Переключатели
rbtn_1 = QRadioButton("")
rbtn_2 = QRadioButton("")
rbtn_3 = QRadioButton("")
rbtn_4 = QRadioButton("")


# Группа для объединения переключателей
radio_group = QButtonGroup()
radio_group.addButton(rbtn_1)
radio_group.addButton(rbtn_2)
radio_group.addButton(rbtn_3)
radio_group.addButton(rbtn_4)


# Группа для отображения правильного ответа
AnswerGroupBox = QGroupBox("Результат")
lb_Result = QLabel("")
lb_Correct = QLabel("")


layout_result = QVBoxLayout()
layout_result.addWidget(lb_Result, alignment=Qt.AlignCenter)
layout_result.addWidget(lb_Correct, alignment=Qt.AlignCenter)
AnswerGroupBox.setLayout(layout_result)


# ============ РАЗМЕЩЕНИЕ ВАРИАНТОВ ОТВЕТОВ ============
layout_ans_1 = QHBoxLayout()
layout_ans_2 = QVBoxLayout()
layout_ans_3 = QVBoxLayout()


layout_ans_2.addWidget(rbtn_1)
layout_ans_2.addWidget(rbtn_2)
layout_ans_3.addWidget(rbtn_3)
layout_ans_3.addWidget(rbtn_4)
layout_ans_1.addLayout(layout_ans_2)
layout_ans_1.addLayout(layout_ans_3)


RadioGroupBox.setLayout(layout_ans_1)


# ============ КНОПКА ============
ansButton = QPushButton("Ответить")


# ============ ОСНОВНОЙ ЛЕЙАУТ ============
layout_line1 = QVBoxLayout()
layout_line1.addWidget(lb_Question, alignment=Qt.AlignCenter)


layout_line3 = QHBoxLayout()
layout_line3.addStretch(1)
layout_line3.addWidget(ansButton, stretch=2)
layout_line3.addStretch(1)


layout_card = QVBoxLayout()
layout_card.addLayout(layout_line1)
layout_card.addWidget(RadioGroupBox)
layout_card.addWidget(AnswerGroupBox)
layout_card.addLayout(layout_line3)


main_win.setLayout(layout_card)


# ============ ПЕРЕМЕННЫЕ ДЛЯ ТЕКУЩЕГО ВОПРОСА ============
buttons = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]
current_question = None   # объект текущего вопроса
correct_answer = ""       # правильный ответ текущего вопроса


# ============ ФУНКЦИЯ ВЫВОДА СТАТИСТИКИ В КОНСОЛЬ ============
def print_statistics():
    """Выводит текущую статистику ответов в консоль"""
    if main_win.total == 0:
        print("Статистика: пока нет отвеченных вопросов.")
    else:
        rating = (main_win.count / main_win.total) * 100
        print(f"   Статистика: Правильных ответов: {main_win.count} из {main_win.total}")
        print(f"   Рейтинг: {rating:.1f}%")


# ============ ФУНКЦИИ-ОБРАБОТЧИКИ ============
def show_question():
    """Отображает форму вопроса и сбрасывает выбор переключателей"""
    AnswerGroupBox.hide()
    RadioGroupBox.show()
    ansButton.setText("Ответить")
   
    # Сброс выбора переключателей
    radio_group.setExclusive(False)
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    radio_group.setExclusive(True)


def show_result():
    """Отображает форму ответа"""
    RadioGroupBox.hide()
    AnswerGroupBox.show()
    ansButton.setText("Следующий вопрос")


def show_correct(res):
    """Отображает результат проверки ответа"""
    lb_Result.setText(res)
    lb_Correct.setText(correct_answer)
    show_result()


def check_answer():
    # Определяем выбранный ответ
    if rbtn_1.isChecked():
        selected = rbtn_1.text()
    elif rbtn_2.isChecked():
        selected = rbtn_2.text()
    elif rbtn_3.isChecked():
        selected = rbtn_3.text()
    elif rbtn_4.isChecked():
        selected = rbtn_4.text()
    else:
        selected = ""
   
    # Если ничего не выбрано — не считаем ответ и не показываем результат
    if selected == "":
        return
   
    # Увеличиваем счётчик отвеченных вопросов
    main_win.total += 1
   
    # Проверяем правильность
    if selected == correct_answer:
        main_win.count += 1
        show_correct("ПРАВИЛЬНО!")
    else:
        show_correct("НЕПРАВИЛЬНО!")
   
    # Выводим статистику в консоль после каждого ответа
    print_statistics()


def ask(question_obj):
    global current_question, correct_answer
    current_question = question_obj
    correct_answer = question_obj.right_answer
   
    # Устанавливаем текст вопроса
    lb_Question.setText(question_obj.text)
   
    # Формируем список всех вариантов: правильный + три неправильных
    all_answers = [question_obj.right_answer] + question_obj.wrong_answers
    # Перемешиваем
    shuffle(all_answers)
   
    # Заполняем переключатели
    for i, button in enumerate(buttons):
        button.setText(all_answers[i])
   
    # Отображаем форму вопроса
    show_question()


def next_random_question():
    """Выбирает случайный вопрос из списка и задаёт его"""
    if questions_list:
        quest_num = randint(0, len(questions_list) - 1)
        random_q = questions_list[quest_num]
        questions_list.pop(quest_num)
        ask(random_q)
    else:
        lb_Question.setText("Нет вопросов в базе")


def start_test():
    """Обработчик нажатия на кнопку"""
    if ansButton.text() == "Ответить":
        # Проверяем, выбран ли хоть один вариант
        if any(btn.isChecked() for btn in buttons):
            check_answer()
    else:  # "Следующий вопрос"
        next_random_question()


# ============ ПЕРВОНАЧАЛЬНЫЙ ЗАПУСК ============
AnswerGroupBox.hide()
next_random_question()  # задаём первый случайный вопрос


ansButton.clicked.connect(start_test)


# ============ ЗАПУСК ПРИЛОЖЕНИЯ ============
main_win.show()
app.exec_()
