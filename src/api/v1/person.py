from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from core.messages import FILM_NOT_FOUND, PERSON_NOT_FOUND
from models.film import FilmShortResponse
from models.person import PersonDetailedResponse
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service
from services.utils import get_params

router = APIRouter()


@router.get(
    '/search',
    response_model=list[PersonDetailedResponse],
    summary='List of suitable person',
    description='List of persons with full_name, roles and film_ids',
    response_description='List of persons with id',
)
@router.get(
    '',
    response_model=list[PersonDetailedResponse],
    summary='List of person',
    description='List of persons with full_name, roles and film_ids',
    response_description='List of persons with id',
)
async def persons_list(request: Request,
                       person_service: PersonService = Depends(get_person_service)) -> list[PersonDetailedResponse]:
    params = get_params(request)
    person_list = await person_service.get_by_params(**params)
    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return [
        PersonDetailedResponse(
            uuid=person.id,
            full_name=person.full_name,
            role=person.role,
            film_ids=person.film_ids,
        ) for person in person_list
    ]


@router.get(
    '/{person_id}/film/',
    response_model=list[FilmShortResponse],
    summary='List of films by person',
    description='List of films in which person participated',
    response_description='List of films with id',
)
async def person_film(person_id: str,
                      request: Request,
                      person_service: PersonService = Depends(get_person_service),
                      film_service: FilmService = Depends(get_film_service)) -> list[FilmShortResponse]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)

    params = get_params(request)
    params.setdefault('should', []).extend([{'id': str(film_id)} for film_id in person.film_ids])
    film_list = await film_service.get_by_params(**params)
    if not film_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)

    return [
        FilmShortResponse(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        ) for film in film_list
    ]


@router.get(
    '/{person_id}',
    response_model=PersonDetailedResponse,
    summary='Person details',
    description='Person details with full_name, roles and film_ids',
    response_description='Person with details by id',
)
async def person_details(person_id: str,
                         person_service: PersonService = Depends(get_person_service)) -> PersonDetailedResponse:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return PersonDetailedResponse(
        uuid=person.id,
        full_name=person.full_name,
        role=person.role,
        film_ids=person.film_ids,
    )
