from abc import ABC
from abc import abstractmethod

from .internal.entities.account import Account
from .internal.entities.lead import Lead
from .internal.entities.pipeline import Pipeline
from .internal.entities.contact import Contact
from .internal.entities.company import Company
from .internal.entities.catalog import Catalog
from .internal.entities.customer import Customer


class BaseAmoCRMAuth(ABC):

    @abstractmethod
    async def get_access_token(self):
        pass


class AMO:
    _instance = None

    def __init__(self, url: str, auth: BaseAmoCRMAuth):
        self.fulldomain = url
        self.auth = auth

    def __new__(cls, url: str, auth: BaseAmoCRMAuth):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __getattr__(self, item):
        if item == 'account':
            return Account(self.fulldomain, self.auth)
        elif item == 'lead':
            return Lead(self.fulldomain, self.auth)
        elif item == 'pipeline':
            return Pipeline(self.fulldomain, self.auth)
        elif item == 'contact':
            return Contact(self.fulldomain, self.auth)
        elif item == 'company':
            return Company(self.fulldomain, self.auth)
        elif item == 'catalog':
            return Catalog(self.fulldomain, self.auth)
        elif item == 'customer':
            return Customer(self.fulldomain, self.auth)
        else:
            return object.__getattribute__(self, item)
