import dash
from dash import html
import dash_bootstrap_components as dbc
from dashboard_sections.components_agent import table_in_row_agents
from dashboard_sections.components_client import table_in_row_clients
from dashboard_sections.components_conversation import table_performances_conversations
from dashboard_sections.components_agent_performances import table_performances
from common_components import home_performances_section, elevated_bar, home_section
from dashboard_sections.components_global_performances import get_global_performances_cards
import pandas as pd

dash.register_page(__name__, path='/')

contact_center_dataset = pd.read_csv("assets/dataset_contact_center.csv", sep = ';')
conversation_dataset = pd.read_csv("assets/dataset_conversations.csv", sep = ';')
survey_dataset = pd.read_csv("assets/dataset_survey_italy.csv", sep = ';')

clean_client_data = conversation_dataset.drop_duplicates(subset=['Contact Id'])
clean_agents_data = contact_center_dataset.drop_duplicates(subset=['user_id'])[contact_center_dataset['user_id'].notnull()][contact_center_dataset['user_name'].notnull()]

layout = html.Div([
    # componenti dashboard
    elevated_bar(
        html.H3(
            "Dashboard",
            className="sideHeadText",
            style={'color': '#365185'}
        ),
        dash.get_asset_url('ic_dashboard.png')),

    home_performances_section(
        "Performance del sistema",
        get_global_performances_cards(
            survey_dataset,
            conversation_dataset
        )),

    # tabella agenti e performance
    home_section(
        "Agenti e performance",
        table_performances(
            dash.get_asset_url('ic_placeholder_profile.png'),
            dash.get_asset_url('ic_search.png'),
            contact_center_dataset,
            survey_dataset,
            conversation_dataset
        )),

    # tabelle agenti clienti affiancate
    dbc.Container([
        home_section("Agenti", table_in_row_agents(
            dash.get_asset_url('ic_placeholder_profile.png'),
            dash.get_asset_url('ic_edit_table.png'),
            dash.get_asset_url('ic_info_table.png'),
            dash.get_asset_url('ic_cancel_table.png'),
            dash.get_asset_url('ic_add.png'),
            clean_agents_data
        )),
        home_section("Clienti", table_in_row_clients(
            dash.get_asset_url('ic_edit_table.png'),
            dash.get_asset_url('ic_cancel_table.png'),
            dash.get_asset_url('ic_add.png'),
            clean_client_data
        )),
    ], className='inRowTables'),

    # tabella conversazioni e sondaggi
    home_section("Conversazioni e sondaggi", table_performances_conversations(
        dash.get_asset_url('ic_search.png'), conversation_dataset
    )),
], className='side')