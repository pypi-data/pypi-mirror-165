from datetime import datetime
from typing import Callable, Awaitable, Any

from tortoise.queryset import QuerySet

from web_foundation.app.infrastructure.database.models import ConcurrentEntity

async def retry_dummy(dummy: Any) -> bool:
    return False

async def concurrent_update(query: QuerySet, should_retry: Callable[[Any], Awaitable[bool]] = retry_dummy, **kwargs):
    """
        This function is designed to apply updates to database objects in concurrent manner
        and uses Read-Modify-Write Pattern (RMW).

        It's implemented in three basic steps:
        1. Read object -> acquire/own it;
        2. Modify local copy;
        3. Apply updates only if we still own it (we have it's latest version)

        Step 3 may fail in case when concurrency detected:
        some other database session modified target object
        while we were modifying our local copy, which means
        we do not 'own' the object and must refresh it
        in order to get the latest version.

        It is perceived by comparing local 'updated_at' field
        with it's actual value at step 3.
        So the typical produced query is going to look like:
        update table set value=x where updated_at=<our local updated_at value>

        'query' is required to contain some filtering expression
        'apply' must contain kwargs to be applied in case of success
        'should_retry' functor can be provided as guard who checks retry neccesarity

        NOTE: To keep database consistency regarding
        concurrently accessed objects - every code must MODIFY
        such objects only through this function.

        NOTE: requires connections to use 'read committed' policy
    """
    while True:
        entity: ConcurrentEntity = await query.first()
        if not entity:
            return None

        kwargs.update({'updated_at': datetime.now()})
        done = await query.filter(updated_at=entity.updated_at) \
            .update(**kwargs)

        if done:
            return await query.first()
        elif not await should_retry(query):
            return None


