# BalanceSheetScanner
Scanning specific profitable and financially ratios - Youtube-Link: https://www.youtube.com/watch?v=9MGYmce9Trk

Wichtig: Um das Programm richtig nutzen zu können muss im Code in der data_operations-Datei erst ein API-Key hinzugefügt werden!


1. Einleitung:
Das Programm zeigt verschiedene finanzwirtschaftliche und erfolgwirtschaftliche Kennzahlen von Unternehmen. Das besondere dabei ist, dass unter "Einstellungen" verschiedene Filter eingestellt werden können, um die Kennzahlen entsprechend hervorzuheben. Standardgemäß sind keine Filter eingestellt.
Die Ergebnisse können in Form einer PDF-Datei gespeichert werden und auch als hard copy ausgedruckt werden.
________________________________________________________________________________________________________________________________________________________________

2. Funktionsweise:
Die Daten werden über die Yahoo Finance API genutzt. Genauer gesagt wird der vierteljährliche Geschäftsabschluss verwendet, wobei es keine vierteljährliche Kapitalflussrechnung gab und deshalb die jährliche Kapitalflussrechnung verwendet wurde.
Das GUI wurde mit Tkinter umgesetzt, wobei alle Funktionen über die Buttons in der GUI.py sind.
Die PDF wurde mit dem Modul FPDF erstellt und in dem Verzeichnis wo sich die main.py befindet gespeichert.
Die Einstellungen werden in einer JSON-Datei in dem Verzeichnis der main.py gespeichert.

Das Programm führt die eingestellten mathematischen Vergleiche aus und falls eine Einstellung zutreffend ist, wird das Ergebnis im Ergebnisfenster hellblau markiert.
________________________________________________________________________________________________________________________________________________________________

3. Besonderheiten:
Sollte keine entsprechende PDF-Datei im Verzeichnis bei der Erstbenutzung sein, muss die Anwendung zuerst komplett geschlossen werden, um die PDF-Datei das erste Mal zu erstellen. Wurde diese einmal erstellt, wird diese immer direkt überschrieben, auch wenn die Anwendung nicht geschlossen wird.
Diese Besonderheit muss also beim Ausdrucken auch beachtete werden, da diese Funktion auf der PDF-Datei basiert.

Manche Unternehmen haben bei manchen Bilanzpositionen keine Angaben, weshalb es vereinzelnt zu Fehlermeldungen kommen kann. Z.B. ist bei dte.de (Deutsche Telekom AG) keine Angabe bei der SG&A-Quote. Teilweise wurde dieser Fehler behoben, jeodch nur für wenige Positionen.

Kennungen, die fehlerfrei ausprobiert worden sind: lyb (Lyondell Basell), dte.de (Deutsche Telekom AG), aapl (Apple Inc.)
