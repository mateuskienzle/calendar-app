from this import d
from dash import Dash, Input, Output, dash_table, callback_context
from dash import html, dcc
import dash
import pandas as pd
import pdb 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
import datetime

# from app import app
from app import *
import calendar
from dash_table import DataTable
import json
import os


#lista dos meses do ano
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
        'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

month = datetime.datetime.today().month

#função que retorna o ano atual
year = datetime.datetime.today().year

#lista, em ordem crescente, dos 50 anos a partir do ano 2000 (2000 a 2050)
anos = [(year+28) - i for i in range(51)]
anos = list(reversed(anos))

#variável de controle dos meses do ano
mm = 0

#variável de controle dos 50 anos
yy = (year - 2000)

#variavel global que retorna o dia atual em formato de string
dia_atual = datetime.datetime.today().day

#função que retorna o dia da semana em que está localizado o primeiro
#dia do mês e também retorna o útlimo dia do mês
def get_calendar(yy, mm):
    
    calendar_ = calendar.month(yy, mm)

    calendar_ = calendar_.split("\n")[2:-1]


    pos_primeiro_dia = (calendar_[0].find('1'))
    dict_position_to_days = {1: "SEG", 4: "TER", 7: "QUA", 10: "QUI", 
                            13: "SEX", 16: "SAB", 19:"DOM"}
    
    #primeiro dia do mês em string (relação à semana)
    first_day = dict_position_to_days[pos_primeiro_dia]

    #último dia do mês em número
    last_day = int(calendar_[-1].split(" ")[-1])
    
    return first_day, last_day


#estrutura da tabela do calendário
df = pd.DataFrame({
                ("SEG"): [None]*6,
                ("TER"): [None]*6,
                ("QUA"): [None]*6,
                ("QUI"): [None]*6,
                ("SEX"): [None]*6,
                ("SAB"): [None]*6,
                ("DOM"): [None]*6,
            })



def save_file(lista_eventos):
    with open('eventos.json', 'w') as f:
        json.dump(lista_eventos, f)

if "eventos.json" in os.listdir():
    lista_de_eventos = json.load(open('eventos.json'))
else:
    lista_de_eventos = {'29/04/2022': 
                [
                    {'horario': '14:00', 'titulo': 'aula', 'local': 'faculdade', 'descricao': 'quimica', 'id': 0},
                    {'horario': '16:00', 'titulo': 'aula2', 'local': 'faculdade', 'descricao': 'fisica', 'id': 1},
                    {'horario': '20:00', 'titulo': 'aula3', 'local': 'faculdade', 'descricao': 'quimica', 'id': 2},
                ],
                'id_max': 3
            }
    save_file(lista_de_eventos)


