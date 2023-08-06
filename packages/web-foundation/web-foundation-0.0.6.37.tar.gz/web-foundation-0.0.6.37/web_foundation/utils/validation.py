from typing import Type

from sanic import Request
from pydantic import ValidationError as PdValidationError, BaseModel as PdModel
from sanic.exceptions import BadRequest

from web_foundation.app.errors.application.application import ValidationError


def validate_dto(dto_cls: Type[PdModel] | None,request: Request) -> PdModel | None:
    if not dto_cls:
        return None
    if "json" in request.content_type:
        data = request.json
    elif "form" in request.content_type:
        data = {key: value[0] for key, value in request.form.items()}
    else:
        raise BadRequest("Incorrect content type")
    try:
        dto = dto_cls(**data)
        return dto
    except PdValidationError as ex:
        failed_fields = ex.errors()
        fields = [field["loc"][-1] for field in failed_fields]
        commment_str = "Some of essential params failed : " + ", ".join(
            [field["loc"][-1] + " - " + field["msg"] for field in failed_fields])
        message = commment_str
        context = {
            "fields": fields,
            "comment": commment_str
        }
        raise ValidationError(message=message,
                              context=context)


def dto_validation_error_format(exeption: PdValidationError):
    failed_fields = exeption.errors()
    commment_str = "Some of essential params failed : " + ", ".join(
        [str(field["loc"][-1]) + " - " + field["msg"] for field in failed_fields])
    return commment_str
