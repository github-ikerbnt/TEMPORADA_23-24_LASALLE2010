import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
from dash.dependencies import Input, Output

#---------------------------------------------------------------------------------------------

# Cargamos los datos
df = pd.read_csv("2021-2022 LASALLE2010B.csv", encoding='latin1', sep=";")
df=df.reset_index()
for index in df.index:
    df.loc[index, 'index'] += 1


data = {
    'Nombre': ["Ibai", "Ander", "Xabi", "Paul", "Adri", "Alazne", "Mikel", "Dori", "Ibon", "Pablo", "Arianna", "Urko", "Jonas"],
    'Goles': [29, 17, 16, 4, 3, 3, 1, 1, 1, 1, 1, 0, 0]
}
dff = pd.DataFrame(data)

#---------------------------------------------------------------------------------------------


# Definimos hoja de estilo externa
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Le asignamos la hoja de estilo a nuestra app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[{"name":"viewport", 
"content":"width=device-width, initial-scale=0.5, maximun-scale=1, minimum-scale=0.5,"}])
server=app.server

#---------------------------------------------------------------------------------------------
#CONTENIDO DE LA PAGINA

row1=html.Div([
            html.Div([html.Label('Selecciona el ranking de los equipos:'),
            dcc.RangeSlider(id="rango", min=df['index'].min(), max=df['index'].max(),
                             step=1, value=[1,9])])           
            ])


tab1=html.Div([dcc.Graph(id='g1')])

tab2=html.Div([dcc.Graph(id='g2')])

tab3=html.Div([
                html.Div([dcc.Graph(id='g3')], className='five columns'),


                html.Div([dash_table.DataTable(
                id = 'tabla',
                columns = [{'name': i, 'id':i} for i in df[['EQUIPO','G.FAVOR','G.CONTRA']].columns],
                data = df[['EQUIPO','G.FAVOR','G.CONTRA']].to_dict('records'),
                filter_action = 'native',
                sort_action = 'native',
                sort_mode='multi',
                page_size=10
                )], className='seven columns'),

                ], className='row')


# Definimos el layout
app.layout = html.Div([html.H1('LIGA 23-24 LASALLE2010'),
                       html.Img(src="https://raw.githubusercontent.com/github-ikerbnt/FOTOS-SHINY-2/main/lasallelogo.png", 
             height=145, width=300),
                # html.H6('Resumen temporada'),
                # html.Br(),
                       row1,
                              dcc.Tabs([
                            dcc.Tab(label='Boxplot de goles', children=tab1),
                            dcc.Tab(label='Goles favor/contra', children=tab2),
                            dcc.Tab(label='Distribución de goles', children=tab3)
                            ])
       ])


#---------------------------------------------------------------------------------------------

# Definimos el callback
@app.callback(
    [Output(component_id='g1', component_property='figure'),
     Output(component_id='g2', component_property='figure'),
     Output(component_id='g3', component_property='figure'),
     Output(component_id='tabla', component_property='data')],
    [Input(component_id='rango', component_property='value')]
)
# Función de actualización
def funcion_actualizacion(rango):
    df_filtro = df.copy()
    df_filtro = df_filtro[(df_filtro['index'] <= rango[1]) &
                          (df_filtro['index'] >= rango[0])]

    f1 = px.box(df_filtro, y="G.FAVOR", color="EQUIPO")
    f1.update_xaxes(showticklabels=False, title=None)
    f1.update_layout(title='Boxplot goles a favor equipos;')

    f2 = px.scatter(df_filtro, x="G.CONTRA", y="G.FAVOR", color="EQUIPO")
    f2.update_layout(title='Relación entre el Goles a favor/Goles en contra.')

    f3 = px.pie(dff, values=dff.groupby('Nombre')['Goles'].sum().sort_index(ascending=True),
                    names=sorted(dff["Nombre"].unique()), hole=0.45)
    f3.update_layout(title='Distribucion de goles del equipo.')
    f3.update_layout(annotations=[dict(text="GOLES A FAVOR", x=0.50, y=0.5, showarrow=False)])

    f4 = df_filtro[['EQUIPO', 'G.FAVOR', 'G.CONTRA']].to_dict('records')

    return f1, f2, f3, f4


#---------------------------------------------------------------------------------------------

# Ejecucción de la app
if __name__ == '__main__':
    app.run_server(debug=False)
