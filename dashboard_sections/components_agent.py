from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
import common_utils
from common_components import text_table_cell, text_table_cell_header, text_table_cell_mid, image_table_cell, image_table_cell_header, table_action_button

# Agent:
# Profile img -> placeholder
# Id -> user_id
# Nome e Cognome -> user_name
# Telefono -> talkdesk_phone_number

def agent_table_row(profile_image, row, actions):
    return html.Tr([
        image_table_cell(profile_image),
        text_table_cell(row.get("user_id")),
        text_table_cell_mid(row.get("talkdesk_phone_display_name")),
        text_table_cell(row.get("user_name")),
        text_table_cell(row.get("talkdesk_phone_number")),
        #html.Td(actions, style={'display': 'block', 'overflow': 'auto', 'width' : '180px'})
    ], style={'height': '51px', 'width': '50px'})

def table_in_row_agents(profile_icon, edit_icon, info_icon, cancel_icon, add_icon, dataset):
    page_size = 5

    # create callback
    @callback(
        Output('agent-table', 'children'),
        Input('agent-pagination', 'active_page'),
    )
    def update_list_survey(page):
        # convert active_page data to integer and set default value to 1
        int_page = 1 if not page else int(page)

        # define filter index range based on active page
        filter_index_1 = (int_page - 1) * page_size
        filter_index_2 = int_page * page_size

        # get data by filter range based on active page number
        filter_agents = dataset[filter_index_1:filter_index_2]

        # load data to dash bootstrap table component
        table = get_table_in_row_agents(profile_icon, edit_icon, info_icon, cancel_icon, filter_agents, (filter_index_1 + 1))

        return table
    
    return dbc.Container([
        html.Div([
            html.H5(["Elenco degli agenti"], style={'color': '#365185'}),
            # html.Div([
            #     dbc.Container([
            #         html.Img(src=add_icon, style={'width': '15px', 'height': '15px'})
            #     ], style={'background-color': '#365185', 'width': '30px', 'height': '31px', 'border-top-left-radius': '20px', 'border-bottom-left-radius': '20px', 'display': 'flex','justify-content': 'center', 'align-items': 'center'}),
            #     dbc.Container([
            #         "Aggiungi agente"
            #     ], style={'color': '#ffffff', 'background-color': '#365185', 'height': '31px', 'border-top-right-radius': '20px', 'border-bottom-right-radius': '20px', 'text-align': 'center', 'padding-top': '2px'})
            # ], style={'background-color': 'white', 'display': 'flex', 'flex-direction': 'row', 'align-self': 'flex-start', 'border-radius': '20px', 'border': '0.3mm solid #dee2e6'})
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='agent-table', style={'min-height':'350px'}),
        dbc.Pagination(id = 'agent-pagination', max_value=common_utils.get_total_page(page_size, dataset.shape[0]), previous_next=True, fully_expanded=False, style={'padding-bottom':'20px', 'align-self':'flex-end'}),
    ], style={'display':'flex', 'flex-direction':'column'})

def get_table_in_row_agents (profile_icon, edit_icon, info_icon, cancel_icon, dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                image_table_cell_header(profile_icon),
                text_table_cell_header("Id"),
                text_table_cell_header("Nome azienda"),
                text_table_cell_header("Nome e Cognome"),
                text_table_cell_header("Telefono"),
                # text_table_cell_header("Azioni")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    actions = dbc.Container([
        table_action_button(edit_icon, "success", '#4fc971'),
        table_action_button(info_icon, "info", '#27bcf1'),
        table_action_button(cancel_icon, "danger", '#fe534d')
    ])

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(agent_table_row(profile_icon, row, actions))
        counter += 1


    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table