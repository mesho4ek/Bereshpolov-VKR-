import matplotlib.pyplot as plt

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, QApplication, QFileDialog
import sys
import os


# Класс построения тхт файла с историей эффективности с дальнейшим построением графика
class History:

    # Процесс сохранения результатов в txt файл
    def SaveValue(self, value, obuh, usli, epohi, file_name="history.txt", f_read=None):
        # Получаем последний ID
        last_id = 0
        # Если файла нет - то значит тут будет ошибка так как нечего читать
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()  # чтение построчно
                last_id = len(lines)  # Нахождение длины списка

            # Если записей не было, то не меняем значение
            if (len(lines) > 0):
                last_id = int(str.split(lines)[0])  # Разделяет строку на список подстрок
            f_read.close()
        except:
            pass
        # Записываем результат
        f_write = open(file_name, "a+")
        # f_write.write(str(last_id + 1) + " " + str(value) + "\n")
        f_write.write(str(last_id + 1) + " " + str(value) + " " + str(obuh) + " " + str(usli) + " " + str(epohi) + "\n")
        f_write.close()

    # Построение графика
    def ShowGraph(self, file_name="history.txt"):
        data_x0 = []
        data_y0 = []
        data_y1 = []
        data_y2 = []
        data_y3 = []
        print("начало работы")

        try:
            f_read = open(file_name, "r")
            lines = f_read.readlines()
            for line in lines:
                arr = str.split(line)  # Возвращает str строковую версию объекта

                data_x0.append(
                    int(arr[0]))  # append() добавляет в конец списка элемент, переданный ему в качестве аргумента.
                data_y0.append(float(arr[1]))
                data_y1.append(float(arr[2]))
                data_y2.append(float(arr[3]))
                data_y3.append(float(arr[4]))
        except:
            return False

        try:
            fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8, 8), num="Графики для анализа")  # figsize - размер окна
            fig.suptitle('Анализ работы нейросети')
           # fig.title('Анализ работы нейросети')
            axs[0, 0].scatter(data_x0, data_y0, color='g')  # Отображение y и x в виде линий
            axs[0, 0].set_title("По Эффективности сети")
            axs[0, 1].scatter(data_x0, data_y1, color='k')  # Отображение y и x в виде линий
            axs[0, 1].set_title("По параметрам коэффициента обучения")
            axs[1, 0].scatter(data_x0, data_y2,)  # Отображение y и x в виде линий
            axs[1, 0].set_title("История по количеству скрытых узлов")
            axs[1, 1].scatter(data_x0, data_y3, color='r')  # Отображение y и x в виде линий
            axs[1, 1].set_title("История по количеству эпох")

            #axs[0, 0].xlabel("Номер попытки")  # ось абсцисс
            #axs[0, 0].ylabel("Эффективность")  # ось ординат
            #axs[0, 1].xlabel("Номер попытки")  # ось абсцисс
            #axs[0, 1].ylabel("Эффективность")  # ось ординат
            #axs[1, 0].xlabel("Номер попытки")  # ось абсцисс
            #axs[1, 0].ylabel("Эффективность")  # ось ординат
            #axs[1, 1].xlabel("Номер попытки")  # ось абсцисс
            #axs[1, 1].ylabel("Эффективность")  # ось ординат

            axs[0, 0].grid()  # Настройка линии сетки
            axs[0, 1].grid()  # Настройка линии сетки
            axs[1, 0].grid()  # Настройка линии сетки
            axs[1, 1].grid()  # Настройка линии сетки

            plt.show()  # Показать график
        except:
            return False

        return True


# Второе окно
class SecondApp(QMainWindow):
    history = History()

    def __init__(self, parent=None):
        super(SecondApp, self).__init__(parent)
        self.ui = uic.loadUi("int22.ui")
        self.ReadComboBox_2()
        self.ui.move(self.ui.pos().x() + 1200, self.ui.pos().y() + 350)
        self.ui.show()
        self.set2()


    def ReadComboBox_2(self):
        files = os.listdir(os.getcwd()) #содержит список файлов и папок в текущей рабочей директории
        self.ui.combo_history.clear()

        for file in files:
            arr = file.split('.')
            if (arr[len(arr) - 1].lower() == "txt"):
                self.ui.combo_history.addItem(file)
                # print(files)

    def set2(self):
        self.ui.history_button.clicked.connect(lambda: self.drawData())
        self.ui.new_history_button.clicked.connect(lambda: self.NewHistory())
        self.ui.delete_button.clicked.connect(lambda: self.warning_delete_button())

    def NewHistory(self):
        dialog = QFileDialog(self)
        dialog.setLabelText(QFileDialog.Accept, "Создать")
        dialog.setLabelText(QFileDialog.Reject, "Отмена")
        #dialog.setNameFilter("Выбор файла (*.txt)")
        # если хочу добавить выбор файлов
        # dialog.setNameFilter("Выбор файла (*.txt *.py)")
        dialog.setNameFilters(["Выбор файла (*.txt *.py)", "Только .py файлы (*.py)", "Только .txt файлы (*.txt)"])
        if (dialog.exec()):
            file = dialog.selectedFiles()[0] #присваиваем путь к переменной

            arr = file.split(".") # скан строки и добавление разделителя в виде точки
            if (arr[len(arr) - 1].lower() != "txt"):
                file += ".txt"

            if (os.path.isfile(file)):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("Изменение файла")
                msg.setText("Перезаписать файл?")
                msg.setInformativeText(
                    'Все данные, которые сохранены были в этот файл до этого будут утеряны')
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

                if msg.exec() == QMessageBox.Cancel:
                    return
            open(file, 'w') #"w" файл только для записи либо перезаписи

        self.ReadComboBox_2()

    def warning_delete_button(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Удаление истории")
        msg.setText("Удалить текущую историю?")
        msg.setInformativeText(
            'Все данные, которые сохранены в этот файл будут утеряны')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = msg.exec()

        if returnValue == QMessageBox.Yes:
            self.DeleteHistory()
            print("Удаление выполнено")

    def DeleteHistory(self):
        filename = self.ui.combo_history.currentText()
        if (filename == ""):
            return

        text = os.getcwd() + "/" + filename
        os.remove(text)
        self.ReadComboBox_2()

    def drawData(self):
        print("Мб работает")
        fn = self.ui.combo_history.currentText()
        if self.history.ShowGraph(fn):
            print("ok")
        else:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("График не построен, данные не связаны с этой работой либо их нет")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()  # Показываем окно ошибки пользавателю

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SecondApp()
    sys.exit(app.exec_())
