import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import csv
import pandas as pd
import re
import random
import dash_table
import numpy as np
import plotly.express as px

import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from dash.dash import no_update
from dash.exceptions import PreventUpdate


rta = pd.read_csv("teamsPorAno.csv")
ncaaj = pd.read_csv("ncaaReduz.csv")

ncaa = ncaaj
ncaa = ncaa.drop(ncaa.loc[ncaa['pos']==''].index)
ncaa.dropna(inplace=True)

file = open('output.txt', 'r')

times_t = []
for line in file:
    if(re.search("\d{4}-\d{2}",line)):
        time = re.sub("\s$","",re.findall("^[^\d]+",line)[0])
        if(time not in times_t):
            times_t.append(time)
file.close()

hover_info = [['Levantador (S)','Libero (L)','Ponteiro (OH)','Ponteiro (OH)','Central (MB)','Oposto (RS)','Especialista em defesa (DS)'],
            ['1951','1401','4202','4202','3030','4278','1536'],
            [0,1401,0,0,0,0],
            ['É o responsável por armar a jogada.','Especialista em defesa. Só joga no fundo da quadra. E possui mais liberdade para entrar e sair de quadra',
            'É o principal atacante.','É o principal atacante.','É  principal bloqueador, e realiza ataques rápidos.',
            'É um atacante e realiza a <br>função do levantador, quando este não pode.','É outro especialista em defesa, porém para<br>entrar e sair de quadra são necessárias substituições.']]

desc_hab = {
'Bloqueio duplo': 'É um bloqueio composto por duas pessoas. É realizado pelas pessoas que estão na rede, normalmente nas suas extremidades.',
'Defesa': 'É a defesa de um ataque realizado pelo time oposto.',
'Erros de recepção': 'Recepção é o primeiro toque na bola após o saque adversário. Um erro de recepção acontece quando a jogada não tem sequência após o saque.',
'Ponto de ataque': 'Ocorre quando o time adversário não consegue defender o ataque realizado.',
'Bloqueio simples': 'É o bloqueio realizado por apenas uma jogadora, é efetuado na maioria das vezes pela central no meio da rede.',
'Pontos': 'É a conquista de um ponto para o time, indepentente do movimento realizado para concluir a jogada.',
'Aces': 'Quando o time adversário não consegue recepcionar o saque, e é ponto imediatamente sem que se consiga continuar a jogada.',
'Ataques errados': 'São ataques que foram para fora da quadra adversária, que foram bloqueados, ou que pegaram na antena',
'Saques errados': 'Saques para fora da quadra, que não passaram pela rede, ou que ocorreu uma falta ao pisar na linha durante o saque.',
'Levantamento': 'Mandar a bola para alguma jogadora do time de forma que seja possível realiar o ataque',
'Tentativa de ataque': 'Quando uma jogadora toca a bola acima de sua cabeça com a intenção de fazer ponto.',
'Erro de bloqueio': 'Ocorre quando a jogadora bloqueando encosta na rede, invade a quadra adversária, ou a jogadora está posicionada no fundo no rodízio atual.'
}

desc_posi = {
'Levantadora': 'A jogadora que organiza e chama as jogadas dentro de quadra. É responsável pelo levantamento, por isso não participa tanto das recepções e defesa.',
'Central': 'É o principal bloqueio do time, já que bloqueia em todas as posições da rede. Não costuma jogar no fundo da quadra.',
'Ponteira': 'A principal atacante do time, e também é importante da defesa do time.',
'Especialista Defesa': 'A diferença entre ela e a libero, é que a especialista em defesa pode jogar na rede e precisa de uma substituição para que entre em quadra.',
'Libero': 'Peça fundamental na defesa. Só pode jogar no fundo da quadra e em geral entra no lugar da central. (Na NCAA a libero pode sacar)',
'Oposta': 'É uma atacante, fica em posição oposta à levantadora e realiza o levantamento quando esta não consegue'
}



