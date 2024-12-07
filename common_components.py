from dash import html
import dash_bootstrap_components as dbc

def home_section(title, content):
    return dbc.Container([
        dbc.Col([
            html.H3([
                title
            ], className="sideHeadText"),
        ], width=11),
        dbc.Container([
            content
        ], className="tableSection elevation", style={'overflow-x': 'auto'})
    ])

def home_performances_section(title, content):
    return dbc.Container([
        dbc.Col([
            html.H3([
                title
            ], className="sideHeadText"),
        ], width=11),
        dbc.Container([
            content
        ])
    ], className="tableSection", style={'overflow-x': 'auto'})

def elevated_bar(content, image) :
    return html.Div([
                dbc.Col([
                    content
                ], width=11),
                html.Img(src=image, className='elevatedCardContent')
            ], className="sideHead")

def performance_card(h5text, h2text, h6text, class_name, image) :
    return dbc.Card([
        dbc.Container([
            dbc.Container([
                html.H5([
                    h5text
                ]),
                html.H2([
                    h2text
                ]),
                html.H6([
                    h6text
                ]),
            ]),
            html.Img(src=image, className='cardImage')
        ], fluid=True, style={'display': 'flex'}),
    ],style={}, className=class_name)

def progress_table_cell(value, color):
    label = "{value}%".format(value = int(value))
    return html.Td(
        dbc.Container([
            html.Div(label, style={'font-size': '10px'}),
            dbc.Progress(value=value, color=color, class_name='tableCellProgress')
        ], style={'padding':'4px'})
    )

def text_table_cell_header(text):
    return html.Th(text, className='textCellHeader', style={'color': '#365185'})

def text_table_cell_header_mid(text):
    return html.Th(text, className='textCellHeader mid', style={'color': '#365185'})

def text_table_cell(text):
    return html.Td(text, className='textCell', style={'color': '#365185'})

def text_table_cell_mid(text):
    return html.Td(text, className='textCell mid', style={'color': '#365185'})

def image_table_cell_header(image):
    return html.Th(html.Img(src=image, style={'height': '35px', 'weight': '35px'}))

def image_table_cell(image):
    return html.Td(html.Img(src=image, style={'height': '25px', 'weight': '25px'}))

def table_action_button(image, color, bg_hex):
    return dbc.Button(html.Img(src=image, style={'height': '15px', 'weight': '15px'}), color=color, style={'background-color': bg_hex, 'margin':'2px'})

def table_text_action_button(text, bg_hex):
    return dbc.Button(text, style={'background-color': bg_hex, 'max-width':'80px', 'font-size': '8pt'})