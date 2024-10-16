import random
import math

def miller_rabin(n, k=7):  # 用于判断是否为素数
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow_mod(a, d, n)  # 计算 a^d % n
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow_mod(x, 2, n)  # 逐次平方
            if x == n - 1:
                break
        else:
            return False  # 说明 n 是合数
    return True  # 说明 n 可能是素数

def get_p_q():  # 获取大素数
    _min = 10**96
    _max = 10**128
    p = random.randint(_min, _max)
    q = random.randint(_min, _max)
    while not(miller_rabin(p)):
        p = random.randint(_min, _max)
    while not(miller_rabin(q)) or p == q:
        q = random.randint(_min, _max)
    return p, q

# 欧几里德算法实现
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# 判断两个数是否互质
def are_coprime(a, b):
    return gcd(a, b) == 1

# 扩展欧几里德算法
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

# 计算 a 在模 m 下的逆元
def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"{a} 和 {m} 不是互质的，逆元不存在")
    return x % m

def get_e(phin):
    e = random.randint(2, phin)
    while not are_coprime(e, phin):
        e = random.randint(2, phin)
    return e

def get_key():
    (p, q) = get_p_q()
    n = p * q
    phin = (p - 1) * (q - 1)
    e = get_e(phin)
    d = mod_inverse(e, phin)
    return (e, n), (d, n) ,(p,q)

def encode(m, key):
    e, n = key
    _c  = []
    for i in m:
        _c.append(pow_mod(i, e, n))
    c = int2str(_c, int(math.log2(n) + 100))
    return c

def decode(c, key):
    d, n = key
    int_list = string2int_group(c, group_size=int(math.log2(n) + 100)) 
    decrypted_list = [pow_mod(i, d, n) for i in int_list]
    return decrypted_list

def int_list_to_string(int_list):
    decoded_str = ""
    for num in int_list:
        str_num = str(num).zfill(6)  # 确保每个ASCII码有3位
        for i in range(0, len(str_num), 3):
            ascii_code = int(str_num[i:i+3])
            decoded_str += chr(ascii_code)  # 转换为字符
    return decoded_str

def pow_mod(a, b, c):
    ans = 1
    a = a % c
    while b > 0:
        if b & 1 == 1:
            ans = (ans * a) % c
        b = b >> 1
        a = (a * a) % c
    return ans

def string2int_group(s, group_size=6):
    string_size = len(s)
    int_list = []
    group_num = string_size // group_size
    for i in range(group_num):
        num_str = s[i * group_size:(i + 1) * group_size]
        int_list.append(int(num_str))
    remainder = string_size % group_size
    if remainder != 0:
        num_str = s[group_num * group_size:]
        int_list.append(int(num_str))
    return int_list

def str2int(s):
    ss = ""
    for i in s:
        ascii_code = str(ord(i)).zfill(3) 
        ss += ascii_code
    return ss

def int2str(int_list, group_size):
    str_list = []
    for num in int_list:
        string = str(num)
        string_size = len(string)
        string = '0' * (group_size - string_size) + string
        str_list.append(string)
    return "".join(str_list)

def read_plaintext_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_ciphertext_to_file(ciphertext, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(ciphertext)

def read_ciphertext_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
def save_ciphertext_to_file(ciphertext, file_path):
    """将密文保存为二进制文件，密文的每两个字符作为一个字节"""
    # 将密文字符串的每两个字符转换为一个字节
    byte_data = bytearray()
    for i in range(0, len(ciphertext), 2):
        # 提取两个字符
        byte_str = ciphertext[i:i + 2]
        # 将两个字符转换为字节并添加到 bytearray 中
        byte_data.append(int(byte_str))  # 将字符串转换为整数并添加

    # 将字节数据写入文件
    with open(file_path, 'wb') as file:
        file.write(byte_data)  # 以二进制方式写入文件

def read_ciphertext_from_file(file_path):
    """从二进制文件读取密文"""
    with open(file_path, 'rb') as file:  # 打开文件为二进制读模式
        byte_data = file.read()  # 读取字节数据
    
    # 将字节数据转换回字符串，每个字节转换为两个字符
    ciphertext = ''.join(f'{byte:02}' for byte in byte_data)  # 将字节格式化为两位字符
    return ciphertext

# 主程序
if __name__ == "__main__":
    # 从文件读取明文
    plaintext_file = 'lab2/lab2-Plaintext.txt'  # 明文文件
    ciphertext_file = 'lab2/ciphertext.bin'  # 密文文件，以二进制格式保存
    m = read_plaintext_from_file(plaintext_file)
    
    int_m = string2int_group(str2int(m))  # 转为整数分组
    pub_key, pri_key , (p,q) = get_key()  # 生成密钥对
    
    # print("公钥:", pub_key)
    # print("私钥:", pri_key)
    e , n = pub_key
    d, _  = pri_key
    
    print("p = ",p)
    print("q = ",q)
    print("n = ",n)
    print("e = ",e)
    print("d = ",d)
    print("phin = ",  (p - 1) * (q - 1))
    # 加密
    c = encode(int_m, pub_key)
    save_ciphertext_to_file(c, ciphertext_file)  # 将密文保存为二进制文件
    print("密文已保存到文件:", ciphertext_file)

    # 解密
    c_from_file = read_ciphertext_from_file(ciphertext_file)  # 从文件读取密文
    decoded_int = decode(c_from_file, pri_key)  # 解密密文
    # print("解密后的整数:", decoded_int)

    # 将解密后的整数列表转换回字符串
    recovered_message = int_list_to_string(decoded_int)
    print("解密后的明文:", recovered_message)