#container princiapal, em que tudo mostrado na página está dentro dele
app.layout = dbc.Container([

        dcc.Location(id="url"),

        dbc.Row([
            dbc.Col([
                dbc.Col([
                    dbc.Row([
                        #botão para avançar para o mês seguinte
                        dbc.Button('<', id='voltar', n_clicks=0, 
                        style={'color' : 'black',
                        'background-color': '#ffffff',
                        'border' : '1px solid black',
                        'border-radius' : '50%',
                        'width' : '35px',
                        'height' : '35px',
                        'margin-top' : '60px',
                        'margin-left' : '280px',
                        'font-weight': 'bold',
                        'font-size' : '20px',
                        'padding' : '0px 0px'
                        }),

                        #botão para voltar para o mês anterior
                        dbc.Button('>',id='avancar', n_clicks=0, 
                        style={'color' : 'black',
                        'background-color': '#ffffff',
                        'border' : '1px solid black',
                        'border-radius' : '50%',
                        'width' : '35px',
                        'height' : '35px',
                        'margin-top' : '60px',
                        'margin-left' : '160px',
                        'font-weight': 'bold',
                        'font-size' : '20px',
                        'padding' : '0px 12px'
                        }),

                        #seção em que é exibido o ano
                        html.Div('Ano', 
                        style={'width' : 'fit-content',
                        'padding' : '0px',
                        'textAlign': 'center',
                        'margin-left' : '-160px', 
                        'margin-top' : '45px', 
                        'font-weight': 'bold',
                        'font-size' : '40px',
                        'background-color' : 'transparent',
                        'color' : '#ffffff'},
                        id='div-ano'),
                    ]), 
                    
                    dbc.Row([
                        html.Div('Mês',
                        style={'width' : '130px',
                        'textAlign': 'center',
                        'margin-left' : '330px',
                        'margin-top' : '0px',
                        'font-weight': 'bold',
                        'font-size' : '26px',
                        'background-color' : 'transparent',
                        'color' : 'rgba(236, 100, 75, 1)'},
                        id='div-mes'),

                    ]),

                    dbc.Row([
                        DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id="calendar",
                        style_table={'border': '2px solid transparent',
                                    'height': '390px',
                                    'width' : '715px',
                                    'color' : '#ffffff',
                                    'margin-top' : '20px',
                                    'margin-left' : '30px'},
                        style_cell={'height': '5.5rem'},
                        style_data={'border': '0px',  
                                    'backgroundColor': 'transparent', 
                                    'textAlign' : 'center'},
                        style_header={'border': '0px', 
                                        'color' : 'rgba(255,255,255, 0.4)',
                                        'backgroundColor': 'transparent', 
                                        'textAlign' : 'center', 
                                        'font-weight': 'bold'},

                        )
                    ]),
                ], md=12, style={'margin-left' : '7.5px', 'margin-top' : '35px'},  className = 'primary-color'),
            ], md=7, style={ 'height' : '100vh'}, className = 'terciary-color'),

            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Div(id='div-dia-mês-atual',
                                style={'margin-left' : '0px',
                                'margin-top' : '20px', 
                                'width' : 'fit-content',
                                'height' : 'fit-content',
                                'color' : '#ffffff',
                                'font-size': '150px',
                                'line-height': '0.85',
                                'background-color' : 'transparent'}
                        ),

                        html.Div(id='div-dia-semana-atual',
                                style={'margin-left' : '172px',
                                'margin-top' : '-50px', 
                                'width' : '140px',
                                'height' : '30px',
                                'color' : '#ffffff',
                                'text-align': 'top',
                                'font-size': '20px',
                                'background-color' : 'transparente'}
                        ),
                    ], md=8, className = 'secundary-color'),

                    dbc.Col([
                        #botão que abre a janela de insersação dos dados das tarefas 
                        dbc.Button("Adicionar tarefa", color="light", className="me-1", id='open-modal-button', n_clicks=0,
                                    style={'margin-top' : '40px',
                                    'margin-left' : '30px',
                                    'width' : '120px',
                                    'font-weight': 'bold',
                                    }),

                        html.Div(id='div-data-concatenada',
                                style={'margin-left' : '90px',
                                'margin-top' : '60px', 
                                'width' : '80px',
                                'height' : '30px',
                                'color' : 'transparent',
                                'background-color' : 'transparent',
                                'text-align' : 'left'}
                        ),
                    ], md=4, className = 'secundary-color', style={ 'border-top-right-radius' : '7%'}),
                ], style={'margin-top' : '35px', 'width' : '550px'}),

                dcc.Store(id='storage-lista-de-eventos', data=lista_de_eventos),

                html.Div(id='div-armazena-numero-de-eventos'),

                dbc.Row([
                    #card principal que abrange todas as tarefa
                    dbc.Card(style = {'color' : '#000000',
                        'border-radius' : '0px',
                        'width' : '550px',
                        'height' : '393px',
                        'margin-left' : '0px',
                        'margin-top' : '0px',
                        'background-color': 'rgba(0,0,0)',
                        'overflow-y': 'scroll'},
                        id='card-geral'
                    ),
                ]),
            ], md=5, className = 'terciary-color'),
        ]), 

        #janela de insersação dos dados das tarefas 
            dbc.Modal([
                dbc.ModalHeader("Nova tarefa"),

                dbc.ModalTitle(
                    dcc.Input(id="titulo-input", 
                                        placeholder="Adicione um título", type="text", 
                                        style={'width' : '400px',
                                                'border-top' : 'transparent',
                                                'border-left' : 'transparent',
                                                'border-right' : 'transparent',
                                                'border-bottom' : '2px solid black',
                                                'border-radius' : '0px',
                                                'margin-left' : '10px',
                                                'font-weight': 'bold',
                                                'margin-top' : '20px'
                                                }
                    )
                ),

                dbc.ModalBody([

                    dcc.Input(id="horario-input", placeholder="Horário", type="text",
                            style={'width' : '62px',
                                    'margin-top' : '20px'}
                    ),

                    dcc.Input(id="local-input", placeholder="Local", type="text", 
                            style={'width' : '450px',
                                    'margin-top' : '20px'}
                    ),

                    dcc.Input(id="descricao-input", placeholder="Descrição", type="text", 
                            style={'width' : '450px',
                                    'margin-top' : '20px'}
                    ),
                    
                    html.Div(id="required-field-notification", 
                            style={'width' : '450px',
                                    'margin-top' : '20px',
                                    'color' : 'red'}
                    ),

                    html.Button('Salvar', id='submit-tarefa', n_clicks=0, 
                                style={'color' : 'rgba(0, 0, 0, 1.0)',
                                        'background-color': 'rgba(128, 128, 128, 0.5)',
                                        'margin-top' : '20px',
                                        'margin-left' : '390px'}
                    )
                ]),

                ],style={'color' : '#000000',
                    'background-color' : 'rgba(255, 255, 255, 0.4)'},
                    id="modal-tarefa",
                    is_open=False
                ),

], fluid=True)


