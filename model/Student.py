from dataclasses import dataclass, field
import datetime as dT
from uuid import uuid4

@dataclass
class Student:
    Name : str 
    Class : str =field(default='Unknown')
    Sex : str = field(default='Female')
    id : int = field(default=uuid4().int,init=True,compare=True)
    Dob : dT.date = field(default=dT.date.today().strftime('%d/%m/%Y'))
    
    

    