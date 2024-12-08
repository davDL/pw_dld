import dash
import dash_bootstrap_components as dbc
from common_components import performance_card

def get_global_performances_cards(production_dataset, orders_dataset, workers_dataset, machinery_dataset):
    production_dataset_count = production_dataset.shape[0]
    orders_dataset_count = orders_dataset.shape[0]

    #init variables
    avg_spent = 0.0
    produced_quantity = 0.0
    avg_by_client = 0.0
    machinery_efficiency = 0.0
    workers_efficiency = 0.0
    energy_consumption = 0.0

    if production_dataset_count != 0:
        # Produzione totale:
        # Formula: (Sommatoria della quantità prodotta)
        produced_quantity = production_dataset['quantia_prodotta_effettiva'].sum()

        # Ricavo medio per cliente:
        # Formula: (Valore totale delle vendite) / (Numero di clienti unici)
        # Seleziona le colonne di interesse
        new_orders_dataset = orders_dataset[['id_cliente', 'nome_cliente', 'cognome_cliente', 'telefono_cliente']]
        # Rimuovi i duplicati basati sulla colonna 'id_cliente'
        clienti_unici_count = new_orders_dataset.drop_duplicates(subset='id_cliente').shape[0]

        avg_by_client = orders_dataset['prezzo_totale'].sum() // clienti_unici_count

        # Efficienza oraria dei macchinari:
        # Formula: (Quantità prodotta) / (Ore di lavoro totali dei macchinari)
        machinery_efficiency = machinery_dataset['quantita_prodotta'].sum() / machinery_dataset['ore_lavoro'].sum()

        # Efficienza oraria dei lavoratori:
        # Formula: (Quantità prodotta) / (Ore di lavoro totali dei lavoratori)
        filtered_workers_dataset = workers_dataset[(workers_dataset['ruolo'] == 'viticoltore') | (workers_dataset['ruolo'] == 'imbottigliatore')]
        workers_efficiency = filtered_workers_dataset['quantita_prodotta'].sum() / filtered_workers_dataset['ore_lavoro'].sum()

        # Intensità energetica:
        # Formula: Energia_consumata / Quantità_prodotta
        energy_consumption = production_dataset['consumi_energia'].sum() / production_dataset['quantia_prodotta_effettiva'].sum()

        if orders_dataset_count != 0 and production_dataset_count != 0:
            # Valore medio del carrello:
            # Formula: (Valore totale degli ordini) / (Numero di ordini)
            avg_spent = orders_dataset['prezzo_totale'].sum() // orders_dataset_count


    return dbc.Container([
        dbc.Container([
            performance_card("Produzione",
                             '{value} kg'.format(value=int(produced_quantity)),
                             "nel periodo",
                             "cardBase purple",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Valore medio del carrello",
                             '{value} €'.format(value=int(avg_spent)),
                             "nel periodo",
                             "cardBase pink",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Ricavo medio per cliente",
                             '{value} €'.format(value=int(avg_by_client)),
                             "nel periodo",
                             "cardBase orange",
                             dash.get_asset_url('ic_service_level.png')),
        ], className="alignCenterContainer"),
        dbc.Container([
            performance_card("Efficienza oraria dei macchinari",
                             '{value} kg/h'.format(value=machinery_efficiency.round(3) if machinery_efficiency != 0.0 else 0.0),
                             "nel periodo",
                             "cardBase blue",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Efficienza oraria dei lavoratori",
                             '{value} Kg/h'.format(value=workers_efficiency.round(3) if workers_efficiency != 0.0 else 0.0),
                             "nel periodo",
                             "cardBase lightViolet",
                             dash.get_asset_url('ic_service_level.png')),
            performance_card("Intensità energetica media/Kg",
                             '{value} kW/h'.format(value=energy_consumption.round(3) if energy_consumption != 0.0 else 0.0),
                             "nel periodo",
                             "cardBase violet",
                             dash.get_asset_url('ic_service_level.png')),
        ], className="alignCenterContainer")
    ], style={'overflow-x': 'auto'})
