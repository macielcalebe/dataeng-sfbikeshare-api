import os
import time
import psycopg2
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def load_env_vars():
    """Carrega as variáveis de ambiente do arquivo .env"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)

def get_db_config():
    """Retorna a configuração do banco de dados a partir das variáveis de ambiente"""
    load_env_vars()
    return {
        'db': os.getenv('POSTGRES_DB_APP'),
        'user': os.getenv('POSTGRES_USER_APP'),
        'password': os.getenv('POSTGRES_PASSWORD_APP'),
        'port': os.getenv('POSTGRES_PORT_APP', '5432'),
        'host': os.getenv('POSTGRES_HOST_APP', 'localhost'),
        'timeout': int(os.getenv('POSTGRES_TIMEOUT', '15'))
    }

def get_connection(dbname=None):
    """
    Cria uma conexão com o banco de dados PostgreSQL
    
    Args:
        dbname: Nome do banco de dados (opcional, usa POSTGRES_DB se não especificado)
    
    Returns:
        psycopg2.connection: Conexão com o banco de dados
    """
    config = get_db_config()
    db = dbname or config['db']
    
    return psycopg2.connect(
        dbname=db,
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )

def wait_for_postgres(timeout=None):
    """
    Aguarda o PostgreSQL ficar disponível
    
    Args:
        timeout: Tempo limite em segundos (opcional, usa POSTGRES_TIMEOUT se não especificado)
    
    Returns:
        bool: True se PostgreSQL estiver disponível, False se timeout
    """
    config = get_db_config()
    timeout = timeout or config['timeout']
    
    start = time.time()
    while time.time() - start < timeout:
        try:
            conn = get_connection(dbname='postgres')
            conn.close()
            logger.info('Postgres está disponível!')
            return True
        except Exception as e:
            logger.info(f'Aguardando Postgres... ({e})')
            time.sleep(2)
    
    logger.warning('Timeout ao esperar pelo Postgres.')
    return False

def create_database_if_not_exists(db_name=None):
    """
    Cria o banco de dados se ele não existir
    
    Args:
        db_name: Nome do banco de dados (opcional, usa POSTGRES_DB se não especificado)
    """
    config = get_db_config()
    db_name = db_name or config['db']
    
    conn = get_connection(dbname='postgres')
    conn.autocommit = True
    
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        
        if not exists:
            logger.info(f"Criando banco {db_name}...")
            cur.execute(f'CREATE DATABASE "{db_name}"')
        else:
            logger.info(f"Banco {db_name} já existe.")
    
    conn.close()

def execute_sql_file(filepath, dbname=None):
    """
    Executa um arquivo SQL no banco de dados
    
    Args:
        filepath: Caminho para o arquivo SQL
        dbname: Nome do banco de dados (opcional, usa POSTGRES_DB se não especificado)
    """
    config = get_db_config()
    db_name = dbname or config['db']
    
    conn = get_connection(dbname=db_name)
    conn.autocommit = True
    
    with conn.cursor() as cur:
        with open(filepath, 'r') as f:
            sql = f.read()
            cur.execute(sql)
    
    conn.close()

def execute_sql_scripts_from_dir(sql_dir, dbname=None):
    """
    Executa todos os arquivos SQL de um diretório em ordem alfabética
    
    Args:
        sql_dir: Diretório contendo os arquivos SQL
        dbname: Nome do banco de dados (opcional, usa POSTGRES_DB se não especificado)
    """
    files = sorted([f for f in os.listdir(sql_dir) if f.endswith('.sql')])
    
    for fname in files:
        filepath = os.path.join(sql_dir, fname)
        logger.info(f'Executando {fname}...')
        execute_sql_file(filepath, dbname)
