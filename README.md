# Service-Dashboard – Management-Prototyp

Grundlage: Prototype_Services(3).xlsx, 68 Services und 10 Spalten.
Die enthaltene dashboard.xlsx ist eine unveränderte Kopie dieser Datei.

## GitHub Pages
Alle Dateien aus diesem Ordner ins Stammverzeichnis des bestehenden Repositories hochladen. In Settings → Pages den gewünschten Branch und / (root) auswählen. index.html lädt dashboard.json im selben Ordner. Ein Austausch der Excel allein aktualisiert die Darstellung noch nicht: zuerst das Python-Script ausführen und die neue JSON hochladen.

## Lokal testen
Im entpackten Ordner:

    python -m pip install -r requirements.txt
    python update_dashboard.py
    python -m http.server 8000 --bind 127.0.0.1

Dann http://localhost:8000 öffnen. Nicht durch Doppelklick auf index.html testen, da der Browser lokale JSON-Abfragen einschränkt.

## Interner Betrieb
index.html und dashboard.json auf dem internen Webserver ablegen. Python samt openpyxl auf dem ausführenden Rechner installieren. Windows-Aufgabenplanung alle 5 oder 15 Minuten:

Programm: vollständiger Pfad zu python.exe
Argumente: "C:\ServiceDashboard\update_dashboard.py" --excel "\\server\share\dashboard.xlsx" --output "C:\inetpub\wwwroot\services\dashboard.json"

Das ausführende Konto braucht Leserechte auf der Excel und Schreibrechte im Zielordner. UNC-Pfade statt zugeordneten Laufwerken verwenden. Excel-Redaktion muss Änderungen speichern. Bei Lesefehlern oder fehlenden Spalten bleibt die letzte JSON erhalten; Aufgabenplanung auf Fehler überwachen. Die Webseite fragt die JSON alle 5 Minuten ohne Browsercache neu ab. HTML wird dabei nicht neu erzeugt.

## Funktionen und Auslegung
Kennzahlen, Zustandsverteilung, Verteilung nach Amt, Suche, Filter nach Departement und Zustand, aufklappbare Details und Service-Links. Alle Kennzahlen und Diagramme beziehen sich auf die aktuelle Filterauswahl. Archiviert ist grau, Produktiv grün und In Entwicklung blau; diese Farben stellen Zustände dar und keine Risikobewertung. Pendenzen und Bemerkungen werden unverändert angezeigt. Es werden keine Service-IDs und keine Publikationsspalte hinzugefügt.

## Daten und Hosting
Die Testdatei wurde als anonymisierte Vorlage bereitgestellt; eine unabhängige Anonymitätsprüfung ist nicht Bestandteil dieses Prototyps. Produktive Excel- und JSON-Dateien nur intern speichern. Der Webserver muss Zugriff auf Intranet/VPN begrenzen. Der Prototyp enthält keine Anmeldung und keine automatisierte GitHub-Aktualisierung. Er benötigt keine externen Bibliotheken, Schriften oder Analyse-Dienste im Browser.
