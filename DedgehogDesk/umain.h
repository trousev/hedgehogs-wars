#ifndef UMAIN_H
#define UMAIN_H

#include <QMainWindow>
#include <QMap>
#include "hedgehog.h"
#include "hcell.h"
namespace Ui {
class uMain;
}

class uMain : public QMainWindow
{
    Q_OBJECT

    QMap<QString, HCell*> _all_cells;
    QList<HedgeHog * > _hogs;
public:
    explicit uMain(QWidget *parent = 0);
    ~uMain();
public slots:
    static int last_id();
    int newHedgehog();
    void moveHedgehog(int id, int x, int y);
    void killHedgehog(int id);
    void takeHedgehog(int id);
    void setHedgehog(int id, QString key, QString value);
    void addCell(int i, int j, int content = HCell::HNone);
    void addCells(int width, int height);
    void throwCabbage(int fromX, int fromY, int x, int y);
    void setStatus(QString status);
private slots:
    void on_actionExit_triggered();

private:
    Ui::uMain *ui;
};

#endif // UMAIN_H
