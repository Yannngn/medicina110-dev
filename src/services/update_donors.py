import json
import os

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from pandas.api.types import is_numeric_dtype

# --- CONFIGURAÇÕES ---
# Nome da planilha no Google Drive
GOOGLE_SHEET_NAME = "Livro de Ouro - Turma de Medicina UFPB 110 (respostas)"
# Nome da aba/worksheet dentro da planilha
WORKSHEET_NAME = "Respostas ao formulário 1"
# Número de doadores para as listas de "maiores" e "últimos"
TOP_N_DONORS = 10
LATEST_N_DONORS = 10
# Faixa de tamanho da fonte para a nuvem de palavras (min, max)
FONT_SIZE_RANGE = (12, 64)
# Arquivo de saída
OUTPUT_JSON_PATH = "donors.json"


def setup_gspread_credentials():
    """
    Configura as credenciais do Google Sheets a partir da variável de ambiente.
    Retorna o cliente gspread autenticado.
    """
    credentials_json = os.getenv("GSPREAD_PANDAS_CONFIG")
    if not credentials_json:
        raise ValueError("GSPREAD_PANDAS_CONFIG environment variable not found")

    # Parse the JSON credentials
    import json

    credentials_dict = json.loads(credentials_json)

    # Define the required scopes for Google Sheets and Drive
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]

    # Create credentials with proper scopes and authorize gspread client
    credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
    gc = gspread.authorize(credentials)

    print("Credenciais do Google configuradas com sucesso.")
    return gc


def main():
    """
    Função principal que orquestra o processo de busca, processamento
    e salvamento dos dados de doadores.
    """
    print("Iniciando o processo de atualização de dados dos doadores...")

    try:
        # --- 0. CONFIGURAÇÃO DAS CREDENCIAIS ---
        gc = setup_gspread_credentials()

        # --- 1. AUTENTICAÇÃO E BUSCA DE DADOS ---
        # Abre a planilha e acessa a worksheet específica
        print(f"Acessando a planilha: '{GOOGLE_SHEET_NAME}'")
        spreadsheet = gc.open(GOOGLE_SHEET_NAME)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

        # Obtém todos os dados como lista de dicionários
        records = worksheet.get_all_records()

        # Converte para DataFrame do Pandas
        df = pd.DataFrame(records)
        print(f"Foram encontradas {len(df)} linhas na planilha.")

        if df.empty:
            print("A planilha está vazia. Gerando arquivo JSON vazio.")
            create_empty_json()
            return

        # --- 2. LIMPEZA E VALIDAÇÃO DOS DADOS ---
        # Garante que as colunas essenciais existem
        required_cols = [
            "Carimbo de data/hora",
            "Nome",
            "Valor",
        ]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(
                "A planilha não contém as colunas necessárias: " + str(required_cols)
            )

        # Remove linhas onde o nome do doador ou o valor da doação estão vazios
        df.dropna(subset=required_cols, inplace=True)

        # Remove linhas onde os campos de texto estão vazios (apenas espaços em branco)
        for col in ["Nome"]:
            if col in df.columns and df[col].dtype == "object":
                df = df[df[col].astype(str).str.strip() != ""]

        # Converte 'Valor' para numérico, tratando erros
        df["Valor"] = df["Valor"].astype(str).str.replace(",", ".")
        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

        # Valida se a coluna é numérica após a conversão
        if not is_numeric_dtype(df["Valor"]):
            raise TypeError(
                "A coluna 'Valor' não pôde ser convertida para um tipo numérico."
            )

        # Remove linhas onde a conversão falhou (resultando em NaT)
        df.dropna(subset=["Valor"], inplace=True)

        # Garante que 'Carimbo de data/hora' seja do tipo datetime para ordenação
        df["Carimbo de data/hora"] = pd.to_datetime(
            df["Carimbo de data/hora"], errors="coerce"
        )
        df.dropna(subset=["Carimbo de data/hora"], inplace=True)

        print(f"Após limpeza e validação, restaram {len(df)} doações válidas.")

        if df.empty:
            print(
                "Nenhuma doação válida encontrada após a limpeza. Gerando arquivo JSON vazio."
            )
            create_empty_json()
            return

        # --- 3. PROCESSAMENTO E AGREGAÇÃO ---
        # Agrega doações pelo nome do doador para somar os valores totais
        # Remove a coluna 'Carimbo de data/hora' antes de agregar
        donors_no_timestamp = df.drop(columns=["Carimbo de data/hora"])
        aggregated_donors: pd.DataFrame = donors_no_timestamp.groupby(
            "Nome", as_index=False
        ).sum()
        print(f"Foram encontrados {len(aggregated_donors)} doadores únicos.")

        # --- 4. GERAÇÃO DAS LISTAS ---
        # Lista dos Maiores Doadores (baseado nos valores agregados)
        top_donors_df: pd.DataFrame = aggregated_donors.nlargest(TOP_N_DONORS, "Valor")
        top_donors_list = [
            {"name": row["Nome"], "amount": row["Valor"]}
            for index, row in top_donors_df.iterrows()
        ]

        # Lista dos Últimos Doadores (baseado no Carimbo de data/hora, pegando doadores únicos)
        latest_donors_df: pd.DataFrame = (
            df.sort_values(by="Carimbo de data/hora", ascending=False)
            .drop_duplicates(subset=["Nome"])
            .head(LATEST_N_DONORS)
        )
        latest_donors_list = [
            {"name": row["Nome"], "amount": row["Valor"]}
            for index, row in latest_donors_df.iterrows()
        ]

        # --- 5. NORMALIZAÇÃO DE PESOS PARA A NUVEM DE PALAVRAS (TIERED) ---
        # Ordena doadores por Valor (maior para menor)
        sorted_donors = aggregated_donors.sort_values(
            by="Valor", ascending=False
        ).reset_index(drop=True)
        weights = []
        for idx in range(len(sorted_donors)):
            if idx == 0:
                weights.append(5)
            elif idx < 4:
                weights.append(4)
            elif idx < 10:
                weights.append(3)
            elif idx < 20:
                weights.append(2)
            else:
                weights.append(1)
        sorted_donors["weight"] = weights

        # Prepara os dados para a nuvem de palavras no formato {text, value}
        word_cloud_data = [
            {"text": row["Nome"], "value": row["weight"]}
            for index, row in sorted_donors.iterrows()
        ]

        # --- 6. ESTRUTURAÇÃO E SALVAMENTO DO JSON FINAL ---
        final_json_data = {
            "wordCloud": word_cloud_data,
            "topDonors": top_donors_list,
            "latestDonations": latest_donors_list,
        }

        with open("public/" + OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(final_json_data, f, ensure_ascii=False, indent=4)

        print(f"Arquivo '{OUTPUT_JSON_PATH}' gerado com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        # Em caso de erro, cria um arquivo JSON vazio para não quebrar o site
        create_empty_json()
        raise e


def create_empty_json():
    """Cria um arquivo JSON vazio com a estrutura esperada pelo frontend."""
    empty_data = {"wordCloud": [], "topDonors": [], "latestDonations": []}
    with open("public/" + OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(empty_data, f, ensure_ascii=False, indent=4)
    print(f"Arquivo '{OUTPUT_JSON_PATH}' vazio foi criado como fallback.")


if __name__ == "__main__":
    main()
