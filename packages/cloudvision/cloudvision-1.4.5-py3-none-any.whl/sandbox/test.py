name = "b"
results = [
    {"description": "a", "prefix": "potato1"},
    {"description": "b", "prefix": "potato2"},
    {"description": "c", "prefix": "potato3"},
]

results = [result["prefix"] for result in results if result["description"] == name]

print(results)


def test():
    pass


test(irrelevant="dasd")
