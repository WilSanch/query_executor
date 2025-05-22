import pandas as pd
from sqlalchemy import create_engine, text
from app.db.models.query_definition import QueryDefinition
from app.db.models.application import Application
from app.storage.blob_client import AzureBlobService
from io import BytesIO
from fastapi import HTTPException

def run_query_and_upload(db, query_id: int, request):
    query_obj = db.query(QueryDefinition).filter_by(id=query_id, active=True).first()
    if not query_obj:
        raise HTTPException(404, detail="Query no encontrado")

    # Obtiene la aplicación asociada al query
    app_obj = db.query(Application).filter_by(id=query_obj.app_id, active=True).first()
    if not app_obj:
        raise HTTPException(404, detail="Aplicación no encontrada para el query")

    # Formatea el SQL con parámetros
    sql = query_obj.sql_template
    if request.parameters:
        try:
            sql = sql.format(**request.parameters)
        except KeyError as e:
            raise HTTPException(400, detail=f"Falta el parámetro: {e}")

    # Ejecuta el query
    engine = create_engine(query_obj.db_url)
    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn)

    # Convierte el DataFrame a bytes
    buf = BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)

    # Usa la configuración específica de la app
    blob_service = AzureBlobService(
        connection_string=app_obj.blob_connection_string,
        container_name=app_obj.blob_container
    )

    blob_service.upload_df_to_blob(df=buf, blob_path=request.blob_path)
