import tkinter as tk
from tkinter import filedialog, scrolledtext
import logging

import ttkbootstrap as ttk
from ttkbootstrap.constants import END, WORD

import functions as func


# ======================================================================================
# Class erstellen
# ======================================================================================
class AppState:
    """
    Zentraler Zustand der Anwendung, ermöglicht Datenübertragung zwischen den Seiten.
    """

    def __init__(self, root):
        # Feldänderungen 
        self.new_accountid = tk.IntVar(master=root, value=0)                    # variable für Checkbutton
        self.info_accountid = tk.IntVar(master=root, value=0)                   # variable fürs Abspeichern
        self.custom_accountid = tk.StringVar(master=root, value="5513755201")   # Input 

        self.new_kündigungsgrund = tk.IntVar(master=root, value=0)
        self.info_kündigungsgrund = tk.IntVar(master=root, value=0)
        self.custom_kündigunsgrund = tk.StringVar(master=root, value="")

        self.new_bestellid = tk.IntVar(master=root, value=0)
        self.info_bestellid = tk.IntVar(master=root, value=0)
        self.custom_bestellID = tk.StringVar(master=root, value="")
        
        self.Versand_entry = tk.StringVar(master=root, value="")

        # Gemeinsame Daten zwischen Seite 1 und Seite 2
        self.shared_data = []

        # Wird nach dem Erzeugen von Seite 2 gesetzt
        self.listbox_uebersicht = None
        self.treeview_uebersicht = None

        # Wird nach dem Logging-Setup gesetzt
        self.logger = None


class TextHandler(logging.Handler):
    """Leitet Logging-Ausgaben in ein Textfeld um."""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_message = self.format(record)

        # Thread-sicheres Aktualisieren des GUI-Widgets
        self.text_widget.after(
            0,
            lambda: self._write_message(log_message)
        )

    def _write_message(self, log_message):
        self.text_widget.insert(END, log_message + "\n")
        self.text_widget.yview(END)


