from datetime import datetime as datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from . import id as idg
from .type import environment as environment_type


def utcnow():
    return datetime.utcnow().replace(microsecond=0)


class version_xqfj(SQLModel, table=True):  # type: ignore
    """Drylab schema module versions deployed in a given instance.

    Migrations of the schema module add rows to this table, storing the schema
    module version to which we migrated along with the user who performed the
    migration.
    """

    v: Optional[str] = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=utcnow, nullable=False)


class environment(SQLModel, table=True):  # type: ignore
    """Compute environment.

    Reference to docker build or conda environment.
    """

    id: Optional[str] = Field(default_factory=idg.environment, primary_key=True)
    v: Optional[str] = Field(default="1", primary_key=True)
    name: Optional[str] = Field(index=True, default=None)
    reference: Optional[str] = Field(index=True, default=None)
    type: environment_type = Field(index=True)
    created_at: datetime = Field(default_factory=utcnow, nullable=False, index=True)
