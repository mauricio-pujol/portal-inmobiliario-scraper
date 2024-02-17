from apache_airflow import DAG, PythonOperator
import datetime
from main_extraction import data_extraction

# Definimos el DAG
dag = DAG(
    dag_id="mi_script_diario",
    description="Este DAG ejecuta la función data_extraction() una vez al día",
    schedule_interval="0 0 * * *",
)

# Definimos la tarea Python
tarea_python = PythonOperator(
    task_id="ejecutar_extraccion",
    python_callable=data_extraction,
    python_path="/ruta/al/archivo/main_extraction.py",
)

# Pruebas
if __name__ == "__main__":
    from airflow.utils.state import State

    dag.run(start_date=datetime.today(), end_date=datetime.today(), state=State.SUCCESS)
