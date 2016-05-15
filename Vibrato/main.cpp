#include <QApplication>
#include "fenonglets.h"

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);

    fenonglets fenetre;
    fenetre.show();

    return app.exec();
}
