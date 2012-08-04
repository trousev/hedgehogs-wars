#include "umain.h"
#include "ui_umain.h"
#include "hcell.h"
#include "hedgehog.h"
#include <QTimeLine>
#include <QImage>
#include <QPixmap>
#include <QGraphicsItemAnimation>
int __singleton_last_id = 0;
uMain::uMain(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::uMain)
{
    ui->setupUi(this);
    ui->_main_view->setScene(new QGraphicsScene);
    ui->_stats->setLayout(new QVBoxLayout);
}

void uMain::addCell(int i, int j, int content)
{
        QString index = QString("%1,%2").arg(i).arg(j);
        if(!_all_cells[index])
        {
            _all_cells[index] = new HCell;
            _all_cells[index]->moveBy(i*CELL_SIZE,j*CELL_SIZE);

            ui->_main_view->scene()->addItem(_all_cells[index]);
        }
        _all_cells[index]->setContent((HCell::CellContent) content);
}
void uMain::addCells(int width, int height)
{
    for(int i=0; i<width; i++) for(int j=0; j<height; j++)
        addCell(i,j);
}
int  uMain::newHedgehog()
{
    int index = _hogs.count();
    HedgeHog * hog = new HedgeHog;
    ui->_main_view->scene()->addItem(hog);
    _hogs << hog;
    __singleton_last_id = index;
    ui->_stats->layout()->addWidget(hog->label());
    hog->setProperty("id",QString("%1").arg(index));
    return index;
}

void uMain::moveHedgehog(int id, int x, int y)
{
    QGraphicsItem *ball = _hogs[id];

    QTimeLine *timer = new QTimeLine(1000);
    timer->setFrameRange(0, 100);

    QGraphicsItemAnimation *animation = new QGraphicsItemAnimation;
    animation->setItem(ball);
    animation->setTimeLine(timer);

    for (int i = 0; i < CELL_SIZE; i++)
        animation->setPosAt(i / CELL_SIZE, QPointF(_hogs[id]->pos().x() + i*x, _hogs[id]->pos().y() + i*y));

    timer->start();
    _hogs[id]->moveBy(CELL_SIZE*x, CELL_SIZE*y);
}
void uMain::throwCabbage(int fromX, int fromY, int x, int y)
{
    QGraphicsPixmapItem * ball = new QGraphicsPixmapItem(QPixmap(":/cabbage_big.png"));
    ball->moveBy(fromX*CELL_SIZE, fromY*CELL_SIZE);

    /*QGraphicsItemAnimation *animation = new QGraphicsItemAnimation;
    animation->setItem(ball);
    animation->setTimeLine(timer);

    for (int i = 0; i < CELL_SIZE; i++)
        animation->setPosAt(i / CELL_SIZE, QPointF(_hogs[id]->pos().x() + i*x, _hogs[id]->pos().y() + i*y));

    timer->start();*/

}

void uMain::killHedgehog(int id)
{
    _hogs[id]->kill();
}

void uMain::takeHedgehog(int id)
{
    ui->_main_view->scene()->removeItem(_hogs[id]);
}

uMain::~uMain()
{
    delete ui;
}

void uMain::on_actionExit_triggered()
{
    exit(0);
}

int uMain::last_id()
{
    return __singleton_last_id;
}

void  uMain::setHedgehog(int id, QString key, QString value)
{
    _hogs[id]->setProperty(key,value);
}
void uMain::setStatus(QString status)
{
    ui->_status->setText(status);
}
