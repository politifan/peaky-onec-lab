import importlib.util,json
from pathlib import Path
from fastapi.testclient import TestClient
from app import create_app

def test_persistence_contract_conflict(tmp_path):
    url="sqlite:///"+str(tmp_path/"receiver.db")
    payload={"schema_version":1,"key":"order-7","warehouse":"north","item":"A","qty":3}
    app=create_app(url)
    with TestClient(app) as c:
        assert c.post("/orders",json=payload).json()["created"] is True
        assert c.post("/orders",json=payload).json()["created"] is False
        assert c.post("/orders",json=dict(payload,qty=4)).status_code==409
        assert c.get("/orders/order-7").json()==payload
        for bad in [dict(payload,qty=True),dict(payload,qty=0),dict(payload,qty=-1),dict(payload,key=" "),dict(payload,extra=1),dict(payload,schema_version=2),dict(payload,qty="3")]:
            assert c.post("/orders",json=bad).status_code==422
        assert c.post("/orders",content="broken").status_code==422
        assert c.get("/orders/missing").status_code==404
    app.state.engine.dispose()
    app2=create_app(url)
    with TestClient(app2) as c:
        assert c.post("/orders",json=payload).json()["created"] is False
        assert c.get("/orders/order-7").json()==payload
        assert c.post("/orders",json=dict(payload,key="order-8",qty=1)).json()["created"] is True
    app2.state.engine.dispose()
