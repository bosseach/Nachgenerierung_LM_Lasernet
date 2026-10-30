# Import
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
from ttkbootstrap import ScrolledText
import ttkbootstrap as ttk
import logging
import requests

# Import eigene Funktionen
from core_services.constants import RESTHOST_PROD,HEADERS_PROD
from core_services.db import execute_sql_query

# ======================================================================================
# Aufträge erstellen
# ======================================================================================

def Button_Aktivieren(dict,logger):
    '''
    Steuert die Anzeige Änderungsoptionen an den Subscriptions
    '''
    # Neue Testfälle
    if dict['var_check'].get() == 1:
        dict['lable']['Name'].grid(row=dict['lable']['row'], column=dict['lable']['column'])
        dict['file_entry']['Name'].grid(row=dict['file_entry']['row'], column=dict['file_entry']['column'])
        dict['button']['Name'].grid(row=dict['button']['row'], column=dict['button']['column'])
    else:  
        # Alle Funktionen zurücksetzen
        dict['file_entry']['Name'].grid_remove()
        dict['lable']['Name'].grid_remove()
        dict['button']['Name'].grid_remove()
        # variable zurück auf Standard setzen
        dict['variable'].set('')
        logger.info(f'{dict['var_name']} ist zurückgesetzt')

def Set_variable_option(
    logger,
    var_name,
    var_entry,
    var_button,
    var_info
    ):
    '''
    Abspeichern der Feldänderungen
    '''
    logger.info(f'{var_name} gewählt: {var_entry.get()}')
    # Zurücksetzen der Variable außer bei Versand unterdrücken
    if var_name not in ['Versand unterdrücken', 'API Call']:
        var_button['state'] = tk.NORMAL
        var_info.set(1)
    else:
        pass

def Save_entry(
    # Bestellungen/Logger
    subscriptionid,
    auswahl_dropdown,
    shared_data,
    logger,
    API_call,
    # Felderänderungen
    info_payerid,
    custom_payerid,
    info_bestellid,
    custom_bestellID,
    info_kündigungsgrund,
    custom_kündigunsgrund,
    Versand_entry,
    #### Zurücksetzen der GUI
    # Payerid
    new_payerid,
    file_entry_payerid,
    label_choose_payerid,
    button_payerid,
    # Bestellid
    new_bestellid,
    file_entry_bestellid,
    label_choose_bestellid,
    button_bestellID,
    # Kündigunsgrund
    new_kündigungsgrund,
    file_entry_kuen,
    label_choose_kuen,
    button_kuen
):
    '''
    Funktion ermöglicht das Abspeichern der eingetragenen Subscriptions inkl. der ausgewählten Änderungen
    '''
    list_subscriptions = subscriptionid.get().split(',')
    
    #### Feldänderungen 
    # Kündigungen
    if info_kündigungsgrund.get()==1:
        new_kündigungsgrund_entry = custom_kündigunsgrund.get()
    else:
        new_kündigungsgrund_entry='Nein'
    # Neue PayerID
    if info_payerid.get() == 1:
        new_payer_id = custom_payerid.get()
    else:
        new_payer_id = 'Nein'
    # neue Bestellid
    if info_bestellid.get()==1:
        new_bestellid_entry=custom_bestellID.get()
    else:
        new_bestellid_entry='Nein'

    # Neue Eintragungen
    new_entry = {
        'Typ': auswahl_dropdown.get(),
        'Nr': len(shared_data) + 1,
        'list_subscriptions': list_subscriptions,
        'custom_payerid': new_payer_id,
        'custom_bestellID': new_bestellid_entry,
        'Versand_unterdrücken': Versand_entry.get(),
        'Kuendigungsgrund': new_kündigungsgrund_entry,
        'API_call':API_call.get()
    }
    shared_data.append(new_entry)

    # Logger
    logger.info(f'############# BestellIDs: {shared_data} hinzugefügt #############')
    logger.info('BestellIDs sind gespeichert')

    #### Bereinigen der Variablen
    subscriptionid.set('')
    Versand_entry.set('Nein')
    API_call.set('Nein')
    # Payerid
    new_payerid.set(0)
    info_payerid.set(0)
    custom_payerid.set(5513755201)
    # Bestellid
    new_bestellid.set(0)
    info_bestellid.set(0)
    custom_bestellID.set('')
    # Kündigungsgrund
    info_kündigungsgrund.set(0)
    new_kündigungsgrund.set(0)
    custom_kündigunsgrund.set('')

    #### Verdecken der Felder
    # Payerid
    file_entry_payerid.grid_remove()
    label_choose_payerid.grid_remove()
    button_payerid.grid_remove()
    # Bestellid
    file_entry_bestellid.grid_remove()
    label_choose_bestellid.grid_remove()
    button_bestellID.grid_remove()
    # Kündigungsgrund
    file_entry_kuen.grid_remove()
    label_choose_kuen.grid_remove()
    button_kuen.grid_remove()

    try:
        pass
    except NameError:
        pass

