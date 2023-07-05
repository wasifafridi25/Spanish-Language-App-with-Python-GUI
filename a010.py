import sys
import webbrowser
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

class LanguageLearningAssistant(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spanish Language Learning Assistant")
        self.setGeometry(500, 200, 600, 400)

        layout = QVBoxLayout()

        self.title_label = QLabel("Welcome to the Spanish Language Learning Assistant")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title_label)

        self.vocab_quiz_button = QPushButton("Spanish Vocabulary Quiz")
        self.vocab_quiz_button.clicked.connect(self.start_vocab_quiz)
        layout.addWidget(self.vocab_quiz_button)

        self.grammar_exercise_button = QPushButton("Grammar Exercise")
        self.grammar_exercise_button.clicked.connect(self.start_grammar_exercise)
        layout.addWidget(self.grammar_exercise_button)

        self.resources_button = QPushButton("Language Learning Resources")
        self.resources_button.clicked.connect(self.open_resources)
        layout.addWidget(self.resources_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.quiz_window = QuizWindow()
        self.grammar_window = GrammarWindow()

    def start_vocab_quiz(self):
        self.setCentralWidget(self.quiz_window)
        self.quiz_window.start_quiz()

    def start_grammar_exercise(self):
        self.setCentralWidget(self.grammar_window)
        self.grammar_window.start_exercise()

    def open_resources(self):
        QMessageBox.information(
            self,
            "Language Learning Resources",
            "Online Resources:\n\n"
            "- Spanish Vocabulary Flashcards: https://www.studystack.com/flashcard-2119255\n"
            # "- Spanish Grammar Guide Book: https://www.spanishgrammarguide.com\n"
        )
        
        webbrowser.open("https://www.studystack.com/flashcard-2119255")
        
class QuizWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.question_label = QLabel()
        self.layout.addWidget(self.question_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.options_buttons = []
        for _ in range(4):
            button = QPushButton()
            button.clicked.connect(self.check_answer)
            self.options_buttons.append(button)
            self.layout.addWidget(button)

        self.score_label = QLabel()
        self.layout.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.next_button = QPushButton("Next Question")
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button)

        self.current_question = 0
        self.score = 0

        self.questions = [
            {
                "question": "What is 'hello' in Spanish?",
                "options": ["Hola", "Bonjour", "Ciao", "こんにちは"],
                "answer": "Hola"
            },
            {
                "question": "What is 'apple' in Spanish?",
                "options": ["Manzana", "Pomme", "Mela", "りんご"],
                "answer": "Manzana"
            },
            {
                "question": "What is 'I will call you today' in Spanish?",
                "options": ["Изгледаш лепо", "Waxaad u egtahay qurux", "te llamaré hoy", "شما به نظر زیبا"],
                "answer": "te llamaré hoy"
            },
            {
                "question": "What is 'You look pretty' in Spanish?",
                "options": ["Nani ʻoe", "Te Ves bonita", "Você está bonita", "তুমি দেখতে সুন্দর"],
                "answer": "Te Ves bonita"
            },
        ]

    def start_quiz(self):
        self.current_question = 0
        self.score = 0
        self.update_score()
        self.display_question(self.current_question)

    def display_question(self, question_index):
        question = self.questions[question_index]
        self.question_label.setText(question["question"])

        for i, option in enumerate(question["options"]):
            self.options_buttons[i].setText(option)
            self.options_buttons[i].setStyleSheet("")  # Reset style

        self.next_button.setEnabled(False)

    def check_answer(self):
        sender = self.sender()
        selected_option = sender.text()
        correct_answer = self.questions[self.current_question]["answer"]

        if selected_option == correct_answer:
            QMessageBox.information(self, "Result", "Correct!")
            self.score += 10
            sender.setStyleSheet("background-color: green;")
        else:
            QMessageBox.information(self, "Result", "Incorrect!")
            self.score -= 10
            sender.setStyleSheet("background-color: red;")

        for button in self.options_buttons:
            button.setEnabled(False)

        self.next_button.setEnabled(True)
        self.update_score()


    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.display_question(self.current_question)
            for button in self.options_buttons:
                button.setEnabled(True)
            self.next_button.setEnabled(False)
        else:
            QMessageBox.information(self, "Quiz Finished", "You have answered all the questions.")
            
            # main_window = self.parent().parent()
            # main_window.setCentralWidget(main_window.language_assistant)
            self.update_score()
            self.go_to_main_screen()

    def update_score(self):
        self.score_label.setText(f"Score: {self.score}")

class GrammarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.score_label = QLabel("Score: 0")
        self.layout.addWidget(self.score_label)

        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.options_buttons = []
        for _ in range(4):
            button = QPushButton()
            button.clicked.connect(self.check_answer)
            self.options_buttons.append(button)
            self.layout.addWidget(button)

        self.next_button = QPushButton("Next Question")
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setEnabled(False)
        self.layout.addWidget(self.next_button)

        self.current_question = 0
        self.score = 0

        self.exercises = [
            {
                "question": "Fill in the blank: Yo ___ español.",
                "options": ["hablo", "hablas", "habla", "hablan"],
                "answer": "hablo"
            },
            {
                "question": "Choose the correct form of the verb: Él ___ al cine.",
                "options": ["va", "vas", "ir", "vamos"],
                "answer": "va"
            },
        ]

    def start_exercise(self):
        self.current_question = 0
        self.score = 0
        self.update_score()
        self.display_question(self.current_question)

    def display_question(self, question_index):
        question = self.exercises[question_index]
        self.question_label.setText(question["question"])

        for i, option in enumerate(question["options"]):
            self.options_buttons[i].setText(option)
            self.options_buttons[i].setEnabled(True)
            self.options_buttons[i].setStyleSheet("")

        self.next_button.setEnabled(False)

    def check_answer(self):
        sender = self.sender()
        selected_option = sender.text()
        correct_answer = self.exercises[self.current_question]["answer"]

        if selected_option == correct_answer:
            QMessageBox.information(self, "Result", "Correct!")
            sender.setStyleSheet("background-color: green;")
            self.score += 10
        else:
            QMessageBox.information(self, "Result", "Incorrect!")
            sender.setStyleSheet("background-color: red;")
            self.score -= 10

        self.update_score()

        for button in self.options_buttons:
            button.setEnabled(False)

        self.next_button.setEnabled(True)

    def next_question(self):
        self.current_question += 1

        if self.current_question < len(self.exercises):
            self.display_question(self.current_question)
        else:
            QMessageBox.information(self, "Exercise Finished", "You have completed all the exercises.")

            main_window = self.parent().parent()
            main_window.setCentralWidget(main_window.language_assistant)

    def update_score(self):
        self.score_label.setText(f"Score: {self.score}")


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    language_assistant = LanguageLearningAssistant()
    language_assistant.show()

    sys.exit(app.exec())


