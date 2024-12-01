import pandas as pd
from dash import html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import common_utils
from common_components import text_table_cell, text_table_cell_header, text_table_cell_mid

def machinery_table_row(row):
    return html.Tr([
        text_table_cell(row.get("ID")),
        text_table_cell_mid(row.get("tipologia")),
        text_table_cell(row.get("ore_lavoro")),
        text_table_cell(row.get("id_vigneto")),
        text_table_cell(row.get("quantita_prodotta"))
    ], style={'height': '51px', 'width': '50px'})

def table_in_row_machinery(machinery_dataset):
    page_size = 5

    # create callback
    @callback(
        Output('machinery-table', 'children'),
        Input('machinery-pagination', 'active_page'),
    )
    def update_list_machinery(page):
        # convert active_page data to integer and set default value to 1
        int_page = 1 if not page else int(page)

        # define filter index range based on active page
        filter_index_1 = (int_page - 1) * page_size
        filter_index_2 = int_page * page_size

        # get data by filter range based on active page number
        filter_dataset = machinery_dataset[filter_index_1:filter_index_2]

        # load data to dash bootstrap table component
        table = get_table_in_row_machinery(filter_dataset, (filter_index_1 + 1))

        return table
    
    return dbc.Container([
        html.Div([
            html.H5(["Elenco dei macchinari"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='machinery-table', style={'min-height':'350px'}),
        dbc.Pagination(id = 'machinery-pagination', max_value=common_utils.get_total_page(page_size, machinery_dataset.shape[0]), previous_next=True, fully_expanded=False, style={'padding-bottom':'20px', 'align-self':'flex-end'}),
    ], style={'display':'flex', 'flex-direction':'column'})

def get_table_in_row_machinery (dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Tipologia"),
                text_table_cell_header("Ore di lavoro (h)"),
                text_table_cell_header("Id vigneto"),
                text_table_cell_header("Quantitá prodotta (Kg)")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(machinery_table_row(row))
        counter += 1


    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table


def workers_table_row(row):
    return html.Tr([
        text_table_cell(row.get("ID")),
        text_table_cell_mid(row.get("nome")),
        text_table_cell(row.get("ruolo")),
        text_table_cell(row.get("ore_lavoro")),
        text_table_cell(row.get("id_vigneto")),
        text_table_cell(row.get("quantita_prodotta"))
    ], style={'height': '51px', 'width': '50px'})

def table_in_row_workers(workers_dataset):
    page_size = 5

    # create callback
    @callback(
        Output('workers-table', 'children'),
        Input('workers-pagination', 'active_page'),
    )
    def update_list_workers(page):
        # convert active_page data to integer and set default value to 1
        int_page = 1 if not page else int(page)

        # define filter index range based on active page
        filter_index_1 = (int_page - 1) * page_size
        filter_index_2 = int_page * page_size

        # get data by filter range based on active page number
        filter_dataset = workers_dataset[filter_index_1:filter_index_2]

        # load data to dash bootstrap table component
        table = get_table_in_row_workers(filter_dataset, (filter_index_1 + 1))

        return table

    return dbc.Container([
        html.Div([
            html.H5(["Elenco dei lavoratori"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='workers-table', style={'min-height': '350px'}),
        dbc.Pagination(id='workers-pagination', max_value=common_utils.get_total_page(page_size, workers_dataset.shape[0]),
                       previous_next=True, fully_expanded=False,
                       style={'padding-bottom': '20px', 'align-self': 'flex-end'}),
    ], style={'display': 'flex', 'flex-direction': 'column'})

def get_table_in_row_workers(dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Nome"),
                text_table_cell_header("Ruolo"),
                text_table_cell_header("Ore di lavoro (h)"),
                text_table_cell_header("Id vigneto"),
                text_table_cell_header("Quantitá prodotta (Kg)")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(workers_table_row(row))
        counter += 1

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table


def vineyards_table_row(row):
    return html.Tr([
        text_table_cell(row.get("ID")),
        text_table_cell_mid(row.get("superficie")),
        text_table_cell(row.get("nome_varieta_coltivata"))
    ], style={'height': '51px', 'width': '50px'})

def table_in_row_vineyards(vineyards_dataset):
    page_size = 5

    # create callback
    @callback(
        Output('vineyards-table', 'children'),
        Input('vineyards-pagination', 'active_page'),
    )
    def update_list_vineyards(page):
        # convert active_page data to integer and set default value to 1
        int_page = 1 if not page else int(page)

        # define filter index range based on active page
        filter_index_1 = (int_page - 1) * page_size
        filter_index_2 = int_page * page_size

        # get data by filter range based on active page number
        filter_dataset = vineyards_dataset[filter_index_1:filter_index_2]

        # load data to dash bootstrap table component
        table = get_table_in_row_vineyards(filter_dataset, (filter_index_1 + 1))

        return table

    return dbc.Container([
        html.Div([
            html.H5(["Elenco dei vigneti"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='vineyards-table', style={'min-height': '350px'}),
        dbc.Pagination(id='vineyards-pagination', max_value=common_utils.get_total_page(page_size, vineyards_dataset.shape[0]),
                       previous_next=True, fully_expanded=False,
                       style={'padding-bottom': '20px', 'align-self': 'flex-end'}),
    ], style={'display': 'flex', 'flex-direction': 'column'})

def get_table_in_row_vineyards(dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Superficie (ettari)"),
                text_table_cell_header("Nome varietá")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(vineyards_table_row(row))
        counter += 1

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table


def get_name_prod(c):
    match c:
        case "ID":
            return "Id"
        case "data_inizio":
            return "Data inizio"
        case "data_fine":
            return "Data fine"
        case "id_vigneto":
            return "Id vigneto"
        case "quantita_prodotta_prevista":
            return "Quantitá prevista(Kg)"
        case "quantia_prodotta_effettiva":
            return "Quantitá effettiva(Kg)"
        case "qualita":
            return "Qualitá"
        case "costo_totale_produzione":
            return "Costo totale produzione(€)"
        case "consumi_acqua":
            return "Consumi acqua(l)"
        case "consumi_energia":
            return "Consumi energia(kW/h)"
        case"litri_vino":
            return "Vino (l)"
        case "bottiglie_prodotte":
            return "Bottiglie prodotte"
        case _:
            return "column"

def table_in_row_production(production_dataset):
    columns = ['ID', 'data_inizio', 'data_fine', 'quantita_prodotta_prevista', 'quantia_prodotta_effettiva', 'qualita',
               'costo_totale_produzione', 'consumi_acqua', 'consumi_energia', 'litri_vino', 'bottiglie_prodotte']
    df_to_show = production_dataset[columns]

    df_to_show['data_inizio'] = pd.to_datetime(df_to_show['data_inizio'])
    df_to_show['data_fine'] = pd.to_datetime(df_to_show['data_fine'])

    # Formatta le date nel formato desiderato (GG-MM-AAAA)
    df_to_show['data_inizio'] = df_to_show['data_inizio'].dt.strftime('%d-%m-%Y')
    df_to_show['data_fine'] = df_to_show['data_fine'].dt.strftime('%d-%m-%Y')

    df_to_show['litri_vino'] = df_to_show['litri_vino'].round(2)
    df_to_show['quantia_prodotta_effettiva'] = df_to_show['quantia_prodotta_effettiva'].round(2)

    return dbc.Container([
        dash_table.DataTable(
            data=df_to_show.to_dict('records'),
            columns=[{'id': c, 'name': get_name_prod(c)} for c in df_to_show.columns],
            page_size=10,
            style_as_list_view=True,
            style_header={
                'font-weight': 'bold',
                'text-align': 'center',
                'font-family': 'Verdana',
                'font-size': '8pt',
                'overflow': 'hidden',
                'white-space': 'nowrap',
                'color': '#365185'
            },
            style_cell={
                'text-align': 'center',
                'font-family':'Verdana',
                'padding':'5px',
                'font-size':'8pt',
                'overflow':'hidden',
                'text-overflow':'ellipsis',
                'white-space':'nowrap',
                'color':'#365185'
            },style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f2f2f2'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'white'
                }
            ]
        )
    ], style={'display': 'flex', 'flex-direction': 'column', 'overflow-x': 'auto'})


def get_name_prod_yield(c):
    match c:
        case "ID":
            return "Id"
        case "id_vigneto":
            return "Id vigneto"
        case "varieta":
            return "Varietá"
        case "quantita_prodotta_prevista":
            return "Quantitá prevista(Kg)"
        case "quantia_prodotta_effettiva":
            return "Quantitá effettiva(Kg)"
        case "reason_primavera":
            return "Primavera"
        case "reason_estate":
            return "Estate"
        case "reason_autunno":
            return "Autunno"
        case _:
            return "column"

def table_in_row_production_yield(production_dataset):
    columns = ['ID', 'id_vigneto', 'varieta', 'quantita_prodotta_prevista',
               'quantia_prodotta_effettiva', 'reason_primavera', 'reason_estate', 'reason_autunno']
    df_to_show = production_dataset[columns]

    df_to_show.loc[:, 'quantia_prodotta_effettiva'] = df_to_show['quantia_prodotta_effettiva'].round(2)

    return dbc.Container([
        dash_table.DataTable(
            data=df_to_show.to_dict('records'),
            columns=[{'id': c, 'name': get_name_prod_yield(c)} for c in df_to_show.columns],
            page_size=10,
            style_as_list_view=True,
            style_header={
                'font-weight': 'bold',
                'text-align': 'center',
                'font-family': 'Verdana',
                'font-size': '8pt',
                'overflow': 'hidden',
                'white-space': 'nowrap',
                'color': '#365185'
            },
            style_cell={
                'text-align': 'center',
                'font-family': 'Verdana',
                'padding': '5px',
                'font-size': '8pt',
                'overflow': 'hidden',
                'text-overflow': 'ellipsis',
                'white-space': 'nowrap',
                'color': '#365185'
            }, style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f2f2f2'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'white'
                }
            ]
        )
    ], style={'display': 'flex', 'flex-direction': 'column', 'overflow-x': 'auto'})


def get_name_orders(c):
    match c:
        case "ID":
            return "Id"
        case "data_ordine":
            return "Data ordine"
        case "id_cliente":
            return "Id cliente"
        case "nome_cliente":
            return "Nome"
        case "cognome_cliente":
            return "Cognome"
        case "telefono_cliente":
            return "Telefono"
        case "quantita":
            return "Quantità ordinata"
        case "stato_ordine":
            return "Stato"
        case "prezzo_totale":
            return "Prezzo totale(€)"
        case _:
            return "column"

def table_in_row_orders(orders_dataset):
    columns = ['ID', 'data_ordine', 'id_cliente', 'nome_cliente', 'cognome_cliente',
               'telefono_cliente', 'quantita', 'stato_ordine', 'prezzo_totale']
    df_to_show = orders_dataset[columns]

    df_to_show['data_ordine'] = pd.to_datetime(df_to_show['data_ordine'], unit='ms')

    # Formatta le date nel formato desiderato (GG-MM-AAAA)
    df_to_show['data_ordine'] = df_to_show['data_ordine'].dt.strftime('%d-%m-%Y')

    return dbc.Container([
        dash_table.DataTable(
            data=df_to_show.to_dict('records'),
            columns=[{'id': c, 'name': get_name_orders(c)} for c in df_to_show.columns],
            page_size=10,
            style_as_list_view=True,
            style_header={
                'font-weight': 'bold',
                'text-align': 'center',
                'font-family': 'Verdana',
                'font-size': '8pt',
                'overflow': 'hidden',
                'white-space': 'nowrap',
                'color': '#365185'
            },
            style_cell={
                'text-align': 'center',
                'font-family': 'Verdana',
                'padding': '5px',
                'font-size': '8pt',
                'overflow': 'hidden',
                'text-overflow': 'ellipsis',
                'white-space': 'nowrap',
                'color': '#365185'
            }, style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f2f2f2'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'white'
                }
            ]
        )
    ], style={'display': 'flex', 'flex-direction': 'column', 'overflow-x': 'auto'})