anos = rta['ano'].drop_duplicates().to_list()

#t_times = [{'label': i, 'value': i} for i in rta['team'].drop_duplicates().to_list()]
t_times = [{'label': i, 'value': i} for i in times_t]
#b_teams = ['abilene-christian','akron','yale']
b_teams = ['Stanford','Nebraska','Wisconsin', 'Florida','BYU','Texas','Penn St.']

data_v = {
    'Ano': [2012,2013,2014,2015,2016,2017,2018,2019],
    'Ouro': ['Texas','Penn St','Penn St','Nebraska','Stanford','Nebraska','Stanford','Stanford'],
    'Prata': ['Oregon','Wisconsin','BYU','Texas','Texas','Florida','Nebraska','Wisconsin'],
    'Placar da Final': ['3-0','3-1','3-0','3-0','3-1','3-1','3-2','3-0']
}
vencedores = pd.DataFrame(data_v,columns=['Ano','Ouro','Placar da Final','Prata'])

saque = ['Saques errados','Aces']
ataque = ['Tentativa de ataque','Ponto de ataque','Ataques errados']
defesa = ['Defesa','Erros de recepção']
bloqueio = ['Bloqueio duplo','Bloqueio simples','Erro de bloqueio']
combo = ['Tentativa de ataque','Ponto de ataque','Pontos','Defesa','Levantamento']
extras = [combo,saque,ataque,defesa,bloqueio]
extrass = ['combo','saque','ataque','defesa','bloqueio']
colunas = ['Bloqueio duplo', 'Defesa', 'Erros de recepção', 'Ponto de ataque', 'Bloqueio simples', 'Pontos',
           'Aces', 'Ataques errados', 'Saques errados', 'Levantamento', 'Tentativa de ataque', 'Erro de bloqueio']

cores = {
    'Pontos' :            '#68C2FA' ,#'#2f937d', #083F05
    'Aces' :              '#4F7EFA' ,#'#367934',#369428
    'Bloqueio duplo' :    '#1A0090' ,#'#2a7779',#17B396  
    'Bloqueio simples' :  '#9B01FA' ,#'#5e8b3c',#6C9D2D
    'Ponto de ataque' :   '#A1783C' ,#"rgb(0, 102, 0)",
    'Levantamento' :      '#D3F500',#'#2b60a1',#03a56a  #702ba1
    'Defesa' :            '#F5C303' ,#'#9C57BC',
    'Tentativa de ataque' :'#FA9203',#"rgb(0, 0, 102)",
    'Erro de bloqueio' :  '#F53C00' ,#'#97193B',
    'Erros de recepção' : '#F57070' ,#'#bb5b35',#B54C4C
    'Saques errados' :    '#DD96F5' ,#'#bb3b35'#EC1317
    'Ataques errados' :   '#962000' ,#"rgb(102, 0, 0)",
}



def box_posi(df,habilidade, por_jogo):
    posicoes = ['Especialista Defesa', 'Libero', 'Levantadora', 'Oposta', 'Ponteira', 'Central']

    fig = go.Figure()
    if(por_jogo):
        df=df.groupby(['dates','pos','team','opponent']).sum().reset_index(drop=False)
        pj=' por jogo'
    else:
        pj=''

    maxa=0
    qnoventa=[]
    for posi in posicoes:
        maximo = df.loc[df['pos']==posi,habilidade].max()

        if(maximo > maxa ):
            maxa = maximo
        qnoventa.append(df.loc[df['pos']==posi,habilidade].quantile(0.95))

        soma = df.loc[df['pos']==posi,habilidade].sum()

        fig.add_trace(
            go.Box(
                y=df.loc[df['pos']==posi,habilidade],
                name=posi,
                boxpoints=False,
                text='Total: '+str(soma) ,
                #textposition='outside',
                #boxmean=True,
                marker={'color':'#289bcc'  },
                showlegend=False,
                width=0.7
        ))
        fig.add_trace(
            go.Scatter(
                x=[posi],
                y=[maximo+1+(maximo*0.01)],
                mode='markers+text',
                marker={'color': colors['background'],'size':1},
                customdata=[soma],
                texttemplate='Total=%{customdata:.2s}',
                textposition='top center',
                hovertext='none',
                showlegend=False,
            )
        )
    fig.add_trace(
        go.Scatter(
            name='95%',
            x=posicoes,
            y=qnoventa,
            mode='markers',
            marker={'color':'#224791', 'symbol':3, 'size':10},
            hovertemplate= "(%{x}, 95%: %{y})",
            showlegend=False,
        )
    )

    fig.update_layout(
        xaxis_title='Posições',
        yaxis_title='Quantidade de '+habilidade.lower()+'s '+pj,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title=habilidade+' por posições'+pj,
        yaxis_range=[0,maxa+5+(maxa*0.1)],
    )

    return fig


