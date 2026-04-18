import Config as cfg
import functools
import time

#função para retentar 3 vezes a execução de uma função em caso de falha
def retry(func=None, retries: int = 3, delay: int = 2):
    """Decorator que tenta executar a função `func` até `retries` vezes em caso de falha.

    Args:
        func (callable, optional): A função a ser decorada.
        retries (int, optional): O número máximo de tentativas. Padrão é 3.
        delay (int, optional): O atraso em segundos entre as tentativas. Padrão é 2.
    Returns:
        callable: A função decorada com lógica de retry.
    """
    def decorator(inner_func):
        @functools.wraps(inner_func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return inner_func(*args, **kwargs)
                except Exception as e:
                    cfg.log.error(f"Tentativa {attempt} falhou: {e}")
                    if attempt < retries:
                        cfg.log.info(f"Re tentando em {delay} segundos...")
                        time.sleep(delay)
            cfg.log.error(f"Todas as {retries} tentativas falharam.")
            return None
        return wrapper

    if func is None:
        return decorator
    return decorator(func)