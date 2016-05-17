#ifndef FENONGLETS_H
#define FENONGLETS_H

#include <QGraphicsScene>
#include <QtWidgets>

class fenonglets : public QWidget
{
    Q_OBJECT

    public:
    fenonglets();

    //private slots:
    //void ajouterConnexion();

    private:
    //QLabel *explication;


    QPushButton *enregistrer;
    QPushButton *enregistrerFin;
    QPushButton *annulerDernierEnregistrement;
    QCheckBox *allumerTele;
    QCheckBox *eteindreTele;
    QCheckBox *eteindreLumiere;
    QCheckBox *allumerLumiere;
    QCheckBox *fermerVolets;
    QCheckBox *ouvrirVolets;
    QCheckBox *allumerClimatisation;
    QCheckBox *eteindreClimatisation;
    QCheckBox *augmenterChauffage;
    QCheckBox *diminuerChauffage;
    QGroupBox *groupCommentaires;
    QDateEdit *date;
    QTextEdit *role;
    QPushButton *valider;
    QPushButton *quitter;

};


#endif // FENONGLETS_H
