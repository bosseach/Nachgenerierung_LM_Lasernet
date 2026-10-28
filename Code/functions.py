# Import
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
import logging
import requests

# Import eigene Funktionen
from core_services.constants import RESTHOST_PROD,HEADERS_PROD
from core_services.db import execute_sql_query


'''# Globale variablen erstellen
    test_entry = tk.IntVar(value=0)
    new_bestellid=tk.IntVar(value=0)
    custom_bestellID=tk.StringVar(value='')
    info_bestellid=tk.IntVar(value=0)
    info_TESTcase=tk.IntVar(value=0)
    custom_TestID=tk.StringVar(value=5513755201)
    Versand_entry = tk.StringVar(value='Nein')
    listbox2=tk.Listbox(root)
    shared_data = []
'''

# ======================================================================================
# Aufträge erstellen
# ======================================================================================

def Button_Aktivieren(
    test_entry,
    lable_choose,
    file_entry_test,
    button_testID,
    new_bestellid,
    button_bestellID,
    file_entry_bestellid,
    lable_choose_bestellid
):

    # Neue Testfälle
    if test_entry.get() == 1:
        lable_choose.grid(row=9, column=1)
        file_entry_test.grid(row=10, column=1)
        button_testID.grid(row=10, column=2)
    else:  # Alle Funktionen zurücksetzen
        file_entry_test.grid_remove()
        lable_choose.grid_remove()
        button_testID.grid_remove()

    # Neue BestellID
    if new_bestellid.get() == 1:
        button_bestellID.grid(row=15, column=2)
        file_entry_bestellid.grid(row=15, column=1)
        lable_choose_bestellid.grid(row=14, column=1)
    else:
        button_bestellID.grid_remove()
        file_entry_bestellid.grid_remove()
        lable_choose_bestellid.grid_remove()

    return test_entry

def choose_testID(
    logger,
    custom_TestID,
    button_testID,
    file_entry_test,
    lable_choose,
    info_TESTcase
):
    logger.info(f'Custom TestID gewählt: {custom_TestID.get()}')
    button_testID['state'] = tk.NORMAL
    file_entry_test.grid(row=10, column=1)
    lable_choose.grid(row=9, column=1)
    info_TESTcase.set(1)

    return info_TESTcase

def choose_BestellID(
    logger,
    custom_bestellID,
    button_bestellID,
    file_entry_bestellid,
    lable_choose_bestellid,
    info_bestellid
):
    logger.info(f'Custom BestellID gewählt: {custom_bestellID.get()}')
    button_bestellID['state'] = tk.NORMAL
    file_entry_bestellid.grid(row=15, column=1)
    lable_choose_bestellid.grid(row=14, column=1)
    info_bestellid.set(1)

    return info_bestellid

def choose_Kündigungsgrund(
    logger,
    custom_bestellID,
    button_bestellID,
    file_entry_bestellid,
    lable_choose_bestellid,
    info_bestellid
):
    logger.info(f'Custom BestellID gewählt: {custom_bestellID.get()}')
    button_bestellID['state'] = tk.NORMAL
    file_entry_bestellid.grid(row=15, column=1)
    lable_choose_bestellid.grid(row=14, column=1)
    info_bestellid.set(1)

    return info_bestellid

def clear_kündigungsgrund(
    choose_kunGrund,
    logger
):
    #list_bestell2 = choose_kunGrund.get().split(',')
    #list_bestell2 = choose_kunGrund.get()
    #for item in list_bestell2:
    #    listbox_uebersicht.insert(tk.END, item)

    logger.info(f'Kündigungsgrund gespeichert:{choose_kunGrund.get()}')
    #logger.info(f'listbox:{list(listbox_uebersicht.get(0, tk.END))}')
    #logger.info('Kündigungsgrund ist gespeichert')
    #choose_kunGrund.set('')

