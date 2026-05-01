import Config as cfg
from Libs     import *
from Modules  import *

def __main__():

    cfg.log.info("Iniciando aplicação...")
    excluir_arquivos = ExcluirArquivos()
    excluir_arquivos.excluir()
    excluir_arquivos.gerar_relatorio_txt()
    

if __name__ == "__main__":
    __main__()