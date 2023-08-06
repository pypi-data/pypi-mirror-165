This Readme contains the detailed specifications of the project.

(Version en français au bas de la page)

# Python : Skeletal animation

#### Project No.: 22INF-TB226

#### Student: Kohler Dimitri

#### Professor: Beurret Stéphane

#### Principal: Le Callennec Benoît

## Context

The Imaging group of HE-Arc Engineering works with motion capture data. These data are obtained
thanks to motion detection tools such as Kinect, then displayed using the GeeXLab program. The
motion capture data is represented using the skeletal animation technique. HE-Arc wants to use
machine learning on this data.
Python is the leading language for machine learning. However, there is currently no python package
for 3D skeletal animation that is not dependent on a specific graphics engine.
The HE-Arc is therefore asking for a standalone python package that will allow them to manipulate
motion capture data or other types of 3D animations.
This package will be used as a base, by the Imaging group, to manipulate skeletal animation and can
be built on as needed.

## Project goals

### Primary objecive
The main goal is to implement a standalone python package to handle 3D skeletal animations.

This package must implement the following features:

- Contain a database of animations in FBX format.
- Load animations from this database or from outside.
- Store animations in an appropriate data structure.
- This data structure must allow the edition of the following elements:
    - The positions and orientations of each joint at a given time, also known as “keys”.
    - Which algorithm to use to interpolate between “keys”.
    - The unfolding in time of a joint’s animation, with the use of “timewarp curves”.
- Compute the transformations to be applied to the joints according to the principles of skeletal animation.
- Export animations in a format compatible with different graphics engines.

To visualize the output, a graphical interface based on the GeeXLab engine must be made. This
interface must allow a user to perform the following actions:

- Load an external animation or from the database.
- View the animation in real time.
- Change the angle and position of the camera.
- Pause the animation.

To demonstrate that the project works, a demonstration process must be created.
This process must include all the objectives presented.
A demonstration video respecting this process must also be created.


### Secondary objective

The secondary objective is the introduction of the motion blending technique. This adds the following
features to the python package:

- Implement a motion blending algorithm.
- Generate a blend of 2 animations using this algorithm.

The user interface must also be adapted to these changes. Therefore, the following actions must be
added:

- Select 2 animations from the database.
- Choose what weight to give to each animation.
- Generate a blend of the 2 animations in proportion to the given weights.
- View the generated animation in real time.
- Export the generated animation to a file.

## Constraints

The package created must comply with the following constraints:

- Be written in Python.
- Be easily built upon.
Moreover, as this project will be used as a basis for the Imaging group to work with skeletal animation,
it is imperative to ensure its quality. Thus, unit tests must be implemented.

## Proposed approach

- Research on the 3 following topics:
    - 3D rendering tools compatible with python.
    - Skeletal animation.
    - Motion blending.
- Choice of the 3D rendering tool to be used for the user interface (GeeXLab).
- Design of the data structure representing a 3D animation
- General design of the package.
- Creation of a mock-up of the demo interface.
- Set up the demonstration process.
- Set up the structure of the python package.
- Implement unit tests on the primary features.
- Creation of the user interface.
- Implementation of the primary features of the package.
- Implementation of motion blending and update of the user interface.

The guidelines for this work are detailed here: https://labinfo.ing.he-arc.ch/


<details><summary>Cahier des charges du projet</summary>

# Titre: Python : Skeletal animation

#### N° projet: 22INF-TB226

#### Etudiant: Kohler Dimitri

#### Professeur: Beurret Stéphane

#### Mandant: Le Callennec Benoît

## Situation initiale

