#include <QtGui/QApplication>
#include "umain.h"
#include "hcell.h"
#include <QThread>
#include <QDebug>
#include <QTcpServer>
#include <QTcpSocket>
class ServerThread: public QThread
{
    Q_OBJECT
public:
    void run()
    {
        QTcpServer srv;
        srv.listen(QHostAddress::Any,10123);
        while(true)
        {
            srv.waitForNewConnection(1000);
            QTcpSocket * socket = srv.nextPendingConnection();
            qDebug() << socket;
            if(!socket)
            {
                qDebug() << " *** Still waiting for session *** ";
                continue;
            }
            socket->waitForConnected();
            socket->write("HedgeDesk 0.2 protocol.\n");
            socket->flush();
            while(true)
            {
                socket->waitForReadyRead(1000);
                //qDebug() << "New Connection";
                if(socket->isOpen() && socket->isValid())
                {
                    // all OK
                }
                else
                {
                    qDebug() << "Socket closed";
                    break;
                }
                QByteArray gotten= socket->readAll();
                gotten = gotten.replace("\n","");
                gotten = gotten.replace("\r","");
                socket->flush();

                QStringList argv = QString::fromUtf8(gotten).split(" ");
                QString command = argv[0];
                int argc = argv.count()-1;
                //qDebug() << "Got query: " << gotten;
                if(command.isEmpty())
                    continue;
                else if(command == "exit")
                {
                    socket->write("Thank you for Your visit.\n");
                    socket->flush();
                    socket->close();
                    break;
                }
                else if (command == "init")
                {
                    if(argc < 2)
                    {
                        socket->write("Specify width and height please\n");
                        continue;
                    }
                    int w = argv[1].toInt();
                    int h = argv[2].toInt();
                    emit init(w,h);
                    socket->write("OK\n"); socket->flush();
                }
                else if (command == "morph")
                {
                    if(argc < 3)
                    {
                        socket->write("Specify width, height, {none,apple,kit,cabbage}\n");socket->flush();
                        continue;
                    }
                    int w = argv[1].toInt();
                    int h = argv[2].toInt();
                    HCell::CellContent content = HCell::HNone;
                    if(argv[3] == "apple") content = HCell::HApple;
                    else if(argv[3] == "kit") content = HCell::HKit;
                    else if(argv[3] == "cabbage") content = HCell::HCabbage;
                    else if(argv[3] == "none") content = HCell::HNone;
                    else
                    {
                        socket->write("Wrong type. Use none,apple,kit,cabbage\n");socket->flush();
                        continue;
                    }
                    emit morph(w,h,content);
                    socket->write("OK\n"); socket->flush();
                }
                else if (command == "new")
                {
                    emit new_hedgehog();
                    socket->write("OK\n"); socket->flush();
                }
                else if(command == "kill")
                {
                    if(argc < 1)
                    {
                        socket->write("Provide ID please\n");socket->flush();
                        continue;
                    }
                    emit kill_hedgehog(argv[1].toInt());
                    socket->write("OK\n"); socket->flush();
                }
                else if(command == "take")
                {
                    if(argc < 1)
                    {
                        socket->write("Provide ID please");socket->flush();
                        continue;
                    }
                    emit take_hedgehog(argv[1].toInt());
                    socket->write("OK\n"); socket->flush();
                }
                else if(command == "id")
                {
                    socket->write(QString("%1\n").arg(uMain::last_id()).toUtf8());socket->flush();
                }
                else if(command == "move")
                {
                    if(argc < 3)
                    {
                        socket->write("Provide ID , X and Y please. X and Y are relative.");socket->flush();
                        continue;
                    }
                    emit move_hedgehog(argv[1].toInt(), argv[2].toInt(), argv[3].toInt());
                    socket->write("OK\n"); socket->flush();
                }
                else if (command == "set")
                {
                    if(argc < 3)
                    {
                        socket->write("Provide ID , key and value to set.");socket->flush();
                        continue;
                    }
                    emit alter_hedgehog(argv[1].toInt(), argv[2], argv[3]);
                    socket->write("OK\n"); socket->flush();
                }
                else if (command == "throw")
                {
                    if(argc < 4)
                    {
                        socket->write("Need fromX,fromY,toX,toY. ");socket->flush();
                        continue;
                    }
                    emit cabbage(argv[1].toInt(),argv[2].toInt(),argv[3].toInt(),argv[4].toInt());
                    socket->write("OK\n"); socket->flush();
                }
                else if (command == "message")
                {
                    emit status(argv.join(" ").replace("message",""));
                    socket->write("OK\n"); socket->flush();
                }
                else
                {
                    socket->write(QString("Command not found: %1\n").arg(command).toUtf8());
                    socket->flush();
                }
            }
        }
    }
signals:
    void init(int width, int height);
    void morph(int x, int y, int content);
    void hedgehog_id();
    void new_hedgehog();
    void kill_hedgehog(int id);
    void move_hedgehog(int id, int x, int y);
    void take_hedgehog(int id);
    void alter_hedgehog(int id, QString name, QString value);
    void status(QString status);
    void cabbage(int fromX, int fromY, int toX, int toY);
};

