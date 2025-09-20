# def max_positive_int(data: list) -> int:
#     if data == []:
#         return 0
#     return max(data)

# def max_positive_int(data: list) -> int:
#     data = [item for item in data if type(item) == int]
#     if data == []:
#         return 0
#     return max(data)

def max_positive_int(data: list) -> int:
    data = [item for item in data if type(item) in (int, float)]
    if data == []:
        return 0
    return max(data)



print(max_positive_int(["one", 2, 3.14]))
