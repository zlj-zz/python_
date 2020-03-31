# 信息校验型反爬虫

## User-Agent 反爬虫

通过校验 `User-Agent` 来区分爬虫. 它是浏览器的身份标识.

### 绕过

在请求 `url` 时,加入 `headers` 指定请求头.

```python
import requeste

url = ''
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100202 Firefox/62.0'}

response = requeste.get(url, headers=headers)
```

## Cookie 反爬虫

`Cookie` 可以理解为在HTTP 协议下,服务器或其他脚本语言维护客户端信息的一种方式,是保存在客户端的文本协议,`Cookie` 往往包含客户端或用户的相关信息.

*服务器可以通过校验 `Cookie` 中是否包含指定信息来进行反爬虫.*

### 绕过

```python
import requeste

url = ''
headers = {'Cookie': 'isfirst=789kq7uc1ppuis'}

response = requeste.get(url, headers=headers)
print(response.status_code)
```

通常会使用 `javascipt` 动态生成验证信息,而不会单纯的重复使用相同的验证信息.

## 签名验证饭爬虫

签名是根据数据源进行计算或加密的过程,签名的结果是一个具有唯一性和一致性的字符串.签名结果的特性使得它成为验证数据来源和数据完整性的条件,可以有效的避免服务器端将伪造的数据或被篡改的数据当成正常数据处理.

可以通过网络分析查看 `data` 中数据参数,解析加密的过程,用相同的加密方式加密,获得正确的签名验证.

案例:[有道翻译验证](https://github.com/zlj-zz/python_/blob/master/anti-crawl_practice/youdao/youdao.py) 

常使用 `MD5` 加密方式和 时间戳 来用作加密基础.

## WebSocket 握手验证反爬虫

通过在接受客户端的信息后,加入数据的校验流程,若检验通过则向客户端发送信息,否则不做处理.

信息校验主要解决了客户端身份鉴别,数据来源判断和合法性判断等问题,避免了数据接收者使用被篡改过的数据,保证了数据的有效性.

---

# 动态渲染反爬虫

## 常见的动态渲染反爬虫案例

### 自动执行的异步请求

异步请求能够减少网络请求的时间,从而提升网页加载的速度.将网页分成若干部分,通过异步请求的方式获取数据,可以提高用户体验,减少用户等待时间.

### 点击事件和计算

点击事件是指用户的鼠标点击按钮或标签等页面元素的操作,这类事件通常会与一个 `JavaScript` 方法绑定在一起, 这里的计算是指使用 `JavaScript` 计算数值并将结果渲染到网页.

### 下拉加载和异步请求

下来加载实际上是一种翻页操作,翻页和下拉都是为了查看不同的内容.

## 通用解决方法


