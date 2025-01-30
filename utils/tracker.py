import json
import os

from utils.utils import send_mail


def in_cache(item, array):
    for a in array:
        if item["title"] == a["title"]:
            return a

    return None


def price_tracking(items, cache_directory, notify):
    update_cache = False
    cache_filename = os.path.join(cache_directory, "items.json")

    if os.path.isfile(cache_filename):
        with open(cache_filename, encoding="utf-8", mode="r") as f:
            saved_items = json.load(f)
    else:
        saved_items = []

    if not saved_items:
        if items:
            print("adding items to cache...")
            saved_items.extend(items)
            update_cache = True
    else:
        print("data validation...")

        for i in items:
            ci = in_cache(i, saved_items)

            if not ci:
                print(f"adding {i['title']}")
                saved_items.append(i)
                update_cache = True
            else:
                print(f"data validation for {i['title']}")

                if not ci["price"] == i["price"]:
                    print(f"change detected... OLD: {ci['price']} -> NEW: {i['price']}")

                    if notify:
                        try:
                            send_mail(
                                subject="Price Tracking",
                                to=notify,
                                message=(
                                    f"<p>current price: <b>${i['price']}</b></p>"
                                    f"<p>previous price: <b>${ci['price']}</b></p>"
                                    f"<p>item: <a href={i['url']}>{i['title']}</a></p>"
                                ),
                            )
                        except Exception as e:
                            print("error sending email...")
                            print(e)

                    saved_items.remove(ci)
                    saved_items.append(i)
                    update_cache = True

    if saved_items and update_cache:
        print("storing data...")

        with open(cache_filename, encoding="utf-8", mode="w") as f:
            json.dump(saved_items, f, indent=4)
