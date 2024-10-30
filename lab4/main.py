import sympy,random ,math ,hashlib,json
def generate_large_prime(bits=256):
    return sympy.randprime(2**(bits - 1), 2**bits)

def find_primitive_root(p):
    if not sympy.isprime(p):
        raise ValueError(f"{p} 不是素数！")
    return sympy.primitive_root(p)


def calculate_mod_exp(p, g):
    x = random.randint(2, p - 2) 
    y = pow(g, x, p)  
    return x, y


def generate_key():
    p = generate_large_prime(bits=256)
    print(f"大素数 p: {p}")

    g = find_primitive_root(p)
    print(f"原根 g: {g}")

    x, y = calculate_mod_exp(p, g)
    print(f"随机选取的整数 x: {x}")
    print(f"计算结果 y = g^x mod p: {y}")
    print(f"私钥 x: {x}")
    print(f"公钥 (p, g, y): ({p}, {g}, {y})")
    
    return (p,g,y),x


def generate_valid_k(p):
    p_minus_1 = p - 1  
    while True:
        k = random.randint(2, p_minus_1 - 1)  
        if math.gcd(k, p_minus_1) == 1:
            return k

def compute_hash(m):
    hash_object = hashlib.sha256(m.encode('utf-8'))
    return int(hash_object.hexdigest(), 16)  
   

def sign_message(p, g, x, m):
    k = generate_valid_k(p)  
    r = pow(g, k, p)  

    H_m = compute_hash(m)  
    p_minus_1 = p - 1

    
    k_inv = sympy.mod_inverse(k, p_minus_1)  
    s = (k_inv * (H_m - x * r)) % p_minus_1

    return r, s



def send_message_with_signature(m, r, s, filename="signed_message.json"):
    
    message_data = {
        "message": m,
        "signature": {
            "r": r,
            "s": s
        }
    }

    
    with open(filename, "w") as f:
        json.dump(message_data, f, indent=4)
    
    print(f"签名消息已保存为 {filename}")



def load_signed_message(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data["message"], data["signature"]["r"], data["signature"]["s"]


def verify_signature(p, g, y, m, r, s):
    H_m = compute_hash(m)  
    left = (pow(y, r, p) * pow(r, s, p)) % p  
    right = pow(g, H_m, p)  
    is_valid = left == right  
    print(f"验证结果: {'通过' if is_valid else '不通过'}")
    return is_valid


def main():
    
    p = generate_large_prime(bits=256)
    g = find_primitive_root(p)
    
    
    x, y = calculate_mod_exp(p, g)
    print(f"公钥 (p, g, y): ({p}, {g}, {y})")
    print(f"私钥 x: {x}")

    
    message = "Hello, this is a test message!"
    print(f"待签消息: {message}")

    
    r, s = sign_message(p, g, x, message)
    print(f"签名值 r: {r}")
    print(f"签名值 s: {s}")

    
    send_message_with_signature(message, r, s, filename="lab4/signed_message.json")

    
    loaded_message, loaded_r, loaded_s = load_signed_message(filename="lab4/signed_message.json")
    print(f"从文件加载的消息: {loaded_message}")
    print(f"从文件加载的签名: r = {loaded_r}, s = {loaded_s}")

    
    verify_signature(p, g, y, loaded_message, loaded_r, loaded_s)


if __name__ == "__main__":
    main()