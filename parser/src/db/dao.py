from tables import Ozon, Wb, Auchan
from base import BaseDAO


class OzonDAO(BaseDAO):
    model = Ozon


class WbDAO(BaseDAO):
    model = Wb


class AuchanDAO(BaseDAO):
    model = Auchan
