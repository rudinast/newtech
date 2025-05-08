import uvicorn
from fastapi import FastAPI

from Requests.auth_requests import user_router
from Requests.delete_requests import delete_route
from Requests.get_requests import get_route
from Requests.post_requests import post_route

app = FastAPI()

app.include_router(user_router)
app.include_router(get_route)
app.include_router(post_route)
app.include_router(delete_route)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
