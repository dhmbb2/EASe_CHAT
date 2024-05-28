def is_sjtu_email(email):
    return email.endswith('@sjtu.edu.cn')

# 测试
print(is_sjtu_email('example@sjtu.edu.cn'))  # 输出：True
print(is_sjtu_email('example@gmail.com'))  # 输出：False