def update_state(
    auswahl_dropdown,
    file_entry_kuen,
    file_button_kuen,
    listbox2
):
    '''
    Die Funktion limiert die Änderungen von Kündigungsgründen auf das Dokument Kündigungsbestätigung
    '''
    if auswahl_dropdown.get() == "Kündigungsbestätigungen":
        state = "normal"
    else:
        state = "disabled"

    file_entry_kuen.config(state=state)
    file_button_kuen.config(state=state)
    if listbox2 is not None:
        listbox2.config(state=state)


# ======================================================================================
# Sonstige
# ======================================================================================

def open_dokumentation(parent):
    text_var = """
    Das Tool generiert einen Subscriptions- und einen Accountreport für
    die Erstellung der Auftragsbestätigungen via Lasernet.

    ##### Prozess #####
    - Lasernet startet jeden Tag zwei Läufe zum Erstellen der Auftrags- und Kündigungsbestätigungen.
      Einen morgen zum Verarbeiten der Daten des Vortages und einen Abends um 20 Uhr der für Korrekturen und
      Test ist. Beide verarbeiten die Daten identisch

    - Das Tool ermöglicht das Erstellen der entsprechenden Reports, inkl. unterschiedlicher Fälle. 

    - Die entsprechenden Reports müssen unter dem folgenden Verzeichnis abgelegt werden:
        \\\\vm-it-zen-shd-2.aschendorff.net\\Lesermarkt-PROD\\CSV\\CSV_IN
    
    #### Bedienung ####
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
    """

    # Fenster erstellen
    root_doku = ttk.Toplevel(title="Dokumentation")
    root_doku.geometry("700x400")
    root_doku.resizable(True, True)

    # Fenster vor dem Hauptfenster halten
    root_doku.transient(root_doku.master)
    root_doku.grab_set()

    doku_text = ScrolledText(
        root_doku,
        height=20,
        width=80,
        wrap="word",
        autohide=True,
        padding=10,
    )
    doku_text.pack(fill="both", expand=True, padx=10, pady=10)

    doku_text.insert("1.0", text_var)
    doku_text.configure(state="disabled")

    close_button = ttk.Button(
        root_doku,
        text="Schließen",
        bootstyle="secondary",
        command=root_doku.destroy
    )
    close_button.pack(pady=(0, 10))

def showdata_treeview(treeview_data, shared_data):
    """
    Ermöglicht das Anzeigen der zu bearbeitenden Fälle in einer Treeview Tabelle
    """
    # treeview als anzuzeigendes Objekt, shared Data als Daten
    # Löschen der bisherigen Anzeige
    #if type(treeview_data) != 'NoneType':
    if treeview_data == None:
        pass
    else:
        for item in treeview_data.get_children():
                treeview_data.delete(item)
    
    # Dictionary-Daten als Tabellenzeilen einfügen
    for item in shared_data:
        treeview_data.insert(
            "",
            tk.END,
            values=(
                item.get("Nr", ""),
                item.get("Typ", ""),
                len(item.get("list_subscriptions", [])),
                item.get("custom_payerid", ""),
                item.get("Versand_unterdrücken", ""),
                item.get("Kuendigungsgrund", ""),
                item.get("custom_bestellID", ""),
                item.get("API_call", "")
            )
        )

# ======================================================================================
# Daten erstellen
# ======================================================================================

# Hilfsfunktionen
def data_folder(folder_data, filedialog):
    folder_data.set(filedialog.askdirectory())

