#include "hcell.h"
#include <QPainter>
#include <QMap>

QMap <HCell::CellContent, QImage> _images;

void HCell::initResources()
{
    _images[HNone] = QImage(":/grass.png");
    _images[HApple] = QImage(":/apple.png");
    _images[HKit] = QImage(":/kit.png");
    _images[HCabbage] = QImage(":/cabbage.png");
}

HCell::HCell(QGraphicsItem *parent, QGraphicsScene * scene) :
    QGraphicsItem(parent,scene)
{
    _content = HNone;
}

void HCell::setContent(CellContent content)
{
    _content = content;
    update();
}

QRectF HCell::boundingRect() const
{
    return QRectF(0.0,0.0,64.0,64.0);
}
void HCell::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    //painter->drawLine(0,0,64.0,64.0);
    //painter->
    QImage grass = _images[HNone];
    grass = grass.scaled(CELL_SIZE,CELL_SIZE);
    painter->drawImage(0,0,grass);
    if(_content != HNone)
    {
        QImage addict = _images[_content];
        addict = addict.scaled(CELL_SIZE,CELL_SIZE);
        painter->drawImage(0,0,addict);
    }
}
