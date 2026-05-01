import Config as cfg
import os
from datetime import datetime, timedelta
from Libs import retry

class ExcluirArquivos():
    arquivos_excluidos = []
    total_arquivos     = 0

    def __init__(self, dias_limite: int = 15):
        self.caminho = cfg.Local.caminho
        self.data_limite = (datetime.now() - timedelta(days=dias_limite)).strftime("%d-%m-%Y")
        cfg.log.info(f"Data limite para exclusão: {self.data_limite}")
    
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
                    
                    self.total_arquivos += 1

                    if os.path.isfile(caminho_arquivo):
                        data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo)).date()
                        
                        if data_modificacao < data_limite_dt:
                            os.remove(caminho_arquivo)
                            try:
                                cfg.log.info(f"{t*2}Arquivo '{arquivo}' excluído com sucesso.")
                                self.arquivos_excluidos.append(caminho_arquivo)
                                
                            except PermissionError:
                                cfg.log.error(f"{t*2}Erro ao excluir '{arquivo}': Arquivo está em uso por outro processo.")
                            except Exception as e:
                                cfg.log.error(f"{t*2}Erro ao excluir '{arquivo}': {e}")

    def gerar_relatorio_txt(self, pasta_caminho: str = "./temp", file: str = "relatorio_exclusao.txt"):
        if not os.path.exists(pasta_caminho):
            os.makedirs(pasta_caminho)

        caminho_arquivo = os.path.join(pasta_caminho, file)

        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            # Cabeçalho Estilizado
            f.write("="*60 + "\n")
            f.write("RELATÓRIO DE EXCLUSÃO DE ARQUIVOS\n")
            f.write("="*60 + "\n\n")

            # Seção de Metadados Alinhada
            f.write(f"{'Data do Relatório:':<30} {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"{'Data Limite para Exclusão:':<30} {self.data_limite.replace('-', '/')}\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'Total de Arquivos Analisados:':<30} {self.total_arquivos}\n")
            f.write(f"{'Total de Arquivos Excluídos:':<30} {len(self.arquivos_excluidos)}\n")
            f.write("-" * 60 + "\n\n")

            # Seção de Detalhes
            f.write("DETALHAMENTO DOS ARQUIVOS:\n")
            if not self.arquivos_excluidos:
                f.write(">>> Nenhum arquivo foi excluído no período informado.\n")
            else:
                for i, arquivo in enumerate(self.arquivos_excluidos, 1):
                    f.write(f"{arquivo}\n")
            
            f.write("="*60 + "\n")
            f.write("FIM DO RELATÓRIO\n")
            f.write("="*60 + "\n")

        cfg.log.info(f"Relatório de exclusão criado em: {caminho_arquivo}")
        