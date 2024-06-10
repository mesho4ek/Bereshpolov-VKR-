from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys
import os
import matplotlib.pyplot as plt
import SecondApp
import Neyroset
import Progress
import grafik_blue



# Класс графический интерфейс основного окна
class App(QMainWindow):

    effect = -1
    resul_active = 0

    def __init__(self, parent=None):
        super().__init__()
        self.win2 = None  # Внешнего окна пока нет
        self.win3 = None  # Внешнего окна пока нет
        self.ui = uic.loadUi("int21.ui")
        self.use = 0
        self.ui.closeEvent = self.closeEvent
        self.ui.show()
        self.set()
        self.ReadComboBox()


    def ReadComboBox(self):
        files = os.listdir(os.getcwd())

        for file in files:
            arr = file.split('.')
            if (arr[len(arr) - 1].lower() == "csv"):
                self.ui.MNIST.addItem(file)

# Привязка методов к кнопкам (что кнопки будут вытворять)
    def set(self):
        # Реагирование на клик
        self.ui.clear_buttom.clicked.connect(lambda: self.all_clear())
        self.ui.train_button.clicked.connect(lambda: self.obuch_click(teht="<span style=\"color: #5d5;\">Обучение началось </span>"))
        self.ui.save_button.clicked.connect(lambda: self.saveData())
        self.ui.data_button.clicked.connect(lambda: self.show_new_window())
        self.ui.test_button.clicked.connect(lambda: self.open_graphic_editor())
        self.ui.pushButton.clicked.connect(lambda: self.show_test_window11())
        self.ui.pushButton_struct.clicked.connect(lambda: self.struct_neyron(self.use))
        self.ui.CommentButton_4.clicked.connect(lambda: self.on_MNIST_finished_all())


        self.ui.funcomboBox.activated.connect(lambda: self.fun_combo_Box())
        # Реагирование на изменение индекса в комбобокс
        self.ui.MNIST.activated.connect(lambda: self.warning_combobox())

        # Добавление картинки к сообщениям
        self.ui.CommentButton_2.setIcon(QIcon('ikonka-informacija.jpg'))
        self.ui.CommentButton_3.setIcon(QIcon("ikonka-informacija.jpg"))
        self.ui.CommentButton_1.setIcon(QIcon("ikonka-informacija.jpg"))
        self.ui.CommentButton_4.setIcon(QIcon("information.png"))

        # Коментарии
        self.ui.CommentButton_1.setToolTip(
            'Коэффициент обучения вводится в пределах [0,1]')  # Комменты к гиперпараметрам
        self.ui.CommentButton_2.setToolTip(
            'Количество скрытых узлов не может быть отрицательным, т.к по ним проходит нейросеть для обучения')
        self.ui.CommentButton_3.setToolTip(
            'Количество эпох показывает: сколько раз нейросеть пройдет по тренировочному набору,\n'
            ' поэтому, чем больше число, тем дольше будет проходить обучение.')
        self.ui.CommentButton_3.setToolTip(
            'Вывести расширенную информацию об эффективности обучения.')

# Работа с комбобокс
    def warning_combobox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Рекомендация")
        msg.setText("Перейти в Данные об обучении?")
        msg.setInformativeText(
            'Для каждого набора данных, для более глубокого анализа лучше использовать свою историю обучения')
        msg.setStandardButtons(QMessageBox.Open | QMessageBox.Cancel)
        returnValue = msg.exec()

        if returnValue == QMessageBox.Open:
            self.show_new_window()
            print('OK clicked')

# Открываем 2-е окно
    def show_new_window(self):
        if self.win2 is None:
            self.win2 = SecondApp.SecondApp(self)
            return

        self.win2.ui.hide()
        self.win2.ui.show()

    def open_graphic_editor(self):
        self.graphic = grafik_blue.GraphicEditor(ex)
        self.graphic.hide()
        self.graphic.show()