##################################################################################################################################

def multi_plot(df, columns, show_medT):
    fig = go.Figure()

    if(df.shape[0] == 0):
        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            #title='Evolução do time durante os anos'
        )
        return fig

    for column in columns:
        fig.add_trace(
            go.Scatter(
                x = df['ano'],
                y = list(df[column]/df['quant_jogos']),
                name = column,
                customdata = [column]*len(df['ano']),
                line = dict(color = cores[column],width=3.5),
                text = [df.loc[(df.index.to_list())[0],'team']]*len(df['ano']),
                hovertemplate=
                        "<b>%{customdata}</b><br><br>" +
                        "Time: %{text}<br>"+
                        "Ano: %{x}<br>" +
                        "Média de ocorrências por jogo: %{y:.2f}<br>" +
                        "<extra></extra>",
                visible = True
            )
        )
        if(show_medT):
            med = (df[column]/df['quant_jogos']).mean()
            fig.add_trace(
                go.Scatter(
                    name='media '+column,
                    x = df['ano'],
                    y = [med]*len(df['ano']),
                    mode = "lines",
                    line = dict(color=cores[column],width=2,dash='dash'),
                    showlegend=True,
                    customdata = [column]*len(df['ano']),
                    hovertemplate=
                        "<b>%{customdata}</b><br>" +
                        "Média de todos os anos: %{y:.2f}<br>" +
                        "<extra></extra>",
                )
            )



    fig.update_layout(
            xaxis_title='Anos',
            yaxis_title='Quantidade média por jogo',
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            #title='Evolução do time durante os anos'
        )
    
    return fig
##############################################################################################################################

