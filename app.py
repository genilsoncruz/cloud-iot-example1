import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.title("Dashboard IoT - Monitoramento Ambiental")

# -------------------------
# CONFIGURAÇÃO DE ATUALIZAÇÃO
# -------------------------

# Adicionando um botão na lateral para resetar o cache
if st.sidebar.button("🔄 Atualizar Dados do Google Sheets"):
    st.cache_data.clear()
    st.rerun()

st.write("Análise de dados coletados por sensores IoT")

# -------------------------
# CARREGAR DADOS
# -------------------------

# ttl=60 define que o cache expira sozinho a cada 60 segundos (opcional)
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTRU9yDHhvmNRpfNT8PJ0t5_WBmqL_Z5pSKgj1-afLSWksO_Kb3Cxdf6Pa7HOV02xMg5gQf8XnagZZ0/pub?gid=0&single=true&output=csv"
    
    # Lendo os dados
    df = pd.read_csv(url)
    
    # Tratamento de decimais e datas
    # (Ajustei para garantir que a conversão ocorra mesmo com strings)
    df["temperatura"] = df["temperatura"].replace(',', '.', regex=True).astype(float)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    return df

df = load_data()

# -------------------------
# INTERFACE PRINCIPAL
# -------------------------

st.subheader("Dados coletados")
st.dataframe(df)

# -------------------------
# GRÁFICOS
# -------------------------

st.subheader("Temperatura ao longo do tempo")
fig, ax = plt.subplots()
ax.plot(df["timestamp"], df["temperatura"], marker='o', linestyle='-')
ax.set_xlabel("Tempo")
ax.set_ylabel("Temperatura")
plt.xticks(rotation=45)
st.pyplot(fig)

# -------------------------
# ESTATÍSTICAS
# -------------------------

st.subheader("Estatísticas")
st.write(df.describe())

# -------------------------
# TREINAMENTO DO MODELO
# -------------------------

# Criando um índice numérico para a regressão
df["time_index"] = np.arange(len(df))

X = df[["time_index"]]
y = df["temperatura"]

model = LinearRegression()
model.fit(X, y)

# -------------------------
# PREVISÃO
# -------------------------

st.divider()
st.subheader("Previsão de Tendência")

future_steps = st.slider("Passos no futuro para previsão", 1, 50, 10)

# Criando índices futuros
last_index = df["time_index"].iloc[-1]
future_index = np.arange(last_index + 1, last_index + 1 + future_steps).reshape(-1, 1)

predictions = model.predict(future_index)

# Exibindo tabela de previsão
pred_df = pd.DataFrame({
    "passo_futuro": range(1, future_steps + 1),
    "temperatura_prevista": predictions
})
st.dataframe(pred_df)

# -------------------------
# ALERTA DE CONFORTO
# -------------------------

limite = 30
if predictions.mean() > limite:
    st.error(f"⚠️ Alerta: Média prevista ({predictions.mean():.2f}°C) acima do limite de {limite}°C!")
else:
    st.success(f"Ambiente estável. Média prevista: {predictions.mean():.2f}°C.")

# -------------------------
# GRÁFICO COM PREVISÃO
# -------------------------

fig2, ax2 = plt.subplots()
# Histórico
ax2.plot(df["time_index"], df["temperatura"], label="Histórico", color="blue")
# Previsão
ax2.plot(
    range(last_index + 1, last_index + 1 + future_steps),
    predictions,
    label="Previsão (Regressão)",
    color="red",
    linestyle="--"
)

ax2.set_xlabel("Índice de Leitura")
ax2.set_ylabel("Temperatura")
ax2.legend()
st.pyplot(fig2)
