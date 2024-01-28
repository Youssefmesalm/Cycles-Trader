from fastapi import APIRouter, status, HTTPException, Query
from dependencies import DBSession
from users_management.data import UserRead, User, user_service
from user.cycles.data.cycle import Cycle, CycleRead, CycleUpdate

router = APIRouter(prefix="/cycles")


@router.get("/", response_model=list[CycleRead])
async def get_all_cycles(session: DBSession, user_id: int):
    return user_service.get_user_cycles(session, user_id)

async def update_cycle():
    pass