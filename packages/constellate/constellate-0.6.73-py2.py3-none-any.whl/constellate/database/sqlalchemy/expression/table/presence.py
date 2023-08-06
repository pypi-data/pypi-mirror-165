from typing import Any

from sqlalchemy import func, column, case, Boolean
from sqlalchemy.cimmutabledict import immutabledict
from sqlalchemy.dialects.postgresql import REGCLASS
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def has_table(
    session: AsyncSession = None,
    shard_id: str = None,
    shard_schema_id: str = None,
    table: Any = None,
) -> bool:
    # FIXME (high) has_table is also available in sqlalchemy/dialects/postgres/base.py (and other backends)
    # FIXME (high) Public API is Inspector.has_table` and legacy API is ` _engine.Engine.has_table`
    # FIXME (high) Use default shema returned by https://docs.sqlalchemy.org/en/14/core/reflection.html?highlight=inspector#sqlalchemy.engine.reflection.Inspector

    # SELECT to_regclass('schema_name.table_name');
    # src: https://stackoverflow.com/a/24089729/219728

    # SELECT (CASE WHEN found IS NULL
    #             THEN False
    #             ELSE True
    #        END) AS found
    # FROM ( SELECT CAST(to_regclass('some_schema_name.some_table_name') AS REGCLASS) ) AS found

    stmt_0 = select(func.to_regclass(table.__tablename__).cast(REGCLASS).label("result")).subquery()
    column_result = column("result")
    stmt_1 = select(
        case((column_result.is_(None), False), else_=True).label("found").cast(Boolean)
    ).select_from(stmt_0)

    # Note: Only compatible with (Sync)MultiEngineShardSession instances
    bind_arguments = {"shard_id": shard_id}
    execution_options = {"shard_schema_id": shard_schema_id}

    value = (
        await session.execute(
            stmt_1,
            bind_arguments=bind_arguments,
            execution_options=immutabledict({"synchronize_session": False, **execution_options}),
        )
    ).scalar()
    return value
