#include "fenonglets.h"

fenonglets::fenonglets()
{
    // Groupe : Enregistrement du son
        enregistrer = new QPushButton("&Commencer l'enregistrement");
        enregistrerFin = new QPushButton("&Arrêter l'enregistrement");
        annulerDernierEnregistrement = new QPushButton("&Annuler le dernier enregistrement");

        //QLabel explication = "Il est conseiller de faire plusieurs enregistrements (3 ou 4) afin que ";
        //QLineEdit* explicationEnregistrement = new QLineEdit(this);
        //QLabel* explication = new QLabel("&Phone:", this);
        //explication->setBuddy(explicationEnregistrement);

        QHBoxLayout *boutonsEnregistrement = new QHBoxLayout;
        boutonsEnregistrement->setAlignment(Qt::AlignRight);

        boutonsEnregistrement->addWidget(enregistrer);
        boutonsEnregistrement->addWidget(enregistrerFin);
        boutonsEnregistrement->addWidget(annulerDernierEnregistrement);

        QGroupBox *groupEnregistrement = new QGroupBox("Enregistrement");
        //groupEnregistrement->setLayout(explicationEnregistrement);
        groupEnregistrement->setLayout(boutonsEnregistrement);


        // Groupe : Associer son avec objet(s)

        allumerTele = new QCheckBox("Allumer la tele");
        allumerTele->setChecked(true);
        eteindreTele = new QCheckBox("Eteindre la tele");
        eteindreLumiere = new QCheckBox("Eteindre lumiere");
        allumerLumiere = new QCheckBox("Allumer lumiere");
        fermerVolets = new QCheckBox("Fermer les volets");
        ouvrirVolets = new QCheckBox("Ouvrir les volets");
        allumerClimatisation = new QCheckBox("Allumer la climatisation");
        eteindreClimatisation = new QCheckBox("Eteindre la climatisation");
        augmenterChauffage = new QCheckBox("Augmenter la température à l'aide du chauffage");
        diminuerChauffage = new QCheckBox("Diminuer la température à l'aide du chauffage");






        QVBoxLayout *optionsLayout = new QVBoxLayout;
        optionsLayout->addWidget(allumerTele);
        optionsLayout->addWidget(eteindreTele);
        optionsLayout->addWidget(eteindreLumiere);
        optionsLayout->addWidget(allumerLumiere);
        optionsLayout->addWidget(fermerVolets);
        optionsLayout->addWidget(ouvrirVolets);
        optionsLayout->addWidget(allumerClimatisation);
        optionsLayout->addWidget(eteindreClimatisation);
        optionsLayout->addWidget(augmenterChauffage);
        optionsLayout->addWidget(diminuerChauffage);

        QGroupBox *groupOptions = new QGroupBox("Objet(s) associe(s)");
        groupOptions->setLayout(optionsLayout);



        // Groupe : Commentaires

        date = new QDateEdit;
        date->setDate(QDate::currentDate());
        role = new QTextEdit;

        QFormLayout *commentairesLayout = new QFormLayout;
        commentairesLayout->addRow("Da&te de creation :", date);
        commentairesLayout->addRow("&Connexion associee au son :", role);

        groupCommentaires = new QGroupBox("Ajouter des commentaires");
        groupCommentaires->setCheckable(true);
        groupCommentaires->setChecked(false);
        groupCommentaires->setLayout(commentairesLayout);


        // Layout : boutons du bas (valider, quitter...)
        valider = new QPushButton("&Valider !");
        quitter = new QPushButton("&Quitter");

        QHBoxLayout *boutonsLayout = new QHBoxLayout;
        boutonsLayout->setAlignment(Qt::AlignRight);

        boutonsLayout->addWidget(valider);
        boutonsLayout->addWidget(quitter);


        // Définition du layout principal, du titre de la fenêtre, etc.

        QVBoxLayout *layoutPrincipal = new QVBoxLayout;
        layoutPrincipal->addWidget(groupEnregistrement);
        layoutPrincipal->addWidget(groupOptions);
        layoutPrincipal->addWidget(groupCommentaires);
        layoutPrincipal->addLayout(boutonsLayout);

        setLayout(layoutPrincipal);
        setWindowTitle("Ajout d'une connexion");
        setWindowIcon(QIcon("icone.png"));
        resize(400, 450);


        // Connexions des signaux et des slots
        connect(quitter, SIGNAL(clicked()), qApp, SLOT(quit()));
        //connect(valider, SIGNAL(clicked()), this, SLOT(ajouterConnexion()));
        connect(valider, SIGNAL(clicked()), qApp, SLOT(quit()));

    }
