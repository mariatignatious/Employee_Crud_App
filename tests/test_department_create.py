# `pytest_asyncio` provides the *async-aware* fixture decorator. Plain
# `@pytest.fixture` doesn't know how to drive an `async def` body — you
# have to use `@pytest_asyncio.fixture` whenever the fixture itself is
# async or yields an async resource.
import pytest
# Same async-flavoured SQLAlchemy imports as the previous slide.

from departments import service as department_service


# The test is now pure "act + assert" — no engine, no create_all, no
# cleanup. Pytest sees the `db_session` parameter, runs the fixture
# above, and hands the yielded session in.
@pytest.mark.asyncio
async def test_create_department_persists_name(db_session):

    # Seed a row directly via the ORM. We construct Employee ourselves
    # (with a real `password_hash`) because service.create currently
    # drops the password field — bypassing it keeps this test focused.


    # Call the function under test — async, so we await.

    fetched = await department_service.create_department(db_session, "Engineering")

    assert fetched.id == 1
    assert fetched.name == "Engineering"