La groupe Imagerie de HE-Arc Ingénierie travaille avec des données de capture de mouvement. Ces
données sont obtenues grâce à des outils de détection de mouvement tel que les Kinect, puis affichées
à l’aide du programme GeeXLab. Les données de capture de mouvements sont représentées grâce au
procédé de l’animation squelettale. La HE-Arc souhaite utiliser des algorithmes de machine learning
sur ces données.
Python est le langage le plus employé dans le domaine du machine learning. Cependant, il n’existe
actuellement aucun package python destiné à l’animation squelettale en 3D qui ne soit pas dépendant
d’un moteur graphique.
La HE-Arc demande, donc, un package python autonome leur permettant de manipuler des données
de capture de mouvements ou d’autres type d’animations en 3D.
Ce package servira de base, au groupe Imagerie, pour traiter l’animation squeletalle et pourra être
enrichi au besoin.

## Buts du projet

### Objectif principal

Le but principal est d’implémenter un package python autonome permettant de manipuler des
animations squelettales en 3D.

Ce package doit implémenter les fonctionnalités suivantes :

- Contenir une base de données d’animations au format FBX.
- Charger des animations depuis cette base de données ou depuis l’extérieur.
- Stocker les animations dans une structure de données adaptée.
- Cette structure de données doit permettre l’édition des éléments ci-dessous :
    - Les positions et orientations de chacune des articulations à un temps donné,
       également appelées « keys ».
    - Le choix de l’algorithme d’interpolation entre les « keys ».
    - Le déroulement dans le temps de l’animation d’une articulation, à l’aide de « timewarp
       curves ».
- Calculer les transformations à appliquer aux articulations selon les principes de l’animation squelettale.
- Exporter des animations dans un format compatible avec différents moteurs graphiques.

Pour visualiser les résultats, une interface graphique basée sur le moteur GeeXLab doit être mise en
place. Cette interface doit permettre à un utilisateur d’effectuer les actions suivantes :

- Charger une animation externe ou depuis la base de données.
- Visionner l’animation en temps réel.
- Modifier l’angle et la position de la caméra.
- Mettre l’animation en pause.


Afin de démontrer le bon fonctionnement du projet, un processus de démonstration doit être créer.
Ce processus doit comprendre la totalité des objectifs présentés.
Une vidéo de démonstration respectant ce processus doit également être réalisée.

### Objectif secondaire

L’objectif secondaire est l’introduction de la technique du « Motion Blending ». Ce qui ajoute au package
python ces fonctionnalités supplémentaires :

- Implémenter un algorithme de « motion blending ».
- Générer un « blend » de 2 animations grâce à cet algorithme.

L’interface utilisateur doit également être adaptée à ces changements, par conséquent les actions
suivantes doivent y être ajouter :

- Sélectionner 2 animations depuis la base de données.
- Choisir quel poids donner à chaque animation.
- Générer un « blend » des 2 animations proportionnellement aux poids donnés.
- Visionner l’animation générée en temps réel.
- Exporter l’animation générée dans un fichier.

## Contraintes

Le package développé doit se soumettre aux contraintes suivantes :

- Être réalisé en python.
- Être facilement améliorable.
De plus, comme ce projet servira de base au groupe Imagerie pour le traitement de l’animation
squelettale, il est impératif d’en assurer la qualité. Ainsi, des tests unitaires doivent être implémenter.

## Démarche proposée

- Recherche sur les 3 thèmes suivants.
    - Outils de rendu graphique 3D compatibles avec python.
    - Animation squelettale.
    - Motion blending
- Choix de l’outil de rendu graphique utilisé pour l’interface utilisateur (GeeXLab).
- Conception de la structure de données représentant une animation 3D.
- Conception générale du package.
- Création d’une maquette de l’interface utilisateur.
- Mise en place du processus de démonstration.
- Mise en place de la structure du package python.
- Implémentation des tests unitaires sur les fonctionnalités principales.
- Création de l’interface utilisateur.
- Implémentation des fonctionnalités principales du package.
- Implémentation du « motion blending » et mise à jour de l’interface utilisateur.


Les directives de travail sont détaillées ici : https://labinfo.ing.he-arc.ch/
</details>