# Делаем опрос сети через свои изображения
    def show_test_window(self, file_name):
        try:
            self.ui.textEdit.clear()
            #plt.imshow(file_name)
            #plt.show()
            print("Работает чи да?")
            test_image_finish = self.zombie.test_own_image(file_name)
            self.ui.textEdit.setText("Тестирование произошло")
            self.display(text="Сеть сказала: " + str(test_image_finish))

        except:
            print("Работает чи не?")
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Не удалось протестировать вашу нейронную сеть, возможно ваша сеть не была обучена или выбран файл без изображения!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()# Не забываем показать ошибки пользователю


    def show_test_window11(self):
        self.ui.textEdit.clear()
        dialog = QFileDialog(self)
        dialog.setLabelText(QFileDialog.Accept, "Выбрать")
        dialog.setLabelText(QFileDialog.Reject, "Отмена")

        dialog.setNameFilters(["Выбор файла (*.png *.jpg *.gif *.raw *.bmp *.psd)"])
        if (dialog.exec()):
            file_name = dialog.selectedFiles()[0] #присваиваем путь к переменной

            try:
                print("Работает чи да?")
                #self.zombie.Calculate
                test_image_finish = self.zombie.test_own_image(file_name)
                self.ui.textEdit.setText("Тестирование произошло")
                self.display(text="Сеть сказала: " + str(test_image_finish))

            except:
                print("Работает чи не?")
                error = QMessageBox()
                error.setWindowTitle("Ошибка")
                error.setText("Не удалось протестировать вашу нейронную сеть, возможно ваша сеть не была обучена или выбран файл без изображения!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()# Не забываем показать ошибки пользователю


    def on_image_finished(self, result):
        self.ui.textEdit.clear()
        print("Сеть сказала ", result, result)
        self.ui.textEdit.setText("Тестирование произошло")
        self.display(text="Сеть сказала: " + result)

# Запись в историю
    def saveDatatest(self):
        filename = self.ui.combo_history.currentText()
        print(filename)

    def saveData(self, combobox_sek=None):
        if (self.effect < 0):
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Для записи результата нужно посчитать эффективность!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()  # Показываем окно ошибки пользавателю
            return False

        print("Сохраниение пошло...")
        history = SecondApp.History()
        ouch = float(self.ui.obuch.toPlainText())
        use = int(self.ui.usel.toPlainText())
        epoch = int(self.ui.epoh.toPlainText())


        if self.win2 is None:
            self.win2 = SecondApp.SecondApp(self)
            self.win2.hide()

        print("Принт 1")
        try:
            filename = self.win2.ui.combo_history.currentText()
            #history.SaveValue(self.effect, filename)
            history.SaveValue(self.effect, ouch, use, epoch, filename)
            self.ui.textEdit.setText("<span style=\"color: #5d5;\">результат записан в:</span>" + " " + filename)
        except:
            #history.SaveValue(self.effect)
            history.SaveValue(self.effect, ouch, use, epoch)
            self.win2.ReadComboBox_2()
            self.ui.textEdit.setText("<span style=\"color: #5d5;\">У вас нет никаких файлов для записи. Результат будет записан в history.txt</span>")

        self.effect = -1
        return True

# Метод очистки полей от введенных значений
    def all_clear(self):
        self.ui.usel.clear()
        self.ui.obuch.clear()
        self.ui.epoh.clear()
        self.ui.textEdit.clear()

    def fun_combo_Box(self):
        resul_text = self.ui.funcomboBox.currentText()
        if resul_text == "Сигмоидальная функция":
            print("RadioButton 0 выбран")
            self.resul_active = 0
        elif resul_text == "Гиперболический тангенс":
            print("RadioButton 1 выбран")
            self.resul_active = 1
        elif resul_text == "Rectified Linear Unit":
            print("RadioButton 2 выбран")
            self.resul_active = 2
        elif resul_text == "Leaky ReLU":
            print("RadioButton 3 выбран")
            self.resul_active = 3
        elif resul_text == "Softmax":
            print("RadioButton 4 выбран")
            self.resul_active = 4
        elif resul_text == "Swish":
            print("RadioButton 5 выбран")
            self.resul_active = 5
        print(self.resul_active)
        return self.resul_active

# Метод рассчета значений
    def obuch_click(self, teht):
        self.ui.textEdit.clear()
        # Берем веденные значения
        try:
            ouch = float(self.ui.obuch.toPlainText())
            self.use = int(self.ui.usel.toPlainText())
            epoch = int(self.ui.epoh.toPlainText())
            file_name = self.ui.MNIST.currentText()

        except:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Гиперпараметры введены неверно!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.setInformativeText("Предупреждение!"" \nкоэффициент обучения вводится в пределах [0;1];"
                                    " \nколичество скрытых узлов не может быть отрицательным или дробным."
                                     " \nКоличество эпох не может быть отрицательным;")

            error.exec_()  # Показываем окно ошибки пользавателю
            return

        #Передали аргументы и начинаем вычислять нейросеть
        func_activ = self.resul_active #Чекаем
        self.zombie = Neyroset.brain(ouch, self.use, epoch, file_name, func_activ)
        self.nezombie = Progress.Progress_Neyro()

        self.zombie.progressignal.connect(self.nezombie.signal_zombie)
        self.zombie.MNIST_finished.connect(self.on_MNIST_finished)
        self.zombie.start()

        #self.nezombie.info_signal.connect(self.display_info)

    def struct_neyron(self, use):
        if use != 0:
            self.zombie.visualize_network(use)
        else:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Cначала обучите сеть!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()  # Показываем окно ошибки пользавателю

    def on_MNIST_finished_all(self):
        try:
            test_MNIST_ALL_finish = self.zombie.test_all_MNIST()
        except:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Cначала обучите сеть!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()  # Показываем окно ошибки пользавателю

    def on_MNIST_finished(self, effect):
        self.effect = float(effect)
        self.display(text="Эффективность = " + effect)

    def display(self, text):
        dialog = self.ui.textEdit.setText(text)

    def closeEvent(self, event):
        print("Закрываем окно")
        reply = QMessageBox.information(self, 'Выход', 'Вы точно хотите выйти?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.closeAllWindows()  # Закрытие всех окон, которые существуют
            event.accept()
        else:
            event.ignore()
    def updateProgress(self, progress):
        self.ui.progressBar.setValue(progress)
        QApplication.processEvents()  # Позволяет обновить интерфейс во время выполнения функции

app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
