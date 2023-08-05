from typing import Optional

# import lnschema_core  # noqa
from sqlmodel import Field, ForeignKeyConstraint, SQLModel


class bfx_pipeline(SQLModel, table=True):  # type: ignore
    """Bioinformatics pipeline metadata."""

    __table_args__ = (
        ForeignKeyConstraint(
            ["id", "v"],
            ["pipeline.id", "pipeline.v"],
            name="pipeline",
        ),
    )
    id: Optional[str] = Field(default=None, primary_key=True, index=True)
    v: Optional[str] = Field(default=None, primary_key=True, index=True)


class bfx_run(SQLModel, table=True):  # type: ignore
    """Bioinformatics pipeline run metadata."""

    __table_args__ = (
        ForeignKeyConstraint(
            ["bfx_pipeline_id", "bfx_pipeline_v"],
            ["bfx_pipeline.id", "bfx_pipeline.v"],
            name="bfx_pipeline",
        ),
    )
    id: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="pipeline_run.id", index=True
    )
    dir: str = Field(default=None)
    bfx_pipeline_id: str = Field(default=None, index=True)
    bfx_pipeline_v: str = Field(default=None, index=True)


class bfxmeta(SQLModel, table=True):  # type: ignore
    """Metadata for files associated with bioinformatics pipelines."""

    id: Optional[int] = Field(default=None, primary_key=True)
    file_type: str = Field(default=None)
    dir: str = Field(default=None)


class dobject_bfxmeta(SQLModel, table=True):  # type: ignore
    """Link table between dobject and bfxmeta tables."""

    dobject_id: Optional[str] = Field(
        default=None, foreign_key="dobject.id", primary_key=True, index=True
    )
    bfxmeta_id: Optional[int] = Field(
        default=None, foreign_key="bfxmeta.id", primary_key=True, index=True
    )
