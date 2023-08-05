# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Dict, Optional, Type

import attr

from gooddata_metadata_client.model.declarative_setting import DeclarativeSetting
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeSetting(Base):
    id: str
    content: Optional[Dict[str, Any]] = None

    @staticmethod
    def client_class() -> Type[DeclarativeSetting]:
        return DeclarativeSetting
