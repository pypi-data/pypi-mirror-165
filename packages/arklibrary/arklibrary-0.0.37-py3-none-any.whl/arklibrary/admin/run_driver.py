import json
from arklibrary.admin import Admin, Bundle
from time import sleep


def game_driver_config():
    with open("config.json", 'r') as r:
        return json.load(r)["gamedriver"]


def order_to_products(order: Order):
    assert order is not None, "An order can not be None."
    user = User.find(xuid=order.xuid)
    account = Account.find(xuid=order.xuid)
    product_orders = {"gamertag": user.gamertag, "player_id": account.player_id, "orders": []}
    for order_item in order:
        product_id = order_item.product_id
        quantity = order_item.quantity
        product_orders["orders"].append({"product": Product.find(id=product_id), "quantity": quantity})
    return product_orders


def iter_orders():
    orders = Order.all_new()
    for order in orders:
        order_prod = order_to_products(order)
        yield order_prod
        gamertag = order_prod["gamertag"]
        print('\033[92m' + f"[{gamertag}]: Finished order." + '\033[0m')
        order.process()


def get_admin():
    config = game_driver_config()
    admin = Admin(password=config["admin_password"])
    admin.enable_admin().execute()
    sleep(1)
    return admin


def run(admin: Admin=None):
    if admin is None:
        admin = get_admin()
    while True:
        try:
            for i, order in enumerate(iter_orders()):
                print('\033[34m' + f"[{order['gamertag']}]: Starting order." + '\033[0m')
                for order_item in order["orders"]:
                    product = order_item["product"]
                    quantity = order_item["quantity"]
                    print('\033[93m' + f"[{order['gamertag']}]: product={product} quantity={quantity}" + '\033[0m')
                    admin.give_items_to_player(order["player_id"], [product.blueprint[1:-1]] * quantity, quantity=product.stack_size)
                if i % 5 == 0:
                    admin.execute()
            admin.execute()
            sleep(5)
        except Exception as e:
            print('\033[31m' + f"[FAILED]: {e}" + '\033[0m')

if __name__ == "__main__":
    pass