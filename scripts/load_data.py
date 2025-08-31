import os
import sys
from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq

import yaml
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, text, Connection

load_dotenv()

DB_ENGINE = os.environ["DB_ENGINE"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASETS_PATH = PROJECT_ROOT / "datasets"
CONFIG_PATH = PROJECT_ROOT / "config.yml"


def load_config(path: Path | str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)["projects"]


def get_engine():
    return create_engine(
        f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


def ensure_schema(engine: Engine, schema: str):
    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))


def truncate_table(engine: Engine, schema: str, table: str):
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {schema}.{table}"))


def load_parquet_in_chunks(
    conn: Connection, schema: str, table: str, file_path: Path
) -> None:
    print(f"Loading f'{file_path}' into {schema}.{table}")
    parquet_file = pq.ParquetFile(file_path)

    for batch in parquet_file.iter_batches():
        df = batch.to_pandas()
        df.to_sql(table, con=conn, schema=schema, if_exists="append", index=False)


def load_csv_in_chunks(
    conn: Connection, schema: str, table: str, file_path: Path, chunk_size=100_000
) -> None:
    print(f"Loading f'{file_path}' into {schema}.{table}")
    chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)

    for i, chunk in enumerate(chunk_iter):
        chunk.to_sql(table, con=conn, schema=schema, if_exists="append", index=False)


def load_table(engine, schema: str, table: str, sources: list[str]) -> None:
    if isinstance(sources, str):
        sources = [sources]

    # truncate table to keep process idempotent and simple
    truncate_table(engine, schema, table)

    for source in sources:
        file_path = DATASETS_PATH / schema / source
        if not file_path.exists():
            raise FileNotFoundError(f"Missing source file: {file_path}")

        with engine.connect() as conn:
            if file_path.suffix == ".csv":
                load_csv_in_chunks(conn, schema, table, file_path)
            elif file_path.suffix in (".parquet", ".pq"):
                load_parquet_in_chunks(conn, schema, table, file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_path.suffix}")


def load_project_data(project_config: dict) -> None:
    engine = get_engine()

    schema = project_config["schema"]
    ensure_schema(engine, schema)

    for table, meta in project_config["tables"].items():
        sources = meta.get("sources") or meta.get("source")
        if not sources:
            raise ValueError(f"⚠️ No sources defined for {schema}.{table}, skipping...")
        load_table(engine, schema, table, sources)


def main() -> None:
    config = load_config(CONFIG_PATH)
    parser = ArgumentParser(
        description="Load Data for the specified project into postgres."
    )
    parser.add_argument(
        "--project",
        type=str,
        required=True,
        help=f"Project to load, which must be defined in 'projects.yml'",
    )
    args = parser.parse_args()

    if args.project not in config.keys():
        print(
            f"❌ Invalid project '{args.project}'. Must be one of: {', '.join(config.keys())}"
        )
        sys.exit(1)

    print(f"✅ Loading data for project: {args.project} - start")
    load_project_data(config[args.project])
    print(f"✅ Loading data for project: {args.project} - complete")


if __name__ == "__main__":
    main()
