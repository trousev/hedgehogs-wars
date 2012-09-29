#-------------------------------------------------
#
# Project created by QtCreator 2012-07-31T21:55:27
#
#-------------------------------------------------

QT       += core gui network

TARGET = DedgehogDesk
TEMPLATE = app


SOURCES += main.cpp\
        umain.cpp \
    hcell.cpp \
    serverthread.cpp \
    hedgehog.cpp \
    flyingcabbage.cpp \
    pysyntax.cpp

HEADERS  += umain.h \
    hcell.h \
    serverthread.h \
    hedgehog.h \
    flyingcabbage.h \
    pysyntax.h

FORMS    += umain.ui

RESOURCES += \
    DeskItems.qrc
