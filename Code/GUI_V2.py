import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import logging

import functions as func

# ======================================================================================
# Class erstellen
# ======================================================================================
class AppState:
    """
    Zentraler Zustand der Anwendung, ermöglicht Datenübertragung zwischen den Seiten
    """

    def __init__(self, root):
        # Tkinter-Variablen von Seite 1
        self.test_entry = tk.IntVar(master=root, value=0)
        self.new_bestellid = tk.IntVar(master=root, value=0)

        self.custom_bestellID = tk.StringVar(master=root, value="")
        self.info_bestellid = tk.IntVar(master=root, value=0)

        self.info_TESTcase = tk.IntVar(master=root, value=0)
        self.custom_TestID = tk.StringVar(master=root, value="5513755201")

        self.Versand_entry = tk.StringVar(master=root, value="Nein")

        # Gemeinsame Daten zwischen Seite 1 und Seite 2
        self.shared_data = []

        # Wird nach dem Erzeugen von Seite 2 gesetzt
        self.listbox_uebersicht = None

        # Wird nach dem Logging-Setup gesetzt
        self.logger = None


class TextHandler(logging.Handler):
    """Leitet Logging-Ausgaben in ein Tkinter-Textfeld um."""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_message = self.format(record)

        # Logging kann ggf. aus einem anderen Thread kommen.
        # after sorgt dafür, dass das Widget im Tkinter-Hauptthread aktualisiert wird.
        self.text_widget.after(
            0,
            lambda: self._write_message(log_message)
        )

    def _write_message(self, log_message):
        self.text_widget.insert(tk.END, log_message + "\n")
        self.text_widget.yview(tk.END)



# ======================================================================================
# GUI Erstellen
# ======================================================================================

