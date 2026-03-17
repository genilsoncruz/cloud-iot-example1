import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.title("Dashboard IoT - Monitoramento Ambiental")

st.write("Análise de dados coletados por sensores IoT")

# -------------------------
# CARREGAR DADOS
# -------------------------

@st.cache_data
def load_data():

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRU9yDHhvmNRpfNT8PJ0t5_WBmqL_Z5pSKgj1-afLSWksO_Kb3Cxdf6Pa7HOV02xMg5gQf8XnagZZ0/pub?gid=0&single=true&output=csv"

    df = pd.read_csv(url, decimal=',')

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


df = load_data()

st.subheader("Dados coletados")

st.dataframe(df)

# -------------------------
# GRÁFICOS
# -------------------------

st.subheader("Temperatura ao longo do tempo")

fig, ax = plt.subplots()

ax.plot(df["timestamp"], df["temperatura"])

ax.set_xlabel("Tempo")
ax.set_ylabel("Temperatura")

st.pyplot(fig)

# -------------------------
# ESTATÍSTICAS
# -------------------------

st.subheader("Estatísticas")

st.write(df.describe())

# -------------------------
# TREINAMENTO DO MODELO
# -------------------------

df["time_index"] = np.arange(len(df))

X = df[["time_index"]]
y = df["temperatura"]

model = LinearRegression()
model.fit(X, y)

# -------------------------
# PREVISÃO
# -------------------------

future_steps = st.slider("Passos no futuro para previsão", 1, 50, 10)

future_index = np.arange(len(df), len(df) + future_steps).reshape(-1,1)

predictions = model.predict(future_index)

st.subheader("Previsão de temperatura")

pred_df = pd.DataFrame({
    "tempo_futuro": range(future_steps),
    "temperatura_prevista": predictions
})

st.dataframe(pred_df)

# -------------------------
# ALERTA DE CONFORTO
# -------------------------

limite = 30

if predictions.mean() > limite:
    st.error("⚠️ Possível desconforto térmico previsto!")
else:
    st.success("Ambiente dentro da faixa confortável.")

# -------------------------
# GRÁFICO COM PREVISÃO
# -------------------------

fig2, ax2 = plt.subplots()

ax2.plot(df["time_index"], df["temperatura"], label="Histórico")

ax2.plot(
    range(len(df), len(df) + future_steps),
    predictions,
    label="Previsão",
)

ax2.legend()

st.pyplot(fig2)
