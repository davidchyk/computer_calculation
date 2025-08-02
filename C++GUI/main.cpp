#include <QApplication>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QGraphicsRectItem>
#include <QGraphicsTextItem>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    // Створення сцени
    QGraphicsScene *scene = new QGraphicsScene();

    // Параметри клітинки
    int cellSize = 80;

    // Координати для 2 змінних: A B => 00, 01, 11, 10 (Ґрей-код)
    QStringList labels = {"00", "01", "11", "10"};
    QStringList values = {"0", "1", "1", "0"};  // Приклад значень

    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            int index = i * 2 + j;
            QRectF rect(j * cellSize, i * cellSize, cellSize, cellSize);
            auto *cell = scene->addRect(rect);
            cell->setPen(QPen(Qt::black));

            // Додаємо текст у центр
            QString text = labels[index] + "\n" + values[index];
            auto *textItem = scene->addText(text);
            textItem->setPos(j * cellSize + 10, i * cellSize + 10);
        }
    }

    // Створення вікна
    QGraphicsView *view = new QGraphicsView(scene);
    view->setWindowTitle("Діаграма Вейча");
    view->resize(300, 300);
    view->show();

    return app.exec();
}
