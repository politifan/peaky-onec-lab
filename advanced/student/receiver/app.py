import json, os
from fastapi import FastAPI, Request, HTTPException
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select, insert
from sqlalchemy.exc import IntegrityError

def create_app(url=None):
    engine=create_engine(url or os.environ.get("DATABASE_URL", "sqlite:///receiver.db"))
    metadata=MetaData()
    orders=Table("orders",metadata,Column("key",String(100),primary_key=True),Column("payload",String,nullable=False),Column("qty",Integer,nullable=False))
    metadata.create_all(engine)
    app=FastAPI(title="Peaky Minds Receiver")
    app.state.engine=engine
    def valid(d):
        fields={"schema_version","key","warehouse","item","qty"}
        return isinstance(d,dict) and set(d)==fields and type(d["schema_version"]) is int and d["schema_version"]==1 and type(d["qty"]) is int and 0<d["qty"]<=10**9 and all(type(d[k]) is str and 0<len(d[k].strip())<=100 for k in ["key","warehouse","item"])
    def reply(row,payload):
        if row["payload"]!=payload:raise HTTPException(409,"key_conflict")
        return {"key":row["key"],"qty":row["qty"],"created":False}
    @app.post("/orders")
    async def accept(request:Request):
        try:d=await request.json()
        except (ValueError,UnicodeError):raise HTTPException(422,"invalid_json")
        if not valid(d):raise HTTPException(422,"invalid_contract")
        payload=json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(",",":"))
        try:
            with engine.begin() as conn:
                row=conn.execute(select(orders).where(orders.c.key==d["key"])).mappings().first()
                if row:return reply(row,payload)
                conn.execute(insert(orders).values(key=d["key"],payload=payload,qty=d["qty"]))
        except IntegrityError:
            with engine.connect() as conn:
                row=conn.execute(select(orders).where(orders.c.key==d["key"])).mappings().one()
                return reply(row,payload)
        return {"key":d["key"],"qty":d["qty"],"created":True}
    @app.get("/orders/{key}")
    def read(key:str):
        with engine.connect() as conn:
            row=conn.execute(select(orders).where(orders.c.key==key)).mappings().first()
            if row is None:raise HTTPException(404,"not_found")
            return json.loads(row["payload"])
    @app.get("/health")
    def health():return {"status":"running"}
    return app

# Factory mode: uvicorn app:create_app --factory
