from fastapi import APIRouter

from app.api.v1.endpoints import author, episode, genre, publisher, tag, series

api_router = APIRouter()
api_router.include_router(author.router, prefix="/authors", tags=["author"])
api_router.include_router(episode.router, prefix="/episodes", tags=["episode"])
api_router.include_router(genre.router, prefix="/genres", tags=["genre"])
api_router.include_router(publisher.router, prefix="/publishers", tags=["publisher"])
api_router.include_router(tag.router, prefix="/tags", tags=["tag"])
api_router.include_router(series.router, prefix="/serieses", tags=["series"])