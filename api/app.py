from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version


from .routers.v1 import main as v1_main
from .routers.v2 import main as v2_main

app = FastAPI()
app.include_router(v1_main.router)
app.include_router(v2_main.router)


app = VersionedFastAPI(app, enable_latest=True)
