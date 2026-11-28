import Config as cfg
import os
import shutil
from datetime import datetime, timedelta
from Libs import retry

class ExcluirArquivos():
    def __init__(self, dias_limite: int = 15):
        self.caminho = cfg.Local.caminho
        self.data_limite = (datetime.now() - timedelta(days=dias_limite)).strftime("%d-%m-%Y")
        self.arquivos_excluidos = []
        self.total_arquivos = 0
        self.total_bytes_excluidos = 0
        self.espaco_livre_antes = None
        self.total_megas_liberados = 0
        self.total_megas_pasta = 0

        cfg.log.info(f"Data limite para exclusão: {self.data_limite}")

    def _formatar_tamanho(self, tamanho_bytes: int) -> str:
        """Converte bytes para MB (ou GB se for maior que 1024 MB)."""
        megas = tamanho_bytes / (1024 * 1024)
        if megas >= 1024:
            return f"{megas / 1024:.2f} GB"
        return f"{megas:.2f} MB"

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

        # Captura o espaço livre no disco ANTES de iniciar as exclusões
        if self.espaco_livre_antes is None and os.path.exists(caminhos[0]):
            self.espaco_livre_antes = shutil.disk_usage(caminhos[0]).free

        for caminho in caminhos:
            try:
                data_limite_dt = datetime.strptime(self.data_limite, "%d-%m-%Y").date()
            except ValueError:
                cfg.log.error(f"Data limite '{self.data_limite}' está em formato inválido. Use 'DD-MM-YYYY'.")
                return

            t = '    '
            pastas_analisar = [caminho]
            pastas_analisadas = []

            while pastas_analisar:
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
                            try:
                                tamanho_arquivo = os.path.getsize(caminho_arquivo)
                                os.remove(caminho_arquivo)
                                
                                self.total_bytes_excluidos += tamanho_arquivo
                                self.arquivos_excluidos.append(caminho_arquivo)
                                cfg.log.info(f"{t*2}Arquivo '{arquivo}' excluído com sucesso ({tamanho_arquivo / (1024 * 1024):.2f} MB).")

                            except PermissionError:
                                cfg.log.error(f"{t*2}Erro ao excluir '{arquivo}': Arquivo está em uso por outro processo.")
                            except Exception as e:
                                cfg.log.error(f"{t*2}Erro ao excluir '{arquivo}': {e}")

    def gerar_relatorio_txt(self,titulo = "RELATÓRIO DE EXCLUSÃO DE ARQUIVOS", pasta_caminho: str = "./temp", file: str = "relatorio_exclusao.txt"):
        if not os.path.exists(pasta_caminho):
            os.makedirs(pasta_caminho)

        caminho_arquivo = os.path.join(pasta_caminho, file)

        # Mede o espaço livre atual no disco de destino dos arquivos
        caminho_referencia = self.caminho if os.path.exists(self.caminho) else pasta_caminho
        espaco_livre_atual = shutil.disk_usage(caminho_referencia).free
        
        if self.espaco_livre_antes is None:
            self.espaco_livre_antes = espaco_livre_atual

        self.total_megas_liberados = self.total_bytes_excluidos / (1024 * 1024)
        self.total_megas_pasta = sum(os.path.getsize(os.path.join(root, f)) for root, _, files in os.walk(self.caminho) for f in files) / (1024 * 1024)

        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            espaco = 40
            f.write("="*espaco + "\n")
            f.write(f"{titulo}\n")
            f.write("="*espaco + "\n\n")
            f.write(f"Data do Relatório: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Data Limite para Exclusão: {self.data_limite.replace('-', '/')}\n")
            f.write("-" * espaco + "\n")
            f.write("Espaço em Disco:\n")
            f.write(f" - Livre antes: {self._formatar_tamanho(self.espaco_livre_antes)}\n")
            f.write(f" - Liberado agora: {self.total_megas_liberados:.2f} MB\n")
            f.write(f" - Livre atual: {self._formatar_tamanho(espaco_livre_atual)}\n")
            f.write(f" - Ocupado pela pasta: {self.total_megas_pasta:.2f} MB\n")
            f.write("-" * espaco + "\n")
            f.write(f"Total de Arquivos Analisados: {self.total_arquivos}\n")
            f.write(f"Total de Arquivos Excluídos: {len(self.arquivos_excluidos)}\n")
            
            f.write("-" * espaco + "\n\n")

            f.write("DETALHAMENTO DOS ARQUIVOS:\n")
            if not self.arquivos_excluidos:
                f.write(">>> Nenhum arquivo foi excluído.\n\n")
            else:
                for arquivo in self.arquivos_excluidos:
                    f.write(f" - {arquivo}\n")
                f.write("\n")

            f.write("="*espaco + "\n")
            f.write("FIM DO RELATÓRIO\n")
            f.write("="*espaco + "\n")

        cfg.log.info(f"Relatório de exclusão criado em: {caminho_arquivo}")
