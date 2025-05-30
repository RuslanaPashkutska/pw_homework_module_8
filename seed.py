import os
from dotenv import load_dotenv
import json
from mongoengine import connect
from models import Author, Quote

from mongoengine.errors import NotUniqueError


load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
connect(host=mongo_uri)


if __name__ == "__main__":
    with open("authors.json", encoding="utf-8") as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get("fullname"), born_date=el.get("born_date"), born_location=el.get("born_location"), description=el.get("description"))
                author.save()
            except NotUniqueError:
                print(f"Author exist {el.get('fullname')}")


    with open("qoutes.json", encoding="utf-8") as fd:
        data = json.load(fd)
        for el in data:
            author, *_ = Author.objects(fullname=el.get("author"))
            quote = Quote(quote=el.get("quote"), tags=el.get("tags"), author=author)
            quote.save()