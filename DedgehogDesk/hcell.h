#ifndef HCELL_H
#define HCELL_H

#include <QObject>
#include <QGraphicsItem>
#define CELL_SIZE 32.0


class HCell : public QGraphicsItem
{
public:
    enum CellContent {HNone, HApple, HKit, HCabbage};
private:
    //Q_OBJECT

    CellContent _content;
public:
    static void initResources();
    void setContent(CellContent content);
    explicit HCell(QGraphicsItem *parent = 0, QGraphicsScene * scene =0 );
    QRectF boundingRect() const;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget);
signals:
    
public slots:
    
};

#endif // HCELL_H
