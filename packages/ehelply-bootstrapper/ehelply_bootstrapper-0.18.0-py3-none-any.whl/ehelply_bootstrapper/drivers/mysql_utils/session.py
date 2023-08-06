from contextlib import contextmanager, asynccontextmanager

from ehelply_bootstrapper.utils.state import State

# Dependency
async def get_db():
    db = State.mysql.SessionLocal()
    try:
        State.logger.warning("Due to the issue described in the link, I recommend you switch from using Depends(get_db) in your endpoint parameters to using The DbSession context manager. `with DbSession() as db:` https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/104 ")
        yield db
    except:
        if State.mysql.use_async:
            await db.rollback()
        else:
            db.rollback()
        raise
    finally:
        if State.mysql.use_async:
            await db.close()
        else:
            db.close()


@asynccontextmanager
async def DbSession():
    db = State.mysql.SessionLocal()
    try:
        yield db
    except:
        # if we fail somehow rollback the connection
        # warnings.warn("We somehow failed in a DB operation and auto-rollbacking...")

        if State.mysql.use_async:
            await db.rollback()
        else:
            db.rollback()
        raise
    finally:
        if State.mysql.use_async:
            await db.close()
        else:
            db.close()
