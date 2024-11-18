import dash
from dash import html, callback, Output, Input, dcc
import dash_bootstrap_components as dbc
from dateutil.utils import today
import numpy as np
import random
import pandas as pd
from datetime import date
import os
from dashboard_sections.registry_table_components import table_in_row_machinery, table_in_row_workers, table_in_row_vineyards, table_in_row_production, table_in_row_orders
from dashboard_sections.performance_table_components import table_performances_vineyards, table_performances_variety, table_performances_sell_orders
from common_components import home_performances_section, elevated_bar, home_section
from dashboard_sections.global_performances_components import get_global_performances_cards

dash.register_page(__name__, path='/')

workers_dataset = pd.read_csv("assets/lavoratori.csv", sep=',')
machinery_dataset = pd.read_csv("assets/macchinari.csv", sep=',')
vineyards_dataset = pd.read_csv("assets/vigneti.csv", sep=',')
production_dataset = pd.read_csv("assets/produzione.csv", sep=',')
orders_dataset = pd.read_csv("assets/ordini.csv", sep=',')

reset_filters_icon = dash.get_asset_url('ic_reset_filters.png')
order_icon = dash.get_asset_url('ic_arrow_down_black.png')

global_variables = {}
global_variables['clicked_times'] = 0

def generate_production_rows():
    # Funzione per generare un timestamp casuale all'interno di un anno
    def genera_timestamp():
        anno = random.randint(2023, 2024)
        inizio_anno = int(pd.Timestamp(f"{anno}-01-01").timestamp() * 1000)
        fine_anno = int(pd.Timestamp(f"{anno}-12-31").timestamp() * 1000)
        return random.randint(inizio_anno, fine_anno)

    path_progetto = "C:\\Users\\dld\\PycharmProjects\\project_work_dld"  # Sostituisci con il percorso esatto
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

    # Creazione del DataFrame
    df = pd.DataFrame({
        'ID': range(1, 1001),
        'data': [genera_timestamp() for _ in range(1000)],
        'id_vigneto': np.random.randint(1, 11, size=1000),
        'varieta': np.random.choice(varieta, size=1000)
    })

    # Funzione per verificare se la data di raccolta è coerente con la varietà
    def check_periodo_raccolta(row):
        if row['data'] is not None:
            mese = pd.to_datetime(row['data'], unit='ms').month
        else:
            # Gestisci il caso in cui row['data'] è None (es. assegna un valore di default, salta il record, ecc.)
            mese = None  # O un altro valore appropriato

        return mese in periodi_raccolta[row['varieta']]

    # Filtraggio dei dati in base al periodo di raccolta
    df = df[df.apply(check_periodo_raccolta, axis=1)]

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
        # Variazioni casuali sul costo base
        return round(costo_base * quantita * (1 + np.random.normal(0, 0.1)), 2)

    df['quantita_prodotta'] = np.random.randint(500, 2000, size=len(df))
    df['qualita'] = np.random.randint(70, 100, size=len(df))
    df['costo_totale_produzione'] = df.apply(lambda row: genera_costo_produzione(row['varieta'], row['quantita_prodotta']), axis=1)
    df['consumi_acqua'] = np.random.randint(1000, 5000, size=len(df))  # Adattare l'intervallo in base ai tuoi dati
    df['consumi_energia'] = np.random.randint(500, 2000, size=len(df))  # Adattare l'intervallo in base ai tuoi dati
    df['litri_vino'] = df['quantita_prodotta'] * 0.75  # Assumendo una resa media di 0.75 litri per kg
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

def filter_dataset_by_date_range(start_date, end_date):
    if start_date is not None and end_date is not None:
        timestamp_start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
        timestamp_end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

        # Conversione dei formati in datetime
        production_dataset['data'] = pd.to_datetime(production_dataset['data'], unit='ms')
        orders_dataset['data_ordine'] = pd.to_datetime(orders_dataset['data_ordine'], unit='ms')

        # Creazione della maschera
        production_mask = (production_dataset['data'] >= timestamp_start_date) & (production_dataset['data'] <= timestamp_end_date)
        orders_mask = (orders_dataset['data_ordine'] >= timestamp_start_date) & (orders_dataset['data_ordine'] <= timestamp_end_date)

        # Applicazione della maschera
        return production_dataset[production_mask], orders_dataset[orders_mask]

    return production_dataset, orders_dataset

def get_home():
    #generate_production_rows()
    #generate_orders()

    @callback(
        Output('system_performances', 'children'),
        Output('varieties_performances', 'children'),
        Output('vineyards_performances', 'children'),
        Output('orders_performances', 'children'),
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
        else:
            filtered_production_dataset, filtered_orders_dataset = filter_dataset_by_date_range(start_date, end_date)

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
            )
        )

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
        # tabelle agenti clienti affiancate
        dbc.Container([
            home_section("Macchine", table_in_row_machinery(
                machinery_dataset=machinery_dataset
            )),
            home_section("Lavoratori", table_in_row_workers(
                workers_dataset=workers_dataset
            )),
        ], className='inRowTables'),
        home_section("Vigneti",
                     table_in_row_vineyards(
                         vineyards_dataset=vineyards_dataset
                     )),
        home_section("Produzioni",
                     table_in_row_production(
                         production_dataset=production_dataset
                     )),
        home_section("Ordini",
                     table_in_row_orders(
                         orders_dataset=orders_dataset
                     )),
    ], className='side')

layout = get_home()