def Save_entry(
    choose_id,
    listbox_uebersicht,
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
):
    list_subscriptions = choose_id.get().split(',')

    try:
        #kuen_var = str(listbox_uebersicht.get(0, tk.END)[0])
        kuen_var = choose_kunGrund.get()
    except:
        kuen_var = ''

    if info_TESTcase.get() == 1:
        test_ID = custom_TestID.get()
    else:
        test_ID = ''

    new_entry = {
        'Typ': auswahl_dropdown.get(),
        'Nr': len(shared_data) + 1,
        'list_subscriptions': list_subscriptions,
        'test_entry': test_entry.get(),
        'info_TESTcase': info_TESTcase.get(),
        'Change_accountID': test_ID,
        'info_bestellid': info_bestellid.get(),
        'custom_bestellID': custom_bestellID.get(),
        'Versand_unterdrücken': Versand_entry.get(),
        'Kuendigungsgrund': kuen_var
    }
    shared_data.append(new_entry)

    logger.info(f'############# BestellIDs: {shared_data} hinzugefügt #############')
    logger.info('BestellIDs sind gespeichert')

    choose_id.set('')
    test_entry.set(0)
    info_bestellid.set(0)
    info_TESTcase.set(0)
    custom_TestID.set(5513755201)
    custom_bestellID.set('')
    Versand_entry.set('Nein')
    choose_kunGrund.set('')
    new_bestellid.set(0)
    listbox_uebersicht.delete(0, tk.END)

    file_entry_test.grid_remove()
    lable_choose.grid_remove()
    button_testID.grid_remove()
    file_entry_bestellid.grid_remove()
    lable_choose_bestellid.grid_remove()
    button_bestellID.grid_remove()

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
    if auswahl_dropdown.get() == "Kündigungsbestätigungen":
        state = "normal"
    else:
        state = "disabled"

    file_entry_kuen.config(state=state)
    file_button_kuen.config(state=state)
    if listbox2 is not None:
        listbox2.config(state=state)

def open_dokumentation():
    text_var = ('''Das Tool generiert einen Subscriptions- und einen Accountreport für \ndie Erstellung der Auftragsbestätigungen via Lasernet. 
            \n- Als Input dienen BestellIds für die zu erstellenden Aufträge, \nMehrere IDs sind durch Komma zu trennen. 
            \n- Ablage der Reports \\vm-it-zen-shd-2.aschendorff.net\Lesermarkt-PROD\CSV\CSV_IN 
            \n- Lasernet startet jeden Tag um 20:00 einen Lauf und prüft ob Reports dort abgelegt wurden und verarbeitet diese. 
            \n- Es besteht die Möglichkeit mit der Funktion "Testfall eintragen" \neinen Test zu generieren, dann werden alle personenbezogenen Daten \nder Bestellungen auf eine zu wählende PayerID geändert, dies erlaubt \ndie Kontrolle und das Testen von Auftragsbestätigungen.
            \n- Mit "Versand unterdrücken" kann der e-Mail und Postversand der Subscriptions unterdrückt werden. 
                    ''')

    root_doku = tk.Tk()
    root_doku.wm_title('Dokumentation')
    root_doku.geometry("600x300")

    doku_tk = tk.Text(root_doku, height=40, width=70)
    doku_tk.grid(row=1, column=0)
    doku_tk.insert(1.0, text_var)
    doku_tk.config(state='disable')

    root_doku.mainloop()


# ======================================================================================
# Daten erstellen
# ======================================================================================

def data_folder(folder_data, filedialog):
    folder_data.set(filedialog.askdirectory())

def showdata_treeview(treeview_data, shared_data):
    """
    Befüllt ein ttk.Treeview mit den Daten aus shared_data.
    """
    # treeview als anzuzeigendes Objekt, shared Data als Daten
    # Löschen der bisherigen Anzeige
    #if type(treeview_data) != 'NoneType':
    if treeview_data == None:
        pass
    else:
        for item in treeview_data.get_children():
                treeview_data.delete(item)

    # Keine Einträge vorhanden
    if not shared_data:
            treeview_data.insert("",
                                tk.END,
                                values=("Keine Einträge vorhanden"))
            return
    
    # Dictionary-Daten als Tabellenzeilen einfügen
    for item in shared_data:
        treeview_data.insert(
            "",
            tk.END,
            values=(
                item.get("Nr", ""),
                item.get("Typ", ""),
                len(item.get("list_subscriptions", [])),
                item.get("Change_accountID", ""),
                item.get("Versand_unterdrücken", ""),
                item.get("Kuendigungsgrund", "")
            )
        )
        
