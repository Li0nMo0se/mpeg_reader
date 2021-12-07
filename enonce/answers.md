# TVID projet

## A. Jouer un flux MPEG-2 élémentaire de test

1. Dans le dossier videos/elementary, avec vlc, visualisez les séquences MPEG-2 suivantes :
`vlc -V <renderer> bw_numbers.m2v / pendulum.m2v / Jaggies1.m2v` avec `<renderer> = x11` ou `xvideo`, selon ce qui fonctionne sur votre machine

`vlc -V x11 bw_numbers.m2v`
Pour dentrelacer, `clic droit` -> `video`-> `deintrelace` -> `Off\On`

2. Avec mpeg2dec, convertissez en pile d’images votre séquence MPEG-2 choisie (cf. aide de mpeg2dec). Il est recommandé de sortir les images au format pgm pour pouvoir les traiter ultérieurement.
`../tools/mpeg2dec/src/mpeg2dec -o pgm ../videos/elementary/bw_numbers.m2v`

3. Observez les pgm générées. Comment sont-elles structurées? Quel est le format de l’image: résolution, profondeur, sampling mode?

![](https://i.imgur.com/7lLn8vP.png)

* Format: PGM
* image haut: 2 images consécutives entrelacées.
* Résolution: 720x480
* chroma: 360x240
* sampling mode: 4\:2\:0 (YUV)
* Profondeur: 8-bit

4. Modifiez mpeg2dec pour logger simplement les flags progressive_frame, top_field_first, repeat_first_field de chaque image décodée.

Dans le fichier `mpeg2dec.c:55` `static int verbose = 1;`, mettre le verbose à 1.

* Progressive Frame: **PROG**
* Top Field First: **TFF**
* Repeat First Field:
Log:
```
5c S- --- --- - SEQUENCE MPEG2 MP@ML 720x480 chroma 360x240 fps 29.97 maxBps 300000 vbv 229376 picture 720x480 display 720x480 pixel 8x9 guessed 10x11
      64 SG --- --- - GOP CLOSED  0: 0: 0: 0
      84 SG AA- --- ? PICTURE I fields 2 TFF time_ref 2 offset 0/0 0/0
    5084 SG aa- --- ? SLICE
    50c4 SG BB- BB- B PICTURE B fields 2 TFF time_ref 0 offset 0/0 0/0
    6c84 SG bb- bb- b SLICE
    6cc4 SG CC- CC- C PICTURE B fields 2 TFF time_ref 1 offset 0/0 0/0
    7804 SG cc- cc- c SLICE
    7844 SG DD- aa- ? PICTURE P fields 2 TFF time_ref 5 offset 0/0 0/0
    8ec4 SG dd- aa- ? SLICE
    8f04 SG EE- EE- E PICTURE B fields 2 TFF time_ref 3 offset 0/0 0/0
    9984 SG ee- ee- e SLICE
    99c4 SG FF- FF- F PICTURE B fields 2 TFF time_ref 4 offset 0/0 0/0
    a3c4 SG ff- ff- f SLICE
    a404 SG GG- dd- a PICTURE P fields 2 TFF time_ref 8 offset 0/0 0/0
    c244 SG gg- dd- a SLICE
    c284 SG HH- HH- H PICTURE B fields 2 TFF time_ref 6 offset 0/0 0/0
    e1c4 SG hh- hh- h SLICE
    e204 SG II- II- I PICTURE B fields 2 TFF time_ref 7 offset 0/0 0/0
   10904 SG ii- ii- i SLICE
   10944 SG JJ- gg- d PICTURE P fields 2 TFF time_ref 11 offset 0/0 0/0
   13104 SG jj- gg- d SLICE
   13144 SG KK- KK- K PICTURE B fields 2 TFF time_ref 9 offset 0/0 0/0
   15704 SG kk- kk- k SLICE
   15744 SG LL- LL- L PICTURE B fields 2 TFF time_ref 10 offset 0/0 0/0
   17e44 SG ll- ll- l SLICE
   17e84 SG MM- jj- g PICTURE P fields 2 TFF time_ref 14 offset 0/0 0/0
   1a544 SG mm- jj- g SLICE
   1a584 SG NN- NN- N PICTURE B fields 2 TFF time_ref 12 offset 0/0 0/0
   1cc84 SG nn- nn- n SLICE
   1ccc4 SG OO- OO- O PICTURE B fields 2 TFF time_ref 13 offset 0/0 0/0
   1f384 SG oo- oo- o SLICE
```

5. Avec votre propre code et dans le langage de votre choix, implémentez un convertisseur d’images vers un format plus humainement lisible (ppm RGB est assez universel). Cela vous servira à:
    * Comprendre et implémenter une conversion YUV → RGB
    * Faire une application que vous allez progressivement enrichir

See `ppm2pgm.py`