def Umwandeln_BestellID(df_sub, new_id):
    '''
    Ändern der BestellIDs auf eine neue ID
    '''
    nr_id = 0
    dict_map_ID = []

    for item in df_sub['BestellId'].unique():
        if item != 'leer':
            dict_map_ID.append({'Alt': item, 'Neu': f"{new_id}_{nr_id}"})
            nr_id += 1

    df_sub['BestellId'] = df_sub['BestellId'].replace(
        {x['Alt']: x['Neu'] for x in dict_map_ID}
    )

    dict_map_leer = []
    nr_id_leer = 0

    for row, col in df_sub.iterrows():
        if col['BestellId'] == 'leer':
            dict_map_leer.append({
                'SubscriptionId': col['SubscriptionId'],
                'BestellId': f"{new_id}_LEER_{nr_id_leer}"
            })
            nr_id_leer += 1

    for item in dict_map_leer:
        df_sub.loc[
            df_sub['SubscriptionId'] == item['SubscriptionId'],
            'BestellId'
        ] = item['BestellId']

    return df_sub

def get_api_call(url, HEADERS_PROD, logging, choose_header=None):
    '''
    Die Funktion führt einen standardisierten API Call durch
    '''
    if choose_header is None:
        choose_header = HEADERS_PROD

    try:
        response = requests.get(
            url,
            verify=False,
            headers=choose_header
        ).json()
        logging.info(f"API-Aufruf erfolgreich")
        return response

    except requests.exceptions.RequestException as e:
        logging.error(f"API-Aufruf fehlgeschlagen: {e}")

# Zentrale Funktionen

def Generiere_Reports(
    folder_data,
    shared_data,
    logger,
    parent
):
    '''
    Zentrale Funktion Steuern der Datenabfragen der ATLAS DB und deren Anpassungen
    '''
    start_time = datetime.now()

    if len(folder_data.get()) == 0:
        logger.info('Kein Verzeichnis ausgewählt')

    elif len(shared_data) == 0:
        logger.info('Keine BestellIDs ausgewählt')

    else:
        check_df = 0

        for item in shared_data:
            df_sub, dict_email = Allg_Verarbeitung(item,
                                                   logger
                                                    )

            if item['custom_bestellID'] != 'Nein':
                df_sub = Umwandeln_BestellID(df_sub, item['custom_bestellID'])

            if item['Typ'] == 'Auftragsbestätigungen':
                df_acc, df_sub = AB_KB_Verarbeitung(df_sub, dict_email, item, 'AB')
            elif item['Typ'] == 'Kündigungsbestätigungen':
                df_acc, df_sub = AB_KB_Verarbeitung(df_sub, dict_email, item, 'KB')
            elif item['Typ'] == 'Beides':
                df_acc, df_sub = AB_KB_Verarbeitung(df_sub, dict_email, item, 'beides')
            elif item['Typ'] == 'Keine Bearbeitung':
                df_acc, df_sub = AB_KB_Verarbeitung(df_sub, dict_email, item, 'raw')

            if check_df == 0:
                df_sub_full = df_sub
                df_acc_full = df_acc
                check_df = 1
            else:
                df_sub_full = pd.concat([df_sub_full, df_sub], ignore_index=True)
                df_acc_full = pd.concat([df_acc_full, df_acc], ignore_index=True)

    EXP_Datum = datetime.now().strftime("%d.%m.%Y")

    imp = folder_data.get()
    imp_acc = imp + r'/Accountreport_Nachlieferung'
    imp_sub = imp + r'/Subscriptionsreport_Nachlieferung'
    EXP_acc = imp_acc + r'_{}.csv'.format(EXP_Datum)
    EXP_sub = imp_sub + r'_{}.csv'.format(EXP_Datum)

    df_sub_full.to_csv(EXP_sub, index=False, sep=',')
    df_acc_full.to_csv(EXP_acc, index=False, sep=',')

    endtime = datetime.now()

    # Ergebnisfenster
    root_result = ttk.Toplevel(title="Ergebnis")
    root_result.geometry("200x100")
    root_result.resizable(True, True)

    # Fenster vor dem Hauptfenster halten
    root_result.transient(root_result.master)
    root_result.grab_set()

    result_text = ttk.Label(
        root_result,
        text=f'Die Testdaten sind erstellt worden \n Laufzeit: {(endtime-start_time).seconds} Sekunden'
    )
    result_text.grid(row=1, column=1)

    #root2.mainloop()

