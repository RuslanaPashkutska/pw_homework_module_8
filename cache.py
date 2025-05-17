import redis
from redis_lru import RedisLRU

from models import Author, Quote
from mongoengine import connect
connect(host="mongodb+srv://usermodule-8:5671234@ruslana.l69lrsa.mongodb.net/hw_module_8?retryWrites=true&w=majority")

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tags(tag: str) -> list[str | None]:
    tag = tag.lower().strip()
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__istartswith=tag)
    result = [q.quote for q in quotes]
    return result

# New function: search by multiple tags (comma-separated)
@cache
def find_by_tags_multi(tag_str: str) -> list[str]:
    tag_list = [t.strip().lower() for t in tag_str.split(",")]
    print(f"Find by multiple tags: {tag_list}")
    quotes = Quote.objects(tags__all=tag_list)
    return [q.quote for q in quotes]


@cache
def find_by_author(author:str) -> dict[str, list[str]]:
    author = author.lower().strip()
    print(f"Find by prefix: {author}")
    authors = Author.objects(fullname__istartswith=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

if __name__ == '__main__':
    # print(find_by_tags("mi"))
    # print(find_by_tags("mi"))

    # print(find_by_author("in"))
    # print(find_by_author("in"))
    #quotes = Quote.objects().all()
    #print([e.to_json() for e in quotes])

    while True:
        command = input("Enter command (name:<prefix>, tag:<prefix>, tags:<tag1,tag2>, or exit:").strip()
        if command == "exit":
            break
        if ":" not in command:
            print("Invalid format.")
            continue
        key, value = command.split(":", 1)
        if key == "name":
            result = find_by_author(value)
        elif key == "tags":
            result = find_by_tags_multi(value)
        elif key == "tag":
            result = find_by_tags(value)
        else:
            print("Unknown command")
            continue
        print(result)