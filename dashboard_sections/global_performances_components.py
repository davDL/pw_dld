import dash
import dash_bootstrap_components as dbc
from common_components import performance_card

def get_global_performances_cards(production_dataset, orders_dataset, workers_dataset, machinery_dataset):
    production_dataset_count = production_dataset.shape[0]
    orders_dataset_count = orders_dataset.shape[0]

    # Produzione media:
    # Formula: (Sommatoria della quantità prodotta) / (Numero di produzioni)
    avg_production = production_dataset['quantita_prodotta'].sum() // production_dataset_count

    # Valore medio del carrello:
    # Formula: (Valore totale degli ordini) / (Numero di ordini)
    avg_spent = orders_dataset['prezzo_totale'].sum() // orders_dataset_count

    # Ricavo medio per cliente:
    # Formula: (Valore totale delle vendite) / (Numero di clienti unici)
    # Seleziona le colonne di interesse
    new_orders_dataset = orders_dataset[['id_cliente', 'nome_cliente', 'cognome_cliente', 'telefono_cliente']]
    # Rimuovi i duplicati basati sulla colonna 'id_cliente'
    clienti_unici_count = new_orders_dataset.drop_duplicates(subset='id_cliente').shape[0]

    avg_by_client = orders_dataset['prezzo_totale'].sum() // clienti_unici_count

    # Efficienza oraria dei macchinari:
    # Formula: (Quantità prodotta) / (Ore di lavoro totali dei macchinari)
    machinery_efficiency = machinery_dataset['quantita_prodotta'].sum() // machinery_dataset['ore_lavoro'].sum()

    # Efficienza oraria dei lavoratori:
    # Formula: (Quantità prodotta) / (Ore di lavoro totali dei lavoratori)
    filtered_workers_dataset = workers_dataset[(workers_dataset['ruolo'] == 'viticoltore') | (workers_dataset['ruolo'] == 'imbottigliatore')]
    workers_efficiency = filtered_workers_dataset['quantita_prodotta'].sum() // filtered_workers_dataset['ore_lavoro'].sum()

    # Intensità energetica:
    # Formula: Energia_consumata / Quantità_prodotta
    energy_consumption = production_dataset['consumi_energia'].sum() // production_dataset['quantita_prodotta'].sum()

    # Intensità idrica:
    # Formula: Acqua_consumata / Quantità_prodotta
    water_consumption = production_dataset['consumi_acqua'].sum() // production_dataset['quantita_prodotta'].sum()


    return dbc.Container([
        dbc.Container([
            performance_card("Produzione media per varietà",
                             '{value} kg'.format(value=int(avg_production)),
                             "Assistenza RAPIDA ed EFFICACE",
                             "cardBase purple",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Valore medio del carrello",
                             '{value} €'.format(value=int(avg_spent)),
                             "Contentezza dei clienti",
                             "cardBase pink",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Ricavo medio per cliente",
                             '{value} €'.format(value=int(avg_by_client)),
                             "Tempo medio di richieste dei clienti",
                             "cardBase orange",
                             dash.get_asset_url('ic_service_level.png')),
        ], className="alignCenterContainer"),
        dbc.Container([
            performance_card("Efficienza oraria dei macchinari",
                             '{value} kg/h'.format(value=int(machinery_efficiency)),
                             "Indice di interruzione delle chiamate",
                             "cardBase blue",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Efficienza oraria dei lavoratori",
                             '{value} kg/h'.format(value=int(workers_efficiency)),
                             "Tempi di attesa di assistenza",
                             "cardBase lightViolet",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Intensità energetica",
                             '{value} kw/h'.format(value=int(energy_consumption)),
                             "Chiamate che superano la durata media",
                             "cardBase violet",
                             dash.get_asset_url('ic_service_level.png')),
        ], className="alignCenterContainer"),
        dbc.Container([
            performance_card("Intensità idrica",
                             '{value} l/h'.format(value=int(water_consumption)),
                             "Indice di interruzione delle chiamate",
                             "cardBase orange",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Temperatura media",
                             '{value} %'.format(value=int(1)),
                             "Indice di interruzione delle chiamate",
                             "cardBase purple",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Umiditá media",
                             '{value} %'.format(value=int(1)),
                             "Indice di interruzione delle chiamate",
                             "cardBase blue",
                             dash.get_asset_url('ic_service_level.png')),
        ], className="alignCenterContainer")
    ])
