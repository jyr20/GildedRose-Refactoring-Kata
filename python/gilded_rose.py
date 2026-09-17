# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from item import Item

# Special item names
AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"

# Quality bounds
MAX_QUALITY = 50
MIN_QUALITY = 0
SUFURAS_QUALITY = 80

# increase or decrease quality
def increase_quality(item: Item, amount: int) -> None:
    item.quality = min(item.quality + amount, MAX_QUALITY)
def decrease_quality(item: Item, amount: int) -> None:
    item.quality = max(item.quality - amount, MIN_QUALITY)

class ItemUpdate(ABC):
    '''
    Base class for updating item quality
    '''
    def update(self, item: Item) -> None:
        self._age(item)
        self._adjust_quality(item)

    def _age(self, item: Item) -> None:
        item.sell_in -= 1

    @abstractmethod
    def _adjust_quality(self, item: Item) -> None:
        ...

class UpdateNormal(ItemUpdate):
    def _adjust_quality(self, item: Item) -> None:
        decrease_quality(item, 2 if item.sell_in < 0 else 1)

class UpdateBrie(ItemUpdate):
    def _adjust_quality(self, item: Item) -> None:
        increase_quality(item, 2 if item.sell_in < 0 else 1)

class UpdateSulfuras(ItemUpdate):
    def _age(self, item: Item) -> None:
        pass

    def _adjust_quality(self, item: Item) -> None:
        item.quality = SUFURAS_QUALITY

class UpdateBackstage(ItemUpdate):
    def _adjust_quality(self, item: Item) -> None:
        if item.sell_in < 0:
            item.quality = 0
            return
        if item.sell_in < 5:
            increase_quality(item, 3)
        elif item.sell_in < 10:
            increase_quality(item, 2)
        else:
            increase_quality(item, 1)

UPDATERS: dict[str, type[ItemUpdate]] = {
    AGED_BRIE: UpdateBrie,
    SULFURAS: UpdateSulfuras,
    BACKSTAGE: UpdateBackstage,
}


def updater_for(item: Item) -> ItemUpdate:
    cls = UPDATERS.get(item.name, UpdateNormal)
    return cls()


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater_for(item).update(item)