def corr_habs(df):
    col = ['Levantamento', 'Pontos', 'Ponto de ataque', 'Tentativa de ataque', 'Ataques errados','Defesa',
           'Erros de recepção', 'Bloqueio duplo',  'Bloqueio simples', 'Erro de bloqueio', 'Aces', 'Saques errados']
    col.append('Sets jogados')

    r =  df.groupby(['team','dates','opponent'])['r'].max()
    nc = df.groupby(['team','dates','opponent'])[col].sum()
    a=nc
    nc = nc.reset_index(drop=False)
    nc['r']=r.values
    col = col[:-1]
    nc.loc[nc['r']==0,'vic']='Perdeu'
    nc.loc[nc['r']==1,'vic']='Ganhou'
    nc = nc[nc['Sets jogados']>21]

    col = ['Levantamento', 'Pontos', 'Ponto de ataque', 'Tentativa de ataque', 'Ataques errados','Defesa',
           'Erros de recepção', 'Bloqueio duplo',  'Bloqueio simples', 'Erro de bloqueio', 'Aces', 'Saques errados']

    matrix = nc[col].corr()
    x=0
    idx = matrix.index.to_list()
    for i in idx:
        y=x
        while y < (len(idx)):
            matrix[idx[y]][i] = 0
            y=y+1
        x=x+1

    fig = make_subplots(rows=2, cols=1, row_heights=[0.1,0.9])
    cor_vic = nc[col].corrwith(nc['r'])

    fig.add_trace(go.Heatmap(
                z= [cor_vic],
                x= col,
                y= ['Vitória'],
                xgap=1, ygap=1,
                zmin=-1, zmax=1,
                coloraxis = "coloraxis",
                hovertemplate =
                    "%{x}<br>" +
                    "%{y}<br>" +
                    "%{z}"
                    "<extra></extra>",
                 ),
        1,1)
    fig.update_xaxes(side='top', row=1, col=1)
    
    fig.add_trace(go.Heatmap(z=matrix,
                      x=col,
                      y=col,
                      xgap=1, ygap=1,
                      zmin=-1, zmax=1,
                      coloraxis = "coloraxis",
                      text = matrix,
                      hovertemplate =
                          "%{x}<br>" +
                          "%{y}<br>" +
                          "%{z}"
                          "<extra></extra>",
                      #transpose=True,
                       ),
        2,1)
    fig.update_yaxes(autorange='reversed', row=2, col=1)


    title = ''               

    fig.update_layout(title_text=title, title_x=0.5, 
                       width=550, height=600,
                       plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'],
                       font_color=colors['text'],
                       xaxis_showgrid=False,
                       yaxis_showgrid=False,
                       coloraxis = {'colorscale':[[0, '#DE9A99'],[0.5,colors['background']], [1, '#289bcc']],
                                   'cmax':1,'cmin':-1},
                       )
    
    return fig


################################################################################################################################

def distr_hab(df,h1,h2):
    col = ['Levantamento', 'Pontos', 'Ponto de ataque', 'Tentativa de ataque', 'Ataques errados','Defesa',
           'Erros de recepção', 'Bloqueio duplo',  'Bloqueio simples', 'Erro de bloqueio', 'Aces', 'Saques errados']
    col.append('Sets jogados')

    r =  df.groupby(['team','dates','opponent'])['r'].max()
    nc = df.groupby(['team','dates','opponent'])[col].sum()
    nc = nc.reset_index(drop=False)
    nc['r']=r.values
    col = col[:-1]
    nc.loc[nc['r']==0,'vic']='Perdeu'
    nc.loc[nc['r']==1,'vic']='Ganhou'
    n = nc[nc['Sets jogados']>21]

    fig = make_subplots(rows=2, cols=2, shared_yaxes=True, shared_xaxes=True,column_widths=[0.7, 0.3],row_heights=[0.3, 0.7])
    #fig = go.Figure()

    #Add traces
    fig.add_trace(go.Scattergl(x=n[h1], y=n[h2],
                             customdata= n['vic'],
                             hovertemplate =
                                "%{xaxis.title.text}: %{x}<br>" +
                                "%{yaxis.title.text}: %{y}<br>" +
                                "%{customdata}"
                                "<extra></extra>",
                             mode='markers',
                             marker_color=n['r'],
                             marker_colorscale = [[0,'#E0534A'],[1,'#5160E0']],
                             showlegend=False
                             ),
                 2,1)
    fig.add_trace(go.Histogram(name='Perdeu o Jogo', x=n.loc[n['r']==0 ,h1], marker_color='#E0534A', opacity=0.8, showlegend=True),1,1)
    fig.add_trace(go.Histogram(name='Venceu o Jogo', x=n.loc[n['r']==1 ,h1], marker_color='#5160E0', opacity=0.8, showlegend=True),1,1)

    fig.add_trace(go.Histogram(name='Perdeu o Jogo', y=n.loc[n['r']==0 ,h2], marker_color='#E0534A', opacity=0.8, showlegend=False),2,2)
    fig.add_trace(go.Histogram(name='Venceu o Jogo', y=n.loc[n['r']==1 ,h2], marker_color='#5160E0', opacity=0.8, showlegend=False),2,2)
    fig.update_layout(barmode='overlay')


    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    fig.update_layout(
        width=580, height=580,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title=h1+' x '+h2,
    )
    fig.update_xaxes(title_text=h1, row=2, col=1)
    fig.update_yaxes(title_text=h2, row=2, col=1)
    
    return fig


