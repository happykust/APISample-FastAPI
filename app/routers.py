from typing import Any
from fastapi_crudrouter import OrmarCRUDRouter
from fastapi_crudrouter.core.ormar import CALLABLE
from datetime import datetime
from ormar import Model


class OrmarCRUDRouterUpdated(OrmarCRUDRouter):
    """
    Modified original class OrmarCRUDRouter
    Changes:
    - Added updating field "updated_at" in the User model
    """

    def _update(self, *args: Any, **kwargs: Any) -> CALLABLE:
        """
        Add updating field "updated_at" in the User model
        :param args:
        :param kwargs:
        :return:
        """

        async def route(
            item_id: self._pk_type,  # type: ignore
            model: self.update_schema,  # type: ignore
        ) -> Model:
            """
            Add field "updated_at" to model dict = UTC time
            :param item_id:
            :param model:
            :return:
            """
            filter_ = {self._pk: item_id}
            model_dict = model.dict(exclude_unset=True)
            model_dict['updated_at'] = datetime.now()
            try:
                await self.schema.objects.filter(_exclude=False, **filter_).update(
                    **model_dict
                )
            except self._INTEGRITY_ERROR as e:
                self._raise(e)
            return await self._get_one()(item_id)

        return route
