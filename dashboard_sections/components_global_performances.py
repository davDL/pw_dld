import dash
import dash_bootstrap_components as dbc
from common_components import  performance_card

    # •	Livello di servizio: Misurato in base alla % di soddisfazione cliente ed alla % di chiamate con tempi inferiori al tempo medio di attesa
	# •	Soddisfazione del cliente: Percentuale delle chiamate valutate con esito positivo sul totale di quelle gestite.
	# •	Tempo medio della gestione: Rapporto tra la somma dei tempi di gestione delle chiamate ed il numero totale delle chiamate.
	# •	Tasso di abbandono: indice di interruzione delle chiamate Percentuale delle chiamate che vengono abbandonate sul totale di quelle gestite.
	# •	Tempo medio di attesa: Rapporto tra la somma dei tempi di attesa delle chiamate ed il numero totale delle chiamate.
	# •	Chiamate che superano la durata media: Percentuale delle che eccedono la durata media sul totale di quelle gestite.

# soddisfazione del cliente : cercarlo in conversation_dataset ed estrarre tutti gli interactionId che hanno come User Id user_id,
# cercare la corrispondenza di interactionId in survey_dataset e dalla riga corrispondente a interventionId (filtrare le righe con Exit Name diverso da 1 e 2), delle righe
# risultare fare il conteggio di quelle con esito positivo e fare il rapporto con le righe totali trovate
def get_client_satisfaction(conversation_dataset, survey_dataset):
    total_interaction_by_user = 0
    user_interaction_ids = conversation_dataset.drop_duplicates(subset=['Interaction Id'])["Interaction Id"]
    for interaction_id in user_interaction_ids.items():
        interactions = survey_dataset[survey_dataset['Interaction Id'] == interaction_id[1]]
        positive_interactions = interactions[interactions["Exit Name"] == '1']
        total_interaction_by_user += positive_interactions.shape[0]

    return (total_interaction_by_user / user_interaction_ids.shape[0]) * 100

# livello di servizio progress : get_client_satisfaction(survey_dataset) in rapporto con la somma del campo wait_time di tutte le
# righe che hanno user_id uguale a quello della row (contact_center_dataset)
def get_service_label(conversation_dataset, total_conversations, avg_duration, client_satisfaction):
    # percentuale di chiamate con durata superiore a quella media
    below_avg_duration_percentage = (
            (conversation_dataset[conversation_dataset['Duration'].astype(int) > avg_duration].shape[0] / total_conversations) * 100)

    return (client_satisfaction / below_avg_duration_percentage) * 100

# tempo medio di gestione
def get_handle_time_minutes(conversation_dataset, total_conversations):
    return (conversation_dataset['Handle Time'].sum() // 60) // total_conversations

# tasso di abbandono : in conversazion_dataset
def get_total_abandon_time(conversation_dataset, total_conversations):
    # righe con Abandon time non nullo
    total_abandon_time = conversation_dataset[conversation_dataset['Abandon Time'].notnull()]
    # percentuale delle chiamate abbandonate
    return(total_abandon_time.shape[0] / total_conversations) * 100

# tempo medio di attesa
def get_wait_time_minutes(conversation_dataset):
    return (conversation_dataset['Wait Time'].sum() // 60) // conversation_dataset.shape[0]

# chiamate oltre la durata media
def get_above_avg_duration_percentage(conversation_dataset, avg_duration, total_conversations):
    # percentuale di chiamate con durata superiore a quella media
    return (conversation_dataset[conversation_dataset['Duration'].astype(int) > avg_duration].shape[0] / total_conversations) * 100

def get_global_performances_cards(survey_dataset, conversation_dataset):
    # numero totale delle conversazioni dell'utente
    total_conversations = conversation_dataset.shape[0]

    if total_conversations == 0:
        return None

    client_satisfaction = get_client_satisfaction(conversation_dataset, survey_dataset)

    # calcolo della durata media della conversazione
    avg_duration = conversation_dataset['Duration'].sum() // total_conversations

    service_level = get_service_label(conversation_dataset, total_conversations, avg_duration, client_satisfaction)

    return dbc.Container([
    dbc.Container([
        performance_card("Livello di servizio",
                         '{value}%'.format(value=int(service_level)),
                         "Assistenza RAPIDA ed EFFICACE",
                         "cardBase purple",
                         dash.get_asset_url('ic_service_level.png')
                         ),
        performance_card("Soddisfazione del cliente",
                         '{value}%'.format(value=int(client_satisfaction)),
                         "Contentezza dei clienti",
                         "cardBase pink",
                         dash.get_asset_url('ic_satisfaction.png')
                         ),
        performance_card("Tempo medio di gestione",
                         '{value} min'.format(value=int(get_handle_time_minutes(conversation_dataset, total_conversations))),
                         "Tempo medio di richieste dei clienti",
                         "cardBase orange",
                         dash.get_asset_url('ic_avg_manage_time.png')
                         ),
    ], className="alignCenterContainer"),
    dbc.Container([
        performance_card("Tasso di abbandono",
                         '{value}%'.format(value=int(get_total_abandon_time(conversation_dataset, total_conversations))),
                         "Indice di interruzione delle chiamate",
                         "cardBase blue",
                         dash.get_asset_url('ic_leave_rate.png')),
        performance_card("Tempo medio di attesa",
                         '{value} min'.format(value=int(get_wait_time_minutes(conversation_dataset))),
                         "Tempi di attesa di assistenza",
                         "cardBase lightViolet",
                         dash.get_asset_url('ic_avg_wait_time.png')),
        performance_card("Chiamate che superano la media",
                         '{value}%'.format(value=int(get_above_avg_duration_percentage(conversation_dataset, avg_duration, total_conversations))),
                         "Chiamate che superano la durata media",
                         "cardBase violet",
                         dash.get_asset_url('ic_above_avg_calls.png')),
    ], className="alignCenterContainer"),
])