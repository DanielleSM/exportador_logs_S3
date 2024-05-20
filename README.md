
### README.md

# Exportador de Logs do CloudWatch para S3

Este script facilita a exportação de logs do AWS CloudWatch para um bucket S3. Ele itera pelos grupos de logs especificados, exporta logs dentro de um intervalo de tempo definido e armazena-os em um bucket S3 designado.

## Índice

- [Visão Geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)


## Visão Geral

O script automatiza o processo de exportação de logs do AWS CloudWatch para um bucket S3. Ele lida com múltiplos clientes e prefixos de grupos de logs, exportando logs dentro de intervalos de tempo especificados. O script utiliza a SDK Boto3 da AWS para interação com os serviços da AWS.

## Pré-requisitos

- Python 3.x
- Biblioteca Boto3
- Credenciais AWS com permissões necessárias

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/exportador-logs-cloudwatch.git
   cd exportador-logs-cloudwatch
   ```

2. Instale as dependências necessárias:
   ```bash
   pip install boto3
   ```

## Configuração

1. **Credenciais AWS**: Certifique-se de ter sua chave de acesso AWS, chave secreta e token de sessão (se aplicável). Você pode definir essas variáveis no ambiente ou diretamente no script.

2. **Configuração do Script**:
   - Defina a variável `destination_bucket` com o nome do seu bucket S3 de destino.
   - Configure a lista `CLIENTS` com as informações apropriadas dos clientes, intervalos de datas e prefixos dos grupos de logs.
   - Certifique-se de que o `region_name` na configuração do `boto3.client` corresponda à sua região AWS.

### Exemplo de Configuração:
```python
destination_bucket = 'logs-lambdas-ps'
AWS_ACCESS_KEY_ID = "sua-chave-de-acesso"
AWS_SECRET_ACCESS_KEY = "sua-chave-secreta"
AWS_SESSION_TOKEN = "seu-token-de-sessao"

CLIENTS = [
    {
        'client': 'cliente1', 
        'from_date': '2022-01-01', 
        'to_date': '2024-01-05', 
        'log_groups_prefixes': ['/aws/lambda/altu-cliente1-prod','/aws/lambda/altu-cliente1-dev']
    },
]
```

## Uso

1. **Execute o Script**:
   ```bash
   python export_logs.py
   ```

2. **O script irá**:
   - Listar todos os grupos de logs com base nos prefixos fornecidos.
   - Exportar logs dentro do intervalo de datas especificado.
   - Monitorar continuamente as tarefas de exportação em andamento e iniciar novas tarefas conforme as tarefas são concluídas.

3. **Modificando o Intervalo de Espera (Sleep)**
   
Se desejar modificar o intervalo de espera entre as verificações de tarefas de exportação em andamento, você pode alterar o valor do sleep dentro do loop principal do script.
```python
while True:
    # ...código anterior...
    print(f"Tem task ainda rodando...")
    time.sleep(60) 
```
Modifique o valor '60' para o número de segundos desejado. Isso ajustará o intervalo entre as verificações de tarefas de exportação em andamento, conforme necessário.

4. **Modificando o Nome da Tarefa**
   
O nome da tarefa (task_name) é gerado automaticamente no script com base nos valores das variáveis client, log_group, from_unix e to_unix. Caso deseje alterar o nome da tarefa para outro valor de sua escolha, você pode modificar a linha correspondente no script.

```python
task_name = f'cloudwatch_s3_logs_{client}_{log_group}_{from_unix}_{to_unix}'.replace('/', '_').replace('-', '_')
```
Substitua pelo nome desejado para a sua tarefa.



### Fluxo do Script:
1. **Listar Grupos de Logs**: Usa o paginador `describe_log_groups` para recuperar grupos de logs com base nos prefixos.
2. **Tarefas de Exportação**: Para cada grupo de logs, cria uma tarefa de exportação para transferir logs para o bucket S3.
3. **Gerenciamento de Tarefas**: Monitora as tarefas de exportação em andamento para garantir que não haja sobreposição ou tarefas redundantes.
