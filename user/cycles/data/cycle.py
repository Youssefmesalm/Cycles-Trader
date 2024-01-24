from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from users_management.data.user import User, UserRead

# Todo: I Think i should remove the number () and only identify the cycle by id (not shown) 

class CycleBase(SQLModel):
    # generated using the logic: (len(user_cycles) + 1)
    symbol: str
    tb: int
    sl: int
    tf: str
    lot: float
    count: int
    candle: str
    auto: bool


class Cycle(CycleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # number: int

    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    user: Optional["User"] = Relationship(back_populates="cycles")


class CycleCreate(CycleBase):
    pass


class CycleRead(CycleBase):
    id: int
    # number: int
    


class CycleReadWithUser(CycleRead):
    user: Optional["UserRead"] = Field(default=None)


class CycleUpdate(SQLModel):
    symbol: str | None = None
    tb: int | None = None
    sl: int | None = None
    tf: str | None = None
    lot: float | None = None
    count: int | None = None
    candle: str | None = None
    auto: bool | None = None