def Allg_Verarbeitung(
    item,
    logger
    ):
    '''
    Ermittelt die Bestellungen aus dem Subscriptionreport und die Dokumentenunabhängigen Anpassungen
    '''
    # ==================
    # Bestellungen bilden
    # ==================
    list_subscriptions = item['list_subscriptions']
    sql_subs = str(list_subscriptions).replace('[', '(')
    sql_subs = sql_subs.replace(']', ')')
    sql_subs = sql_subs.replace('None,', '')

    SQLAbfrage_sub = f'''
                       SELECT *
                        FROM dbm_lesermarkt.tb_subscriptionsreport_ff
                        # Alle Kompletten Bestellungen der Subs mit Bestellid
                        WHERE bestellid <> 'leer'
                        and bestellid IN (
                                SELECT bestellid 
                                FROM dbm_lesermarkt.tb_subscriptionsreport_ff
                                WHERE subscriptionid IN {sql_subs}
                                )
                        # Alle Subs mit Bestellid = leer
                        OR subscriptionid IN (
                                SELECT subscriptionid
                                FROM dbm_lesermarkt.tb_subscriptionsreport_ff
                                WHERE subscriptionid IN {sql_subs}
                                AND bestellid = 'leer'
                        )
                        '''

    df_sub = execute_sql_query(SQLAbfrage_sub)

    dict_email = {}

    # API Calls
    # Bearbeiter verändern das Startdatum eines Bestellung, diese ist nicht live in der DB, daher Updateoption durch API Call
    if item['API_call']=='Ja':
        for item_acc in list(df_sub['AccountId'].unique()):
            url_acc = f"{RESTHOST_PROD}accounts/{item_acc}"
            response_acc = get_api_call(url_acc,HEADERS_PROD,logger)
            dict_email[item_acc] = response_acc['email']

            url_sub = f"{RESTHOST_PROD}accounts/{item_acc}/subscriptions"
            response_sub = get_api_call(url_sub,HEADERS_PROD,logger)

            for sub in response_sub:
                df_sub.loc[
                    df_sub['SubscriptionReference'] ==
                    sub['recurringPaymentInfo']['subscriptionReference'],
                    'EmailAddress'
                ] = response_acc['email']

                df_sub.loc[
                    df_sub['SubscriptionReference'] ==
                    sub['recurringPaymentInfo']['subscriptionReference'],
                    'StartDate'
                ] = sub['startDate']

    # Anpassungen Formate
    df_sub['StartDate'] = pd.to_datetime(df_sub['StartDate'], errors='coerce')
    mask = df_sub['StartDate'].dt.time == pd.to_datetime('00:00:00').time()
    df_sub.loc[mask, 'StartDate'] = df_sub.loc[mask, 'StartDate'] + pd.Timedelta(hours=1)
    df_sub['SubscriptionId'] = df_sub['SubscriptionId'].astype(int)

    # ==================
    # Änderungen durchführen
    # ==================

    # Payer ID hinzufügen
    if item['custom_payerid'] != 'Nein':
        if len(item['custom_payerid']) == 10:
            df_sub['Payer'] = item['custom_payerid']
            logging.info('Custom PayerID hinzugefügt')
        else:
            pass

    # Custom Bestellid hinzufügen
    if item['custom_bestellID'] != 'Nein':
        df_sub['BestellId'] = item['custom_bestellID']
        logger.info('Custom BestellID ist eingebaut')
    else:
        pass

    # Versand Unterdrücken
    if item['Versand_unterdrücken'] == 'Ja':
        df_sub['ZZBestaetigung'] = 'Nein'
        logger.info('Versand unterdrückt')
    else:
        pass

    return df_sub, dict_email