# =========  Layout  =========== #

@app.callback(
    Output('calendar', 'data'),
    Output('calendar', 'active_cell'),
    Output('div-mes', 'children'),
    Output('div-ano', 'children'),

    [Input('avancar', 'n_clicks'),
    Input('voltar', 'n_clicks'),
    Input('url', 'pathname')],
    prevent_initial_call=True
)
def render_calendar_content(botao_avanca, botao_volta, pathname):
    global mm
    global yy

    if pathname == "/":

        changed_id = [p['prop_id'] for p in callback_context.triggered][0]

        if 'avancar' in changed_id:
            mm += 1 
            if mm > 12:
                mm = 1
                yy += 1

        elif 'voltar' in changed_id:
            mm -= 1 
            if mm < 1:
                mm = 12
                yy -= 1

        else:
            mm = month
            yy = year-2000

        day, last_day = get_calendar(yy+2000, mm)

        empty_dict = df.to_dict("records")

        days_of_week = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM']
        c = 0
        for d in range(1, last_day+1):
            empty_dict[c][day] = d
            
            if d == dia_atual and meses[month-1] == meses[mm-1] and year == anos[yy]:
                initial_active_cell = {'row': c, 'column' : (days_of_week.index(day)), 'column_id' : day, 'row_id' : c}
            
            elif meses[month-1] != meses[mm-1] or year != anos[yy]:
                if d == 1:
                    initial_active_cell = {'row': c, 'column' : (days_of_week.index(day)), 'column_id' : day, 'row_id' : c}

            day = "SEG" if days_of_week.index(day) + 1 >= 7 else days_of_week[days_of_week.index(day) + 1]

            if day == "SEG": 
                c += 1

        return empty_dict, initial_active_cell, meses[mm-1], anos[yy]


@app.callback(
        Output('modal-tarefa', 'is_open'),

        Input('open-modal-button', 'n_clicks'),
        Input('submit-tarefa', 'n_clicks'),

        State('modal-tarefa', 'is_open'),
        State('horario-input', 'value'),
        prevent_initial_call=True
        )
def toggle_modal(n1, n2, is_open, horario):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    if changed_id.split('.')[0] == 'open-modal-button':
        return not is_open

    if changed_id.split('.')[0] == 'submit-tarefa' and horario:
        return not is_open
    return is_open



@app.callback(
    [
    Output('storage-lista-de-eventos', 'data'),
    Output('horario-input', 'value'),
    Output('titulo-input', 'value'),
    Output('local-input', 'value'),
    Output('descricao-input', 'value'),
    Output('required-field-notification', 'children')
    ],

    [
    Input('submit-tarefa', 'n_clicks'),
    Input({'type': 'delete_event', 'index': ALL}, 'n_clicks'),
    Input('avancar', 'n_clicks'),
    Input('voltar', 'n_clicks')
    ],

    [
    State('div-data-concatenada', 'children'),
    State('horario-input', 'value'),
    State('titulo-input', 'value'),
    State('local-input', 'value'),
    State('descricao-input', 'value')
    ], 
    prevent_initial_call=True
    )
