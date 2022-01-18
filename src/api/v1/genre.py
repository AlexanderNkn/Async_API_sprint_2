from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from core.messages import GENRE_NOT_FOUND
from models.genre import GenreDetailedResponse
from services.genre import GenreService, get_genre_service
from services.utils import get_params

router = APIRouter()


@router.get(
    '/search',
    response_model=list[GenreDetailedResponse],
    summary='List of suitable genre',
    description='List of genre with sort, filter and pagination and text search',
    response_description='List of genres with id',
)
@router.get(
    '',
    response_model=list[GenreDetailedResponse],
    summary='List of genre',
    description='List of genre with sort, filter and pagination',
    response_description='List of genres with id',
)
async def genres_list(request: Request,
                      genre_service: GenreService = Depends(get_genre_service)) -> list[GenreDetailedResponse]:
    params = get_params(request)
    genres = await genre_service.get_by_params(**params)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)
    return [
        GenreDetailedResponse(
            uuid=genre.id,
            name=genre.name,
            description=genre.description,
        ) for genre in genres
    ]


@router.get(
    '/{genre_id}',
    response_model=GenreDetailedResponse,
    summary='Genre details',
    description='Genre details with name and description',
    response_description='Genre with details by id',
)
async def genre_details(genre_id: str,
                        genre_service: GenreService = Depends(get_genre_service)) -> GenreDetailedResponse:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)
    return GenreDetailedResponse(
        uuid=genre.id,
        name=genre.name,
        description=genre.description,
    )
