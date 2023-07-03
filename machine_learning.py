import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Carregar o arquivo CSV
df = pd.read_csv('/data/patients.csv')

# Separar a coluna 'blood_pressure' em duas colunas: 'systolic_pressure' e 'diastolic_pressure'
df[['systolic_pressure', 'diastolic_pressure']] = df['blood_pressure'].str.split('/', expand=True)

# Remover a coluna original 'blood_pressure'
df = df.drop('blood_pressure', axis=1)

# Definir os dados de entrada (features) e saída (labels)
X = df[['temperature', 'systolic_pressure', 'diastolic_pressure']].astype(float)
y = df['high_risk']

# Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo de Regressão Logística
model = LogisticRegression()
model.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
y_pred = model.predict(X_test)

# Avaliar o desempenho do modelo
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Imprimir as métricas de desempenho
print(f'Acurácia: {accuracy}')
print(f'Precisão: {precision}')
print(f'Recall: {recall}')
print(f'F1-score: {f1}')
