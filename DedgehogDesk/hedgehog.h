#ifndef HEDGEHOG_H
#define HEDGEHOG_H

#include <QGraphicsItem>
#include <QLabel>
class HedgeHog : public QGraphicsItem
{
    bool killed;
    QMap<QString, QString> props;
    QStringList propsorder;
    QLabel * _myLabel;
public:
    int x;
    int y;
    void setProperty(QString name, QString value);
    QString property(QString name);
    QLabel * label();

    static void initResources();
    HedgeHog(QGraphicsItem *parent = 0, QGraphicsScene * scene =0 );
    QRectF boundingRect() const;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget);
    void kill();

};

#endif // HEDGEHOG_H