##########################################################################################################################3####

def bar_teams(ds, columns, q_med):
    fig = go.Figure()
    
    df = ds.groupby('team').sum()

    if(q_med):
        med = rta[columns].sum()/rta['quant_jogos'].sum()
        texto = 'Média de todos os times'
    else:
        med = df[columns].sum()/df['quant_jogos'].sum()
        texto = 'Média dos times presentes'

    med.sort_values(ascending=False,inplace=True)
    columns = med.index.to_list()

    
    for i in range(len(columns)):
        column = columns[i]
        fig.add_trace(
            go.Bar(
                x = df.index.to_list(),
                y = df[column]/df['quant_jogos'],
                name = column,
                opacity=0.95,
                marker = dict(color = cores[column]),
                customdata = [column]*len(df['ano']),
                hovertemplate=
                        "<b>%{customdata}</b><br><br>" +
                        "Time: %{x}<br>"+
                        "Média de ocorrências por jogo: %{y:.2f}<br>" +
                        "<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                name='media '+column,
                x = df.index.to_list(),
                y = [med[i]]*len(df.index.to_list()),
                mode = "markers",
                line = dict(color='#000000',width=3),
                opacity=0.7,
                showlegend=False)
        )
        fig.add_trace(
            go.Scatter(
                name='media '+column,
                x = df.index.to_list(),
                y = [med[i]]*len(df.index.to_list()),
                mode = "lines+markers",
                line = dict(color=cores[column],width=2.6),
                opacity=0.65,     #dash='dash'
                showlegend=True,
                customdata = [column]*len(df.index.to_list()),
                hovertext = [texto]*len(df.index.to_list()),
                hovertemplate=
                        '%{hovertext}<br>'
                        "<b>%{customdata}</b>: %{y:.2f}" +
                        "<extra></extra>",
                )
        )


    fig.update_layout(
        xaxis_title='Times',
        yaxis_title='Quantidade média por jogo',
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        barmode='overlay'
        )
    
    return fig



###########################################################################################################################
###########################################################################################################################333



app = dash.Dash(__name__)
server = app.server
app.title='NCAA'

colors = {
    'background': '#F6FDFD',
    'text': '#19070B'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Analysis NCAA volleyball 2012-2019',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop': 20
        }
    ),
    html.H3(
        id='posi_div',
        children='Comparando as posições e suas funções.', 
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop': 30,
            'paddingDown': 30
    }),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Label('Selecione aquantidade que deseja ver:'),
                    dcc.Dropdown(
                        id = 'hab_p',
                        options = [{'label': i, 'value': i} for i in colunas],
                        value = colunas[1],
                        placeholder = 'Selecione o que deseja ver',
                        style={'width':400}
                    ),
                ], className="six columns"),
                html.Div([
                    html.Label('Ver por jogadora ou por jogo?'),
                    dcc.RadioItems(
                        id='por_jogo',
                        options=[{'label':'Jogo', 'value':1},
                                 {'label':'Jogadora', 'value':0}],
                        value=1,
                        style={'width':'auto'}),
                ], className="six columns",style={'width':300, 'marginLeft':50,'paddingTop':6})
            ],className="row" ,style={'width':750, 'marginLeft': 45, 'columnCount':2,'display':'flex'}),
            
            dcc.Graph(
                id='hab_posi',
                #figure=box_posi(ncaa,ataque[0],0)
            )
        ], className="six columns", style = {'width':750,'display': 'block'}),
        html.Div([
            html.Div([
                html.Div([
                    html.H4(
                        id='titulo_hab',
                        children='Habilidade',
                        style={'paddingLeft': 30,'color': '#224791'}
                    ),
                    html.Div(
                        id='expli_hab',
                        children='Explicação',
                        style={'paddingLeft':26, "color":colors['text'],'textAlign': 'justify', 'width':'80%'}
                    )],style={'height':'43%','paddingTop':5}
                ),
                html.Div([
                    html.H4(
                        id='titulo_pos',
                        children='Posição',
                        style={'paddingLeft': 30,'color': '#224791'}
                    ),
                    html.Div(
                        id='expli_pos',
                        children='Clique no boxplot de alguma das posições à esquerda para saber mais sobre ela.',
                        style={'paddingLeft':26, "color":colors['text'],'textAlign': 'justify', 'width':'80%'}
                    )],style={'height':'57%'}
                )
            ],style={'border': '1.8px solid #224791', 'borderRadius': '12px', 'width':340, 'height':360,
                'marginLeft': 'auto',  'marginRight': 'auto','marginUp': 'auto',  'marginDown': 'auto'}
            )
        ], className="six columns",style={'width':300,'paddingLeft':40,'display': 'inline-block'})
    ],className="row", style={'width': '90%','paddingLeft':20, 'display': 'flex','alignItems': 'center', 'columnCount':2}),