def starte_GUI():

    # ===============================================
    # Hauptfenster
    # ===============================================
    root = tk.Tk()
    root.wm_title("Lasernet Bestätigungen Auftrag/Kündigung")
    root.geometry("700x600")

    # Gemeinsamer Laufzeit-Zustand
    app_state = AppState(root)

    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky="nsew")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    notebook.grid_rowconfigure(0, weight=1)
    notebook.grid_columnconfigure(0, weight=1)

    # ===============================================
    # Hilfsfunktionen
    # ===============================================

    def erstelle_logger(log_text):
        """
        Erstellt den Logger bzw. bindet die Ausgabe an das angegebene Textfeld.
        """
        logger = logging.getLogger("TkinterLogger")
        logger.setLevel(logging.INFO)

        text_handler = TextHandler(log_text)
        text_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        text_handler.setFormatter(formatter)

        logger.addHandler(text_handler)
        return logger

    def aktualisiere_uebersicht():
        """
        Aktualisiert die Listbox auf Seite 2 aus derselben shared_data-Liste,
        die auf Seite 1 durch func.Save_entry befüllt wird.
        """
        if app_state.listbox_uebersicht is not None:
            func.showdata(
                app_state.listbox_uebersicht,
                app_state.shared_data
            )

    def tab_gewechselt(event):
        """
        Bei Wechsel auf Seite 2 die Daten neu darstellen.
        """
        aktueller_tab_index = notebook.index(notebook.select())

        # Tab 1 = Seite 2, da Index bei 0 beginnt
        if aktueller_tab_index == 1:
            aktualisiere_uebersicht()

    # ===============================================
    # Seite 1: Aufträge erstellen
    # ===============================================
    
    def Aufträge_erstellen(notebook_widget):

        frame = ttk.Frame(notebook_widget)
        notebook_widget.add(frame, text="Dokumente erstellen")

        frame.grid_columnconfigure(1, weight=1)

        # Überschrift
        ueberschrift = tk.Label(
            frame,
            text="Tool zum Nachgenerieren der Lasernetschreiben"
        )
        ueberschrift.grid(row=1, column=1, pady=5)

        # Dokumentation
        doku = tk.Button(
            frame,
            text="Dokumentation",
            command=func.open_dokumentation
        )
        doku.grid(row=1, column=2, padx=5)

        # ==================
        # SubscriptionIDs
        # ==================

        choose_id = tk.StringVar(master=root)

        label_bestellid = tk.Label(
            frame,
            text="SubscriptionIDs eintragen "
                 "(inkl. Kommatrennung, z. B. 555555,666666)"
        )
        label_bestellid.grid(row=4, column=1, pady=(10, 2))

        file_entry = tk.Entry(
            frame,
            textvariable=choose_id,
            width=50
        )
        file_entry.grid(row=5, column=1)

        # ==================
        # AB/KB-Auswahl
        # ==================
        optionen = [
            "Auftragsbestätigungen",
            "Kündigungsbestätigungen",
            "Keine Bearbeitung",
            "Beides"
        ]

        auswahl_dropdown = tk.StringVar(
            master=root,
            value="Auftragsbestätigungen"
        )

        dropdown = ttk.OptionMenu(
            frame,
            auswahl_dropdown,
            auswahl_dropdown.get(),
            *optionen
        )
        dropdown.grid(row=6, column=2, padx=5)

        # ==================
        # Test-ID Widgets
        # ==================
        file_entry_test = tk.Entry(
            frame,
            textvariable=app_state.custom_TestID,
            width=50
        )
        file_entry_test.grid(row=11, column=1)
        file_entry_test.grid_remove()

        label_choose = tk.Label(
            frame,
            text="PayerID der Testperson eintragen"
        )
        label_choose.grid(row=12, column=1)
        label_choose.grid_remove()

        button_testID = tk.Button(
            frame,
            text="Test ID speichern",
            command=lambda: func.choose_testID(
                app_state.logger,
                app_state.custom_TestID,
                button_testID,
                file_entry_test,
                label_choose,
                app_state.info_TESTcase
            )
        )
        button_testID.grid(row=11, column=2, padx=5)
        button_testID.grid_remove()

        checkbutton_test_id = tk.Checkbutton(
            frame,
            text="TEST ID",
            variable=app_state.test_entry,
            command=lambda: func.Button_Aktivieren(
                app_state.test_entry,
                label_choose,
                file_entry_test,
                button_testID,
                app_state.new_bestellid,
                button_bestellID,
                file_entry_bestellid,
                label_choose_bestellid
            )
        )
        checkbutton_test_id.grid(row=6, column=0, padx=5)

        # ==================
        # Versand unterdrücken
        # ==================
        checkbutton_versand = tk.Checkbutton(
            frame,
            text="Versand unterdrücken",
            variable=app_state.Versand_entry,
            onvalue="Ja",
            offvalue="Nein"
        )
        checkbutton_versand.grid(row=7, column=0, padx=5)

        # ==================
        # Kündigungsgrund
        # ==================
        choose_kunGrund = tk.StringVar(master=root)

        label_kuen = tk.Label(
            frame,
            text="Kündigungsgrund eintragen (nur einen!)"
        )
        label_kuen.grid(row=6, column=1)

        file_entry_kuen = tk.Entry(
            frame,
            textvariable=choose_kunGrund,
            width=50
        )
        file_entry_kuen.grid(row=7, column=1)

        file_button_kuen = tk.Button(
            frame,
            text="Kündigungsgrund speichern",
            command=lambda: func.clear_kündigungsgrund(
                choose_kunGrund,
                app_state.listbox_uebersicht,
                app_state.logger
            )
        )
        file_button_kuen.grid(row=7, column=2, padx=5)

        auswahl_dropdown.trace_add(
            "write",
            lambda *_: func.update_state(
                auswahl_dropdown,
                file_entry_kuen,
                file_button_kuen,
                app_state.listbox_uebersicht
            )
        )

        # ==================
        # Neue Bestell-ID
        # ==================
        file_entry_bestellid = tk.Entry(
            frame,
            textvariable=app_state.custom_bestellID,
            width=50
        )
        file_entry_bestellid.grid(row=15, column=1)
        file_entry_bestellid.grid_remove()

        label_choose_bestellid = tk.Label(
            frame,
            text="Neue BestellID eintragen"
        )
        label_choose_bestellid.grid(row=14, column=1)
        label_choose_bestellid.grid_remove()

        button_bestellID = tk.Button(
            frame,
            text="BestellID Test speichern",
            command=lambda: func.choose_BestellID(
                app_state.logger,
                app_state.custom_bestellID,
                button_bestellID,
                file_entry_bestellid,
                label_choose_bestellid,
                app_state.info_bestellid
            )
        )
        button_bestellID.grid(row=15, column=2, padx=5)
        button_bestellID.grid_remove()

        checkbutton_neue_bestellid = tk.Checkbutton(
            frame,
            text="Neue BestellID",
            variable=app_state.new_bestellid,
            command=lambda: func.Button_Aktivieren(
                app_state.test_entry,
                label_choose,
                file_entry_test,
                button_testID,
                app_state.new_bestellid,
                button_bestellID,
                file_entry_bestellid,
                label_choose_bestellid
            )
        )
        checkbutton_neue_bestellid.grid(row=8, column=0, padx=5)

        # ==================
        # Button: IDs speichern
        # ==================
        file_button_ids = tk.Button(
            frame,
            text="IDs speichern",
            command=lambda: (
                func.Save_entry(
                    choose_id,
                    app_state.listbox_uebersicht,
                    app_state.info_TESTcase,
                    app_state.custom_TestID,
                    auswahl_dropdown,
                    app_state.shared_data,
                    app_state.test_entry,
                    app_state.info_bestellid,
                    app_state.custom_bestellID,
                    app_state.Versand_entry,
                    app_state.logger,
                    choose_kunGrund,
                    app_state.new_bestellid,
                    file_entry_test,
                    label_choose,
                    button_testID,
                    file_entry_bestellid,
                    label_choose_bestellid,
                    button_bestellID
                ),
                aktualisiere_uebersicht()
            )
        )
        file_button_ids.grid(row=5, column=2, padx=5)

        # Initialen Sichtbarkeitsstatus setzen
        func.update_state(
            auswahl_dropdown,
            file_entry_kuen,
            file_button_kuen,
            app_state.listbox_uebersicht
        )

        # ==================
        # Logging auf Seite 1
        # ==================
        log_frame = tk.Frame(frame)
        log_frame.grid(
            row=17,
            column=0,
            columnspan=6,
            padx=10,
            pady=10
        )

        log_text = scrolledtext.ScrolledText(
            log_frame,
            width=85,
            height=20,
            wrap=tk.WORD
        )
        log_text.grid(row=0, column=0)

        # Ein zentraler Logger; Anzeige vorerst in Seite 1.
        app_state.logger = erstelle_logger(log_text)

        return frame

    # ===============================================
    # Seite 2: Übersicht / Download
    # ===============================================

    def Daten_erstellen(notebook_widget):

        frame = ttk.Frame(notebook_widget)
        notebook_widget.add(frame, text="Übersicht/Download")

        frame.grid_columnconfigure(1, weight=1)

        # Exportordner
        folder_data = tk.StringVar(master=root)

        label = tk.Label(frame, text="Ablageort wählen:")
        label.grid(row=2, column=1, pady=(10, 2))

        file_entry = tk.Entry(
            frame,
            textvariable=folder_data,
            width=50
        )
        file_entry.grid(row=3, column=1)

        file_button = tk.Button(
            frame,
            text="Durchsuchen",
            command=lambda: func.data_folder(folder_data, filedialog)
        )
        file_button.grid(row=3, column=2, padx=5)

        # Starten
        start_button = tk.Button(
            frame,
            text="Starten",
            command=lambda: func.Generiere_Reports(
                folder_data,
                app_state.shared_data,
                app_state.logger
            )
        )
        start_button.grid(row=9, column=2, padx=5, pady=10)

        # DIE gemeinsame Listbox für die Übersicht.
        app_state.listbox_uebersicht = tk.Listbox(
            frame,
            width=85,
            height=10
        )
        app_state.listbox_uebersicht.grid(
            row=10,
            column=0,
            columnspan=6,
            padx=10,
            pady=10
        )

        # Initiale Anzeige
        aktualisiere_uebersicht()

        # Logging auf Seite 2
        log_frame = tk.Frame(frame)
        log_frame.grid(
            row=15,
            column=0,
            columnspan=6,
            padx=10,
            pady=10
        )

        log_text = scrolledtext.ScrolledText(
            log_frame,
            width=85,
            height=20,
            wrap=tk.WORD
        )
        log_text.grid(row=0, column=0)

        # Optional: Auch Log-Ausgaben auf Seite 2 anzeigen.
        # app_state.logger.addHandler(...)
        text_handler = TextHandler(log_text)
        text_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
        )
        app_state.logger.addHandler(text_handler)

        return frame

    # ==================
    # Seiten erzeugen
    # ==================
    
    seite1_frame = Aufträge_erstellen(notebook)
    seite2_frame = Daten_erstellen(notebook)

    # Beim Wechsel in den Tab "Übersicht/Download" Daten aktualisieren.
    notebook.bind("<<NotebookTabChanged>>", tab_gewechselt)

    # Startansicht
    notebook.select(seite1_frame)

    root.mainloop()