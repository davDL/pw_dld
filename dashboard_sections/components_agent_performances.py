from dash import html
import dash_bootstrap_components as dbc
import common_utils
from common_components import text_table_cell, text_table_cell_header, progress_table_cell, image_table_cell, image_table_cell_header
import math

# soddisfazione del cliente : cercarlo in conversation_dataset ed estrarre tutti gli interactionId che hanno come User Id user_id,
# cercare la corrispondenza di interactionId in survey_dataset e dalla riga corrispondente a interventionId (filtrare le righe con Exit Name diverso da 1 e 2), delle righe
# risultare fare il conteggio di quelle con esito positivo e fare il rapporto con le righe totali trovate
def get_client_satisfaction(conversation_rows_by_user_id, survey_dataset):
    total_interaction_by_user = 0
    user_interaction_ids = conversation_rows_by_user_id.drop_duplicates(subset=['Interaction Id'])["Interaction Id"]
    for interaction_id in user_interaction_ids.items():
        interactions = survey_dataset[survey_dataset['Interaction Id'] == interaction_id[1]]
        positive_interactions = interactions[interactions["Exit Name"] == '1']
        total_interaction_by_user += positive_interactions.shape[0]

    return (total_interaction_by_user / user_interaction_ids.shape[0]) * 100

# livello di servizio progress : get_client_satisfaction(survey_dataset) in rapporto con la somma della somma della duration di tutte le
# righe che hanno duration inferiore alla durata media (contact_center_dataset)
def get_service_level_label (conversation_rows_by_user_id, total_conversations, avg_duration, client_satisfaction):
    below_avg_duration_percentage = (
            (conversation_rows_by_user_id[conversation_rows_by_user_id['Duration'].astype(int) < avg_duration].shape[0] / total_conversations) * 100)
    return (client_satisfaction / below_avg_duration_percentage) * 100

#tempo medio di gestione : in conversation_dataset
def get_avg_handle_time_label(conversation_rows_by_user_id, total_conversations):
    # tempo medio di gestione
    handle_time_minutes = (conversation_rows_by_user_id['Handle Time'].sum() // 60) // total_conversations
    return '{value} min'.format(value=int(handle_time_minutes))

#tempo medio di attesa : in conversation_dataset
def get_wait_time_label(conversation_rows_by_user_id):
    wait_time_minutes = (conversation_rows_by_user_id['Wait Time'].sum() // 60) // conversation_rows_by_user_id.shape[0]
    return '{value} min'.format(value=int(wait_time_minutes))

def get_above_avg_duration(conversation_rows_by_user_id, avg_duration, total_conversations):
    # percentuale di chiamate con durata superiore a quella media
    return  (conversation_rows_by_user_id[conversation_rows_by_user_id['Duration'].astype(int) > avg_duration].shape[0] / total_conversations) * 100

def performances_table_row (image, row, index, survey_dataset, conversation_dataset):
    color = common_utils.get_color_by_index(index)

    #tutte le righe conversazioni di un singolo utente (agente)
    conversation_rows_by_user_id = conversation_dataset[conversation_dataset["User Id"] == row.get("user_id")]

    #numero totale delle conversazioni dell'utente
    total_conversations = conversation_rows_by_user_id.shape[0]

    if total_conversations == 0:
        return None

    client_satisfaction = get_client_satisfaction(conversation_rows_by_user_id, survey_dataset)

    # calcolo della durata media
    avg_duration = conversation_rows_by_user_id['Duration'].sum() // total_conversations

    service_level = get_service_level_label(conversation_rows_by_user_id, total_conversations, avg_duration, client_satisfaction)

    return  html.Tr([
        image_table_cell(image),
        text_table_cell(row.get("user_name")),

        #livello di servizio progress
        progress_table_cell(service_level, color),

        #soddisfazione del cliente : per ogni riga prendere user_id, cercarlo in conversation_dataset ed estrarre tutti gli interactionId che hanno come User Id user_id,
        #cercare la corrispondenza di interactionId in survey_dataset e dalla riga corrispondente a interventionId (filtrare le righe con Exit Name diverso da 1 e 2), delle righe
        #risultare fare il conteggio di quelle con esito positivo e fare il rapporto con le righe totali trovate
        progress_table_cell(client_satisfaction, color),

        #tempo medio di gestione : in conversation_dataset
        text_table_cell(get_avg_handle_time_label(conversation_rows_by_user_id, total_conversations)),

        # con il dataset attuale non esistono dati di abbandono relativi agli agenti, è possibile effettuare solo la statistica globale
        #tasso di abbandono : in conversazion_dataset
        #progress_table_cell(abandon_percentage, color),

        #tempo medio di attesa : in conversation_dataset
        text_table_cell(get_wait_time_label(conversation_rows_by_user_id)),

        #chiamate oltre la media
        progress_table_cell(math.trunc(get_above_avg_duration(conversation_rows_by_user_id, avg_duration, total_conversations)), color),
    ])

def table_performances(image, search_icon, contact_center_dataset, survey_dataset, conversation_dataset):
    table_header = [
        html.Thead(
            html.Tr([
                image_table_cell_header(image),
                text_table_cell_header("Agente"),
                text_table_cell_header("Livello di servizio"),
                text_table_cell_header("Soddisfazione del cliente"),
                text_table_cell_header("Tempo medio di gestione"),
                #text_table_cell_header("Tasso di abbandono"),
                text_table_cell_header("Tempo medio di attesa"),
                text_table_cell_header("Chiamate oltre la media"),
            ])
        )
    ]

    clean_agents_data = contact_center_dataset.drop_duplicates(subset=['user_id'])[contact_center_dataset['user_id'].notnull()][contact_center_dataset['user_name'].notnull()]

    table_row_list = []
    for index, row in clean_agents_data.iterrows():
        performance_row = performances_table_row(image, row, index, survey_dataset, conversation_dataset)
        if performance_row is not None:
            table_row_list.append(performance_row)

    table_body = [html.Tbody(
        table_row_list
    )]

    return dbc.Container([
        html.Div([
            html.H5(["Indicatori di performance"], style={'color': '#365185'}),
            # html.Div([
            #     dbc.Input(size="sm", placeholder="Search...", type="text", style={'border': '0', 'border-radius': '20px'}),
            #     dbc.Container([
            #         html.Img(src=search_icon, style={'width': '15px', 'height': '15px'})
            #     ], style={'background-color': '#365185', 'width': '30px', 'height': '31px',
            #               'border-top-right-radius': '20px', 'border-bottom-right-radius': '20px', 'display': 'flex',
            #               'justify-content': 'center', 'align-items': 'center'})
            # ], style={'background-color': 'white', 'display': 'flex', 'flex-direction': 'row', 'align-self': 'flex-end',
            #           'border-radius': '20px', 'border': '0.3mm solid #dee2e6'})
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-bottom': '8px'}),
        dbc.Table(
            table_header + table_body,
            bordered=True,
            striped=True,
        )
    ])