
# Lean Api for FastApi

LeanAPI is an interface that allows you to create a FastAPI router as a Class.

## An example class structure

``` python

from leanapi.path import controller
from leanapi.server import router


@controller("personnel", router)
class Personnel:

    @router.get("/get/{personnel_id}")
    def get_personel(self, personnel_id: int) -> dict:
        return {"personnel_id": personnel_id}

```

As a result definition the "/personnel/get/:personnel_id" address becomes active.
"personnel_id" is a path parameter and is a of type *int*

