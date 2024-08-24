from typing import Optional

from pydantic import BaseModel, error_wrappers


class Blog(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool


blog = Blog(title="My First Blog",is_active=True)
print(blog)

try:
    Blog(title="My First Blog",is_active="Yeah")
except error_wrappers.ValidationError as e:
    print(e)