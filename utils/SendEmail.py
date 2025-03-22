# -*- coding: utf-8 -*-
'''
@Time    : 2025/3/21 17:34
@Author  : cody
@File    : SendEmail.py

'''
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from playwright.sync_api import sync_playwright

from config.setting import BASE_PATH, Send_Email_Account, Authorization, Receiver_To, Receiver_Cc, REPORT_PATH

from utils.TimeFormat import get_local_date


class SMTP:
    def __init__(self, smtp_host="smtp.gmail.com", port=465):
        # 连接邮件服务器
        self.__server = smtplib.SMTP_SSL(smtp_host, port)
        # self.__sender = "cody接口自动化测试"  # 发件人邮箱账号
        self.__mailboxContainer = MIMEMultipart()  # 创建邮箱容器
        self.__receiver = []
        self.mail_from_name = "XXX自动化测试"  # 标题

    def __del__(self):  # 对象销毁的时候,自动调用执行
        """
        关闭连接对象
        :return:
        """
        try:

            self.__server.quit()
        except Exception as e:
            pass

    def login(self, account, authorization):
        """登录邮箱服务器"""
        self.__sender = account
        self.__server.login(account, authorization)  # 括号中对应的是发件人邮箱账号、邮箱密码

    def add_subject(self, subject):
        """添加邮件主题"""
        self.__mailboxContainer['Subject'] = subject  # 邮箱主题

    def add_receiver(self, receiver_to: list, receiver_cc: list = None):
        """
        添加邮件接收人
        receiver_to：收件人
        receiver_cc：抄送人
        """
        self.__mailboxContainer["From"] = formataddr(pair=(self.mail_from_name, self.__sender))
        self.__mailboxContainer["To"] = ",".join(receiver_to)  # 邮箱接收人
        self.__mailboxContainer['Cc'] = ",".join(receiver_cc)  # 邮箱抄送人
        self.__receiver = receiver_to + receiver_cc

    def add_content(self, content, mail_type="plain", append_imgs: list = None):
        """
        添加邮箱内容
        content：邮箱内容
        mail_type：内容的类型
        append_imgs：当为html类型时追加图片内容
        """
        if mail_type != "html" and append_imgs is not None:
            raise ValueError(f"main_type的值不为html，但append_img不是空")

        if mail_type == "html" and append_imgs is not None:
            for append_img in append_imgs:
                img_tag = f"<p><img src='cid:image{append_imgs.index(append_img)}'></p>"
                content += img_tag
                # 读取图片信息
                with open(append_img, "rb") as f:
                    msg = f.read()
                msgImage = MIMEImage(msg, 'html', name="reportPicture.png")

                # 定义图片 ID，在 HTML 文本中引用
                msgImage.add_header('Content-ID', f'<image{append_imgs.index(append_img)}>')
                self.__mailboxContainer.attach(msgImage)
        self.__mailboxContainer.attach(MIMEText(content, mail_type, "utf-8"))

    def add_attach(self, file_path, filename):
        """添加单个附件"""
        if not os.path.exists(file_path):
            raise ValueError(f"文件【{file_path}】不存在")

        if not os.path.isfile(file_path):
            raise ValueError(f"【{file_path}】不是文件")

        # 构造文本附件
        with open(file_path, "rb") as f:
            msg = f.read()
        att = MIMEText(msg, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = f'attachment; filename="{filename}"'  # 这里的filename可以任意写，写什么名字，邮件附件中显示什么名字
        self.__mailboxContainer.attach(att)

    def add_attachs(self, file_paths: list):
        """添加多个附件"""
        for file_path in file_paths:
            self.add_attach(file_path)

    def send(self):
        """发送邮件"""
        self.__server.sendmail(self.__sender, self.__receiver, self.__mailboxContainer.as_string())

    def mail_content(self, appKey, builder, commitId, startTime, gitBranch, type="app_smoke"):
        '''

        :param appKey:
        :param builder:
        :param commitId:
        :param startTime:
        :param gitBranch:
        :return:
        '''
        if type == "app_regression":
            mail_content = f"""
            <h2>{appKey}应用自动化回归测试成功，请构建人{builder}关注</h2>
            <p>本次自动化冒烟测试执行概况如下：</p>
            <p>{builder}在{startTime}触发了一次{appKey}构建任务，构建commitid：{commitId}；构建分支：{gitBranch}</p>
            <p>报告内容如下，如需查看更多细节，请查看附件</p>
            <p>(此邮件是系统自动发出，不要回复此邮件)</p>
            """
        elif type == "app_performance":
            mail_content = f"""
            <h2>{appKey}应用自动化性能测试成功，请构建人{builder}关注</h2>
            <p>本次自动化冒烟测试执行概况如下：</p>
            <p>{builder}在{startTime}触发了一次{appKey}构建任务，构建commitid：{commitId}；构建分支：{gitBranch}</p>
            <p>报告内容如下，如需查看更多细节，请查看附件</p>
            <p>(此邮件是系统自动发出，不要回复此邮件)</p>
            """
        else:
            mail_content = f"""
            <h2>{appKey}应用自动化冒烟测试成功，请构建人{builder}关注</h2>
            <p>本次自动化冒烟测试执行概况如下：</p>
            <p>{builder}在{startTime}触发了一次{appKey}构建任务，构建commitid：{commitId}；构建分支：{gitBranch}</p>
            <p>报告内容如下，如需查看更多细节，请查看附件</p>
            <p>(此邮件是系统自动发出，不要回复此邮件)</p>
            """
        return mail_content


def get_report_picture(htmlName):
    pic_path = REPORT_PATH + "test.png"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(htmlName)
        page.screenshot(path=pic_path)
        browser.close()
    return pic_path


def send_email(htmlName, url_report, test_type='自动化冒烟'):
    '''
    发送文件
    待定项：获取当前软件版本
    :return:
    '''
    mailbox = SMTP()
    mailbox.login(Send_Email_Account, Authorization)

    # 添加邮箱主题
    mailbox.add_subject("使用SMTP封装类发送的邮件")

    mailbox.add_receiver(Receiver_To, Receiver_Cc)

    # 添加邮箱内容
    send_time = get_local_date()
    mail_content = """
    <h2>%s版本%s冒烟测试失败，请构建人%s关注</h2>
    <p>本次自动化冒烟测试执行概况如下：</p>
    <p>%s在%s分触发了一次自动化测试构建任务</p>
    <p>简陋报告内容如下，如需查看具体执行错误，请查看附件</p>
    <p>访问以下地址亦可查看详细报告：%s </p>
    <p>(此邮件是系统自动发出，不要回复此邮件)</p>
    """ % ("test", test_type, "cody", "cody", send_time, url_report)
    report_picture_name = get_report_picture(htmlName=htmlName)
    append_imgs = [report_picture_name]
    # print(append_imgs)
    mailbox.add_content(mail_content, mail_type="html", append_imgs=append_imgs)

    # 添加附件
    mailbox.add_attach(file_path=htmlName, filename="test.html")
    #
    # 发送邮箱
    mailbox.send()


if __name__ == '__main__':
    print(BASE_PATH, Send_Email_Account, Authorization, Receiver_To, Receiver_Cc)
    htmlName = REPORT_PATH + "2025_03_21_164424_report.html"
    url_report = "www.baidu.com"
    send_email(htmlName, url_report, test_type='自动化')
