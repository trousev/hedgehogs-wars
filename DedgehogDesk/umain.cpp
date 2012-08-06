#include "umain.h"
#include "ui_umain.h"
#include <QScrollBar>
#include <QInputDialog>
#include <QDebug>
#include <QFile>
#include <QDir>
#include <QTimer>
#include "hcell.h"
#include "hedgehog.h"
#include <QTimeLine>
#include <QImage>
#include <QPixmap>
#include <QGraphicsItemAnimation>
#include <QProcess>

int __singleton_last_id = 0;
uMain::uMain(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::uMain)
{
    ui->setupUi(this);
    ui->_main_view->setScene(new QGraphicsScene);
    ui->_stats->setLayout(new QVBoxLayout);
    QTimer * timer = new QTimer(this);
    connect(timer,SIGNAL(timeout()),this,SLOT(onTimer()));
    timer->start(100);
    updateBotList();
    player_id = 0;
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
void uMain::scrollDown(QTextBrowser *br)
{
    QScrollBar *sb = br->verticalScrollBar();
    sb->setValue(sb->maximum());
}

void uMain::log(QString message)
{
    ui->_log->insertHtml(QString("<br />%1").arg(message));
    scrollDown(ui->_log);
}

void uMain::addCells(int width, int height)
{
    for(int i=0; i<width; i++) for(int j=0; j<height; j++)
        addCell(i,j);
    log(QString::fromUtf8("Игровое поле будет размера %1 на %2").arg(width).arg(height));
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
    log(QString::fromUtf8("В игру вступает ёжик за номером %1!").arg(index));
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
        animation->setPosAt(i / CELL_SIZE, QPointF(_hogs[id]->x*CELL_SIZE + i*x, _hogs[id]->y*CELL_SIZE + i*y));

    timer->start();

    _hogs[id]->x += x;
    _hogs[id]->y += y;
    log(QString::fromUtf8("Ёжик %1 перемещается на (%2,%3) ").arg(id).arg(x).arg(y));
    //_hogs[id]->moveBy(CELL_SIZE*x, CELL_SIZE*y);
}
void uMain::throwCabbage(int fromX, int fromY, int x, int y)
{
    QGraphicsPixmapItem * ball = new QGraphicsPixmapItem(QPixmap(":/cabbage_big.png"));
    ball->moveBy(fromX*CELL_SIZE, fromY*CELL_SIZE);
    ui->_main_view->scene()->addItem(ball);

    QTimeLine *timer = new QTimeLine(1000);
    timer->setFrameRange(0, 100);

    QGraphicsItemAnimation *animation = new QGraphicsItemAnimation;
    animation->setItem(ball);
    animation->setTimeLine(timer);
    x -= fromX;
    y -= fromY;
    for (int i = 0; i < CELL_SIZE; i++)
    {
        animation->setPosAt(i / CELL_SIZE, QPointF(ball->x() + i*x, ball->y() + i*y));
        animation->setScaleAt(i/CELL_SIZE,1.0,1.0);
    }
    animation->setScaleAt(1.0,0.0,0.0);

    timer->start();
    log(QString::fromUtf8("В точку (%1,%2) летит капуста !").arg(fromX+x).arg(fromY+y));
}

void uMain::killHedgehog(int id)
{
    log(QString::fromUtf8("Ёжик %1 умирает. Мы скорбим о нем. ").arg(id));
    _hogs[id]->kill();
}

void uMain::takeHedgehog(int id)
{
    log(QString::fromUtf8("Труп ёжика %1 полностью разложился. ").arg(id));
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
    QString oldprop = _hogs[id]->property(key);
    if(oldprop == value)
        return ;
    log(QString::fromUtf8("У ежика %1 %2 становится %3").arg(id).arg(key).arg(value));
    _hogs[id]->setProperty(key,value);
}
void uMain::setStatus(QString status)
{
    log(status);
    ui->statusBar->showMessage(status);
    ui->_status->setText(status);
}

void uMain::onTimer()
{
}
void uMain::output()
{
    QProcess * process = qobject_cast<QProcess*>(sender());
    QTextBrowser * browser = outputs[process];
    if(browser)
    {
        QByteArray stdout = process->readAllStandardOutput();
        QByteArray stderr = process->readAllStandardError();
        if(!stdout.isEmpty())
            browser->insertHtml(QString("<br><font color=\"blue\">%1</font>").arg(QString(stdout)));
        if(!stderr.isEmpty())
            browser->insertHtml(QString("<br><font color=\"red\">%1</font>").arg(QString(stderr)));
        scrollDown(browser);
    }
    else
        qDebug() << process->readAll();
}

void uMain::spawnProcess(QString name, QString process, QStringList arguments)
{

    QProcess * p = new QProcess(this);
    p->start(process, arguments);
    connect(p,SIGNAL(readyReadStandardOutput()),this,SLOT(output()));
    connect(p,SIGNAL(readyReadStandardError()),this,SLOT(output()));

    QTextBrowser * l = new QTextBrowser(this);
    l->setFontFamily("monospace");
    ui->_tab->addTab(l,name);
    connect(ui->_tab,SIGNAL(tabCloseRequested(int)),this,SLOT(closeTab(int)));
    outputs[p] = l;
}
void uMain::closeTab(int i)
{
    QTextBrowser * logfile = qobject_cast<QTextBrowser*> (ui->_tab->widget(i));
    if(!logfile)
        return ;
    ui->_tab->removeTab(i);

}

void uMain::on__start_game_clicked()
{

    spawnProcess("Game: main thread", "bash", QStringList() << "-c" << QString("python3 -u ../game.py -Splayers=%1 -Sport=8966").arg(ui->_player_count->value()));
    //spawnProcess("test","python3", QStringList("../game.py") );
}

void uMain::updateBotList()
{
    foreach(QString file, QDir("..").entryList(QStringList()<<"bot_*.py"))
    {
        ui->_player_list->addItem(file);
    }

}

void uMain::on__add_player_clicked()
{
    save();
    QString script_name = ui->_player_list->currentText();
    player_id ++;
    spawnProcess(QString("%1").arg(script_name),"python3",QStringList()<< "-u"<<QString("../%1").arg(script_name) << QString("-Cname=%1%2").arg(script_name).arg(player_id) );
}

void uMain::on__duplicate_clicked()
{
    save();
    QString script_name = ui->_player_list->currentText();
    QString text = QInputDialog::getText(this, tr("Enter name of new bot"),
                                         tr("Bot name:"), QLineEdit::Normal,
                                         QString());
    if(text.isEmpty())
        return;
    QFile::copy(QString("../%1").arg(script_name), QString("../bot_%2.py").arg(text));

}
void uMain::save()
{
    QFile f(ui->_filename->text());
    if(!f.open(QFile::WriteOnly))
        return ;
    f.write(ui->_text->toPlainText().toUtf8());
    f.close();
    ui->_savebut->setVisible(false);
}

void uMain::open(QString filename)
{
    QFile f (filename);
    if(!f.open(QFile::ReadOnly))
        return ;
    ui->_text->clear();
    ui->_text->insertPlainText(f.readAll());
    f.close();
    ui->_filename->setText(filename);
    ui->_savebut->setVisible(false);
}

void uMain::on__player_list_activated(const QString &arg1)
{
    save();
    open(QString("../%1").arg(arg1));
}

void uMain::on__text_textChanged()
{
    ui->_savebut->setVisible(true);
}

void uMain::on__savebut_clicked()
{
    save();
}

void uMain::on_actionNew_Game_triggered()
{
    foreach(QProcess * process, outputs.keys())
    {
        process->terminate();
        process->kill();
    }
}
