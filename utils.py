import os

def get_asset_path(*paths):
    """
    Retorna o caminho completo para um arquivo de asset,
    garantindo que funcione em qualquer sistema operacional.
    
    Args:
        *paths: Sequência de diretórios/arquivos para juntar ao caminho base
    
    Returns:
        str: Caminho completo para o arquivo
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(base_dir, *paths))

def ensure_dir_exists(*paths):
    """
    Garante que um diretório existe, criando-o se necessário.
    
    Args:
        *paths: Sequência de diretórios para juntar ao caminho base
    
    Returns:
        str: Caminho completo do diretório criado
    """
    dir_path = get_asset_path(*paths)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def get_resource_path(resource_type, filename):
    """
    Retorna o caminho para um recurso específico (imagem, som, etc).
    
    Args:
        resource_type (str): Tipo de recurso ('images', 'sounds', 'maps', etc)
        filename (str): Nome do arquivo
    
    Returns:
        str: Caminho completo para o recurso
    """
    # Se o resource_type já inclui 'assets', não adiciona novamente
    if resource_type.startswith('assets/'):
        return get_asset_path(resource_type, filename)
    else:
        return get_asset_path('assets', resource_type, filename) 