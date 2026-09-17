# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from item import Item

# Special item names
AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
SpecialItemNames = (AGED_BRIE, SULFURAS, BACKSTAGE)

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


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name in SpecialItemNames:
                if item.name != AGED_BRIE and item.name != BACKSTAGE:
                    if item.quality > 0:
                        if item.name != SULFURAS:
                            item.quality = item.quality - 1
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1
                        if item.name == BACKSTAGE:
                            if item.sell_in < 11:
                                if item.quality < 50:
                                    item.quality = item.quality + 1
                            if item.sell_in < 6:
                                if item.quality < 50:
                                    item.quality = item.quality + 1
                if item.name != SULFURAS:
                    item.sell_in = item.sell_in - 1
                if item.sell_in < 0:
                    if item.name != AGED_BRIE:
                        if item.name != BACKSTAGE:
                            if item.quality > 0:
                                if item.name != SULFURAS:
                                    item.quality = item.quality - 1
                        else:
                            item.quality = item.quality - item.quality
                    else:
                        if item.quality < 50:
                            item.quality = item.quality + 1
            else:
                UpdateNormal().update(item)