def AB_KB_Verarbeitung(
    df_sub,
    dict_email,
    item,
    typ
    ):
    '''
    Funktion ermittelt die zu den Bestellungen gehörenden GPs und bildet den Accountreport. Ebenso werden Dokumentenspezifische Anpassungen durchgeführt
    '''
    # ==================
    # Accountreport bilden
    # ==================
    list_payer = []
    # Accountreport bilden
    for item_payer in df_sub['Payer'].unique():
        list_payer.append(item_payer[1:])

    list_payer = str(list_payer).replace('[', '(')
    list_payer = list_payer.replace(']', ')')
    list_payer = list_payer.replace('None,', '')

    SQLAbfrage_acc = '''
                select *
                from dbm_lesermarkt.tb_accountreport_faktur
                where accountid in {}
                '''.format(list_payer)

    df_acc = execute_sql_query(SQLAbfrage_acc)

    df_acc['AccountId'] = df_acc['AccountId'].astype(str)
    df_acc['EmailAddress'] = df_acc['AccountId'].map(dict_email).fillna(df_acc['EmailAddress'])

    Datum = datetime.now() - timedelta(days=1)
    Datum = Datum.strftime("%Y-%m-%d %H:%M:%S")

    # Ändern der Mailaddressen im SubRep bei geänderter PayerID 
    if item['custom_payerid'] != 'Nein':
        df_sub['EmailAddress'] = df_sub['EmailAddress'].apply(
            lambda x: df_acc['EmailAddress'][0]
        )
        df_sub['VkOrg'] = df_sub['VkOrg'].apply(
            lambda x: 'WN' if x == 'SLV' else x
        )

    # ==================
    # Dokumentenspezifische Verarbeitung
    # ==================

    #### Verarbeitung AB
    if typ == 'AB':
        df_sub['Kuendigungseingangsdatum'] = 'leer'
        df_sub['KuendigungsgrundName'] = 'leer'
        df_sub['Kuendigungsgrund'] = 'leer'
        df_sub['CreatedDate'] = Datum
        df_sub['Erstellungsdatum'] = (
            datetime.now() - timedelta(days=1)
        ).strftime("%Y-%m-%dT%H:%M:%S")
        df_sub['SubscriptionStatus'] = 'Subscription pending Start Date'
        df_acc['AccountId'] = df_acc['AccountId'].astype(int)

    # Versand Unterdrücken
    if item['Versand_unterdrücken'] == 'Ja':
            df_sub['ZZBestaetigung'] = 'Nein'


    #### Verarbeitung KB
    elif typ == 'KB':
        # Änderung Kündigungsgrund
        if item['Kuendigungsgrund'] != 'Nein':
            df_sub['Kuendigungsgrund'] = item['Kuendigungsgrund']
        
        # Anpassen des Kündigunseingangsdatums auf das aktuelle Datum  
        df_sub['Kuendigungseingangsdatum'] = df_sub.apply(
            lambda x: Datum if x['Kuendigungseingangsdatum'] != 'leer'
            else x['Kuendigungseingangsdatum'],
            axis=1
        )
        # Anpassen des Subscriptionstatus für Lasernet
        df_sub['SubscriptionStatus'] = df_sub.apply(
            lambda x: 'Active Subscription'
            if x['Kuendigungsgrund'] != '95'
            else x['SubscriptionStatus'],
            axis=1
        )

        df_acc['AccountId'] = df_acc['AccountId'].astype(int)
        # Hinzufügen der indirekten Unterdrückung
        if item['Versand_unterdrücken'] == 'Ja':
            df_acc['EmailAddress'] = 'Hendrik.Bosse@aschendorff.de'

    #### Verarbeitung beides
    elif typ == 'beides':
        if len(item['Kuendigungsgrund']) != 0:
            df_sub['Kuendigungsgrund'] = item['Kuendigungsgrund']

        df_sub['Kuendigungseingangsdatum'] = df_sub.apply(
            lambda x: Datum if x['Kuendigungseingangsdatum'] != 'leer'
            else x['Kuendigungseingangsdatum'],
            axis=1
        )

        df_sub['SubscriptionStatus'] = df_sub.apply(
            lambda x: 'Active Subscription'
            if x['Kuendigungsgrund'] != '95'
            else x['SubscriptionStatus'],
            axis=1
        )

        df_acc['AccountId'] = df_acc['AccountId'].astype(int)

        df_sub['CreatedDate'] = Datum
        df_sub['Erstellungsdatum'] = (
            datetime.now() - timedelta(days=1)
        ).strftime("%Y-%m-%dT%H:%M:%S")
        df_sub['SubscriptionStatus'] = 'Active Subscription'

    #### Keine Verarbeitung
    elif typ == 'raw':
        pass

    # ==================
    # Endanpassungen
    # ==================
    reverse_mapping = {
        "CreatedDate": "Created Date",
        "LastUpdated": "Last Updated",
        "SHIPPINGHOUSEFLATNUMBER": "ShippingHous, cols.[Abladestelle",
        "OrderDescription": "Order Description",
        "RefundCode": "Refund Code",
        "RefundReason": "Refund Reason",
        "RefundUser": "Refund User",
        "FullName": "Full Name",
        "AccountID": "eSuite Account",
        "Schedule": "Schedule_Mon-Sun",
    }

    df_sub.rename(columns=reverse_mapping, inplace=True)
    df_acc.rename(columns=reverse_mapping, inplace=True)

    try:
        df_sub.drop(columns='SubID_AccID', inplace=True)
    except:
        pass

    return df_acc, df_sub