from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# con_param = {'host': 'precisiontrack.net', 'port': 5432, 'dbname': 'greenlit_test_db', 'user': 'greenlit_test', 'password': 'gr33nl1tB1gDB'}
# con = psycopg2.connect(**con_param)