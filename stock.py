import uuid

# =========================================================
# DOMAIN MODEL
# =========================================================
# NOTE:
# This is a STOCK / INVENTORY example.
# - Item represents a product type (not a unique physical object)
# - Stock is an event-sourced inventory system
# - Quantity is derived from event history (not stored directly)
# =========================================================

class Item:
    def __init__(self, name: str):
        # UUID included for demonstration only (not used in events)
        self.id = uuid.uuid4()
        self.name = name

    def __repr__(self):
        return f"Item(name={self.name})"


# =========================================================
# EVENTS (WRITE MODEL)
# =========================================================
# NOTE:
# These events represent changes in stock quantity.
# They are NOT tracking individual item identity.
# =========================================================

class StockEvent:
    pass


class ItemAdded(StockEvent):
    def __init__(self, name: str):
        # STOCK EVENT: one unit of this item type was added
        self.name = name


class ItemRemoved(StockEvent):
    def __init__(self, name: str):
        # STOCK EVENT: one unit of this item type was removed
        self.name = name


# =========================================================
# STOCK (EVENT-SOURCED AGGREGATE)
# =========================================================
# NOTE:
# This is an EVENT-SOURCED INVENTORY AGGREGATE.
# - Events are the source of truth
# - State is rebuilt by replaying events
# - Current state = {item_name -> quantity}
# =========================================================

class Stock:
    def __init__(self):
        # Event log (single source of truth)
        self.events: list[StockEvent] = []

    # -------------------
    # COMMANDS (WRITE SIDE)
    # -------------------

    def add_item(self, item: Item):
        # COMMAND: increase stock for this item type
        self.events.append(ItemAdded(item.name))

    def remove_item_by_name(self, name: str):
        # COMMAND: decrease stock for this item type
        self.events.append(ItemRemoved(name))

    # -------------------
    # READ MODEL (REBUILD STATE)
    # -------------------

    # TODO: Implement get_summary()
    # Returns the current stock summary as a dictionary:
    # { "<item_name>": <quantity> }
    def get_summary(self):
        items: dict[str, int] = {}

        for event in self.events:
            # 1. Handle edge cases: ตรวจสอบว่า event มี property 'name' หรือไม่
            if not hasattr(event, 'name'):
                continue
            
            name = event.name
            
            # ตรวจสอบ Null/None, Empty input (ค่าว่าง) และ Invalid input types (ต้องเป็น String)
            if name is None or not isinstance(name, str) or name.strip() == "":
                continue

            # 2. Rebuild state (ประมวลผลจาก Event)
            if isinstance(event, ItemAdded):
                # ถ้ามีของเข้ามา ให้บวก 1 (ถ้ายังไม่มีใน dict ให้ค่าเริ่มต้นเป็น 0 แล้วบวก 1)
                items[name] = items.get(name, 0) + 1
                
            elif isinstance(event, ItemRemoved):
                # ถ้ามีการเอาของออก ให้ลบ 1
                if name in items and items[name] > 0:
                    items[name] -= 1
                    
                    # (ทางเลือก) หากจำนวนเหลือ 0 สามารถลบ key ออกจาก summary ได้เลย
                    if items[name] == 0:
                        del items[name]

        return items

    def print_summary(self):
        summary = self.get_summary()

        for name, quantity in summary.items():
            print({"name": name, "quantity": quantity})


# =========================================================
# DEMO
# =========================================================
# NOTE:
# Demonstrates inventory behavior:
# - Multiple Item("Woody") increases quantity
# - Removal affects only count, not identity
# =========================================================

if __name__ == "__main__":
    stock = Stock()

    stock.add_item(Item("Mama"))
    stock.add_item(Item("Mama"))
    stock.add_item(Item("Coke"))

    stock.remove_item_by_name("Coke")

    stock.print_summary()
