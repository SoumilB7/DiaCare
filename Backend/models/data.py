from pydantic import BaseModel
from typing import Optional

class UserData(BaseModel):
    userid: str
    val0: Optional[str] = None
    val1: Optional[str] = None
    val2: Optional[str] = None
    val3: Optional[str] = None
    val4: Optional[str] = None
    val5: Optional[str] = None
    val6: Optional[str] = None
    val7: Optional[str] = None
