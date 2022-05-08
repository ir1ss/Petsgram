# 定义一些公共接口
import random, string
from io import BytesIO

from PIL import Image, Image, ImageFont, ImageDraw

# 验证码类
class ImageCode():
    # 随机生成颜色
    def rand_color(self):
        red = random.randint(32, 200)
        green = random.randint(22, 255)
        blue = random.randint(0, 200)
        return red, green, blue

    # 随机生成字符串数据
    def gen_next(self):
        # 从sample中生成随机的list
        list = random.sample(string.ascii_letters, 4)
        for i, j in enumerate(list):
            if j == 'l':
                list[i] = 'L'
            elif j == 'I':
                list[i] = 'i'
        return ''.join(list)

    # 画干扰线
    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width/2)
            y1 = random.randint(0, height/2)
            x2 = random.randint(0, width)
            y2 = random.randint(height/2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    # 画验证码
    def draw_verify_code(self):
        code = self.gen_next()
        width, height = 120, 50
        im = Image.new('RGB', (width, height), 'white')
        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(im)
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)), text=code[i], fill=self.rand_color(), font=font)
        self.draw_lines(draw, 2, width, height)
        return im, code

    # 生成验证码返回给后端的控制器
    def get_code(self):
        image, code = self.draw_verify_code()
        # 二级制对象
        # 这一步的目的是把图片转换成二进制数据传给控制器
        buf = BytesIO()
        image.save(buf, 'jpeg')
        bstring = buf.getvalue()
        return code, bstring

# 邮箱验证码
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

# 发送QQ邮箱验证码，参数为收件地址和随机生成的验证码
def send_email(receiver, ecode):
    sender = 'Petsgram <alexsun01@qq.com>'
    content = f"<br/>欢迎注册Petsgram，您的邮箱验证码为：<span style='color: black; font-size: 20px'>{ecode}</span></br>"
    # 转化为MIME格式
    message = MIMEText(content, 'html', 'utf-8')
    message['subject'] = Header('Petsgram验证码', 'utf-8')
    message['From'] = sender
    message['To'] = receiver
    # 建立与QQ邮箱服务器的连接
    smtpObj = SMTP_SSL('smtp.qq.com')
    smtpObj.login(user='alexsun01@qq.com', password='nhvgaifloxfibdfi')
    smtpObj.sendmail(sender, receiver, str(message))
    smtpObj.quit()

# 生成邮件验证码
def gen_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    return ''.join(str)

