import pandas as pd
import dash
import common_utils
from dash import html, Output, Input, callback
import dash_bootstrap_components as dbc
from common_components import text_table_cell, text_table_cell_header, image_table_cell_header, image_table_cell, table_action_button

dash.register_page(__name__)
agents_data = pd.read_csv("assets/dataset_contact_center.csv", sep = ';')
clean_agents_data = agents_data.drop_duplicates(subset=['user_id'])[agents_data['user_id'].notnull()][agents_data['user_name'].notnull()]

profile_image = dash.get_asset_url('ic_placeholder_profile.png')

page_size = 50

def agent_table_row(row, actions):
    return html.Tr([
        image_table_cell(profile_image),
        text_table_cell(row.get("user_id")),
        text_table_cell(row.get("talkdesk_phone_display_name")),
        text_table_cell(row.get("user_name")),
        text_table_cell(row.get("talkdesk_phone_number")),
        #html.Td(actions)
    ], style={'height': '51px', 'width': '50px'})

def generate_table_rows_from_dataframe(dataset, actions):
    table_row_list = []
    for index, row in dataset.iterrows():
        table_row_list.append(agent_table_row(row, actions))
    return table_row_list

def get_table_agents (dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                image_table_cell_header(profile_image),
                text_table_cell_header("Id"),
                text_table_cell_header("Nome azienda"),
                text_table_cell_header("Nome e Cognome"),
                text_table_cell_header("Telefono"),
                #text_table_cell_header("Azioni")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    actions = dbc.Container([
        table_action_button(dash.get_asset_url('ic_edit_table.png'), "success", '#4fc971'),
        table_action_button(dash.get_asset_url('ic_info_table.png'), "info", '#27bcf1'),
        table_action_button(dash.get_asset_url('ic_cancel_table.png'), "danger", '#fe534d')
    ])

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(agent_table_row(row, actions))
        counter += 1


    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table

@callback(
    Output('agents-table-detail', 'children'),
    Input('agents-pagination-detail', 'active_page'),
)
def update_list_scores(page):
    # convert active_page data to integer and set default value to 1
    int_page = 1 if not page else int(page)

    # define filter index range based on active page
    filter_index_1 = (int_page - 1) * page_size
    filter_index_2 = int_page * page_size

    # get data by filter range based on active page number
    filtered_agents = clean_agents_data[filter_index_1:filter_index_2]

    # load data to dash bootstrap table component
    table = get_table_agents(filtered_agents, (filter_index_1 + 1))

    return table


content = dbc.Container([
        html.Div([
            html.H5(["Elenco degli agenti"], style={'color': '#365185', 'margin-top':'32px'}),
            # html.Div([
            #     dbc.Container([
            #         html.Img(src=add_icon, style={'width': '15px', 'height': '15px'})
            #     ], style={'background-color': '#365185', 'width': '30px', 'height': '31px', 'border-top-left-radius': '20px', 'border-bottom-left-radius': '20px', 'display': 'flex','justify-content': 'center', 'align-items': 'center'}),
            #     dbc.Container([
            #         "Aggiungi agente"
            #     ], style={'color': '#ffffff', 'background-color': '#365185', 'height': '31px', 'border-top-right-radius': '20px', 'border-bottom-right-radius': '20px', 'text-align': 'center', 'padding-top': '2px'})
            # ], style={'background-color': 'white', 'display': 'flex', 'flex-direction': 'row', 'align-self': 'flex-start', 'border-radius': '20px', 'border': '0.3mm solid #dee2e6'})
        ]),
        dbc.Table(id='agents-table-detail', style={'width':'1270px', 'margin':'16px'}),
        dbc.Pagination(id='agents-pagination-detail', max_value=common_utils.get_total_page(page_size, clean_agents_data.shape[0]), previous_next=True, fully_expanded=False, style={'padding-right':'20px', 'padding-bottom': '20px', 'align-self': 'flex-end'}),
    ], style={'display': 'flex', 'flex-direction': 'column'})

layout = html.Div([
    html.Div([
        content
    ]),
], className='side', style={'justify-content': 'space-between'})