# ======================================================================================
# GUI Erstellen
# ======================================================================================
def starte_GUI():

    # ===============================================
    # Hauptfenster / ttkbootstrap Theme
    # ===============================================
    root = ttk.Window(
        title="Lasernet Bestätigungen Auftrag/Kündigung",
        themename="darkly",  # Alternativen: darkly, superhero, minty, cosmo, litera ...
        size=(700, 600),
        resizable=(True, True)
    )

    # Gemeinsamer Laufzeit-Zustand
    app_state = AppState(root)

    notebook = ttk.Notebook(root, bootstyle="primary")
    notebook.grid(row=0, column=0, sticky="nsew")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    notebook.grid_rowconfigure(0, weight=1)
    notebook.grid_columnconfigure(0, weight=1)

    # ===============================================
    # Hilfsfunktionen
    # ===============================================
    def erstelle_logger(log_text):
        """Erstellt Logger und bindet die Ausgabe an das Textfeld."""

        logger = logging.getLogger("TkinterLogger")
        logger.setLevel(logging.INFO)

        # Verhindert doppelte Meldungen, wenn starte_GUI mehrfach aufgerufen wird.
        logger.handlers.clear()
        logger.propagate = False

        text_handler = TextHandler(log_text)
        text_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        text_handler.setFormatter(formatter)

        logger.addHandler(text_handler)

        return logger

    def aktualisiere_uebersicht():
        """Aktualisiert die Übersicht auf Seite 2."""

        if app_state.treeview_uebersicht is not None:
            func.showdata_treeview(app_state.treeview_uebersicht,
                                    app_state.shared_data)

    def tab_gewechselt(event):
        """Aktualisiert die Daten beim Wechsel auf Tab 2."""

        aktueller_tab_index = notebook.index(notebook.select())

        # Index 1 = zweiter Tab
        if aktueller_tab_index == 1:
            aktualisiere_uebersicht()

    # ===============================================
    # Seite 1: Aufträge erstellen
    # ===============================================
    def Auftraege_erstellen(notebook_widget):
        # Erstellen des Frames
        frame = ttk.Frame(notebook_widget, padding=15)
        notebook_widget.add(frame, text="Dokumente erstellen")

        frame.grid_columnconfigure(1, weight=1)

        # Überschrift
        ueberschrift = ttk.Label(
            frame,
            text="Tool zum Nachgenerieren der Lasernetschreiben",
            font=("Segoe UI", 12, "bold"),
            bootstyle="primary"
        )
        ueberschrift.grid(row=1, column=1, pady=5)

        # Dokumentation
        doku = ttk.Button(
            frame,
            text="Dokumentation",
            command=func.open_dokumentation,
            bootstyle="info-outline"
        )
        doku.grid(row=1, column=2, padx=5)

        # ==================
        # SubscriptionIDs
        # ==================
        choose_id = tk.StringVar(master=root)

        # Label
        label_bestellid = ttk.Label(
            frame,
            text=(
                "SubscriptionIDs eintragen "
                "(inkl. Kommatrennung, z. B. 555555,666666)"
            )
        )
        label_bestellid.grid(row=4, column=1, pady=(10, 2))

        # Eingabe
        file_entry = ttk.Entry(
            frame,
            textvariable=choose_id,
            width=50
        )
        file_entry.grid(row=5, column=1, sticky="ew")

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

        dropdown = ttk.Combobox(
            frame,
            textvariable=auswahl_dropdown,
            values=optionen,
            state="readonly",
            width=24,
            bootstyle="primary"
        )
        dropdown.grid(row=6, column=2, padx=5, sticky="ew")

        # ==================
        # Neue Accountid
        # ==================
        #### Checkbutton Sichtbarkeit der Funktion einstellen ####
        checkbutton_accountid = ttk.Checkbutton(
                                    frame,
                                    text="Neue PayerID",
                                    variable=app_state.new_accountid,
                                    bootstyle="primary-round-toggle",
                                    command=lambda: func.Button_Aktivieren({'var_name':'Neue PayerID',
                                                                            'var_check':app_state.new_accountid,
                                                                            'lable':{'Name':label_choose,'row':7,'column':1},
                                                                            'file_entry':{'Name':file_entry_test,'row':8,'column':1},
                                                                            'button':{'Name':button_accountid,'row':8,'column':2},
                                                                            'variable':app_state.custom_accountid
                                                                            },app_state.logger)
                                )
        checkbutton_accountid.grid(row=4, column=0, padx=0, sticky="w")

        #### Funktion bei Sichtbarkeit = Ja ####
        # Eingabefeld
        file_entry_test = ttk.Entry(
            frame,
            textvariable=app_state.custom_accountid,
            width=50
        )
        file_entry_test.grid(row=11, column=1, sticky="ew")
        file_entry_test.grid_remove()
        # 
        label_choose = ttk.Label(
            frame,
            text="PayerID der Testperson eintragen"
        )
        label_choose.grid(row=12, column=1)
        label_choose.grid_remove()
        
        # Speichern
        button_accountid = ttk.Button(
            frame,
            text="Test ID speichern",
            bootstyle="secondary",
            command=lambda: func.Set_variable_option(
                app_state.logger,
                'Neue PayerID',
                app_state.custom_accountid,
                button_accountid,
                app_state.info_accountid
            )
        )


        button_accountid.grid(row=11, column=2, padx=5)
        button_accountid.grid_remove()
        
        # ==================
        # Versand unterdrücken
        # ==================
        checkbutton_versand = ttk.Checkbutton(
            frame,
            text="Versand unterdrücken",
            variable=app_state.Versand_entry,
            onvalue="Ja",
            offvalue="Nein",
            bootstyle="warning-round-toggle"
        )
        checkbutton_versand.grid(row=5, column=0, padx=0, sticky="w")


        # ==================
        # Neue Bestell-ID
        # ==================

        #### Sichtbarkeit einstellen
        checkbutton_neue_bestellid = ttk.Checkbutton(
                    frame,
                    text="Neue BestellID",
                    variable=app_state.new_bestellid,
                    bootstyle="primary-round-toggle",
                    command=lambda: func.Button_Aktivieren({'var_name':'Neue BestellID',
                                                            'var_check':app_state.new_bestellid,
                                                            'lable':{'Name':label_choose_bestellid,'row':17,'column':1},
                                                            'file_entry':{'Name':file_entry_bestellid,'row':18,'column':1},
                                                            'button':{'Name':button_bestellID,'row':18,'column':2},
                                                            'variable':app_state.custom_bestellID
                                                            },app_state.logger)
                                                            )
        checkbutton_neue_bestellid.grid(row=6, column=0, padx=0, sticky="w")

        #### Funktion bei Sichtbarkeit = Ja 
        # Label
        label_choose_bestellid = ttk.Label(
                    frame,
                    text="Neue BestellID eintragen"
                )
        label_choose_bestellid.grid(row=14, column=1)
        label_choose_bestellid.grid_remove()

        # Eingabefeld
        file_entry_bestellid = ttk.Entry(
            frame,
            textvariable=app_state.custom_bestellID,
            width=50
        )
        file_entry_bestellid.grid(row=15, column=1, sticky="ew")
        file_entry_bestellid.grid_remove()
        
        # Eingabe Speichern
        button_bestellID = ttk.Button(
            frame,
            text="BestellID Test speichern",
            bootstyle="secondary",
            command=lambda: func.Set_variable_option(
                app_state.logger,
                'Neue BestellID',
                app_state.custom_bestellID,
                button_bestellID,
                app_state.info_bestellid
            )
        )
        button_bestellID.grid(row=15, column=2, padx=5)
        button_bestellID.grid_remove()

        # ==================
        # Kündigungsgrund
        # ==================
        #### Sichtbarkeit einstellen
        checkbutton_kuendigungsgrund = ttk.Checkbutton(
                            frame,
                            text="Neuer Kündigungsgrund",
                            variable=app_state.new_kündigungsgrund,
                            bootstyle="primary-round-toggle",
                            command=lambda: func.Button_Aktivieren({'var_name':'Neuer Kündigungsgrund',
                                                                    'var_check':app_state.new_kündigungsgrund,
                                                                    'lable':{'Name':label_kuen,'row':27,'column':1},
                                                                    'file_entry':{'Name':file_entry_kuen,'row':28,'column':1},
                                                                    'button':{'Name':file_button_kuen,'row':28,'column':2},
                                                                    'variable':app_state.custom_kündigunsgrund
                                                                    },app_state.logger)
                                                            )
        checkbutton_kuendigungsgrund.grid(row=7, column=0, padx=0, sticky="w")


        #### Funktion bei Sichtbarkeit = Ja 
        #choose_kunGrund = tk.StringVar(master=root)

        # label
        label_kuen = ttk.Label(
            frame,
            text="Kündigungsgrund eintragen (nur einen!)"
        )
        label_kuen.grid(row=6, column=1)
        label_kuen.grid_remove()

        # Eingabefeld 
        file_entry_kuen = ttk.Entry(
            frame,
            textvariable=app_state.custom_kündigunsgrund,
            width=50
        )
        file_entry_kuen.grid(row=7, column=1, sticky="ew")
        file_entry_kuen.grid_remove()

        # Speichern
        file_button_kuen = ttk.Button(
            frame,
            text="Kündigungsgrund speichern",
            bootstyle="secondary",
            command=lambda: func.Set_variable_option(
                    app_state.logger,
                    'Neuer Kündigungsgrund',
                    app_state.custom_kündigunsgrund,
                    file_button_kuen,
                    app_state.info_kündigungsgrund
            )
        )
        file_button_kuen.grid(row=7, column=2, padx=5)
        file_button_kuen.grid_remove()

        # Auswahl der Kündigunsggründe nur bei Kündigungen!
        auswahl_dropdown.trace_add(
            "write",
            lambda *_: func.update_state(
                auswahl_dropdown,
                file_entry_kuen,
                file_button_kuen,
                app_state.treeview_uebersicht
            )
        )

        # ==================
        # IDs speichern
        # ==================
        file_button_ids = ttk.Button(
            frame,
            text="IDs speichern",
            bootstyle="success",
            command=lambda: (
                func.Save_entry(
                    choose_id,
                    app_state.info_accountid,
                    app_state.custom_accountid,
                    auswahl_dropdown,
                    app_state.shared_data,
                    app_state.new_accountid,
                    app_state.info_bestellid,
                    app_state.custom_bestellID,
                    app_state.Versand_entry,
                    app_state.logger,
                    app_state.custom_kündigunsgrund,
                    app_state.new_bestellid,
                    file_entry_test,
                    label_choose,
                    button_accountid,
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
            app_state.treeview_uebersicht
        )

        # ==================
        # Logging auf Seite 1
        # ==================
        log_frame = ttk.Labelframe(
            frame,
            text="Protokoll",
            padding=8,
            bootstyle="secondary"
        )
        log_frame.grid(
            row=38,
            column=0,
            columnspan=6,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        log_text = scrolledtext.ScrolledText(
            log_frame,
            width=85,
            height=20,
            wrap=WORD
        )
        log_text.grid(row=0, column=0, sticky="nsew")

        # Zentraler Logger; Anzeige zunächst auf Seite 1.
        app_state.logger = erstelle_logger(log_text)

        return frame

    # ===============================================
    # Seite 2: Übersicht / Download
    # ===============================================
    def Daten_erstellen(notebook_widget):

        frame = ttk.Frame(notebook_widget, padding=15)
        notebook_widget.add(frame, text="Übersicht / Download")

        frame.grid_columnconfigure(1, weight=1)

        # Exportordner
        folder_data = tk.StringVar(master=root)

        label = ttk.Label(frame, text="Ablageort wählen:")
        label.grid(row=2, column=1, pady=(10, 2), sticky="w")

        file_entry = ttk.Entry(
            frame,
            textvariable=folder_data,
            width=50
        )
        file_entry.grid(row=3, column=1, sticky="ew")

        file_button = ttk.Button(
            frame,
            text="Durchsuchen",
            bootstyle="info-outline",
            command=lambda: func.data_folder(folder_data, filedialog)
        )
        file_button.grid(row=3, column=2, padx=5)

        # Starten
        start_button = ttk.Button(
            frame,
            text="Starten",
            bootstyle="success",
            command=lambda: func.Generiere_Reports(
                folder_data,
                app_state.shared_data,
                app_state.logger
            )
        )
        start_button.grid(row=9, column=2, padx=5, pady=10)

        ####################### Treeview hinzufügen
        # Spalten definieren
        # columns = ("name", "alter", "stadt")
        columns=("Nr","Typ","Anzahl","Testkunde","Versand unterdrückt","Kündigungsgrund")

        # Tabelle erstellen
        app_state.treeview_uebersicht = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        # Überschriften
        app_state.treeview_uebersicht.heading("Nr", text="Nr")
        app_state.treeview_uebersicht.heading("Typ", text="Typ")
        app_state.treeview_uebersicht.heading("Anzahl", text="Anzahl")
        app_state.treeview_uebersicht.heading("Testkunde", text="Testkunde")
        app_state.treeview_uebersicht.heading("Versand unterdrückt", text="Versand unterdrückt")
        app_state.treeview_uebersicht.heading("Kündigungsgrund", text="Kündigungsgrund")

        # Spaltenbreiten und Ausrichtung
        app_state.treeview_uebersicht.column("Nr", width=30, anchor="center", stretch=False)
        app_state.treeview_uebersicht.column("Typ", width=130, anchor="w")
        app_state.treeview_uebersicht.column("Anzahl", width=80, anchor="center", stretch=False)
        app_state.treeview_uebersicht.column("Testkunde", width=80, anchor="center")
        app_state.treeview_uebersicht.column("Versand unterdrückt", width=150, anchor="center")
        app_state.treeview_uebersicht.column("Kündigungsgrund", width=150, anchor="w")


        # Tabelle anzeigen
        app_state.treeview_uebersicht.grid(
            row=20,
            column=0,
            columnspan=6,
            padx=10,
            pady=10,
            sticky="nsew"
        )
    
    # ==================
    # Seiten erzeugen
    # ==================
    seite1_frame = Auftraege_erstellen(notebook)
    seite2_frame = Daten_erstellen(notebook)

    # Beim Wechsel in den Tab "Übersicht / Download" Daten aktualisieren.
    notebook.bind("<<NotebookTabChanged>>", tab_gewechselt)

    # Startansicht
    notebook.select(seite1_frame)

    root.mainloop()


if __name__ == "__main__":
    starte_GUI()