##################################################################################################################################
    html.H3(
        id='evolu_div',
        children='A evolução do time nos anos.', 
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop': 70,
            'paddingDown': 60
    }),
    html.Div([
        html.Div([
            html.Label('Selecione o time que deseja ver (digite para aparecer opções que se aproximem):'),
            dcc.Dropdown(
                id = 'times_opu',
                options = [{'label': 'Abilene Christian', 'value': 'Abilene Christian'}],
                searchable=True,
                value = 'Abilene Christian',
                placeholder = 'Selecione o time que deseja ver', 
                style={ 'maxHeight': '100px'}
            ),
            html.Div(style={'paddingTop':10}),
            html.Label('Mostrar a média do time?'),
            dcc.RadioItems(
                id='show_med',
                options=[{'label': 'Sim', 'value': 1},
                        {'label': 'Não', 'value': 0}],
                value=0,
                #labelStyle={'display': 'inline-block'}
        )], className="six columns",style={'width':'450px','marginLeft':90,'display': 'block'}),
        html.Div([
            html.Label('Selecione as habilidades que deseja ver:'),
            dcc.Dropdown(
                id='hab_visible',
                options=[{'label': extrass[i], 'value': i} for i in range(len(extras))],
                value=0,
                placeholder="Selecione um conjunto para exibir"
            ),
            html.Div(style={'paddingTop':10}),
            dcc.Dropdown(
                id='hab_unica',
                options=[{'label': i, 'value': i} for i in colunas],
                multi = True,
                placeholder="Selecione algumas habilidades para serem exibidas"
            )
            ], className="six columns",style={'width':'450px','display': 'inline-block','paddingLeft':15})
        ], className="row", style={'width': '90%', 'display': 'flex', 'marginLeft':60, 'columnCount':2}),
    #,'columnCount': 2
    html.Div([
    dcc.Graph(
        id='Grafico times por ano',
        figure=multi_plot(rta[rta['team']=='abilene-christian'],extras[0],0)
    )], style = dict(width='85%',marginLeft= 'auto',  marginRight= 'auto')
    ),

################################################################################################################################
    html.H3(children='Correlação entre habilidades',
                style={'textAlign':'center','paddingTop':50}),
    html.Div([
        html.Div([
            dcc.Graph(
                id='Correlacao',
                figure=corr_habs(ncaaj)
            )
        ],className="six columns",style = dict(width='85%',marginLeft=40)),
        html.Div([
            dcc.Graph(
                id='Relacao_hab',
                figure=distr_hab(ncaaj,'Pontos','Levantamento')
            )
        ],className="six columns" , style = dict(width='85%',marginLeft= 30,  marginRight= 'auto'))
    ],className="row", style={'width': '90%','paddingLeft':20, 'paddingDown':60, 'display': 'flex','alignItems': 'center', 'columnCount':2}
    ),
