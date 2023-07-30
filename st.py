import streamlit as st  
import funciones as fn
import pandas as pd
import ast

movies = pd.read_csv(r"movies.csv")

#################### CABECERA ####################
st.markdown("# Sistema de Recomendación de Películas")

################# Distribución de las consultas ###############
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Recomendación de Pelis', 'Actor', 'Director', 'Mes y Día', 'Popularidad y Votos'])


########## Sistema de recomendación de película ##########
with tab1:
    titulos = movies['title'].values
    sel_peli = st.selectbox('Elige una película', titulos)
    recomendaciones = fn.recomendacion(sel_peli)
    st.write(recomendaciones)

########## Retorno y Cantidad de filmaciones por actor###########
with tab2:
    st.markdown("Retorno y cantidad de filmaciones de un actor")
    def get_actor_name(movies):
        """Iterar sobre cada fila del DataFrame,
        Convertir el string en una lista real,
        luego iterar sobre cada nombre en la lista de la fila, 
        luego verifica si el nombre ya está en la lista, si no
        está, se agrega, al final se retorna la lista"""
        name = []
    
        for row in movies['actor']:

            actor_list = ast.literal_eval(row)
            
            for actor_name in actor_list:
                
                if actor_name not in name:
                    
                    name.append(actor_name)
        return name

    actor = get_actor_name(movies)

    sel_actor = st.selectbox('Elige un actor', actor)
    view_actor = fn.get_actor(sel_actor)

    st.write(view_actor)

########## Mayor éxito de un director ###########
with tab3:
    st.markdown("Mayor éxito de un director?")
    director = movies['director'].values
    sel_dir = st.selectbox('Elige un director', director)
    view_dir = fn.get_director(sel_dir)

    st.write(view_dir)

###########Cantidad de filmaciones por mes y día###########
with tab4:
    st.markdown("Cantidad de filmaciones se estrenan por mes?")
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    sel_mes = st.selectbox('Elige un mes del año', meses)
    fil_mes = fn.cantidad_filmaciones_mes(sel_mes)

    st.write(fil_mes)

    st.markdown("Cantidad de filmaciones que se estrenan por día de la semana?")
    dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
    sel_dia = st.selectbox('Elige un día de la semana', dias)
    fil_dia = fn.cantidad_filmaciones_dia(sel_dia)
    st.write(fil_dia)

###########Votos y popularidad###########
with tab5:
    st.markdown("Popularidad y rating de título favorito?")
    sel_peli2 = st.selectbox('Elige tu película favorita', titulos)
    film_scor = fn.score_titulo(sel_peli2)
    film_vote = fn.votos_titulo(sel_peli2)
    st.write(film_scor,film_vote)


