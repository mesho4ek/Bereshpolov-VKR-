from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import sys
import tempfile
from PIL import Image

class GraphicEditor(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Первые настройки
        self.setWindowTitle("Тестирование")
        self.setGeometry(100, 200, 300, 300)
        format = 380
        self.setMaximumSize(format, format)
        self.setMinimumSize(format, format)



        # Создаем форму картинки на всю геометрию
        self.image = QImage(self.size(), QImage.Format_RGB32)
        # Красим в белый цвет форму
        self.image.fill(Qt.white)

        # Стандартные настройки
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black

        # Объект QPoint для определения точки
        self.lastPoint = QPoint()

        # Cоздаем меню, режимы
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Файл")
        b_size = mainMenu.addMenu("Шрифт")
        b_color = mainMenu.addMenu("Цвет шрифта")

        testingMenu = mainMenu.addMenu("Тестируем")
        testAction = QAction("Начать тестирование", self)
        testAction.setShortcut("Ctrl + D")
        testingMenu.addAction(testAction)
        testingMenu.triggered.connect(self.on_testing_triggered)

        # Cоздаем меню сохранения
        saveAction = QAction("Сохранить изображение", self)
        # добавляем ярлык для действия сохранения
        saveAction.setShortcut("Ctrl + S")
        # Сохранить меню в файл
        fileMenu.addAction(saveAction)
        # Добавление действия к сохранению
        saveAction.triggered.connect(self.save)

        # creating clear action
        clearAction = QAction("Стереть все", self)
        # Добавляем ярлык для действия очищения
        clearAction.setShortcut("Ctrl + C")
        # Добавляем в меню
        fileMenu.addAction(clearAction)
        # Добавляем триггер или действие на функцию очищения
        clearAction.triggered.connect(self.clear)

        # creating clear action
        downloadAction = QAction("Загрузить изображение", self)
        # Добавляем ярлык для действия очищения
        downloadAction.setShortcut("Ctrl + F")
        # Добавляем в меню
        fileMenu.addAction(downloadAction)
        # Добавляем триггер или действие на функцию очищения
        downloadAction.triggered.connect(self.download)


        # Создаем для шрифта доп размер пикселя
        pix_4 = QAction("4px", self)
        # добавляем в b_size
        b_size.addAction(pix_4)
        # Создаем тригер к функции на 4 пикселя
        pix_4.triggered.connect(self.Pixel_4)

        pix_7 = QAction("7px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)

        pix_9 = QAction("9px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)

        pix_12 = QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        # Создаем цвет
        black = QAction("Черный", self)
        # Добавляем в цвет шрифта
        b_color.addAction(black)
        # Связываем с функцией цвета
        black.triggered.connect(self.blackColor)

        # Делаем так для каждого цвета
        white = QAction("Белый", self)
        b_color.addAction(white)
        white.triggered.connect(self.whiteColor)

        green = QAction("Зеленый", self)
        b_color.addAction(green)
        green.triggered.connect(self.greenColor)

        yellow = QAction("Желтый", self)
        b_color.addAction(yellow)
        yellow.triggered.connect(self.yellowColor)

        red = QAction("Красный", self)
        b_color.addAction(red)
        red.triggered.connect(self.redColor)

# метод проверки щелчков мыши
    def mousePressEvent(self, event):

        #  если нажата левая кнопка мыши
        if event.button() == Qt.LeftButton:
            # сделать флаг рисования истинным
            self.drawing = True
            # установить последнюю точку на точку курсора
            self.lastPoint = event.pos()

# метод отслеживания активности мыши
    def mouseMoveEvent(self, event):

        # проверка, нажата ли левая кнопка и установлен ли флаг рисования true
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            # cоздаем painter объект
            painter = QPainter(self.image)

            #  устанавливаем перо художника
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            # проведите линию от последней точки курсора до текущей точки
            # это позволит нарисовать только один шаг
            painter.drawLine(self.lastPoint, event.pos())

            # изменить последнюю точку
            self.lastPoint = event.pos()
            # обновляем
            self.update()

# метод для отпускания левой кнопки
    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            # сделать флаг рисования ложным
            self.drawing = False

# paint event
    def paintEvent(self, event):
        # создаем холст
        canvasPainter = QPainter(self)
        # рисуем прямоугольник на холсте
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # Метод сохранения
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    # Метод очищения
    def clear(self):
        # Создаем форму картинки на всю геометрию
        self.image = QImage(self.size(), QImage.Format_RGB32)
        # make the whole canvas white
        self.image.fill(Qt.white)
        # update
        self.update()

    def download(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            image = QPixmap(file_path)
            #image = image.scaled(28, 28, aspectRatioMode=Qt.KeepAspectRatio)
            self.image = QImage(self.size(), QImage.Format_RGB32)
            self.image = image.toImage()
            self.update()

    def on_testing_triggered(self):
        with tempfile.NamedTemporaryFile(prefix="zero_image", suffix='0.png', delete=False) as temp_file:
            temp_file_path = temp_file.name  # Получаем имя временного файла
            self.image.save(temp_file_path)  # Сохраняем изображение во временный файл
            temp_file.close()  # Важно закрыть временный файл

        abs_temp_file_path = os.path.abspath(temp_file_path)  # Получаем абсолютный путь к временному файлу
        print(f"Абсолютный путь к временному файлу: {abs_temp_file_path}")
        image = Image.open(temp_file_path)  # Загрузка изображения из временного файла
        self.main_window.show_test_window(temp_file_path)


# Методы с разными пикселями
    def Pixel_4(self):
        self.brushSize = 4
    def Pixel_7(self):
        self.brushSize = 7
    def Pixel_9(self):
        self.brushSize = 9
    def Pixel_12(self):
        self.brushSize = 12

# Методы цветов
    def blackColor(self):
        self.brushColor = Qt.black
    def whiteColor(self):
        self.brushColor = Qt.white
    def greenColor(self):
        self.brushColor = Qt.green
    def yellowColor(self):
        self.brushColor = Qt.yellow
    def redColor(self):
        self.brushColor = Qt.red

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = GraphicEditor()
    window.show()
    sys.exit(App.exec())