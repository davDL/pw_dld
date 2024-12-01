import dash
from dash import html, callback, Output, Input, dcc
import dash_bootstrap_components as dbc
from dateutil.utils import today
import numpy as np
import random
import pandas as pd
from datetime import date
import os
from dashboard_sections.registry_table_components import table_in_row_machinery, table_in_row_workers, \
    table_in_row_vineyards, table_in_row_production, table_in_row_production_yield, table_in_row_orders
from dashboard_sections.performance_table_components import table_performances_vineyards, table_performances_variety, table_performances_sell_orders
from common_components import home_performances_section, elevated_bar, home_section
from dashboard_sections.global_performances_components import get_global_performances_cards
import plotly.graph_objects as go
from meteostat import Point, Daily

dash.register_page(__name__, path='/')

workers_dataset = pd.read_csv("assets/lavoratori.csv", sep=',')
machinery_dataset = pd.read_csv("assets/macchinari.csv", sep=',')
vineyards_dataset = pd.read_csv("assets/vigneti.csv", sep=',')
production_dataset = pd.read_csv("assets/produzione.csv", sep=',')
orders_dataset = pd.read_csv("assets/ordini.csv", sep=',')

def get_weather_dataset_by_date_2023_2024():
    location = Point(lat=41.9028, lon=12.4964)  # Roma, Italia (esempio)
    param_start = pd.Timestamp("2023-01-01")
    param_end = pd.Timestamp("2024-12-30")

    data = Daily(location, param_start, param_end)
    data = data.fetch()

    # Crea il DataFrame con le colonne desiderate
    df = data[['tavg', 'tmin', 'tmax', 'prcp']]
    df.columns = ['temperatura_media', 'temperatura_minima', 'temperatura_massima', 'precipitazioni']

    return df

weather_conditions_dataset = get_weather_dataset_by_date_2023_2024()

reset_filters_icon = dash.get_asset_url('ic_reset_filters.png')
order_icon = dash.get_asset_url('ic_arrow_down_black.png')

global_variables = {}
global_variables['clicked_times'] = 0
global_variables['clicked_times_2'] = 0

mesi_italiani = {
        'January': 'Gennaio',
        'February': 'Febbraio',
        'March': 'Marzo',
        'April': 'Aprile',
        'May': 'Maggio',
        'June': 'Giugno',
        'July': 'Luglio',
        'August': 'Agosto',
        'September': 'Settembre',
        'October': 'Ottobre',
        'November': 'Novembre',
        'December': 'Dicembre'
    }

def plot_data_temp(df, y_columns):
    fig = go.Figure()

    for col in y_columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col))

    fig.update_layout(xaxis_title='Tempo')
    fig.update_layout(yaxis_title='Temperatura (°C)')
    fig.update_layout(
        xaxis=dict(
            tickformat='%d %B %Y',
        )
    )
    return fig

def plot_data_prcp(df, y_columns):
    fig = go.Figure()

    for col in y_columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col))
    fig.update_layout(xaxis_title='Tempo')
    fig.update_layout(yaxis_title='Precipitazioni (mm)')
    fig.update_layout(
        xaxis=dict(
            tickformat='%d %B %Y',
        )
    )
    return fig

def get_filtered_weather(start, end):
    location = Point(lat=41.9028, lon=12.4964)  # Roma, Italia (esempio)

    data = Daily(location, start, end)
    data = data.fetch()

    # Crea il DataFrame con le colonne desiderate
    df = data[['tavg', 'tmin', 'tmax', 'prcp']]
    df.columns = ['temperatura_media', 'temperatura_minima', 'temperatura_massima', 'precipitazioni']

    return df

def get_season_dates(year, season_item):
    # Definisci i mesi di inizio e fine per ogni stagione
    seasons = [(12, 3), (3, 5), (6, 8), (9, 11)]
    start_month, end_month = seasons[season_item - 1]

    start_date_time = pd.to_datetime(f"{year}-{start_month}-01")
    end_date_time = pd.to_datetime(f"{year}-{end_month}-30")

    return start_date_time, end_date_time

