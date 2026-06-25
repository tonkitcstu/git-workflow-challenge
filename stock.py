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

        # Replay the event log to rebuild current quantities.
        for event in self.events:
            if isinstance(event, ItemAdded):
                items[event.name] = items.get(event.name, 0) + 1
            elif isinstance(event, ItemRemoved):
                # Quantity never drops below zero.
                items[event.name] = max(0, items.get(event.name, 0) - 1)

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
