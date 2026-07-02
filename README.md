# Cobertura Vacinal no Brasil: Análise Regional e Temporal

> Análise da evolução da cobertura vacinal infantil no Brasil, identificando desigualdades regionais e possíveis fatores associados à queda pós-pandemia.

## 📌 Contexto

A cobertura vacinal infantil no Brasil vem apresentando queda nos últimos anos, especialmente após a pandemia de COVID-19. Este projeto investiga:

- Como a cobertura vacinal evoluiu por estado/região entre 2013 e 2022
- Quais vacinas tiveram as quedas mais acentuadas
- Se há correlação entre cobertura vacinal e indicadores socioeconômicos municipais

## 🎯 Perguntas de negócio

1. Quais estados apresentam menor cobertura vacinal hoje?
2. A queda foi generalizada ou concentrada em regiões específicas?
3. Existe relação entre cobertura vacinal e indicadores de desenvolvimento?

## 📊 Principais insights

- **Queda generalizada, mas desigual entre vacinas**: a Tríplice viral teve a maior queda entre 2019 e 2022 (-12,4 p.p., de 93,1% para 80,7%), seguida pela Poliomielite (-7,0 p.p.). BCG e Pentavalente, por outro lado, tiveram leve recuperação no período.

- **Desigualdade regional se aprofundou**: Roraima (-17,0 p.p.), Paraíba (-14,4 p.p.) e Amapá (-14,3 p.p.) tiveram as maiores quedas de cobertura vacinal média entre 2019 e 2022.

- **Nem todo estado seguiu a tendência de queda**: Piauí (+10,4 p.p.), Distrito Federal (+6,9 p.p.) e Sergipe (+4,2 p.p.) melhoraram no mesmo período — sugerindo que a queda não foi uniforme nem inevitável.

- **Situação crítica em 2022**: Amapá (64,2%), Rio de Janeiro (65,0%) e Roraima (68,2%) têm hoje a menor cobertura vacinal média entre as vacinas analisadas, distantes da meta ideal de 95% recomendada pela OMS/PNI.

## 🖼️ Dashboard

![Evolução temporal da cobertura vacinal](dashboard/grafico_evolucao_temporal.png)

![Variação por estado (2019-2022)](dashboard/grafico_ranking_estados.png)

![Mapa de cobertura vacinal por estado](dashboard/mapa_cobertura_2022.png)

## 🗂️ Fontes de dados

| Fonte | Descrição | Link |
|---|---|---|
| DATASUS/TabNet | Cobertura vacinal por estado/ano | http://tabnet.datasus.gov.br |

## 🛠️ Tecnologias

- Python (Pandas, Matplotlib, Seaborn, Plotly)
- SQL (SQLite)

## 📁 Estrutura do projeto