#################################################################################################################################
    html.Div([
        html.H3(
            children='Finalistas dos anos de 2012 a 2019',
            style={'paddingLeft':'30px',  'paddingTop':'30px'}),
        dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in vencedores.columns.to_list()],
        data=vencedores.to_dict('records'),
        css=[{
            'selector': '.dash-spreadsheet-container',
            'rule': 'border: 1px solid blue; border-radius: 15px; overflow: hidden;'
        }],
        style_table={
            'border': '3.3px #224791',
            'borderRadius': '12px',
            'width': 350,
        },
        style_cell={
            'textAlign': 'left',
            'backgroundColor': colors['background'],
            'color': colors['text'],
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'Placar da Final'},
                'textAlign': 'center'
            },
            {
                'if': {'column_id': 'Ano'},
                'width': '60px',
                'paddingLeft': '9px'
            }
        ],
        style_header={
            'backgroundColor': '#289bcc',
            },

        style_as_list_view=True,
        )
        ],style=dict(width=400,marginLeft= 'auto',  marginRight= 'auto', paddingTop= '30px')
        #],style={'paddingTop': 40, 'paddingDown':40 , 'paddingLeft': 80}
        ),


#####################################################################################################################################

    html.H3(
        id='compatime_div',
        children='cresceu', 
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop': 90,
            'paddingDown': 60
    }),
    html.Div([
    html.Div([
        html.Label('Selecione os times que deseja ver:'),
        dcc.Dropdown(
            id = 'times_op',
            options = [{'label': i, 'value': i} for i in b_teams],
            value = b_teams,
            searchable=True,
            placeholder = 'Selecione os times que deseja ver',
            multi = True
        ),
        html.Div(style={'paddingTop':10}),
        html.Label('Mostrar a média de todos os times ou apenas dos presentes no gráfico?'),
        dcc.RadioItems(
            id='qual_med',
            options=[{'label': 'Todos os times', 'value': 1},
                    {'label': 'Apenas os do gráfico', 'value': 0}],
            value=0,
        )], className="six columns",style={'width':'450px','marginLeft':90,'display': 'block'}),
    html.Div([
        html.Label('Selecione as habilidades que deseja ver:'),
        dcc.Dropdown(
            id='hab_visibles',
            options=[{'label': extrass[i], 'value': i} for i in range(1,len(extras))],
            value=2,
            placeholder="Selecione um conjunto para exibir"
        ),
        html.Div(style={'paddingTop':10}),
        dcc.Dropdown(
            id='hab_unicas',
            options=[{'label': i, 'value': i} for i in colunas],
            multi = True,
            placeholder="Selecione algumas habilidades para serem exibidas"
        )], className="six columns",style={'width':'450px','display': 'inline-block','paddingLeft':15}
        )], className="row", style={'width': '90%', 'display': 'flex', 'marginLeft':60, 'columnCount':2}),
    html.Div([
    dcc.Graph(
        id='Grafico times por hab',
        figure=bar_teams(rta[rta['team'].isin(b_teams)],extras[2],0)
    )], style = dict(width='85%',marginLeft= 'auto',  marginRight= 'auto')
    ),
    html.Div([
    dcc.RangeSlider(
        id = 'ano_bg',
        min = 2012,
        max = 2019,
        marks={i : str(i) for i in anos},

        value=[2012, 2019]
    )], style = dict(width='50%',marginLeft= 'auto',  marginRight= 'auto')
    ),

])

######################################################################################################################################
############################################################################################################################33333333####

@app.callback(
    [Output('hab_posi','figure'),
    Output('titulo_hab', 'children'),
    Output('expli_hab', 'children')],
    [Input('hab_p', 'value'),
    Input('por_jogo', 'value')])

def update_box(habilidade, por_jogo):
    return box_posi(ncaa,habilidade, por_jogo), habilidade, desc_hab[habilidade]

