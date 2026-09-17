from gilded_rose import GildedRose, Item

AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
NORMAL = "Normal Item"


def update(name, sell_in, quality):
    item = Item(name, sell_in, quality)
    GildedRose([item]).update_quality()
    return item


class TestNormalItems:
    def test_quality_and_sell_in_decrease_by_one_before_sell_by(self):
        item = update(NORMAL, 10, 20)
        assert item.sell_in == 9
        assert item.quality == 19

    def test_quality_degrades_twice_as_fast_on_sell_by(self):
        item = update(NORMAL, 0, 20)
        assert item.sell_in == -1
        assert item.quality == 18

    def test_quality_degrades_twice_as_fast_after_sell_by(self):
        item = update(NORMAL, -1, 20)
        assert item.sell_in == -2
        assert item.quality == 18

    def test_quality_does_not_go_negative_before_sell_by(self):
        item = update(NORMAL, 5, 0)
        assert item.sell_in == 4
        assert item.quality == 0

    def test_quality_does_not_go_negative_after_sell_by(self):
        item = update(NORMAL, -1, 0)
        assert item.sell_in == -2
        assert item.quality == 0

    def test_quality_of_one_on_sell_by_floors_at_zero(self):
        item = update(NORMAL, 0, 1)
        assert item.sell_in == -1
        assert item.quality == 0


class TestQualityBounds:
    def test_normal_item_quality_never_goes_negative(self):
        item = update(NORMAL, 0, 0)
        assert item.quality == 0

    def test_aged_brie_quality_does_not_exceed_50_before_sell_by(self):
        item = update(AGED_BRIE, 2, 50)
        assert item.sell_in == 1
        assert item.quality == 50

    def test_aged_brie_quality_does_not_exceed_50_after_sell_by(self):
        item = update(AGED_BRIE, 0, 50)
        assert item.sell_in == -1
        assert item.quality == 50

    def test_backstage_quality_does_not_exceed_50_when_increasing_by_two(self):
        item = update(BACKSTAGE, 10, 50)
        assert item.sell_in == 9
        assert item.quality == 50

    def test_backstage_quality_does_not_exceed_50_when_increasing_by_three(self):
        item = update(BACKSTAGE, 5, 50)
        assert item.sell_in == 4
        assert item.quality == 50


class TestAgedBrie:
    def test_quality_increases_by_one_before_sell_by(self):
        item = update(AGED_BRIE, 2, 0)
        assert item.sell_in == 1
        assert item.quality == 1

    def test_quality_increases_by_two_after_sell_by(self):
        item = update(AGED_BRIE, 0, 0)
        assert item.sell_in == -1
        assert item.quality == 2

    def test_quality_at_49_after_sell_by_caps_at_50(self):
        item = update(AGED_BRIE, 0, 49)
        assert item.sell_in == -1
        assert item.quality == 50


class TestSulfuras:
    def test_does_not_change_when_sell_in_is_zero(self):
        item = update(SULFURAS, 0, 80)
        assert item.sell_in == 0
        assert item.quality == 80

    def test_does_not_change_when_sell_in_is_negative(self):
        item = update(SULFURAS, -1, 80)
        assert item.sell_in == -1
        assert item.quality == 80


class TestBackstagePasses:
    def test_quality_increases_by_one_when_sell_in_is_above_ten(self):
        item = update(BACKSTAGE, 11, 20)
        assert item.sell_in == 10
        assert item.quality == 21

    def test_quality_increases_by_two_when_sell_in_is_ten(self):
        item = update(BACKSTAGE, 10, 20)
        assert item.sell_in == 9
        assert item.quality == 22

    def test_quality_increases_by_two_when_sell_in_is_six(self):
        item = update(BACKSTAGE, 6, 20)
        assert item.sell_in == 5
        assert item.quality == 22

    def test_quality_increases_by_three_when_sell_in_is_five(self):
        item = update(BACKSTAGE, 5, 20)
        assert item.sell_in == 4
        assert item.quality == 23

    def test_quality_drops_to_zero_on_the_concert_day(self):
        item = update(BACKSTAGE, 0, 20)
        assert item.sell_in == -1
        assert item.quality == 0

    def test_quality_stays_zero_after_the_concert(self):
        item = update(BACKSTAGE, -1, 20)
        assert item.sell_in == -2
        assert item.quality == 0

    def test_quality_at_49_with_ten_days_caps_at_50(self):
        item = update(BACKSTAGE, 10, 49)
        assert item.sell_in == 9
        assert item.quality == 50

    def test_quality_at_49_with_five_days_caps_at_50(self):
        item = update(BACKSTAGE, 5, 49)
        assert item.sell_in == 4
        assert item.quality == 50


class TestInventory:
    def test_items_in_the_same_inventory_update_independently(self):
        vest = Item(NORMAL, 10, 20)
        brie = Item(AGED_BRIE, 2, 0)
        GildedRose([vest, brie]).update_quality()
        assert vest.sell_in == 9
        assert vest.quality == 19
        assert brie.sell_in == 1
        assert brie.quality == 1
