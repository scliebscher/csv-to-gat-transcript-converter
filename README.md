# csv-to-gat-transcript-converter
A python prorgram to make writing transcripts of conversations according to the GAT rules easier. You write the transcript text, the speakers and the time stamps in a csv table and the program will output the transcript, which you can then paste into a text editor.

# Handbuch
Der CSV-to-GAT-Konverter liest Transkripte im CSV-Format mit einem bestimmten Aufbau
und einer bestimmten Codierung ein. Das CSV-Format ist kein eindeutiges Format. Um die richtige
Funktionsweise des Konverters sicherzustellen, müssen folgende Codierungsoptionen gewählt
werden:

1. Zeichensatz: Unicode (UTF-8)
2. Feldtrenner: % (Prozentzeichen)
3. Zeichenketten-Trenner: "(Anführungszeichen)

Wenn man in Microsoft Word eine CSV-Datei speichert, wird einem nicht die Option gegeben,
diese Einstellungen zu ändern. Benutzt man LibreOffice oder OpenOffice, werden diese
Einstellungen beim Abspeichern abgefragt. Desweiteren ist der richtige Aufbau der CSV-Datei
wichtig. Dieser ist bereits an das fertige Transkript angelehnt und sieht so aus:
1. Spalte: Zeitstempel (z.B. 00:01:22)
2. Spalte: bleibt leer (hier stehen die Segmentnummern, die automatisch eingefügt werden)
3. Spalte: Sprechermarkierungen
4. Spalte: Transkripttext
   
# Verwendung des Konverters
Für die automatische Anonymisierung von Namen im Transkripttext kann der Konverter eine
Anonymisierungstabelle einlesen und anwenden. Diese muss so aufgebaut sein, dass in der ersten
Spalte die echten Namen stehen, in der zweiten Spalte die dazugehörigen anonymisierten Namen.
Die restlichen Spalten werden vom Konverter ignoriert und können für Anmerkungen genutzt
werden. Die Codierung ist wie beim Transkript zu wählen. Anhand der Anonymisierungstabelle
wird der Transkripttext in der vierten Spalte durchgegangen und jedes Vorkommnis der zu anonymisierenden
Namen automatisch ersetzt. Dabei ist zu beachten, dass Spitznamen wie Fabi
statt Fabian einzeln in der Tabelle aufzuführen sind. Die Anonymisierungstabelle kann mit neuen
Namen erweitert werden und in gleicher Weise für alle Transkripte benutzt werden.
Für die Sprechermarkierungen hält der Konverter eine ähnliche Funktionalität bereit. Der Einfachheit
halber schreibe ich im CSV-Transkript als Sprechermarkierungen immer die ersten beiden
Buchstaben des Namens, also z.B. pa für Paul. Anhand der Sprechertabelle können diese
Markierungen dann mit den richtigen Sprechermarkierungen S(m1) etc. ersetzt werden. Die
Nummerierung der Schüler richtet sich danach, in welcher Reihenfolge sie zum ersten Mal im
Transkript auftauchen. Dementsprechend ist die Reihenfolge in der Sprechertabelle für jedes
Transkript individuell anzupassen. Die Ersetzung wird nur auf die 3te Spalte im Transkript angewendet.
Um den Konverter zu verwenden, wird die Datei einfach ausgeführt. Sie fordert einen dann auf,
das Transkript im .csv-Format, die Anonymisierungstabelle und die Sprechertabelle auszuwählen.
Sind keine Erestzungen gewünscht, kann bei den der Anonymisierungs- und Sprechertabelle
auch 'Abbrechen' geklickt werden. Als Ausgabe erhält man eine Textdatei mit dem Transkript
im GAT-Format.

# Nachbearbeitung der Ausgabe des Konverters
Diesen rohen Text kopiert man nun in ein Word-Dokument mit der richtigen Formatierung des
Textes (z.B. Courier New, Schriftgröße 10), dem Transkriptkopf, und der Kopfzeile des Projekts.
Das ausgegebene Transkript hat alle nötigen Zeilenumbrüche und Einrückungen bereits eingefügt.
Was das Programm allerdings nicht leisten kann, ist die richtige Behandlung der Übersprechungen.
Daher muss das Transkript noch einmal manuell durchgegangen und an den Stellen, an
denen Übersprechungen auftreten, überarbeitet werden. Die Klammern von zueinander gehörenden
Übersprechungen müssen übereinander angeordnet werden. Dazu kann es nötig sein, eine
Übersprechung in eine neue Zeile zu verschieben. Da dabei kein neues Segment entsteht, ist dies
aber problemlos möglich. Handelt es sich um eine Übersprechung, die nur ein bestätigendes Partikel
enthält (z.B. hm_hm), wird dies als Unterbrechung des laufenden Segments direkt in die
Zeile unter die Übersprechung des ursprünglichen Sprechers eingefügt. Wahrscheinlich muss die
Zeile also im Transkript ausgeschnitten und weiter oben wieder eingefügt werden. Da die GATRegeln
besagen, dass nach einer bestätigenden Übersprechung das Segment des Unterbrochenen
weiterläuft, ist aber auch dies problemlos möglich. Problematisch sind die Stellen, an denen eine
Übersprechung so lang ist, dass sie nicht in eine Zeile passt. Dann gibt der Konverter bereits bei
der Konvertierung eine Fehlermeldung mit entsprechender Zeilenangabe aus. Um das Problem
zu lösen, muss die Übersprechung auf mehrer Segmente aufgeteilt werden, also aus [aa bb] wird
[aa] und im nächsten Segment [bb] gemacht.
Auch nach erfolgreicher Konvertierung des Transkripts ist es lohnenswert, die ursprüngliche .csv-
Datei aufzubewahren. Falls nachträglich zum Beispiel ein Segment am Anfang des Transkripts
eingefügt wird, müsste man im fertigen GAT-Transkript per Hand alle Segmentnummern ändern,
während man in der .csv-Datei das neue Segment einfach oben einfügt, nochmal konvertiert, und
so automatisch die richtige Nummerierung bekommt. Allerdings muss man dann noch einmal die
Übersprechungen überarbeiten.
