#!/usr/bin/env python3
import json
import logging

logger = logging.getLogger(__name__)


def add_item(stock_data, item, qty):
    if not isinstance(item, str) or not item.strip():
        logger.warning("Invalid item name: %s. Must be a non-empty string.", item)
        return

    if not isinstance(qty, int) or qty <= 0:
        logger.warning("Invalid quantity: %s. Must be a positive integer.", qty)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logger.info("Added %d of %s. New total: %d",
                qty, item, stock_data[item])


def remove_item(stock_data, item, qty):
    if not isinstance(qty, int) or qty <= 0:
        logger.warning("Invalid quantity: %s. Must be a positive integer.", qty)
        return

    try:
        current_qty = stock_data[item]
        if current_qty <= qty:
            del stock_data[item]
            logger.info("Removed all %d of %s (attempted to remove %d).",
                        current_qty, item, qty)
        else:
            stock_data[item] -= qty
            logger.info("Removed %d of %s. New total: %d",
                        qty, item, stock_data[item])
    except KeyError:
        logger.error("Failed to remove '%s': Item not in stock.", item)


def get_qty(stock_data, item):
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info("Data loaded successfully from %s", file)
            return data
    except FileNotFoundError:
        logger.warning("Data file '%s' not found. Starting with empty stock.", file)
        return {}
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from '%s'. Starting with empty stock.",
                     file)
        return {}


def save_data(stock_data, file="inventory.json"):
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
            logger.info("Data saved successfully to %s", file)
    except IOError as e:
        logger.error("Failed to save data to %s: %s", file, e)


def print_data(stock_data):
    print("\n--- Items Report ---")
    if not stock_data:
        print(" Stock is empty.")
    else:
        for item, qty in stock_data.items():
            print(f" {item}: {qty}")
    print("--------------------\n")


def check_low_items(stock_data, threshold=5):
    return [item for item, qty in stock_data.items() if qty <= threshold]


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    stock_data = load_data("inventory.json")

    print_data(stock_data)

    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", 20)
    add_item(stock_data, "orange", 5)

    add_item(stock_data, "apple", -5)
    add_item(stock_data, 123, 10)
    add_item(stock_data, "pear", "ten")

    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "grape", 1)
    remove_item(stock_data, "banana", 25)

    print(f"Current apple stock: {get_qty(stock_data, 'apple')}")
    print(f"Low items (threshold=5): {check_low_items(stock_data, 5)}")

    print_data(stock_data)

    save_data(stock_data, "inventory.json")

    logger.info("Inventory check complete.")


if __name__ == "__main__":
    main()