#ifndef PYSYNTAX_H
#define PYSYNTAX_H

#include <QSyntaxHighlighter>

class PySyntax : public QSyntaxHighlighter
{
public:
    PySyntax(QTextEdit * textEditor);
};

#endif // PYSYNTAX_H
