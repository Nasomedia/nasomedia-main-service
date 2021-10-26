from fastapi import APIRouter

from app.api.v1.endpoints import author, episode, genre, publisher, tag, series

api_router = APIRouter()
api_router.include_router(author.router, prefix="/authors", tag=["author"])
api_router.include_router(episode.router, prefix="/episodes", tag=["episode"])
api_router.include_router(genre.router, prefix="/genres", tag=["genre"])
api_router.include_router(publisher.router, prefix="/publishers", tag=["publisher"])
api_router.include_router(tag.router, prefix="/tags", tag=["tag"])
api_router.include_router(series.router, prefix="/series", tag=["series"])