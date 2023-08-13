import hashlib
import random
import string
import binascii


def generate_password_1(salt, raw_password: str, min_length: int, max_length: int, lower_count: int,
                        upper_count: int, number_count: int, special_count: int):
    salt_hex = binascii.hexlify(salt).decode('utf-8')
    # 将输入数据连接成一个字符串
    input_data = raw_password + salt_hex
    # 计算 SHA-256 哈希值
    hex_dig = hashlib.sha256(input_data.encode()).hexdigest()

    seed = int.from_bytes(salt, byteorder='big')
    # 创建一个随机数生成器
    rng = random.Random(seed)
    random_string = ''
    for _ in range(lower_count):
        random_string += rng.choice(string.ascii_uppercase)
    for _ in range(upper_count):
        random_string += rng.choice(string.ascii_lowercase)
    for _ in range(number_count):
        random_string += rng.choice(string.digits)
    for _ in range(special_count):
        random_string += rng.choice("()`!@#$%^&*_-+=|{}[]:;'<>,.?")
    password_length = rng.randint(min_length, max_length)
    password = random_string + hex_dig[0:password_length - len(random_string)]
    return password