def update_lista_eventos(n_clicks, n_clicks2, n2, n3, data_conc, horario, titulo, local, descricao):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    if 'submit-tarefa' in changed_id:
        if not horario:
            notificacao = 'Insira um horário válido'
            return lista_de_eventos, horario, titulo, local, descricao, notificacao

        else:
            if data_conc not in lista_de_eventos:
                lista_de_eventos[data_conc] = []
            lista_de_eventos[data_conc].append({'horario' : horario, 'titulo' : titulo,
                                                    'local' : local, 'descricao' : descricao,
                                                    'id' : lista_de_eventos['id_max']}
                                                        )
            lista_de_eventos['id_max'] += 1
    
    if 'delete_event' in changed_id and any(n_clicks2):
        dict_id = json.loads(changed_id.split(".")[0])
        idx = dict_id["index"]
        lista_de_eventos[data_conc] = [i for i in lista_de_eventos[data_conc] if i["id"] != idx]

    horario = None
    titulo = None
    local = None
    descricao = None
    notificacao = ''

    return lista_de_eventos, horario, titulo, local, descricao, notificacao



@app.callback(
    [Output('div-data-concatenada', 'children'),
    Output('card-geral', 'children'),
    Output('div-dia-mês-atual', 'children'),
    Output('div-dia-semana-atual', 'children'),
    ],

    [
    Input('calendar', 'active_cell'),
    Input('storage-lista-de-eventos', 'data')
    ],

    [
    State('div-mes', 'children'),
    State('div-ano', 'children'),
    State('calendar', 'data'), 
    ],

    prevent_initial_call=True
    )
def update_card_geral(active_cell, lista_de_eventos, mes, ano, calendar_data):
    save_file(lista_de_eventos)
    
    dia = calendar_data[active_cell['row']][active_cell['column_id']]

    if dia == None:
        dia = 1

    data_conc = '{:02d}/{:02d}/{:02d}'.format(dia, meses.index(str(mes)) + 1, ano)
    card_tarefa = []


    num_events = 0 if data_conc not in lista_de_eventos.keys() else len(lista_de_eventos[data_conc])


    if num_events != 0:
        lista_ordenada_de_eventos = sorted(lista_de_eventos[data_conc], key=lambda d: d['horario']) 


    col = active_cell['column_id']

    if col == 'SEG':
        col = 'Segunda-Feira'
    elif col == 'TER':
        col = 'Terça-Feira'
    elif col == 'QUA':
        col = 'Quarta-Feira'
    elif col == 'QUI':
        col = 'Quinta-Feira'
    elif col == 'SEX':
        col = 'Sexta-Feira'
    elif col == 'SAB':
        col = 'Sábado'
    elif col == 'DOM':
        col = 'Domingo'

    dia_mês_atual = data_conc[:2] 
    dia_semana_atual = col


    for i in range(num_events):
        new_card = dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H4(lista_ordenada_de_eventos[i]['horario'],
                                style={'font-weight' : 'bold',
                                        'text-align' : 'center',
                                        'font-size' : '16px'}),
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4(lista_ordenada_de_eventos[i]['titulo'],
                                        style={'font-weight' : 'bold',
                                                'margin-top' : '-10px',
                                                'font-size' : '16px'}),
                                        html.P(lista_ordenada_de_eventos[i]['local'],
                                        style={'margin-top' : '-4px',
                                                'font-size' : '12px',
                                                'color' : 'gray'}),
                                        html.P(lista_ordenada_de_eventos[i]['descricao'])
                                    ]
                                ),
                                className="col-md-9",
                            ),
                            dbc.Col(
                                dbc.Button('X', 
                                        id={
                                            'type': 'delete_event',
                                            'index': lista_ordenada_de_eventos[i]['id']
                                        },     
                                        style={'color' : 'black',
                                        'background-color': '#ffffff',
                                        'border' : '1px solid black',
                                        'border-radius' : '50%',
                                        'width' : '20px',
                                        'height' : '20px',
                                        'font-weight': 'bold',
                                        'font-size' : '12px',
                                        'padding' : '0px 6px'
                                        }),
                                className="col-md-1",
                            )
                        ],
                        className="g-0 d-flex align-items-center",
                        style={'border-bottom': '1px solid white',}
                    )
                ],
                className="mb-3",
                style={"maxWidth": "540px",
                        'background-color' : '#000000'},
                id='card-tarefa'
                )
        card_tarefa.append(new_card)

    return data_conc, card_tarefa, dia_mês_atual, dia_semana_atual



if __name__ == "__main__":
    app.run_server(debug=True)