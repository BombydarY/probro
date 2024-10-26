# def my_decorator(func):
#     def wrapper():
#         func()
#         print("Что-то происходит до вызова функции.")
#         print("Что-то происходит после вызова функции.")
#     return wrapper
#
#
# @my_decorator
# def say_hello():
#     print("Hello!")
#
# say_hello()
# from aiogram import types pep8

# def s (a,b,*args):
#     print(args)
# s(1,2,3,4,5,6)
x = [{"2075010057": "Grisharyzo"}, {"629401483": "pavelgodx"}, {"2075010057": "Grisharyzo"}, {"629401483": "pavelgodx"}, {"629401483": "pavelgodx"}, {"629401483": "pavelgodx"}, {"629401483": "pavelgodx"}, {"629401483": "pavelgodx"}, {"629401483": "pavelgodx"}, {"629401483": "pavelgodx"}, {"629401483": "pavelgodx"}, {"629401483": "pavelgodx"}, {"629401483": "pavelgodx"}]
ids = [list(f.keys())[0] for f in x ]

# for f in x:
#     ids.append(list(f.keys())[0])
print(ids)
