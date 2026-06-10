# def check_brakets(infix_str: str) -> int:
#     braket_stack: list = []
#     for i in range(len(infix_str)):
#         if infix_str[i] not in "()": continue
#         if infix_str[i] == "(": 
#             braket_stack.append(infix_str[i])
#         else:
#             if len(braket_stack) == 0:
#                 return i
#             else:
#                 braket_stack.pop()
#         if len(braket_stack) !=0:
#             return len(infix_str)
#         else:
#             return -1
        
# infix_str = "ahdayda09) dhsg dasj( +ef) )"
# print(check_brakets(infix_str))
