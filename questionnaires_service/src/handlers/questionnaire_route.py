from __future__ import annotations

import uuid
from uuid import UUID
from typing import Optional

from fastapi import UploadFile, Body, Request, APIRouter, HTTPException, Response

from src.models.models import QuestionnaireOut, QuestionnaireIn
from src.database import questionnaires_methods
from src.utils.utils import save_questionnaire_image

questionnaire_router = APIRouter()


@questionnaire_router.post(
    '/questionnaire',
    response_model=Optional[QuestionnaireOut],
)
async def post_questionnaire(
        user_id: UUID,
        request: Request,
        questionnaire_in: QuestionnaireIn = Body(...),
        image: Optional[UploadFile] = None,
) -> Response:
    if user_id == questionnaire_in.author_id:
        questionnaire_id = uuid.uuid4()
        image_path = await save_questionnaire_image(image, questionnaire_id, str(request.url))
        response_questionnaire = await questionnaires_methods.add_questionnaire(
            questionnaire_in, image_path, questionnaire_id
        )
        return Response(status_code=201, content=response_questionnaire.model_dump_json())
    raise HTTPException(400, "author_id and user_id must be the same")


@questionnaire_router.delete(
    '/questionnaire/{questionnaire_id}',
)
async def delete_questionnaire(
        user_id: UUID,
        questionnaire_id: UUID
) -> Response:
    try:
        questionnaire = await questionnaires_methods.get_questionnaires(questionnaire_id=questionnaire_id)
        questionnaire = questionnaire[0]
        if questionnaire.author_id == user_id:
            deleted = await questionnaires_methods.delete_questionnaire(questionnaire_id)
            if deleted:
                return Response(status_code=200, content=f"Deleted {questionnaire_id}")
            raise HTTPException(500)
        raise HTTPException(status_code=400, detail="Questionnaire don't belong to user")
    except IndexError:
        raise HTTPException(status_code=404, detail="Wrong questionnaire id")
