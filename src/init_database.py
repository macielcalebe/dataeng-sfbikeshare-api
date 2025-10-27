import os
import logging
import sys
from db_utils import (
    wait_for_postgres,
    create_database_if_not_exists,
    execute_sql_scripts_from_dir,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SQL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sql")


def main():
    logger.info("Iniciando inicialização do banco de dados")
    if not wait_for_postgres():
        logger.error("Falha ao conectar com PostgreSQL")
        sys.exit(1)
    create_database_if_not_exists()
    execute_sql_scripts_from_dir(SQL_DIR)
    logger.info("Inicialização do banco de dados concluída com sucesso")


if __name__ == "__main__":
    main()
