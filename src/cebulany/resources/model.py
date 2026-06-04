from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy import select, insert

# from cebulany.auth import token_required
from cebulany.deps import SessionDep
from cebulany.models import Base


def unpack[T: BaseModel](model_type: type[T], obj: object) -> T:
    raw = {
        key: getattr(obj, key)
        for key, field in model_type.model_fields.items()
    }
    return model_type(**raw)


class ModelListResource[SqlModel: Base, Model: BaseModel]:
    _sql_model: type[SqlModel]
    _model: type[Model]

    def __init_subclass__(cls, sql_model: type[SqlModel], model: type[Model]) -> None:
        cls._sql_model = sql_model 
        cls._model = model

    def make_router(self):
        router = APIRouter()
        router.add_api_route("/", self.list, methods=["GET"])
        router.add_api_route("/", self.post, methods=["POST"])
        router.add_api_route("/{id}", self.get, methods=["GET"])
        router.add_api_route("/{id}", self.put, methods=["PUT"])
        router.add_api_route("/{id}", self.delete, methods=["DELETE"])
        return router

    async def list(self, session: SessionDep) -> list[Model]:
        stmt = select(self._sql_model)
        result = await session.execute(stmt)
        return [unpack(self._model, obj) for obj in result]

    async def post(self, item: Model, session: SessionDep) -> Model:
        # 201
        stmt = select(self._sql_model).filter_by(id=id)
        await session.execute(stmt)
        session.commit()
        if obj is None:
            raise HTTPException(status_code=404)
        return unpack(self._model, item)
        data = self.parser.parse_args()
        obj = self.cls(**data)
        db.session.add(obj)
        db.session.commit()
        return marshal(obj, self.resource_fields), 201

    async def get(self, id: int, session: SessionDep):
        stmt = select(self._sql_model).filter_by(id=id)
        obj = await session.execute(stmt).first()
        obj = self.cls.query.get(id)
        if obj is None:
            raise HTTPException(status_code=404)
        return unpack(self._model, obj)

    def put(self, id: int):
        stmt = select(self._sql_model).filter_by(id=id)
        obj = self.cls.query.get(id)
        if obj is None:
            abort(404)

        data = self.parser.parse_args()
        for key, value in data.items():
            setattr(obj, key, value)
        db.session.commit()

        return marshal(obj, self.resource_fields)

    def delete(self, id):
        query = self.cls.query.filter_by(id=id)
        is_exists = db.session.query(query.exists()).scalar()
        if not is_exists:
            abort(404)
        query.delete()
        db.session.commit()
        return '', 204


# class ModelListResource(Resource):
#     cls: Base
#     parser: RequestParser
#     resource_fields: dict[str, Raw]
#     method_decorators = [token_required]


# class ModelResourceWithoutDelete(Resource):
#     cls: type[Base]
#     parser: RequestParser
#     resource_fields: dict[str, Raw]
#     method_decorators = [token_required]


# class ModelResource(ModelResourceWithoutDelete):
#     pass