def get_weather_dataset_by_date(start_date):
    location = Point(lat=41.9028, lon=12.4964)  # Roma, Italia (esempio)
    param_start = pd.Timestamp(f"{start_date.year}-01-01")
    param_end = pd.Timestamp(f"{start_date.year}-12-30")

    data = Daily(location, param_start, param_end)
    data = data.fetch()

    # Crea il DataFrame con le colonne desiderate
    df = data[['tavg', 'tmin', 'tmax', 'prcp']]
    df.columns = ['temperatura_media', 'temperatura_minima', 'temperatura_massima', 'precipitazioni']

    return df

def generate_production_quantity_by_weather(quantita_prevista, start_date_millis):
    # Soglia per il numero totale di occorrenze
    soglia_occorrenze = 10

    # Assumiamo che start_date_millis sia la tua data di inizio in millisecondi
    start_date = pd.to_datetime(start_date_millis, unit='ms')

    location = Point(lat=41.9028, lon=12.4964)  # Roma, Italia (esempio)
    param_start = pd.Timestamp(f"{start_date.year}-01-01")
    param_end = pd.Timestamp(f"{start_date.year}-12-31")

    data = Daily(location, param_start, param_end)
    data = data.fetch()

    # Crea il DataFrame con le colonne desiderate
    df = data[['tavg', 'tmin', 'tmax', 'prcp']]
    df.columns = ['temperatura_media', 'temperatura_minima', 'temperatura_massima', 'precipitazioni']

    df_weather_by_date = get_weather_dataset_by_date(start_date)

    df_primavera = None
    df_estate = None
    df_autunno = None

    for season in range(1, 5):
        start, end = get_season_dates(start_date.year, season)
        if season == 2:
            df_primavera = df_weather_by_date[(df_weather_by_date.index >= start) & (df_weather_by_date.index <= end)]
        elif season == 3:
            df_estate = df_weather_by_date[(df_weather_by_date.index >= start) & (df_weather_by_date.index <= end)]
        else:
            df_autunno = df_weather_by_date[(df_weather_by_date.index >= start) & (df_weather_by_date.index <= end)]

    # Conteggio delle occorrenze temperatura
    conteggio_primavera_temp = len(df_primavera[(df_primavera['temperatura_minima'] < 10) & (df_primavera['temperatura_massima'] > 15)])
    conteggio_estate_temp = len(df_estate[(df_estate['temperatura_minima'] < 25) & (df_estate['temperatura_massima'] > 35)])
    conteggio_autunno_temp = len(df_autunno[(df_autunno['temperatura_minima'] < 15) & (df_autunno['temperatura_massima'] > 25)])

    # Conteggio delle occorrenze precipitazioni
    conteggio_primavera_prcp = len(df_primavera[(df_primavera['precipitazioni'] < 2) | (df_primavera['precipitazioni'] > 4)])
    conteggio_estate_prcp = len(df_estate[(df_estate['precipitazioni'] < 2) | (df_estate['precipitazioni'] > 4)])
    conteggio_autunno_prcp = len(df_autunno[(df_autunno['precipitazioni'] < 2) | (df_autunno['precipitazioni'] > 4)])

    # Riduciamo la quantità del 10% per le stagioni che superano la soglia
    if conteggio_primavera_temp + conteggio_primavera_prcp > soglia_occorrenze:
        quantita_prevista *= 0.9

    if conteggio_estate_temp + conteggio_estate_prcp > soglia_occorrenze:
        quantita_prevista *= 0.9

    if conteggio_autunno_temp + conteggio_autunno_prcp > soglia_occorrenze:
        quantita_prevista *= 0.9

    return quantita_prevista

def generate_reason_primavera(start_date_millis):
    soglia_occorrenze = 20
    reason_primavera = "produzione ottimale"

    # Assumiamo che start_date_millis sia la tua data di inizio in millisecondi
    start_date = pd.to_datetime(start_date_millis, unit='ms')

    df_weather_by_date = get_weather_dataset_by_date(start_date)

    df_primavera = None

    for season in range(1, 5):
        start, end = get_season_dates(start_date.year, season)
        if season == 2:
            df_primavera = df_weather_by_date[(df_weather_by_date.index >= start) & (df_weather_by_date.index <= end)]

    # Conteggio delle occorrenze temperatura
    conteggio_primavera_temp = len(
        df_primavera[(df_primavera['temperatura_minima'] < 10) & (df_primavera['temperatura_massima'] > 15)])

    # Conteggio delle occorrenze precipitazioni
    conteggio_primavera_prcp = len(df_primavera[(df_primavera['precipitazioni'] < 2) | (df_primavera['precipitazioni'] > 4)])

    # Riduciamo la quantità del 10% per le stagioni che superano la soglia
    if conteggio_primavera_temp + conteggio_primavera_prcp > soglia_occorrenze:
        reason_primavera = "probabili danni germogli"

    return reason_primavera

