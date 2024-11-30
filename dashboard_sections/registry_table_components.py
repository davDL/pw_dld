import pandas as pd
from dash import html, Input, Output, callback
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


def production_table_row(row):
    return html.Tr([
        text_table_cell(row.get("ID")),
        text_table_cell_mid(pd.to_datetime(row.get('data_inizio'), unit='ms').strftime('%d/%m/%Y')),
        text_table_cell_mid(pd.to_datetime(row.get('data_fine'), unit='ms').strftime('%d/%m/%Y')),
        text_table_cell(row.get("id_vigneto")),
        text_table_cell(round(float(row.get("quantita_prodotta_prevista")), 2)),
        text_table_cell(round(float(row.get("quantia_prodotta_effettiva")), 2)),
        text_table_cell(row.get("qualita")),
        text_table_cell(round(float(row.get("costo_totale_produzione")), 2)),
        text_table_cell(round(float(row.get("consumi_acqua")), 2)),
        text_table_cell(round(float(row.get("consumi_energia")), 2)),
        text_table_cell(round(float(row.get("litri_vino")), 2)),
        text_table_cell(round(float(row.get("bottiglie_prodotte")), 2))
    ], style={'height': '51px', 'width': '50px'})

def table_in_row_production(production_dataset):
    page_size = 5

    # create callback
    @callback(
        Output('production-table', 'children'),
        Input('production-pagination', 'active_page'),
    )
    def update_list_production(page):
        # convert active_page data to integer and set default value to 1
        int_page = 1 if not page else int(page)

        # define filter index range based on active page
        filter_index_1 = (int_page - 1) * page_size
        filter_index_2 = int_page * page_size

        # get data by filter range based on active page number
        filter_dataset = production_dataset[filter_index_1:filter_index_2]

        # load data to dash bootstrap table component
        table = get_table_in_row_production(filter_dataset, (filter_index_1 + 1))

        return table

    return dbc.Container([
        html.Div([
            html.H5(["Elenco della produzione"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='production-table', style={'min-height': '350px'}),
        dbc.Pagination(id='production-pagination', max_value=common_utils.get_total_page(page_size, production_dataset.shape[0]),
                       previous_next=True, fully_expanded=False,
                       style={'padding-bottom': '20px', 'align-self': 'flex-end'}),
    ], style={'display': 'flex', 'flex-direction': 'column'})

def get_table_in_row_production(dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Data inizio"),
                text_table_cell_header("Data fine"),
                text_table_cell_header("Id vigneto"),
                text_table_cell_header("Quantitá prevista (Kg)"),
                text_table_cell_header("Quantitá effettiva (Kg)"),
                text_table_cell_header("Qualitá"),
                text_table_cell_header("Costo totale produzione (€)"),
                text_table_cell_header("Consumi acqua (l)"),
                text_table_cell_header("Consumi energia (kW/h)"),
                text_table_cell_header("Vino (l)"),
                text_table_cell_header("Bottiglie prodotte")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(production_table_row(row))
        counter += 1

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table

def table_in_row_production_single_page(production_dataset):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Data inizio"),
                text_table_cell_header("Data fine"),
                text_table_cell_header("Id vigneto"),
                text_table_cell_header("Quantitá prevista (Kg)"),
                text_table_cell_header("Quantitá effettiva (Kg)"),
                text_table_cell_header("Qualitá"),
                text_table_cell_header("Costo totale produzione (€)"),
                text_table_cell_header("Consumi acqua (l)"),
                text_table_cell_header("Consumi energia (kW/h)"),
                text_table_cell_header("Vino (l)"),
                text_table_cell_header("Bottiglie prodotte")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    table_rows = []
    for index, row in production_dataset.iterrows():
        table_rows.append(production_table_row(row))

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return dbc.Container([
        html.Div([
            html.H5(["Elenco della produzione"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='production-table', style={'min-height': '350px'}, children=table),
    ], style={'display': 'flex', 'flex-direction': 'column'})


def production_yield_table_row(row):
    return html.Tr([
        text_table_cell(row.get("ID")),
        text_table_cell(row.get("id_vigneto")),
        text_table_cell(row.get("varieta")),
        text_table_cell(row.get("quantita_prodotta_prevista")),
        text_table_cell(round(float(row.get("quantia_prodotta_effettiva")),2)),
        text_table_cell(row.get("reason_primavera")),
        text_table_cell(row.get("reason_estate")),
        text_table_cell(row.get("reason_autunno"))
    ], style={'height': '51px', 'width': '50px'})

def table_in_row_production_yield(production_dataset):
    page_size = 5

    # create callback
    @callback(
        Output('production-table-yield', 'children'),
        Input('production-pagination-yield', 'active_page'),
    )
    def update_list_production(page):
        # convert active_page data to integer and set default value to 1
        int_page = 1 if not page else int(page)

        # define filter index range based on active page
        filter_index_1 = (int_page - 1) * page_size
        filter_index_2 = int_page * page_size

        # get data by filter range based on active page number
        filter_dataset = production_dataset[filter_index_1:filter_index_2]

        # load data to dash bootstrap table component
        table = get_table_in_row_production_yield(filter_dataset, (filter_index_1 + 1))

        return table

    return dbc.Container([
        html.Div([
            html.H5(["Elenco della produzione - resa vigneto"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='production-table-yield', style={'min-height': '350px'}),
        dbc.Pagination(id='production-pagination-yield', max_value=common_utils.get_total_page(page_size, production_dataset.shape[0]), previous_next=True, fully_expanded=False, style={'padding-bottom': '20px', 'align-self': 'flex-end'}),
    ], style={'display': 'flex', 'flex-direction': 'column'})

def table_in_row_production_yield_single_page(production_dataset):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Id vigneto"),
                text_table_cell_header("Varietá"),
                text_table_cell_header("Quantitá prevista (Kg)"),
                text_table_cell_header("Quantitá effettiva (Kg)"),
                text_table_cell_header("Primavera"),
                text_table_cell_header("Estate"),
                text_table_cell_header("Autunno")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    table_rows = []
    for index, row in production_dataset.iterrows():
        table_rows.append(production_yield_table_row(row))

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return dbc.Container([
        html.Div([
            html.H5(["Elenco della produzione"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='production-table', style={'min-height': '350px'}, children=table),
    ], style={'display': 'flex', 'flex-direction': 'column'})

def get_table_in_row_production_yield(dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Id vigneto"),
                text_table_cell_header("Varietá"),
                text_table_cell_header("Quantitá prevista (Kg)"),
                text_table_cell_header("Quantitá effettiva (Kg)"),
                text_table_cell_header("Primavera"),
                text_table_cell_header("Estate"),
                text_table_cell_header("Autunno")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(production_yield_table_row(row))
        counter += 1

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table


def orders_table_row(row):
    return html.Tr([
        text_table_cell(row.get("ID")),
        text_table_cell_mid(pd.to_datetime(row.get('data_ordine'), unit='ms').strftime('%d/%m/%Y')),
        text_table_cell(row.get("id_cliente")),
        text_table_cell(row.get("nome_cliente") + " " + row.get("cognome_cliente")),
        text_table_cell(row.get("telefono_cliente")),
        text_table_cell(row.get("quantita")),
        text_table_cell(row.get("stato_ordine")),
        text_table_cell(row.get("prezzo_totale"))
    ], style={'height': '51px', 'width': '50px'})

def table_in_row_orders(orders_dataset):
    page_size = 5

    # create callback
    @callback(
        Output('orders-table', 'children'),
        Input('orders-pagination', 'active_page'),
    )
    def update_list_orders(page):
        # convert active_page data to integer and set default value to 1
        int_page = 1 if not page else int(page)

        # define filter index range based on active page
        filter_index_1 = (int_page - 1) * page_size
        filter_index_2 = int_page * page_size

        # get data by filter range based on active page number
        filter_agents = orders_dataset[filter_index_1:filter_index_2]

        # load data to dash bootstrap table component
        table = get_table_in_row_orders(filter_agents,(filter_index_1 + 1))

        return table

    return dbc.Container([
        html.Div([
            html.H5(["Elenco degli ordini"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='orders-table', style={'min-height': '350px'}),
        dbc.Pagination(id='orders-pagination', max_value=common_utils.get_total_page(page_size, orders_dataset.shape[0]),
                       previous_next=True, fully_expanded=False,
                       style={'padding-bottom': '20px', 'align-self': 'flex-end'}),
    ], style={'display': 'flex', 'flex-direction': 'column'})

def table_in_row_orders_single_page(orders_dataset_):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Data ordine"),
                text_table_cell_header("Id cliente"),
                text_table_cell_header("Nome"),
                text_table_cell_header("Telefono"),
                text_table_cell_header("Quantità ordinata"),
                text_table_cell_header("Stato"),
                text_table_cell_header("Prezzo totale (€)")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    table_rows = []
    for index, row in orders_dataset_.iterrows():
        table_rows.append(orders_table_row(row))

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return dbc.Container([
        html.Div([
            html.H5(["Elenco della produzione"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between',
                  'margin-bottom': '8px'}),
        dbc.Table(id='orders-table', style={'min-height': '350px'}, children=table),
    ], style={'display': 'flex', 'flex-direction': 'column'})

def get_table_in_row_orders(dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Data ordine"),
                text_table_cell_header("Id cliente"),
                text_table_cell_header("Nome"),
                text_table_cell_header("Telefono"),
                text_table_cell_header("Quantità ordinata"),
                text_table_cell_header("Stato"),
                text_table_cell_header("Prezzo totale (€)")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(orders_table_row(row))
        counter += 1

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table