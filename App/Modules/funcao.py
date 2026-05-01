import Config as cfg
import os
from datetime import datetime, timedelta
from Libs import retry

class ExcluirArquivos():
    def __init__(self, dias_limite: int = 15):
        self.caminho = cfg.Local.caminho
        self.data_limite = (datetime.now() - timedelta(days=dias_limite)).strftime("%d-%m-%Y")
    
    @retry
    def excluir(self, caminhos: list = None, data_limite: str = None):
        """Exclui arquivos modificados antes da data limite.
        
        Args:           
            data_limite (str, optional): Data limite no formato 'DD-MM-YYYY'.
        """
        if not caminhos:
            caminhos = [self.caminho]
        
        if not isinstance(caminhos, list):
            caminhos = [caminhos]

        if data_limite:
            self.data_limite = data_limite

        for caminho in caminhos:
            try:
                data_limite_dt = datetime.strptime(self.data_limite, "%d-%m-%Y").date()
            except ValueError:
                cfg.log.error(f"Data limite '{self.data_limite}' está em formato inválido. Use 'DD-MM-YYYY'.")
                return
            t = '    '
            pastas_analisar   = [caminho]
            pastas_analisadas = []

            while True:
                if pastas_analisar == []:
                    break

                pasta = pastas_analisar.pop(0)
                pastas_analisadas.append(pasta)

                arquivos = os.listdir(pasta)
                cfg.log.info(f"{t}Analisando pasta: {pasta} | Arquivos encontrados: {len(arquivos)}")

                for arquivo in arquivos:
                    caminho_arquivo = os.path.join(pasta, arquivo)

                    if os.path.isdir(caminho_arquivo):
                        pastas_analisar.append(caminho_arquivo)
                        cfg.log.info(f"{t*2}Pasta '{arquivo}' adicionada para análise.")
                        continue

                    if os.path.isfile(caminho_arquivo):
                        data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo)).date()
                        
                        if data_modificacao < data_limite_dt:
                            os.remove(caminho_arquivo)
                            try:
                                cfg.log.info(f"{t*2}Arquivo '{arquivo}' excluído com sucesso.")
                            except PermissionError:
                                cfg.log.error(f"{t*2}Erro ao excluir '{arquivo}': Arquivo está em uso por outro processo.")
                            except Exception as e:
                                cfg.log.error(f"{t*2}Erro ao excluir '{arquivo}': {e}")

                        