def generate_reason_estate(start_date_millis):
    soglia_occorrenze = 20
    reason_estate = "produzione ottimale"

    # Assumiamo che start_date_millis sia la tua data di inizio in millisecondi
    start_date = pd.to_datetime(start_date_millis, unit='ms')

    df_weather_by_date = get_weather_dataset_by_date(start_date)

    df_estate = None

    for season in range(1, 5):
        start, end = get_season_dates(start_date.year, season)
        if season == 3:
            df_estate = df_weather_by_date[(df_weather_by_date.index >= start) & (df_weather_by_date.index <= end)]

    conteggio_estate_temp = len(
        df_estate[(df_estate['temperatura_minima'] < 25) & (df_estate['temperatura_massima'] > 35)])

    # Conteggio delle occorrenze precipitazioni
    conteggio_estate_prcp = len(df_estate[(df_estate['precipitazioni'] < 2) | (df_estate['precipitazioni'] > 4)])

    if conteggio_estate_temp + conteggio_estate_prcp > soglia_occorrenze:
        reason_estate = "probabile quantitá zuccheri negli acini compromessa"


    return reason_estate

def generate_reason_autunno(start_date_millis):
    soglia_occorrenze = 20
    reason_autunno = "produzione ottimale"

    # Assumiamo che start_date_millis sia la tua data di inizio in millisecondi
    start_date = pd.to_datetime(start_date_millis, unit='ms')

    df_weather_by_date = get_weather_dataset_by_date(start_date)

    df_autunno = None

    for season in range(1, 5):
        start, end = get_season_dates(start_date.year, season)
        if season == 3:
            df_autunno = df_weather_by_date[(df_weather_by_date.index >= start) & (df_weather_by_date.index <= end)]

    conteggio_autunno_temp = len(
        df_autunno[(df_autunno['temperatura_minima'] < 15) & (df_autunno['temperatura_massima'] > 25)])

    conteggio_autunno_prcp = len(df_autunno[(df_autunno['precipitazioni'] < 2) | (df_autunno['precipitazioni'] > 4)])

    if conteggio_autunno_temp + conteggio_autunno_prcp > soglia_occorrenze:
        reason_autunno = "probabile equilibrio zuccheri-aciditá compromesso"

    return reason_autunno

def get_id_by_variety(variety, id_varieta):
    return id_varieta[variety]

