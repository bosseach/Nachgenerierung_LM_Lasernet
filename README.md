##### Nachgenerierung der Auftrags- und Kündigungsbestätigungen von Lasernet
Das Tool generiert einen Subscriptions- und einen Accountreport für
die Erstellung der Auftragsbestätigungen via Lasernet.

##### Installation
venv mit den in requirements.txt hinterlegten Modulen erstellen. Ausführen des Skripts via main.py 


##### Prozess 
- Lasernet startet jeden Tag zwei Läufe zum Erstellen der Auftrags- und Kündigungsbestätigungen.
  Einen morgen zum Verarbeiten der Daten des Vortages und einen Abends um 20 Uhr der für Korrekturen und
   Test ist. Beide verarbeiten die Daten identisch

- Das Tool ermöglicht das Erstellen der entsprechenden Reports, inkl. unterschiedlicher Fälle. 

- Die entsprechenden Reports müssen unter dem folgenden Verzeichnis abgelegt werden:
        \\\\vm-it-zen-shd-2.aschendorff.net\\Lesermarkt-PROD\\CSV\\CSV_IN
    
#### Bedienung 
- Als Input dienen SubscriptionsIDs für die zu erstellenden Aufträge, Seite "Dokumente erstellen".
  Das Tool ermittelt für gültige BestellIDs (Bestellid <> leer) die entsprechend benötigten Subscriptions. 
  * Bei leeren Bestellids werden keine zusätzlichen Subscriptions ermittelt. 
  * Für jede Bestellid bitte nur eine Subscription angeben. 
  * "ID speichert" speichert alle eingetragenen IDs als einen zu bearbeitenden Fall ab und leer alle Felder  
     für eine erneute Eingabe.
  * Mehrere Subscriptionid können kommasepariert eingegeben werden. Sie gelten dann als ein Bearbeitungsfall.
  * Der ausgewählte Dokumententyp und die gewählten Änderungsoptionen gelten für alle in einem Bearbeitungsfall
    enthaltenen Bestellungen.

- Auf der Seite "Übersicht/Download" findet sich eine Übersicht der bisher gespeicherten Bearbeitungsfälle, inkl.
  ihrer Verarbeitungsoptionen, sowie die Option zum Erstellen der Reports.

- Das Tool ändert die Daten des Subscriptionsreport so ab, dass die zu den gewählten Fällen AB und KB passen
  und auf normalen Weg im nächsten Abendlauf verarbeitet werden können. Für den Fall, dass eine Bearbeitung 
  unterbleiben ssoll gibt es die Option "Keine Bearbeitung".

- Es gibt darüberhinaus die Möglichkeit einige Daten gezielt anzupassen:
  1. API: Updated die Subscriptions direkt aus der eSuie statt aus der ATLAS DB. Für den Fall von Schiefständen
     durch z.B Verschieben des Startdatums.
  2. PayerID: Es kann eine neue Payer ID als Ziel für die AB/KB angegeben werden. Z.b Für Testfällen.
  3. Versand unterdrücken: Der Versand kann variabel unterdrückt werden.
  4. Neue Bestellid: Es können neue Bestellids angegeben werden. Es findet hierbei keine Änderung in der ATLAS DB
      oder in der eSuite statt.
  5. Neue Kündigungsgründe. Bei Kündigungen kann ein neuer Kündigungsgrund hinterlegt werden. 