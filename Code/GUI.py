# Import
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import logging
from tkinter import scrolledtext
import requests

# Import eigene Funktionen
from core_services.constants import RESTHOST_PROD,HEADERS_PROD
from core_services.db import execute_sql_query

# Lokale Funktion 
import functions as func


def starte_GUI():

    # //////////////////////////////////////////////////////////////////////////////////////
    # Hauptfenster
    # //////////////////////////////////////////////////////////////////////////////////////
    
    # Custom Logging Handler bilden
    class TextHandler(logging.Handler):
        def __init__(self, text_widget):
            super().__init__()
            self.text_widget = text_widget

        def emit(self, record):
            log_message = self.format(record)
            self.text_widget.insert(tk.END, log_message + "/n")
            self.text_widget.yview(tk.END)  # Scrollt automatisch zum neuesten Eintrag
            self.text_widget.update_idletasks()  # Stellt sicher, dass das GUI live aktualisiert wird

    # Hauptfenster erstellen
    root = tk.Tk()  # Erstellt das Hauptfenster
    root.wm_title('Lasernet Bestätigungen Auftrag/Kündigung')
    root.geometry("700x600")  # Fenstergröße: 300x200 Pixel

    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0)

    # Globale variablen erstellen
    test_entry = tk.IntVar(value=0)
    new_bestellid=tk.IntVar(value=0)
    custom_bestellID=tk.StringVar(value='')
    info_bestellid=tk.IntVar(value=0)
    info_TESTcase=tk.IntVar(value=0)
    custom_TestID=tk.StringVar(value=5513755201)
    Versand_entry = tk.StringVar(value='Nein')
    listbox2=tk.Listbox(root)
    shared_data = []

    # //////////////////////////////////////////////////////////////////////////////////////
    # Seiten
    # //////////////////////////////////////////////////////////////////////////////////////

    def Aufträge_erstellen(notebook):

        #### Seite 1: Dateneingabe
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Dokumente erstellen")
        notebook.grid(row=0, column=0, sticky="nsew")
        # Intro
        Überschrift=tk.Label(frame,text='Tool zum Nachgenenerieren der Lasernetschreiben')
        Überschrift.grid(row=1,column=1)
        # Listbox erstellen
        listbox_data = tk.Listbox(frame, width=85, height=10)
        #listbox_data.grid(row=10,column=0,columnspan=6, padx=10, pady=10)
        #func.showdata(listbox_data, shared_data) # Sofortiges Update

        # Dokumentation
        doku=tk.Button(frame,text='Dokumentation',command=lambda: func.open_dokumentation())
        doku.grid(row=1,column=2)

        #### BestellIds festlegen
        choose_id=tk.StringVar()
        file_entry = tk.Entry(frame, textvariable=choose_id, width=50)
        file_entry.grid(row=5,column=1)
        lable_bestellid=tk.Label(frame,text='SubscriptionIDs eintragen (Inkl. Kommatrennung. Bsp 555555,666666)')
        lable_bestellid.grid(row=4,column=1)
        file_button = tk.Button(frame, text="IDs speichern", command=lambda: func.Save_entry(
                                                                                            choose_id,
                                                                                            listbox2,
                                                                                            info_TESTcase,
                                                                                            custom_TestID,
                                                                                            auswahl_dropdown,
                                                                                            shared_data,
                                                                                            test_entry,
                                                                                            info_bestellid,
                                                                                            custom_bestellID,
                                                                                            Versand_entry,
                                                                                            logger,
                                                                                            choose_kunGrund,
                                                                                            new_bestellid,
                                                                                            file_entry_test,
                                                                                            lable_choose,
                                                                                            button_testID,
                                                                                            file_entry_bestellid,
                                                                                            lable_choose_bestellid,
                                                                                            button_bestellID
                                                                                        ))
        file_button.grid(row=5,column=2)
        # AB/KB Auswahl 
        optionen = ["Auftragsbestätigungen",'Kündigungsbestätigungen','Keine Bearbeitung','Beides']
        auswahl_dropdown = tk.StringVar(value='Auftragsbestätigungen') # Erste Option vordefinieren
        dropdown = ttk.OptionMenu(frame, auswahl_dropdown, auswahl_dropdown.get(), *optionen)
        dropdown.grid(row=6, column=2)

        #### Testfall eintragen ####
        # ID Button
        file_button = tk.Checkbutton(frame, text="TEST ID",variable=test_entry, command=lambda: func.Button_Aktivieren(
                                                                                                                    test_entry,
                                                                                                                    lable_choose,
                                                                                                                    file_entry_test,
                                                                                                                    button_testID,
                                                                                                                    new_bestellid,
                                                                                                                    button_bestellID,
                                                                                                                    file_entry_bestellid,
                                                                                                                    lable_choose_bestellid
                                                                                                                ))
        file_button.grid(row=6,column=0)
        
        # Testfall Ebene 2
        # Testfall Choose Eintrag
        file_entry_test=tk.Entry(frame,textvariable=custom_TestID,width=50)
        file_entry_test.grid(row=11,column=1)
        file_entry_test.grid_remove()
        # Testfall Choose Lable
        lable_choose=tk.Label(frame,text='PayerID der Testperson eintragen')
        lable_choose.grid(row=12,column=1)
        lable_choose.grid_remove()
        # Testfall Fix
        button_testID = tk.Button(frame,text='Test ID Speichern',command=lambda: func.choose_testID(
                                                                                                    logger,
                                                                                                    custom_TestID,
                                                                                                    button_testID,
                                                                                                    file_entry_test,
                                                                                                    lable_choose,
                                                                                                    info_TESTcase
                                                                                                ))
        button_testID.grid(row=11,column=2)
        button_testID.grid_remove()

        #### Versand unterdrücken Button ####
        file_button = tk.Checkbutton(frame, text="Versand unterdrücken",variable=Versand_entry,onvalue="Ja",offvalue="Nein", command=lambda: func.Button_Aktivieren)
        file_button.grid(row=7,column=0)


        #### Kündigungsgründe festlegen ####
        choose_kunGrund=tk.StringVar()
        file_entry_kuen = tk.Entry(frame, textvariable=choose_kunGrund, width=50)
        file_entry_kuen.grid(row=7,column=1)
        file_button_kuen = tk.Button(frame, text="Kündigungsgrund speichern", command=lambda: func.clear_kündigungsgrund(
                                                                                                                        choose_kunGrund,
                                                                                                                        listbox2,
                                                                                                                        logger
                                                                                                                    ))
        file_button_kuen.grid(row=7,column=2)
        lable_kuen=tk.Label(frame,text='Kündigungsgrund eintragen (Nur einen!)')
        lable_kuen.grid(row=6,column=1)
        auswahl_dropdown.trace_add("write", lambda: func.update_state(
                                                                    auswahl_dropdown,
                                                                    file_entry_kuen,
                                                                    file_button_kuen,
                                                                    listbox2
                                                                ))
        func.update_state(
                        auswahl_dropdown,
                        file_entry_kuen,
                        file_button_kuen,
                        listbox2
                )  


        #### Neue BestellID Button ####
        # BestellID Button
        file_button = tk.Checkbutton(frame, text="Neue BestellID",variable=new_bestellid, command=lambda: func.Button_Aktivieren(
                                                                                                                                test_entry,
                                                                                                                                lable_choose,
                                                                                                                                file_entry_test,
                                                                                                                                button_testID,
                                                                                                                                new_bestellid,
                                                                                                                                button_bestellID,
                                                                                                                                file_entry_bestellid,
                                                                                                                                lable_choose_bestellid
                                                                                                                            ))
        file_button.grid(row=8,column=0)

        # BestellID Ebene 2
        # BestellID Choose Eintrag
        file_entry_bestellid=tk.Entry(frame,textvariable=custom_bestellID,width=50)
        file_entry_bestellid.grid(row=15,column=1)
        file_entry_bestellid.grid_remove()
        # BestellID Choose Lable
        lable_choose_bestellid=tk.Label(frame,text='Neue BestellID eintragen')
        lable_choose_bestellid.grid(row=14,column=1)
        lable_choose_bestellid.grid_remove()
        # BestellID Fix
        button_bestellID = tk.Button(frame,text='BestellID Test Speichern',command=lambda: func.choose_BestellID(
                                                                                                                logger,
                                                                                                                custom_bestellID,
                                                                                                                button_bestellID,
                                                                                                                file_entry_bestellid,
                                                                                                                lable_choose_bestellid,
                                                                                                                info_bestellid
                                                                                                            ))
        button_bestellID.grid(row=15,column=2)
        button_bestellID.grid_remove()


        #### Logging
        # Frame für Log-Anzeige
        log_frame = tk.Frame(frame)
        log_frame.grid(row=17, column=0,columnspan=6, padx=10, pady=10)
        # Text-Widget für Log-Ausgabe
        log_text = scrolledtext.ScrolledText(log_frame, width=85, height=20, wrap=tk.WORD)
        log_text.grid(row=18,columnspan=6, column=0)
        # Custom Logging-Handler ins Textfeld umleiten
        text_handler = TextHandler(log_text)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        text_handler.setFormatter(formatter)
        logging.getLogger().addHandler(text_handler)
        # Logger
        logger = logging.getLogger("TkinterLogger")
        logger.setLevel(logging.INFO)

        return frame

    def Daten_erstellen(notebook):
        ## Inhaltsliste darstellen
        
        #### 
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Übersicht/Download")
        notebook.grid(row=0, column=0, sticky="nsew")
        
        # Exportordner festlegen
        folder_data = tk.StringVar()
        file_entry = tk.Entry(frame, textvariable=folder_data, width=50)
        file_entry.grid(row=3,column=1)
        file_button = tk.Button(frame, text="Durchsuchen", command=lambda: func.data_folder(folder_data, filedialog))
        file_button.grid(row=3,column=2)
        lable=tk.Label(frame,text='Ablageort wählen:')
        lable.grid(row=2,column=1)

        ##### Hauptfunktion
        # Starten
        file_button = tk.Button(frame, text="Starten",command=lambda: func.Generiere_Reports(
                                                                                        folder_data,
                                                                                        shared_data,
                                                                                        logger
                                                                                    ))
        file_button.grid(row=9,column=2)

        ## Inhaltsliste darstellen
        # Listbox erstellen
        listbox_data = tk.Listbox(frame, width=85, height=10)
        listbox_data.grid(row=10,column=0,columnspan=6, padx=10, pady=10)
        func.showdata(listbox_data, shared_data) # Sofortiges Update

        ## Logging
        # Frame für Log-Anzeige
        log_frame = tk.Frame(frame)
        log_frame.grid(row=15, column=0,columnspan=6, padx=10, pady=10)
        # Text-Widget für Log-Ausgabe
        log_text = scrolledtext.ScrolledText(log_frame, width=85, height=20, wrap=tk.WORD)
        log_text.grid(row=16,columnspan=6, column=0)
        # Custom Logging-Handler ins Textfeld umleiten
        text_handler = TextHandler(log_text)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        text_handler.setFormatter(formatter)
        logging.getLogger().addHandler(text_handler)
        # Logger
        logger = logging.getLogger("TkinterLogger")
        logger.setLevel(logging.INFO)

 

        return frame, func.showdata(listbox_data, shared_data)


    # Laden der Seiten
    seite1_frame = Aufträge_erstellen(notebook)
    seite2_frame= Daten_erstellen(notebook)  # showdata wird benötigt um die Listbox nach dem Speichern der BestellIDs zu aktualisieren
    # func.showdata(listbox_data, shared_data) beim Aufrufen der zweiten Seite wieder einfügen
    # Ereignisschleife starten
    root.mainloop()