def generate_production_rows():
    path_progetto = "C:\\Users\\dld\\PycharmProjects\\project_work_dld"
    nome_file = "produzione.csv"
    percorso_completo = os.path.join(path_progetto, "assets", nome_file)

    # Definizione delle varietà e dei periodi di raccolta (semplificati)
    varieta = ["Pinot Grigio", "Chardonnay", "Syrah", "Cabernet Franc", "Sauvignon Blanc", "Merlot", "Nebbiolo", "Sangiovese", "Pinot Noir", "Cabernet Sauvignon"]
    periodi_raccolta = {
        "Pinot Grigio": (8, 9),
        "Chardonnay": (8, 10),
        "Syrah": (9, 11),
        "Cabernet Franc": (9, 11),
        "Sauvignon Blanc": (8, 9),
        "Merlot": (9, 11),
        "Nebbiolo": (10, 11),
        "Sangiovese": (9, 11),
        "Pinot Noir": (8, 10),
        "Cabernet Sauvignon": (9, 11)
    }

    id_varieta = {
        "Pinot Grigio": 1,
        "Chardonnay": 2,
        "Syrah": 3,
        "Cabernet Franc": 4,
        "Sauvignon Blanc": 5,
        "Merlot": 6,
        "Nebbiolo": 7,
        "Sangiovese": 7,
        "Pinot Noir": 9,
        "Cabernet Sauvignon": 10
    }

    def get_production_start_month (variety, all_variety):
        anno = random.randint(2023, 2024)
        mese_inizio, mese_fine = all_variety[variety]
        inizio = int(pd.Timestamp(f"{anno}-{mese_inizio}-01").timestamp() * 1000)
        fine = int(pd.Timestamp(f"{anno}-{mese_inizio}-30").timestamp() * 1000)
        return random.randint(inizio, fine)

    def get_production_end_month (variety, all_variety, data_inizio):
        anno = pd.to_datetime(data_inizio, unit='ms').year
        mese_inizio, mese_fine = all_variety[variety]
        inizio = int(pd.Timestamp(f"{anno}-{mese_fine}-01").timestamp() * 1000)
        fine = int(pd.Timestamp(f"{anno}-{mese_fine}-30").timestamp() * 1000)
        return random.randint(inizio, fine)

    # Creazione del DataFrame
    df = pd.DataFrame({
        'ID': range(1, 1001),
        'varieta': np.random.choice(varieta, size=1000),
    })

    # Applicazione delle funzioni a ogni riga
    df['id_vigneto'] = df.apply(lambda row: get_id_by_variety(row['varieta'], id_varieta), axis=1)
    df['data_inizio'] = df.apply(lambda row: get_production_start_month(row['varieta'], periodi_raccolta), axis=1)
    df['data_fine'] = df.apply(lambda row: get_production_end_month(row['varieta'], periodi_raccolta, row['data_inizio']), axis=1)

    # Funzione per generare costi di produzione più realistici (con variazioni in base alla varietà)
    def genera_costo_produzione(varieta_vino, quantita):
        # Costi base per varietà (semplificati)
        costi_base = {
            "Pinot Grigio": 1.5,  # Varietà spesso coltivata in grandi volumi, costo medio
            "Chardonnay": 1.8,  # Versatilità e domanda elevata
            "Syrah": 2.2,  # Spesso utilizzata per vini di alta qualità, costo più elevato
            "Cabernet Franc": 2.0,  # Qualità e versatilità
            "Sauvignon Blanc": 1.6,  # Popolarità e resa generalmente buona
            "Merlot": 1.9,  # Versatilità e diffusione
            "Nebbiolo": 2.5,  # Bassa resa, vini pregiati, costo elevato
            "Sangiovese": 1.8,  # Varietà molto diffusa in Italia, costo medio
            "Pinot Noir": 2.3,  # Bassa resa, vini pregiati, costo elevato
            "Cabernet Sauvignon": 2.1,  # Varietà molto apprezzata, costo medio-alto
            "Barbera": 1.7,  # Varietà molto diffusa in Piemonte
            "Tempranillo": 1.9,  # Varietà spagnola molto versatile
            "Grenache": 1.8,  # Varietà utilizzata in molti blend
            "Riesling": 2.0,  # Varietà aromatica, spesso coltivata in climi freschi
            "Pinot Bianco": 1.6,  # Varietà spesso utilizzata per vini base e spumanti
        }
        costo_base = costi_base.get(varieta_vino, 2)  # Valore di default se la varietà non è presente

        return round(costo_base * quantita * (1 + np.random.normal(0, 0.1)), 2)

    df['quantita_prodotta_prevista'] = np.random.randint(500, 2000, size=len(df))
    df['quantia_prodotta_effettiva'] = df.apply(lambda row: generate_production_quantity_by_weather(row['quantita_prodotta_prevista'], row['data_inizio'], ), axis=1)
    df['reason_primavera'] = df.apply(lambda row: generate_reason_primavera(row['data_inizio'], ), axis=1)
    df['reason_estate'] = df.apply(lambda row: generate_reason_estate(row['data_inizio'], ), axis=1)
    df['reason_autunno'] = df.apply(lambda row: generate_reason_autunno(row['data_inizio'], ), axis=1)
    df['qualita'] = np.random.randint(70, 100, size=len(df))
    df['costo_totale_produzione'] = df.apply(lambda row: genera_costo_produzione(row['varieta'], row['quantia_prodotta_effettiva'], ), axis=1)
    df['consumi_acqua'] = np.random.randint(1000, 5000, size=len(df))  # Adattare l'intervallo in base ai tuoi dati
    df['consumi_energia'] = np.random.randint(500, 2000, size=len(df))  # Adattare l'intervallo in base ai tuoi dati
    df['litri_vino'] = df['quantia_prodotta_effettiva'] * 0.75  # Assumendo una resa media di 0.75 litri per kg
    df['bottiglie_prodotte'] = (df['litri_vino'] / 0.75).astype(int)

    # Salvataggio del DataFrame come CSV
    df.to_csv(percorso_completo, index=False)