@app.callback(
    [Output('titulo_pos', 'children'),
    Output('expli_pos', 'children')],
    [Input('hab_posi', 'clickData')])
def display_click_data(clickData):
    
    if(clickData is None):
        raise PreventUpdate
    else:
        p = clickData['points'][0]['x']
        return p, desc_posi[p]

###################################################################################################################################

@app.callback(
    [Output('Grafico times por ano', 'figure'),
    Output('evolu_div', 'children')],
    [Input('hab_visible', 'value'),
    Input('hab_unica', 'value'),
    Input('show_med', 'value'),
    Input('times_opu', 'value')])

def update_graph(habs_visible, habs_unica, showt, time_es):
    if(habs_visible != None):
       habs = extras[int(habs_visible)]
    if(habs_unica):
       habs = habs_unica
    if(habs_unica and (habs_visible != None)):
       habs = extras[int(habs_visible)] + habs_unica
    if((not habs_unica) & (habs_visible==None)):
       habs = []
    habs = list(set(habs))
    if(time_es != None):
        time = re.sub("\s","-",time_es).lower()
        time = re.sub("\(|\)|\.|\?|&",'',time)
        return multi_plot(rta[rta['team'] == time],habs,showt), 'A evolução do time '+time_es+' nos anos'
    else:
        return multi_plot(rta[rta['team'] == ''],habs,showt), 'A evolução do time nos anos'   

@app.callback(
    Output("times_opu", "options"),
    [Input("times_opu", "search_value"),
    State("times_opu", "value")])

def update_options(search_value,value):
    if not search_value:
        if (not value):
            raise PreventUpdate
        return [
            o for o in t_times if o["value"] in value
        ]
    return [o for o in t_times if search_value.lower() in o["label"].lower()]


##################################################################################################################################

@app.callback(
    Output('Relacao_hab', 'figure'),
    [Input('Correlacao', 'clickData')])

def display_click_data(clickData):
    if(clickData is None):
        raise PreventUpdate
    else:
        h1 = clickData['points'][0]['x']
        h2 = clickData['points'][0]['y']
        return distr_hab(ncaaj,h1,h2)


###################################################################################################################################


@app.callback(
    [Output('Grafico times por hab', 'figure'),
    Output('compatime_div','children')],
    [Input('hab_visibles', 'value'),
    Input('hab_unicas', 'value'),
    Input('times_op', 'value'),
    Input('qual_med', 'value'),
    Input('ano_bg', 'value')])

def update_bgraph(habs_visible, habs_unica, times_escolhidos, q_med, min_max):
    if(habs_visible != None):
      habs = extras[int(habs_visible)]
    if(habs_unica):
      habs = habs_unica
    if(habs_unica and (habs_visible != None)):
      habs = extras[int(habs_visible)] + habs_unica
    if((not habs_unica) & (habs_visible==None)):
      habs = []
    habs = list(set(habs))
    anos_escolhidos = [i for i in anos if ((int(i) >= min_max[0])&(int(i) <= min_max[1]))]
    times=[]
    msg = 'Comparação dos times '
    for i in times_escolhidos:
        msg = msg + i +', '
        time = re.sub("\s","-",i).lower()
        time = re.sub("\(|\)|\.|\?|&",'',time)
        times.append(time)
    msg = msg[0:-2]+' do ano '+str(min_max[0])+' até '+str(min_max[1])
    return (bar_teams(rta[(rta['team'].isin(times))&(rta['ano'].isin(anos_escolhidos))],habs,q_med), msg)

@app.callback(
    Output('times_op', 'options'),
    [Input('times_op', 'search_value'),
    State('times_op', 'value')])

def update_times_options(search_value, value):
    if not search_value:
        return [
            o for o in t_times if o["value"] in value
        ]
    # Make sure that the set values are in the option list, else they will disappear
    # from the shown select list, but still part of the `value`.
    return [
        o for o in t_times if search_value.lower() in o["label"].lower() or o["value"] in (value or [])
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
