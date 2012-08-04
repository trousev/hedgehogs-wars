#include "hedgehog.h"
#include "hcell.h"
#include <QPainter>
static QImage _Hedge_dog;
static QImage _Hedge_dog_dead;

void HedgeHog::initResources()
{
    _Hedge_dog = QImage(":/hedgehog.png").scaled(CELL_SIZE,CELL_SIZE);
    _Hedge_dog_dead = QImage(":/dying_hedgehog.png").scaled(CELL_SIZE,CELL_SIZE);
}
void HedgeHog::setProperty(QString name, QString value)
{
    if(!propsorder.contains(name))
        propsorder << name;
    props[name] = value;
    label();
    _myLabel->update();
}
QLabel * HedgeHog::label()
{
    QString text;

    foreach(QString prop, propsorder)
    {
        if(prop == "id") continue;
        text += QString("<tr><td>%1</td><td>&nbsp;</td><td>%2</td></tr>").arg(prop,props[prop]);
    }
    _myLabel->setText(QString("HH#%1<table>%2</table>").arg(props["id"],text));
    return _myLabel;
}

HedgeHog::HedgeHog(QGraphicsItem *parent, QGraphicsScene *scene)
    :QGraphicsItem(parent,scene)
{
    killed   = false;
    _myLabel = new QLabel("Hedgehog");
}

QRectF HedgeHog::boundingRect() const
{
    return QRectF(0,0,CELL_SIZE,CELL_SIZE);
}

void HedgeHog::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    if(!killed)
        painter->drawImage(0,0,_Hedge_dog);
    else
        painter->drawImage(0,0,_Hedge_dog_dead);
}

void HedgeHog::kill()
{
    killed = true;
    update();
}