def generate_orders():
    path_progetto = "C:\\Users\\dld\\PycharmProjects\\project_work_dld"
    nome_file = "ordini.csv"
    percorso_completo = os.path.join(path_progetto, "assets", nome_file)

    # Funzione per generare un numero di telefono casuale (esempio per l'Italia)
    def genera_telefono():
        return f"3{np.random.randint(300, 900)}-{' '.join(str(np.random.randint(0, 10)) for _ in range(7))}"

    # Creazione del DataFrame
    num_ordini = 1000  # Numero di ordini da generare

    def genera_timestamp():
        anno = random.randint(2023, 2024)
        inizio_anno = int(pd.Timestamp(f"{anno}-01-01").timestamp() * 1000)
        fine_anno = int(pd.Timestamp(f"{anno}-12-31").timestamp() * 1000)
        return random.randint(inizio_anno, fine_anno)

    df = pd.DataFrame({
        'ID': range(1, num_ordini + 1),
        'data_ordine': [genera_timestamp() for _ in range(num_ordini)],
        'id_cliente': np.random.randint(1, 100, size=num_ordini),
        'nome_cliente': np.random.choice(['Mario', 'Anna', 'Luca'], size=num_ordini),
        'cognome_cliente': np.random.choice(['Rossi', 'Verdi', 'Bianchi'], size=num_ordini),
        'telefono_cliente': [genera_telefono() for _ in range(num_ordini)],
        'quantita': np.random.randint(1, 10, size=num_ordini),
        'stato_ordine': np.random.choice(['In elaborazione', 'Spedito', 'Consegnato', 'Cancellato'], size=num_ordini),
        'prezzo_totale': np.random.randint(50, 500, size=num_ordini)
    })

    grouped = df.groupby(['nome_cliente', 'cognome_cliente'])

    df['id_cliente'] = grouped.ngroup() + 1

    # Salvataggio del DataFrame come CSV
    df.to_csv(percorso_completo, index=False)

def filter_prod_dataset_by_date_range(start_date, end_date):
    if start_date is not None and end_date is not None:
        timestamp_start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
        timestamp_end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

        # Conversione dei formati in datetime
        production_dataset['data_inizio'] = pd.to_datetime(production_dataset['data_inizio'], unit='ms')

        # Creazione della maschera
        production_mask = ((production_dataset['data_inizio'] >= timestamp_start_date) & (production_dataset['data_inizio'] <= timestamp_end_date)
                           # | (production_dataset['data_fine'] >= timestamp_start_date) & (production_dataset['data_fine'] <= timestamp_end_date)
                           )

        # Applicazione della maschera
        return production_dataset[production_mask]

    return production_dataset

def filter_orders_dataset_by_date_range(start_date, end_date):
    if start_date is not None and end_date is not None:
        timestamp_start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
        timestamp_end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

        # Conversione dei formati in datetime
        orders_dataset['data_ordine'] = pd.to_datetime(orders_dataset['data_ordine'], unit='ms')

        # Creazione della maschera
        orders_mask = (orders_dataset['data_ordine'] >= timestamp_start_date) & (orders_dataset['data_ordine'] <= timestamp_end_date)

        # Applicazione della maschera
        return orders_dataset[orders_mask]

    return orders_dataset

