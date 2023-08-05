# import sys
# from pathlib import Path

# import pytest
# from sqlalchemy import event
# from sqlalchemy.exc import IntegrityError, OperationalError
# from sqlmodel import Session, SQLModel, create_engine, select
# from sqlmodel.sql.expression import Select, SelectOfScalar

# sys.path.append(str(Path(__file__).parents[1]))

# import lnbfx.schema as schema  # noqa
# from lnbfx._core import BfxRun, get_bfx_files_from_dir  # noqa

# # avoid SAWarning from sqlalchemy
# SelectOfScalar.inherit_cache = True
# Select.inherit_cache = True


# # activate foreign key constraint for sqlite
# def _fk_pragma_on_connect(dbapi_con, con_record):
#     dbapi_con.execute("pragma foreign_keys=ON")


# # provision test db and automatically delete it at the end of testing
# @pytest.fixture(scope="module")
# def engine():
#     db_path = str(Path(__file__).parent / "test-data" / "dummy.db")
#     engine = create_engine(f"sqlite:///{db_path}")
#     event.listen(engine, "connect", _fk_pragma_on_connect)
#     SQLModel.metadata.create_all(engine)
#     yield engine
#     Path(db_path).unlink()


# test_data_path = Path("tests/test-data")


# def test_get_bfx_files_from_dir():
#     bfx_files = get_bfx_files_from_dir(test_data_path)
#     assert 3 <= len(bfx_files) <= 4


# def test_check_and_ingest(engine):
#     test_bfx_run = BfxRun(pipeline_run_name="Test Run")
#     test_bfx_run.set_dir(test_data_path)
#     test_bfx_run.set_engine(engine)
#     test_bfx_run.check_and_ingest()
#     test_bfx_run.check_and_ingest()
#     with Session(engine) as session:
#         test_pipeline_run = session.exec(
#             select(schema.bfx_run).where(
#                 schema.bfx_run.name == "Test Run"
#             )
#         ).one()
#         assert (
#             test_pipeline_run.bfx_pipeline_id == \
# test_bfx_run._bfx_pipeline_id
#         )
#         session.delete(test_pipeline_run)
#         session.commit()
#     with Session(engine) as session:
#         test_pipeline = session.exec(
#             select(schema.bfx_pipeline).where(
#                 schema.bfx_pipeline.name == "nf-core/rnaseq"
#             )
#         ).one()
#         session.delete(test_pipeline)
#         session.commit()


# def test_link_pipeline_run_to_bfx_run(engine):
#     test_bfx_run = BfxRun(pipeline_run_name="Test Run")
#     test_bfx_run.set_dir(test_data_path)
#     test_bfx_run.set_engine(engine)
#     with pytest.raises(IntegrityError):
#         test_bfx_run.link_pipeline_run(pipeline_run_id="test")


# def test_link_dobject(engine):
#     test_bfx_run = BfxRun(pipeline_run_name="Test Run")
#     test_bfx_run.set_dir(test_data_path)
#     test_bfx_run.set_engine(engine)
#     with pytest.raises(OperationalError):
#         test_bfx_run.link_dobject(
#             dobject_id="1",
#             dobject_filepath=(test_data_path / "salmon.merged.gene_counts.rds"),
#         )
