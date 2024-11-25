from dash import html, Output, Input, callback
import dash_bootstrap_components as dbc
from common_components import text_table_cell, text_table_cell_header

def generate_performance_variety_values_by_row(row, production_dataset) :
    # ---filtrare le righe per varietá : renderlo filtrabile in base al campo data (convertire da millisecond epoch a datetime)
    filtered_production = production_dataset[production_dataset['varieta'] == row.get("nome_varieta_coltivata")]

    filtered_production_count = filtered_production.shape[0]

    if filtered_production_count == 0:
        return

    # quantitá media per varietá
    avg_quantity = filtered_production['quantia_prodotta_effettiva'].sum() // filtered_production_count
    # qualitá media per varietá
    avg_quality = filtered_production['qualita'].sum() // filtered_production_count
    # costo medio per varietá
    avg_price = filtered_production['costo_totale_produzione'].sum() // filtered_production_count
    # resa vino
    wine_yield = round((filtered_production['quantia_prodotta_effettiva'].sum() // filtered_production_count) / (filtered_production['litri_vino'].sum() // filtered_production_count), 5)  # (kg per litro)

    return (row.get("nome_varieta_coltivata"),
            int(avg_quantity),
            int(avg_quality),
            int(avg_price),
            float(wine_yield)
    )

def performances_variety_table_row_by_values (row):

    return html.Tr([
        text_table_cell(row[0]),
        text_table_cell(float(row[1])),
        text_table_cell(float(row[2])),
        text_table_cell(float(row[3])),
        text_table_cell(float(row[4]))
    ])

def performances_variety_table_row (row, production_dataset):
    # ---filtrare le righe per varietá : renderlo filtrabile in base al campo data (convertire da millisecond epoch a datetime)
    filtered_production = production_dataset[production_dataset['varieta'] == row.get("nome_varieta_coltivata")]

    filtered_production_count = filtered_production.shape[0]

    if filtered_production_count == 0:
        return

    # quantitá media per varietá
    avg_quantity = filtered_production['quantia_prodotta_effettiva'].sum() // filtered_production_count
    # qualitá media per varietá
    avg_quality = filtered_production['qualita'].sum() // filtered_production_count
    # costo medio per varietá
    avg_price = filtered_production['costo_totale_produzione'].sum() // filtered_production_count
    # resa vino
    wine_yield = round((filtered_production['quantia_prodotta_effettiva'].sum() // filtered_production_count) / (filtered_production['litri_vino'].sum() // filtered_production_count), 5) #(kg per litro)

    return  html.Tr([
        text_table_cell(row.get("nome_varieta_coltivata")),
        text_table_cell(avg_quantity),
        text_table_cell(avg_quality),
        text_table_cell(avg_price),
        text_table_cell(wine_yield)
    ])

def table_performances_variety(order_image, production_dataset, vineyard_dataset):

    @callback(
        Output('table_variety', 'children'),
        Input('avg_quantity_header_variety', 'n_clicks'),
        Input('avg_quality_header_variety', 'n_clicks'),
        Input('avg_price_header_variety', 'n_clicks'),
        Input('wine_yield_header_variety', 'n_clicks'),
    )
    def update_table(avg_quantity_clicks, avg_quality_clicks, avg_price_time_clicks, wine_yield_time_clicks):
        _sorted_table_row_list = []
        _performance_rows: list[tuple[str, int, int, int, float]] = []
        _new_table_row_list = []

        def get_service(item):
            return item[1]

        def get_satisfaction(item):
            return item[2]

        def get_handling(item):
            return item[3]

        def get_wait_avg(item):
            return item[4]

        if avg_quantity_clicks is None and avg_quality_clicks is None and avg_price_time_clicks is None and wine_yield_time_clicks is None:
            return table_header + table_body
        else :
            for new_index, new_row in vineyard_dataset.iterrows():
                new_performance_row = generate_performance_variety_values_by_row(new_row, production_dataset)
                if new_performance_row is not None:
                    _performance_rows.append(new_performance_row)

            if avg_quantity_clicks is not None and avg_quantity_clicks > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_service)# ordinamento delle righe in base al livello di servizio
            if avg_quality_clicks is not None and avg_quality_clicks > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_satisfaction)# ordinamento delle righe in base alla soddisfazione del cliente
            if avg_price_time_clicks is not None and avg_price_time_clicks > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_handling)# ordinamento delle righe in base al tempo medio della gestione
            if wine_yield_time_clicks is not None and wine_yield_time_clicks > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_wait_avg)# ordinamento delle righe in base al tempo medio di attesa

            for new_index, new_row in enumerate(reversed(_sorted_table_row_list)):
                new_performance_row = performances_variety_table_row_by_values(new_row)
                if new_performance_row is not None:
                    _new_table_row_list.append(new_performance_row)

            new_table_body = [html.Tbody(
                _new_table_row_list
            )]

            return table_header + new_table_body

    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Varietá"),
                html.Th([
                    dbc.Container([
                        html.Div("Quantitá media", style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display': 'flex', 'justify-content': 'center'})
                ], className='textCellHeader', id='avg_quantity_header_variety'),
                html.Th([
                    dbc.Container([
                        html.Div("Qualitá media", className='textCellHeader', style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display':'flex', 'justify-content':'center'})
                ], className='textCellHeader', id='avg_quality_header_variety'),
                html.Th([
                    dbc.Container([
                        html.Div("Costo medio", className='textCellHeader', style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display': 'flex', 'justify-content': 'center'})
                ], className='textCellHeader', id='avg_price_header_variety'),
                html.Th([
                    dbc.Container([
                        html.Div("Resa", className='textCellHeader', style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display': 'flex', 'justify-content': 'center'})
                ], className='textCellHeader', id='wine_yield_header_variety'),
            ])
        )
    ]

    table_row_list = []
    for index, row in vineyard_dataset.iterrows():
        performance_row = performances_variety_table_row(row, production_dataset)
        if performance_row is not None:
            table_row_list.append(performance_row)

    table_body = [html.Tbody(
        table_row_list
    )]

    return dbc.Container([
        html.Div([
            html.H5(["Indicatori di performance"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-bottom': '8px'}),
        dbc.Container([
            dbc.Table(
                table_header + table_body,
                bordered=True,
                striped=True,
                id='table_variety'
            )
        ])
    ])



def generate_performance_vineyards_values_by_row(row, production_dataset) :
    filtered_production = production_dataset[production_dataset['id_vigneto'] == row.get("ID")]

    filtered_production_count = filtered_production.shape[0]

    if filtered_production_count == 0:
        return

    # quantitá media per varietá
    avg_quantity = filtered_production['quantia_prodotta_effettiva'].sum() // filtered_production_count
    # qualitá media per varietá
    avg_quality = filtered_production['qualita'].sum() // filtered_production_count
    # costo medio per varietá
    avg_price = filtered_production['costo_totale_produzione'].sum() // filtered_production_count
    # resa vino
    wine_yield = round((filtered_production['quantia_prodotta_effettiva'].sum() // filtered_production_count) / (filtered_production['litri_vino'].sum() // filtered_production_count), 5)  # (kg per litro)

    return (row.get("ID"),
            int(avg_quantity),
            int(avg_quality),
            int(avg_price),
            float(wine_yield)
    )

def performances_vineyards_row_by_values (row):

    return html.Tr([
        text_table_cell(row[0]),
        text_table_cell(float(row[1])),
        text_table_cell(float(row[2])),
        text_table_cell(float(row[3])),
        text_table_cell(float(row[4]))
    ])

def performances_vineyards_table_row (row, production_dataset):
    # ---filtrare le righe per varietá : renderlo filtrabile in base al campo data (convertire da millisecond epoch a datetime)
    filtered_production = production_dataset[production_dataset['id_vigneto'] == row.get("ID")]

    filtered_production_count = filtered_production.shape[0]

    if filtered_production_count == 0:
        return

    # quantitá media per varietá
    avg_quantity = filtered_production['quantia_prodotta_effettiva'].sum() // filtered_production_count
    # qualitá media per varietá
    avg_quality = filtered_production['qualita'].sum() // filtered_production_count
    # costo medio per varietá
    avg_price = filtered_production['costo_totale_produzione'].sum() // filtered_production_count
    # resa vino
    wine_yield = round((filtered_production['quantia_prodotta_effettiva'].sum() // filtered_production_count) / (filtered_production['litri_vino'].sum() // filtered_production_count), 5) #(kg per litro)

    return  html.Tr([
        text_table_cell(row.get("ID")),
        text_table_cell(avg_quantity),
        text_table_cell(avg_quality),
        text_table_cell(avg_price),
        text_table_cell(wine_yield)
    ])

def table_performances_vineyards(order_image, production_dataset, vineyard_dataset):

    @callback(
        Output('table_production', 'children'),
        Input('avg_quantity_header_vineyards', 'n_clicks'),
        Input('avg_quality_header_vineyards', 'n_clicks'),
        Input('avg_price_header_vineyards', 'n_clicks'),
        Input('wine_yield_header_vineyards', 'n_clicks'),
    )
    def update_table(avg_quantity_header_vineyards, avg_quality_header_vineyards, avg_price_header_vineyards, wine_yield_header_vineyards):
        _sorted_table_row_list = []
        _performance_rows: list[tuple[str, int, int, int, float]] = []
        _new_table_row_list = []

        def get_service(item):
            return item[1]

        def get_satisfaction(item):
            return item[2]

        def get_handling(item):
            return item[3]

        def get_wait_avg(item):
            return item[4]

        if avg_quantity_header_vineyards is None and avg_quality_header_vineyards is None and avg_price_header_vineyards is None and wine_yield_header_vineyards is None:
            return table_header + table_body
        else :
            for new_index, new_row in vineyard_dataset.iterrows():
                new_performance_row = generate_performance_vineyards_values_by_row(new_row, production_dataset)
                if new_performance_row is not None:
                    _performance_rows.append(new_performance_row)

            if avg_quantity_header_vineyards is not None and avg_quantity_header_vineyards > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_service)# ordinamento delle righe in base al livello di servizio
            if avg_quality_header_vineyards is not None and avg_quality_header_vineyards > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_satisfaction)# ordinamento delle righe in base alla soddisfazione del cliente
            if avg_price_header_vineyards is not None and avg_price_header_vineyards > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_handling)# ordinamento delle righe in base al tempo medio della gestione
            if wine_yield_header_vineyards is not None and wine_yield_header_vineyards > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_wait_avg)# ordinamento delle righe in base al tempo medio di attesa

            for new_index, new_row in enumerate(reversed(_sorted_table_row_list)):
                new_performance_row = performances_vineyards_row_by_values(new_row)
                if new_performance_row is not None:
                    _new_table_row_list.append(new_performance_row)

            new_table_body = [html.Tbody(
                _new_table_row_list
            )]

            return table_header + new_table_body

    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Produzione"),
                html.Th([
                    dbc.Container([
                        html.Div("Quantitá media", style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display': 'flex', 'justify-content': 'center'})
                ], className='textCellHeader', id='avg_quantity_header_vineyards'),
                html.Th([
                    dbc.Container([
                        html.Div("Qualitá media", className='textCellHeader', style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display':'flex', 'justify-content':'center'})
                ], className='textCellHeader', id='avg_quality_header_vineyards'),
                html.Th([
                    dbc.Container([
                        html.Div("Costo medio", className='textCellHeader', style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display': 'flex', 'justify-content': 'center'})
                ], className='textCellHeader', id='avg_price_header_vineyards'),
                html.Th([
                    dbc.Container([
                        html.Div("Resa", className='textCellHeader', style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display': 'flex', 'justify-content': 'center'})
                ], className='textCellHeader', id='wine_yield_header_vineyards')
            ])
        )
    ]

    table_row_list = []
    for index, row in vineyard_dataset.iterrows():
        performance_row = performances_vineyards_table_row(row, production_dataset)
        if performance_row is not None:
            table_row_list.append(performance_row)

    table_body = [html.Tbody(
        table_row_list
    )]

    return dbc.Container([
        html.Div([
            html.H5(["Indicatori di performance"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-bottom': '8px'}),
        dbc.Container([
            dbc.Table(
                table_header + table_body,
                bordered=True,
                striped=True,
                id='table_production'
            )
        ])
    ])



def generate_performance_sell_orders_values_by_row(row, orders_dataset) :
    # ---filtrare le righe per id_cliente : renderlo filtrabile in base al campo data (convertire da millisecond epoch a datetime)
    filtered_orders = orders_dataset[orders_dataset['id_cliente'] == row.get("id_cliente")]

    filtered_orders_count = filtered_orders.shape[0]

    if filtered_orders_count == 0:
        return

    # numero ordini cancellati
    n_deleted_orders = filtered_orders[filtered_orders['stato_ordine'] == "Cancellato"].shape[0]
    # quantitá media ordinata
    avg_ordered_quantity = filtered_orders['quantita'].sum() // filtered_orders_count
    # spesa media su ordini
    avg_spent = filtered_orders['prezzo_totale'].sum() // filtered_orders_count

    return (row.get("nome_cliente"),
            filtered_orders_count,
            n_deleted_orders,
            avg_ordered_quantity,
            avg_spent
    )

def performances_sell_orders_table_row_by_values (row):

    return html.Tr([
        text_table_cell(row[0]),
        text_table_cell(row[1]),
        text_table_cell(row[2]),
        text_table_cell(row[3]),
        text_table_cell(row[4])
    ])

def performances_sell_orders_table_row (row, orders_dataset):
    # ---filtrare le righe per id_cliente : renderlo filtrabile in base al campo data (convertire da millisecond epoch a datetime)
    filtered_orders = orders_dataset[orders_dataset['id_cliente'] == row.get("id_cliente")]

    filtered_orders_count = filtered_orders.shape[0]

    if filtered_orders_count == 0:
        return

    # quantitá media ordinata
    avg_quantity = filtered_orders['quantita'].sum() // filtered_orders_count
    # numero ordini cancellati
    n_deleted_orders = filtered_orders[filtered_orders['stato_ordine'] == "Cancellato"].shape[0]
    # spesa media su ordini
    avg_spent = filtered_orders['prezzo_totale'].sum() // filtered_orders_count

    return html.Tr([
        text_table_cell(row.get("nome_cliente") + " " + row.get("cognome_cliente")),
        text_table_cell(filtered_orders_count),
        text_table_cell(n_deleted_orders),
        text_table_cell(avg_quantity),
        text_table_cell(avg_spent)
    ])

def table_performances_sell_orders(order_image, orders_dataset):

    @callback(
        Output('table_sell_orders', 'children'),
        Input('orders_count_header', 'n_clicks'),
        Input('n_deleted_orders_header', 'n_clicks'),
        Input('avg_quantity_header', 'n_clicks'),
        Input('avg_spent_header', 'n_clicks')
    )
    def update_table(orders_count_clicks, n_deleted_orders_clicks, avg_quantity_clicks, avg_spent_clicks):
        _sorted_table_row_list = []
        _performance_rows: list[tuple[str, int, int, int, int]] = []
        _new_table_row_list = []

        def get_service(item):
            return item[1]

        def get_satisfaction(item):
            return item[2]

        def get_handling(item):
            return item[3]

        def get_wait_avg(item):
            return item[4]

        if orders_count_clicks is None and n_deleted_orders_clicks is None and avg_quantity_clicks is None and avg_spent_clicks is None:
            return table_header + table_body
        else :
            for new_index, new_row in clienti_unici.iterrows():
                new_performance_row = generate_performance_sell_orders_values_by_row(new_row, orders_dataset)
                if new_performance_row is not None:
                    _performance_rows.append(new_performance_row)

            if orders_count_clicks is not None and orders_count_clicks > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_service)
            if n_deleted_orders_clicks is not None and n_deleted_orders_clicks > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_satisfaction)
            if avg_quantity_clicks is not None and avg_quantity_clicks > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_handling)
            if avg_spent_clicks is not None and avg_spent_clicks > 0:
                _sorted_table_row_list = sorted(_performance_rows, key = get_wait_avg)

            for new_index, new_row in enumerate(reversed(_sorted_table_row_list)):
                new_performance_row = performances_sell_orders_table_row_by_values(new_row)
                if new_performance_row is not None:
                    _new_table_row_list.append(new_performance_row)

            new_table_body = [html.Tbody(
                _new_table_row_list
            )]

            return table_header + new_table_body

    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Nome cliente"),
                html.Th([
                    dbc.Container([
                        html.Div("Numero ordini totale", className='textCellHeader', style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display':'flex', 'justify-content':'center'})
                ], className='textCellHeader', id='orders_count_header'),
                html.Th([
                    dbc.Container([
                        html.Div("Numero ordini cancellati", className='textCellHeader', style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display': 'flex', 'justify-content': 'center'})
                ], className='textCellHeader', id='n_deleted_orders_header'),
                html.Th([
                    dbc.Container([
                        html.Div("Quantitá media ordinata", className='textCellHeader', style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display': 'flex', 'justify-content': 'center'})
                ], className='textCellHeader', id='avg_quantity_header'),
                html.Th([
                    dbc.Container([
                        html.Div("Spesa media", className='textCellHeader',
                                 style={'color': '#365185', 'cursor': 'pointer'}),
                        html.Img(src=order_image, style={'width': '15px', 'height': '15px', 'margin-top': '2px'}),
                    ], style={'display': 'flex', 'justify-content': 'center'})
                ], className='textCellHeader', id='avg_spent_header')
            ])

        )
    ]

    # Seleziona le colonne di interesse
    new_orders_dataset = orders_dataset[['id_cliente', 'nome_cliente', 'cognome_cliente', 'telefono_cliente']]

    # Rimuovi i duplicati basati sulla colonna 'id_cliente'
    clienti_unici = new_orders_dataset.drop_duplicates(subset='id_cliente')

    table_row_list = []
    for index, row in clienti_unici.iterrows():
        performance_row = performances_sell_orders_table_row(row, orders_dataset)
        if performance_row is not None:
            table_row_list.append(performance_row)

    table_body = [html.Tbody(
        table_row_list
    )]

    return dbc.Container([
        html.Div([
            html.H5(["Indicatori di performance"], style={'color': '#365185'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-bottom': '8px'}),
        dbc.Container([
            dbc.Table(
                table_header + table_body,
                bordered=True,
                striped=True,
                id='table_sell_orders'
            )
        ])
    ])