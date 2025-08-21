#Dataset

import pandas as pd
import numpy as np
import random

clientes = []
consultor = []
data_ativação = []
data_cancelamento = []
csat = []
motivo_cancelamento = []
status = []

for i in range(1000):
    clientes.append(f'Cliente_{i+1}')
    consultor.append(random.choice(['Consultor_A', 'Consultor_B', 'Consultor_C']))
    data_ativação.append(pd.Timestamp('2023-01-01') + pd.Timedelta(days=random.randint(0, 365)))
    
    if random.random() < 0.2:  # 20% chance of cancellation
        status.append('Cancelado')
        data_cancelamento.append(data_ativação[-1] + pd.Timedelta(days=random.randint(1, 30)))
        csat.append(random.uniform(1, 5))  # CSAT score between 1 and 5
        motivo_cancelamento.append(random.choice(['Motivo_A', 'Motivo_B', 'Motivo_C']))
    else:
        status.append('Ativo')
        data_cancelamento.append(None)
        csat.append(random.uniform(3, 5))  # CSAT para clientes ativos
        motivo_cancelamento.append(None)

data = {
    'Cliente': clientes,
    'Consultor': consultor,
    'Data_Ativação': data_ativação,
    'Data_Cancelamento': data_cancelamento,
    'CSAT': csat,
    'Motivo_Cancelamento': motivo_cancelamento,
    'Status': status
}

df = pd.DataFrame(data) 

print(df.head())
df.to_csv('clientes_data.csv', index=False)  # Save to CSV file