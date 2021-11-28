import time
import selenium.webdriver
import random
from selenium.webdriver.common.keys import Keys


usr_name = '042040415'
password = 'Charlotte2001826'

# 优点
youdian = ['老师平时上课的时候很认真，在课堂上讲解知识的时候很耐心，我们听不懂的时候会放慢节奏帮助我们一起弄清楚知识点',
           '老师授课的方式非常适合我们,他根据本课程知识结构的特点,重点突出,层次分明。',
           '课堂内容充实,简单明了,使学生能够轻轻松松掌握知识。']

# 建议
jianyi = ['合适的讲课速度。由于大学的一些课程在理解上还是有一定的难度的',
          '在每节上课之前讲一些有趣的开场白。上课时,用一些风趣幽默的语言。',
          '希望老师可以允许学生不经过导员请假,有时候学生会有一些急事不能及时上课']


# 函数功能: 提取字符串中第一个数字,支持科学计数法. 如果字符串中不包含数字则返回0
def get_num_from_string(sss):
    slen = len(sss)
    ret_value = 0  # 返回值
    sflag = 0  # 标记是否遇到第一个数字字符 0-未遇到 1-已遇到
    zflag = 1  # 数字整数部分标记  默认1-整数
    pnflag = 1  # 正负号标记   默认1-正数
    scientificEnumerationFlag = 0  # 科学计数法标记
    cnt = 1  # 小数部分长度计数
    power_num = 0  # 幂
    power_pnFlag = 1
    # print("字符串长度=%s"%slen)
    for i in range(slen):
        if sss[i].isdigit():
            sflag = 1
            if scientificEnumerationFlag:
                power_num = power_num * 10 + int(sss[i])
            # print("current step power_num=%s"%power_num)
            else:
                if zflag == 1:
                    ret_value = ret_value * 10 + int(sss[i])
                # print(ret_value)
                else:
                    divnum = 10 ** cnt
                    ret_value = ret_value + float(sss[i]) / (divnum)
                    # print("div_num=%s, current step ret_value=%s"%(divnum,ret_value))
                    cnt += 1
        else:
            if sflag == 1:
                if sss[i] == '.':
                    zflag = 0
                elif sss[i] == 'e' and (sss[i + 1] == '+' or sss[i + 1] == '-'):
                    scientificEnumerationFlag = 1  # 开启科学计数法
                    if sss[i + 1] == '+':
                        power_pnFlag = 1
                    else:
                        power_pnFlag = -1
                # print("幂的符号=%s"%power_pnFlag)
                else:
                    if sss[i - 1] == 'e' and (sss[i] == '+' or sss[i] == '-'):
                        continue
                    else:
                        # print("-------------break------------")
                        break
            else:
                if sss[i] == '-':
                    pnflag = -1
    return pnflag * ret_value * (10 ** (power_num * power_pnFlag))  # 符号*返回值*(10**(幂*幂的符号))


web = selenium.webdriver.Edge()
# 登录网页
web.get('http://cdjwc.ccu.edu.cn/jsxsd/')
el_user = web.find_element('xpath', '//*[@id="userAccount"]').send_keys(usr_name)
el_password = web.find_element('xpath', '//*[@id="userPassword"]').send_keys(password)
el_login = web.find_element('xpath', '//*[@id="btnSubmit"]').click()
print(web.title)
time.sleep(1)
el_PJ = web.find_element('xpath', '/html/body/div[5]/a[2]/div').click()
time.sleep(1)
el_FL_list = web.find_elements('xpath', '//*[@id="Form1"]/table/tbody/tr')
# 获取当前窗口的句柄
handles = web.current_window_handle
hrefs = []

for el_FL in el_FL_list[1:]:
    href = el_FL.find_element('xpath', './td[8]/a').get_attribute("href")
    hrefs.append(href)

for url in hrefs:
    web.get(url)

    print(web.window_handles)

    page_sum = get_num_from_string(web.find_element('xpath', '//*[@id="PagingControl1_divOuterClass"]/div/div[2]/span').text)
    page = int(web.find_element('xpath', '//*[@id="pageIndex"]').get_attribute("value"))
    while page <= page_sum:
        el_tea_list = web.find_elements('xpath', '//*[@id="dataList"]/tbody/tr')
        for el_tea in el_tea_list[1:]:
            el_tea_assess = el_tea.find_element('xpath', './td[9]')
            el_tea_assess_text = el_tea_assess.text
            print(web.window_handles)
            print(el_tea_assess_text)
            if el_tea_assess_text == '[查看]':
                continue
            elif el_tea_assess_text == '[评价] [查看]':
                el_tea_assess_ass = el_tea_assess.find_element('xpath', './a[1]')
                el_tea_assess_ass.click()
                web.switch_to.window(web.window_handles[-1])
                print(web.window_handles)
                res_list = web.find_elements('xpath', '//*[@id="table1"]/tbody/tr')
                values = []
                for res in res_list[1:-2]:
                    value = res.find_element('xpath', 'td[1] / input').get_attribute('value')
                    values.append(value)
                # / html / body / div / form / table[1] / tbody / tr[12] / td[2] / textarea
                ran_youdian = random.randint(0, len(youdian)-1)
                ran_jianyi = random.randint(0, len(jianyi)-1)
                PJ_text_area = res_list[-2].find_element('xpath', 'td[2] / textarea')
                PJ_text_area.send_keys(youdian[ran_youdian])

                PJ_text_area = res_list[-1].find_element('xpath', 'td[2] / textarea')
                PJ_text_area.send_keys(jianyi[ran_jianyi])

                print(values)
                ran = random.randint(0, len(values) - 1)
                ran_value = values[ran]
                for value in values:
                    web.find_element('xpath', '//*[@id="pj0601id_' + value + '_1"]').click()
                    if ran_value == value:
                        web.find_element('xpath', '//*[@id="pj0601id_' + value + '_2"]').click()
                web.find_element('xpath', '//*[@id="tj"]').click()
                time.sleep(1)

                dig = web.switch_to.alert
                time.sleep(1)
                # 打印对话框的内容
                print(dig.text)
                # 点击“确认”按钮
                dig.accept()
                # 点击“取消”按钮
                # dig_confirm.dismiss()
                time.sleep(1)

                dig_2 = web.switch_to.alert
                time.sleep(1)
                # 打印对话框的内容
                print(dig_2.text)
                # 点击“确认”按钮
                dig_2.accept()

                time.sleep(1)

                web.switch_to.window(handles)

        # 翻页
        page = page + 1
        loc = web.find_element('xpath', '//*[@id="pageIndex"]')
        loc.send_keys(Keys.CONTROL + 'a')  # 全选
        loc.send_keys(Keys.DELETE)  # 删除，清空
        loc.send_keys(page)  # 写入新的值
        loc.send_keys(Keys.ENTER)
