#include <QtGui/QApplication>
#include "umain.h"
#include "hcell.h"
#include "hedgehog.h"
#include <QThread>
#include <QDebug>
#include <QTcpServer>
#include <QTcpSocket>
#include "serverthread.h"
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    HCell::initResources();
    HedgeHog::initResources();
    uMain w;

    ServerThread t;
    t.start();
    qRegisterMetaType<HCell::CellContent>("HCellContent");
    QObject::connect(&t,SIGNAL(init(int,int)),&w,SLOT(addCells(int,int)));
    QObject::connect(&t,SIGNAL(morph(int,int,int)),&w,SLOT(addCell(int,int,int)));
    QObject::connect(&t,SIGNAL(new_hedgehog()),&w,SLOT(newHedgehog()));
    QObject::connect(&t,SIGNAL(move_hedgehog(int,int,int)),&w,SLOT(moveHedgehog(int,int,int)));
    QObject::connect(&t,SIGNAL(kill_hedgehog(int)),&w,SLOT(killHedgehog(int)));
    QObject::connect(&t,SIGNAL(take_hedgehog(int)),&w,SLOT(takeHedgehog(int)));
    QObject::connect(&t,SIGNAL(alter_hedgehog(int,QString,QString)),&w,SLOT(setHedgehog(int,QString,QString)));
    QObject::connect(&t,SIGNAL(status(QString))  ,&w,SLOT(setStatus(QString)));
    w.show();
    return a.exec();
}
