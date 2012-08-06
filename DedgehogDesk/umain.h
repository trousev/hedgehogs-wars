#ifndef UMAIN_H
#define UMAIN_H

#include <QMainWindow>
#include <QProcess>
#include <QMap>
#include <QTextBrowser>
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

    QMap<QProcess*, QTextBrowser*> outputs;
    int player_id;
public:
    explicit uMain(QWidget *parent = 0);
    ~uMain();
public slots:

    void log(QString message);
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
    void spawnProcess(QString name, QString process, QStringList arguments);
    void onTimer();
    void output();
    void updateBotList();
private slots:
    void on_actionExit_triggered();

    void on__start_game_clicked();

    void on__add_player_clicked();

    void on__duplicate_clicked();

    void on__player_list_activated(const QString &arg1);

    void on__text_textChanged();



    void on__savebut_clicked();

    void on_actionNew_Game_triggered();
    void closeTab(int i);
private:
    void scrollDown(QTextBrowser * br);
    void save();
    void open(QString filename);
    Ui::uMain *ui;
};

#endif // UMAIN_H