def showdata(listbox_data, shared_data):
    listbox_data.delete(0, tk.END)

    if not shared_data:
        #listbox_data.insert(tk.END,shared_data)
        listbox_data.insert(tk.END, "Keine Einträge vorhanden")
        return

    for item in shared_data:
        display_text = (
            f"Typ: {item['Typ']}, "
            f"Anzahl: {len(item['list_subscriptions'])}, "
            f"Testkunde: {item['Change_accountID']}, "
            f"Versand unterdrückt: {item['Versand_unterdrücken']}, "
            f"Kündigungsgrund: {item['Kuendigungsgrund']}"
        )
        listbox_data.insert(tk.END, display_text)

def Generiere_Reports(
    folder_data,
    shared_data,
    logger
):
    start_time = datetime.now()

    if len(folder_data.get()) == 0:
        logger.info('Kein Verzeichnis ausgewählt')

    elif len(shared_data) == 0:
        logger.info('Keine BestellIDs ausgewählt')

    else:
        check_df = 0

        for item in shared_data:
            df_sub, dict_email = Allg_Verarbeitung(item,
                                                   logger,
                                                   item['custom_bestellID']
                                                    )

            if item['info_bestellid'] != 0:
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

    root2 = tk.Tk()
    root2.wm_title('Result')
    root2.geometry("200x100")

    result_text = tk.Label(
        root2,
        text=f'Die Testdaten sind erstellt worden \n Laufzeit: {(endtime-start_time).seconds} Sekunden'
    )
    result_text.grid(row=1, column=1)

    root2.mainloop()

def Umwandeln_BestellID(df_sub, new_id):
    '''
    Ändern der BestellIDs auf eine generische neue ID
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

def Allg_Verarbeitung(
    item,
    logger,
    custom_bestellID
):
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

    df_sub['StartDate'] = pd.to_datetime(df_sub['StartDate'], errors='coerce')
    mask = df_sub['StartDate'].dt.time == pd.to_datetime('00:00:00').time()
    df_sub.loc[mask, 'StartDate'] = df_sub.loc[mask, 'StartDate'] + pd.Timedelta(hours=1)

    df_sub['SubscriptionId'] = df_sub['SubscriptionId'].astype(int)

    if item['info_TESTcase'] == 1:
        if len(item['Change_accountID']) == 10:
            df_sub['Payer'] = item['Change_accountID']
            logging.info('Testanpassung erfolgt')
        else:
            logger.error('Keine gültige PayerID!')

    # Custom Bestellid hinzufügen
    if item['info_bestellid'] == 1:
        if len(custom_bestellID) != 0:
            df_sub['BestellId'] = custom_bestellID
            logger.info('Custom BestellID ist eingebaut')
        else:
            logger.error('Keine gültige BestellID eingegeben')

    if item['Versand_unterdrücken'] == 'Ja':
        df_sub['ZZBestaetigung'] = 'Nein'
        logger.info('Versand unterdrückt')
    else:
        logger.info('Versand aktiv')

    return df_sub, dict_email

def AB_KB_Verarbeitung(
    df_sub,
    dict_email,
    item,
    typ
):
    list_payer = []

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

    if item['test_entry'] != 0:
        df_sub['EmailAddress'] = df_sub['EmailAddress'].apply(
            lambda x: df_acc['EmailAddress'][0]
        )
        df_sub['VkOrg'] = df_sub['VkOrg'].apply(
            lambda x: 'WN' if x == 'SLV' else x
        )

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

    elif typ == 'KB':
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

        if item['Versand_unterdrücken'] == 'Ja':
            df_acc['EmailAddress'] = 'Hendrik.Bosse@aschendorff.de'

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

    elif typ == 'raw':
        pass

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