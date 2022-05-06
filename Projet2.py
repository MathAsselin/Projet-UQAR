import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Calculatrice de Planification financière")

st.title("Calculatrice de Planification financière")

st.header("**Revenu par mois**")
st.subheader("Salaire et imposition")
colSalaireAnnuel, coltaxe = st.columns(2)

with colSalaireAnnuel:
    salaire = st.number_input("Entrer votre salaire annuel($) : ", min_value=0.0, format='%f')
with coltaxe:
    taxe_taux = st.number_input("Entrer votre taux d'imposition(%): ", min_value=0.0, format='%f')

taxe_taux = taxe_taux / 100.0
salaire_après_taxes = salaire * (1 - taxe_taux)
salaire_mensuel_ai = round(salaire_après_taxes / 12.0, 2)

st.header("**Dépenses mensuelles**")
colDépenses1, colDépenses2 = st.columns(2)

with colDépenses1:
    st.subheader("Loyer mensuel")
    loyer_mensuel = st.number_input("Entrer votre loyer mensuel($): ", min_value=0.0,format='%f' )

    st.subheader("Budget pour manger quotidien")
    Quot_manger = st.number_input("Entrer votre budget pour manger au quotidien ($): ", min_value=0.0,format='%f' )
    manger_mensuel = Quot_manger * 30

    st.subheader("Dépenses imprévues mensuelles")
    mensuelles_imprévus = st.number_input("Entrer vos dépenses imprévues mensuelles ($): ", min_value=0.0,format='%f' ) 

with colDépenses2:
    st.subheader("transport mensuel")
    transport_mensuel = st.number_input("Entrer vos frais de transport mensuels($): ", min_value=0.0,format='%f' )   

    st.subheader("Dépenses de base mensuelles")
    base_mensuel = st.number_input("Entrer vos dépenses de base mensuelles ($): ", min_value=0.0,format='%f' )

    st.subheader("Dépenses de divertissement mensuel")
    divertissement_mensuel = st.number_input("Entrer vos dépenses de divertissement mensuels ($): ", min_value=0.0,format='%f' )   

dépenses_mensuelles = loyer_mensuel + manger_mensuel + transport_mensuel + divertissement_mensuel + base_mensuel + mensuelles_imprévus
épargnes_mensuelles = salaire_mensuel_ai - dépenses_mensuelles 

st.header("**Épargnes**")
st.subheader("Salaire mensuel moyen, après impot: $" + str(round(salaire_mensuel_ai,2)))
st.subheader("Dépenses mensuelles: $" + str(round(dépenses_mensuelles, 2)))
st.subheader("Épargnes mensuelles: $" + str(round(épargnes_mensuelles, 2)))

st.markdown("---")

st.header("**Pévisions concernant les Épargnes**")
colPrévisions1, colPrévisions2 = st.columns(2)
with colPrévisions1:
    st.subheader("Prévision annuelle")
    Prévision_annuelle = st.number_input("Entrer vos prévisions annuelles (Min 1 an): ", min_value=0,format='%d')
    prévisions_mensuelles = Prévision_annuelle*12

    st.subheader("Taux d'inflation annuelle")
    inflation_annuelle = st.number_input("Entrer le taux d'inflation annuelle(%): ", min_value=0.0,format='%f')
    inflation_mensuelle = (1+inflation_annuelle)**(1/12) - 1
    prévision_inflation_cumul = np.cumprod(np.repeat(1 + inflation_mensuelle, prévisions_mensuelles))
    prévisions_dépenses = dépenses_mensuelles*prévision_inflation_cumul
with colPrévisions2:
    st.subheader("Taux de croissance annuelle du salaire")
    croissance_annuelle = st.number_input("Entrer votre augmentation salariale prévu en pourcentage (%): ", min_value=0.0,format='%f')
    croissance_mensuelle = (1 + croissance_annuelle) ** (1/12) - 1
    croissance_salaire_cumul = np.cumprod(np.repeat(1 + croissance_mensuelle, prévisions_mensuelles))
    salaire_prévu = salaire_mensuel_ai * croissance_salaire_cumul 

économie_prévu = salaire_prévu - prévisions_dépenses 
économie_total = np.cumsum(économie_prévu)

x_values = np.arange(Prévision_annuelle + 1)

fig = go.Figure()
fig.add_trace(
        go.Scatter(
            x=x_values, 
            y=salaire_prévu,
            name="Prévisions salariales"
        )
    )

fig.add_trace(
        go.Scatter(
            x=x_values,
            y=prévisions_dépenses,
            name= "Dépenses prévues"
        )
    )

fig.add_trace(
        go.Scatter(
                x=x_values, 
                y=économie_total,
                name= "Épargnes Prévues"
            )
    )
fig.update_layout(title="Prévision pour: salaire, dépenses & épargnes dans le futur",
                   xaxis_title='Année',
                   yaxis_title='montant($)')

st.plotly_chart(fig, use_container_width=True)