def get_home():
    #generate_production_rows()
    #generate_orders()
    #generate_weather_conditions_2023_2024()

    @callback(
        Output('system_performances', 'children'),
        Output('varieties_performances', 'children'),
        Output('vineyards_performances', 'children'),
        Output('orders_performances', 'children'),
        Output('produced-quantity-graph', 'children'),
        Output('temp-graph', 'children'),
        Output('prcp-graph', 'children'),
        Output('prods', 'children'),
        Output('prods-yield', 'children'),
        Output('ordrs', 'children'),
        Input('reset_filters', 'n_clicks'),
        Input('date-picker-range-filter', 'start_date'),
        Input('date-picker-range-filter', 'end_date'),
    )
    def filter_dataset(n_clicks, start_date, end_date):
        if n_clicks is not None and n_clicks > global_variables['clicked_times']:
            global_variables['clicked_times'] = n_clicks

            # Reset filter logic
            filtered_production_dataset = production_dataset
            filtered_orders_dataset = orders_dataset
            filtered_weather_dataset = weather_conditions_dataset
        else:
            start = start_date
            end = end_date

            filtered_production_dataset = filter_prod_dataset_by_date_range(start_date, end_date)
            filtered_orders_dataset = filter_orders_dataset_by_date_range(start_date, end_date)

            if start is None:
                start = pd.Timestamp("2023-01-01")
            if end_date is None:
                end = pd.Timestamp("2024-12-30")

            filtered_weather_dataset = get_filtered_weather(pd.Timestamp(start), pd.Timestamp(end))

        return (
            home_performances_section(
                "Performance del sistema",
                get_global_performances_cards(
                    production_dataset=filtered_production_dataset,
                    orders_dataset=filtered_orders_dataset,
                    workers_dataset=workers_dataset,
                    machinery_dataset=machinery_dataset
                )
            ),
            home_section("Varietá e produzione",
                         table_performances_variety(
                             order_icon,
                             production_dataset=filtered_production_dataset,
                             vineyard_dataset=vineyards_dataset
                         )
            ),
            home_section("Vigneti e produzione",
                         table_performances_vineyards(
                             order_icon,
                             production_dataset=filtered_production_dataset,
                             vineyard_dataset=vineyards_dataset
                         )
            ),
            home_section("Vendite e ordini per cliente",
                         table_performances_sell_orders(
                             order_icon,
                             orders_dataset=filtered_orders_dataset
                         )
            ),
            home_section("Andamento produzione (previsto - effettivo) per produzione",
                         dcc.Graph(figure={'data': [
                             {'x': filtered_production_dataset['ID'], 'y': filtered_production_dataset['quantita_prodotta_prevista'], 'type': 'line', 'name': 'Previsto'},
                             {'x': filtered_production_dataset['ID'], 'y': filtered_production_dataset['quantia_prodotta_effettiva'], 'type': 'line', 'name': 'Effettivo'}
                         ],
                             'layout': {
                                 'xaxis': {'title': 'ID Prodotto'},  # Titolo asse x
                                 'yaxis': {'title': 'Quantità Prodotta'}  # Titolo asse y
                             }
                         })
            ),
            home_section("Andamento delle temperature nel tempo",
                         dcc.Graph(figure=plot_data_temp(filtered_weather_dataset,['temperatura_minima', 'temperatura_massima'])),
            ),
            home_section("Andamento delle precipitazioni nel tempo",
                         dcc.Graph(figure=plot_data_prcp(filtered_weather_dataset, ['precipitazioni']))
            ),
            home_section("Produzioni",
                         table_in_row_production(production_dataset=filtered_production_dataset)
                         if production_dataset.shape[0] > 0
                         else html.H5(["Nessun dato disponibile per il periodo selezionato"],
                                      style={'color': '#365185', 'margin': '32px'})
            ),
            home_section("Produzioni - resa raccolti",
                         table_in_row_production_yield(production_dataset=filtered_production_dataset)
                         if filtered_production_dataset.shape[0] > 0
                         else html.H5(["Nessun dato disponibile per il periodo selezionato"], style={'color': '#365185', 'margin': '32px'})
            ),
            home_section("Ordini",
                         table_in_row_orders(orders_dataset=filtered_orders_dataset)
                         if filtered_orders_dataset.shape[0] > 0
                         else html.H5(["Nessun dato disponibile per il periodo selezionato"], style={'color': '#365185', 'margin': '32px'})
            ),
        )

    production_dataset['data_inizio'] = pd.to_datetime(production_dataset['data_inizio'], unit='ms')
    production_dataset['data_fine'] = pd.to_datetime(production_dataset['data_fine'], unit='ms')

    # componenti dashboard
    return html.Div([
        elevated_bar(
            dbc.Container([
                html.H3(
                    "Dashboard",
                    className="sideHeadText",
                    style={'color': '#365185'}
                ),
                dbc.Container([
                    dcc.DatePickerRange(
                        id='date-picker-range-filter',
                        min_date_allowed=date(2023, 1, 31),
                        max_date_allowed=date(2030, 12, 31),
                        initial_visible_month=date(today().year, today().month, today().day),
                        end_date=date(today().year, today().month, today().day),
                        display_format='DD-MM-YYYY'
                    ),
                    html.Div(id='output-container-date-picker-range', style={'cursor': 'pointer'}),
                    html.Img(src=reset_filters_icon, id='reset_filters',
                             style={'width': '30px', 'height': '30px', 'margin-top': '12px', 'margin-left': '12px',
                                    'cursor': 'pointer'}),
                ], style={'align-content': 'center', 'display': 'flex', 'margin-top': '12px'}),
            ], style={'display': 'flex'}),
            dash.get_asset_url('ic_dashboard.png')
        ),

        dbc.Container([
            home_performances_section(
                "Performance del sistema",
                get_global_performances_cards(
                    production_dataset=production_dataset,
                    orders_dataset=orders_dataset,
                    workers_dataset = workers_dataset,
                    machinery_dataset = machinery_dataset
                )
            ),
        ], id='system_performances'),
        dbc.Container([
            home_section("Andamento produzione (previsto - effettivo) per produzione",
                         dcc.Graph(figure={'data': [
                             {'x': production_dataset['ID'], 'y': production_dataset['quantita_prodotta_prevista'], 'type': 'line', 'name': 'Previsto'},
                             {'x': production_dataset['ID'], 'y': production_dataset['quantia_prodotta_effettiva'], 'type': 'line', 'name': 'Effettivo'}
                         ],
                             'layout': {
                                 'xaxis': {'title': 'ID Prodotto'},  # Titolo asse x
                                 'yaxis': {'title': 'Quantità Prodotta'}  # Titolo asse y
                             }
                         }),
            )
        ], id='produced-quantity-graph'),
        dbc.Container([
            home_section("Andamento delle temperature nel tempo",
                         dcc.Graph(figure=plot_data_temp(weather_conditions_dataset, ['temperatura_minima', 'temperatura_massima'])),
            )
        ], id='temp-graph'),
        dbc.Container([
            home_section("Andamento delle precipitazioni nel tempo",
                         dcc.Graph(figure=plot_data_prcp(weather_conditions_dataset, ['precipitazioni']))
            )
        ], id='prcp-graph'),
        dbc.Container([
            home_section("Produzioni",
                         table_in_row_production(production_dataset=production_dataset)
                         if production_dataset.shape[0] > 0
                         else html.H5(["Nessun dato disponibile per il periodo selezionato"], style={'color': '#365185', 'margin': '32px'})
            )
        ], id='prods'),
        dbc.Container([
            home_section("Produzioni - resa raccolti",
                         table_in_row_production_yield(production_dataset=production_dataset)
                         if production_dataset.shape[0] > 0
                         else html.H5(["Nessun dato disponibile per il periodo selezionato"], style={'color': '#365185', 'margin': '32px'})
            ),
        ], id='prods-yield'),
        dbc.Container([
            home_section("Ordini",
                         table_in_row_orders(orders_dataset=orders_dataset)
                         if orders_dataset.shape[0] > 0
                         else html.H5(["Nessun dato disponibile per il periodo selezionato"], style={'color': '#365185', 'margin': '32px'})
                         ),
        ], id='ordrs'),
        dbc.Container([
            home_section("Varietá e produzione",
                         table_performances_variety(
                             order_icon,
                             production_dataset=production_dataset,
                             vineyard_dataset=vineyards_dataset
                         )
            )
        ], id= 'varieties_performances'),
        dbc.Container([
            home_section("Vigneti e produzione",
                         table_performances_vineyards(
                             order_icon,
                             production_dataset=production_dataset,
                             vineyard_dataset=vineyards_dataset
                         )
            )
        ], id= 'vineyards_performances'),
        dbc.Container([
            home_section("Vendite e ordini",
                         table_performances_sell_orders(
                             order_icon,
                             orders_dataset=orders_dataset
                         )
            )
        ], id= 'orders_performances'),
        dbc.Container([
            home_section("Lavoratori", table_in_row_workers(
                workers_dataset=workers_dataset
            )),
        ], className='inRowTables'),
        dbc.Container([
            home_section("Macchine", table_in_row_machinery(
                machinery_dataset=machinery_dataset
            )),
        ], className='inRowTables'),
        home_section("Vigneti",
                     table_in_row_vineyards(
                         vineyards_dataset=vineyards_dataset
                     ))
    ], className='side')

layout = get_home()
