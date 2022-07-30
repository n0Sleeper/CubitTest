import json
import time
from pathlib import Path

import requests
import shodan
from ttkbootstrap.scrolled import ScrolledText

from CollapsingFrame import CollapsingFrame
from MenuBtn import *
from saveAPI import *

windows = ttk.Window(title='Cubit_Yu 【一款集成式工具】 制作者：Yu0ri')
windows.wm_iconbitmap(True,'logo.ico')
time_now = time.strftime("%Y%m%d_%H_%M", time.localtime())


#窗口初始化
# width = str(windows.winfo_screenwidth())      #获取屏幕长度
# height = str(windows.winfo_screenheight())    #获取屏幕宽度
windows.geometry('1600x900+200+100')

#添加图片
img_file = {
    'setting':'icons8_settings_32px.png',
    'help':'icons8_wrench_32px.png',
    'fofa':'fofa.png',
    'shodan':'shodan.png',
    'Exp':'Exp.png',
    'zoomEye':'zoomEye.png',
    'Quake':'Quake.png'
}
photoFile = []
absPath = Path(__file__).parent.absolute()   #获取绝对路径
imgPath = absPath / 'image'
for key,val in img_file.items():
    _path = imgPath / val
    photoFile.append(ttk.PhotoImage(name=key,file=_path))

#fofa对应项
def fofa_btn():
    shodan_left.pack_forget()
    shodan_right.pack_forget()
    fofa_left.pack(side=LEFT, anchor=NW,padx=5,pady=5)
    fofa_right.pack(side=LEFT, anchor=NW, padx=3, pady=3)

#shodan对应项
def shodan_btn():
    fofa_left.pack_forget()
    fofa_right.pack_forget()
    shodan_left.pack(side=LEFT, anchor=NW, padx=5, pady=5)
    shodan_right.pack(side=LEFT, anchor=NW, padx=3, pady=3)


#菜单栏
buttonBar = ttk.Frame(windows,style='primary.TFrame')
buttonBar.pack(fill=X,side=TOP,padx=1)

#设置项
btn_set = ttk.Button(
                    master=buttonBar,
                    text='设置',
                    image='setting',
                    command=menuSetting
                    )
btn_set.grid(row=0,column=0)

#帮助项
btn_help = ttk.Button(
                    master=buttonBar,
                    text='帮助',
                    image='help',
                    command=menuHelp
                     )
btn_help.grid(row=0,column=1)

#exp
btn_exp = ttk.Button(
                    master=buttonBar,
                    text='Exp',
                    image='Exp',
                    command=menuExp
                     )
btn_exp.grid(row=0,column=2)


'''左边布局'''
left_panel = ttk.Frame(windows, style='bg.TFrame')
left_panel.pack(side=LEFT, fill=Y)

bus_cf = CollapsingFrame(left_panel)
bus_cf.pack(fill=X, pady=1)

#空间测绘
net_tools = ttk.Frame(bus_cf, padding=0)
net_tools.columnconfigure(1, weight=1)
bus_cf.add(
            child=net_tools,
            title='空间测绘搜索',
            bootstyle=SECONDARY,
            )

#fofa搜索
fofa_btn1 = ttk.Button(
            master=net_tools,
            text='fofa搜索',
            image='fofa',
            compound=LEFT,
            command=fofa_btn,
            bootstyle='danger-outline'
        )
fofa_btn1.pack(side=TOP,fill=X)

#shodan搜索
shodan_btn1 = ttk.Button(
            master=net_tools,
            text='shodan搜索',
            image='shodan',
            compound=LEFT,
            command=shodan_btn,
            bootstyle='info-outline'
        )
shodan_btn1.pack(side=TOP,fill=X)

#ZoomEye钟馗之眼
zoomEye_func = lambda:Messagebox.ok(message='zoomEye逻辑代码正在开发',alert=True)
zoomEye_btn = ttk.Button(
            master=net_tools,
            text='zoomEye钟馗之眼',
            image='zoomEye',
            compound=LEFT,
            command=zoomEye_func,
            bootstyle='info-outline'
        )
zoomEye_btn.pack(side=TOP,fill=X)

#Quake搜索
Quake_func = lambda:Messagebox.ok(message='Quake逻辑代码正在开发',alert=True)
Quake_btn = ttk.Button(
            master=net_tools,
            text='Quake搜索',
            image='Quake',
            compound=LEFT,
            command=Quake_func,
            bootstyle='info-outline'
        )
Quake_btn.pack(side=TOP,fill=X)

#实用工具(尚在开发中)
net_tools = ttk.Frame(bus_cf, padding=5)
net_tools.columnconfigure(1, weight=1)
bus_cf.add(
            child=net_tools,
            title='使用小工具',
            bootstyle=SECONDARY,
            )


'''右边布局'''
right_frame = ttk.Frame(windows)
right_frame.pack(side=TOP,fill=BOTH,anchor=W)

#fofa_frame容器
fofa_left = ttk.LabelFrame(
                            master=right_frame,
                            text='fofa搜索',
                            style=INFO,
                            padding=5
                            )
fofa_left.pack(side=LEFT, anchor=NW,padx=5,pady=5)


#fofa查询标签
lab_fofa = ttk.Label(master=fofa_left, text='查询语句：')
lab_fofa.grid(row=0,column=0)

#fofa搜索框
fofaBase64Search = ttk.StringVar(master=fofa_left,value="填写base64加密后的fofa搜索语法，具体可以参照右边")
text_search_fofa = ttk.Entry(
                    master=fofa_left,
                    width=90,
                    font=('宋体',10),
                    textvariable=fofaBase64Search
                        )

def text_search_fofa_delete(event):
    text_search_fofa.delete(0,END)
    return None

text_search_fofa.bind('<Button-1>',text_search_fofa_delete)
text_search_fofa.grid(row=0,column=1,ipadx=3,ipady=3,padx=3,pady=3,sticky=W)

def fofaSearch():
    global fofaBase64Search,fofa_ST,sizeFofaSearch
    param = fofa_read()
    # print(param)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }
    url = 'https://fofa.info/api/v1/search/all'
    size = sizeFofaSearch.get()
    if size.isdigit():
        param['size'] = int(size)
    fofaBase64 = fofaBase64Search.get()
    param['qbase64'] = fofaBase64
    try:
        res = requests.get(headers=headers,
                           url=url,
                           params=param)
        if res.status_code == -1:
            funcFofaError = lambda:Messagebox.show_error(message="账号出错，请检查email和key的配置信息")
            funcFofaError()
            fofa_ST.insert(END,"账号出错，请检查email和key的配置信息")
        elif res.status_code == -4:
            funcFofaError = lambda:Messagebox.show_error(message="请求参数出错，请检查搜索语句。注意：请填写base64编码后的语句")
            funcFofaError()
            fofa_ST.insert(END,"请求参数出错，请检查搜索语句。注意：请填写base64编码后的语句")
        elif res.status_code == -5:
            funcFofaError = lambda: Messagebox.show_error(message="查询异常，请检查配置的email和key,请注意，非普通会员以上用户，如果F币不足，将无法查询")
            funcFofaError()
            fofa_ST.insert(END, "查询异常，请检查配置的email和key,请注意，非普通会员以上用户，如果F币不足，将无法查询")
        else:
            resT = json.loads((res.content).decode('utf-8'))
            length = len(resT['results'])
            fofa_ST.insert(END,"正在对搜索到的信息进行整合：\n")
            fileUrlPath = str(os.getcwd()) +'\\results\\fofa\\' +time_now + '_url.txt'
            fileAllPath = str(os.getcwd()) + '\\results\\fofa\\' + time_now + '_all.txt'
            with open(fileAllPath,'a+') as allF:
                for i in range(length):
                    all = 'url:' + resT['results'][i][0] + '\t' + \
                          'ip:' + resT['results'][i][1] + '\t' + \
                          'port:' + resT['results'][i][2]
                    allF.write(all+'\n')
            with open(fileUrlPath,'a+') as urlF:
                for j in range(length):
                    url = resT['results'][j][0]
                    if url[:7] == 'http://' or url[:8] == 'https://':
                        fofa_ST.insert(END,url+'\n')
                        urlF.write(url+'\n')
                    else:
                        newurl = 'http://'+ str(url)
                        fofa_ST.insert(END,newurl+'\n')
                        urlF.write(newurl+'\n')

            successSearch = lambda:Messagebox.ok(message='搜索完成，文件已保存在results目录下')
            successSearch()
            fofa_ST.insert(END,'搜索完成，文件已保存在results目录下\n'
                               '=====================================================\n')

    except Exception as error:
        FailedSearch = lambda:Messagebox.show_error(message="出错了！请检查base64编码前的语句是否正确，如有问题，请联系作者修改\n")
        FailedSearch()


#查询条数
sizeFofaSearch = ttk.StringVar(master=fofa_left,value="根据需求填写查询条数,若不填写，则默认搜索全部")
num_fofa = ttk.Label(
                    master=fofa_left,
                    text='查询条数：'
                    )
num_fofa.grid(row=1,column=0)
num_search_fofa = ttk.Entry(
                        master=fofa_left,
                        width=30,
                        font=('宋体',10),
                        textvariable=sizeFofaSearch
                        )

#点击输入框，自动清除内容
def num_search_fofa_delete(event):
    num_search_fofa.delete(0,END)
    return None
num_search_fofa.bind('<Button-1>',num_search_fofa_delete)

num_search_fofa.grid(row=1,column=1,ipadx=3,ipady=3,padx=3,pady=3,sticky=W)


#查询按钮
btnSearch_fofa = ttk.Button(master=fofa_left, style=INFO, text='点击查询',width=10,command=fofaSearch)
btnSearch_fofa.grid(row=2,column=0,ipadx=3,ipady=3,padx=3,pady=3,sticky=W)

#查询结果
res_lab_fofa = ttk.Label(
                    master=fofa_left,
                    text='  查询条数：'
                    )
res_lab_fofa.grid(row=3,column=0,sticky=N)

fofa_ST = ScrolledText(master=fofa_left, width=90, height=50,font=('楷体',10),bootstyle='danger-round')
fofa_ST.grid(row=3,column=1,sticky=W)

#fofa语法参考
fofa_right = ttk.LabelFrame(
                            master=right_frame,
                            text='fofa语法参考',
                            style=SUCCESS,
                            padding=5
                            )
fofa_right.pack(side=LEFT, anchor=NW,padx=3,pady=3)

fofa_CMD = ScrolledText(master=fofa_right, width=90, height=55,font=('黑体',12),bootstyle='success-round')
fofa_CMD.pack(side=RIGHT,fill=BOTH)

fofa_CMD.insert(END, r"""直接输入查询语句，将从标题，html内容，http头信息，url字段中搜索

• title="abc" 从标题中搜索abc。例：标题中有北京的网站

• header="abc" 从http头中搜索abc。例：jboss服务器

• body="abc" 从html正文中搜索abc。例：正文包含Hacked by

• domain="qq.com" 搜索根域名带有qq.com的网站。例： 根域名是qq.com的网站

• host=".gov.cn" 从url中搜索.gov.cn,注意搜索要用host作为名称。例： 政府网站, 教育网站

• port="443" 查找对应443端口的资产。例： 查找对应443端口的资产

• ip="1.1.1.1" 从ip中搜索包含1.1.1.1的网站,注意搜索要用ip作为名称。例： 查询IP为220.181.111.1的网站; 如果想要查询网段，可以是： ip="220.181.111.1/24"，例如查询IP为220.181.111.1的C网段资产

• protocol="https" 搜索指定协议类型(在开启端口扫描的情况下有效)。例： 查询https协议资产

• city="Hangzhou" 搜索指定城市的资产。例： 搜索指定城市的资产

• region="Zhejiang" 搜索指定行政区的资产。例： 搜索指定行政区的资产

• country="CN" 搜索指定国家(编码)的资产。例： 搜索指定国家(编码)的资产

• cert="google" 搜索证书(https或者imaps等)中带有google的资产。例： 搜索证书(https或者imaps等)中带有google的资产

• banner=users && protocol=ftp 搜索FTP协议中带有users文本的资产。例： 搜索FTP协议中带有users文本的资产

• type=service 搜索所有协议资产，支持subdomain和service两种。例： 搜索所有协议资产

• os=windows 搜索Windows资产。例： 搜索Windows资产

• server=="Microsoft-IIS/7.5" 搜索IIS 7.5服务器。例： 搜索IIS 7.5服务器

• app="海康威视-视频监控" 搜索海康威视设备，更多app规则。例： 搜索海康威视设备

• after="2017" && before="2017-10-01" 时间范围段搜索。例： 时间范围段搜索，注意： after是大于并且等于，before是小于，这里after="2017" 就是日期大于并且等于 2017-01-01 的数据，而 before="2017-10-01" 则是小于 2017-10-01 的数据

• asn="19551" 搜索指定asn的资产。例： 搜索指定asn的资产

• org="Amazon.com, Inc." 搜索指定org(组织)的资产。例： 搜索指定org(组织)的资产

• base_protocol="udp" 搜索指定udp协议的资产。例： 搜索指定udp协议的资产

• is_ipv6=true 搜索ipv6的资产,只接受true和false。例： 搜索ipv6的资产

• is_domain=true 搜索域名的资产,只接受true和false。例： 搜索域名的资产

• ip_ports="80,443" 或者 ports="80,443" 搜索同时开放80和443端口的ip资产(以ip为单位的资产数据)。例： 搜索同时开放80和443端口的ip

• ip_country="CN" 搜索中国的ip资产(以ip为单位的资产数据)。例： 搜索中国的ip资产

• ip_region="Zhejiang" 搜索指定行政区的ip资产(以ip为单位的资产数据)。例： 搜索指定行政区的资产

• ip_city="Hangzhou" 搜索指定城市的ip资产(以ip为单位的资产数据)。例： 搜索指定城市的资产

• ip_after="2019-01-01" 搜索2019-01-01以后的ip资产(以ip为单位的资产数据)。例： 搜索2019-01-01以后的ip资产

• ip_before="2019-01-01" 搜索2019-01-01以前的ip资产(以ip为单位的资产数据)。例： 搜索2019-01-01以前的ip资产


高级搜索：可以使用括号 和 && || !=等符号，如
title="powered by" && title!=discuz

title!="powered by" && body=discuz

( body="content=\"WordPress" || (header="X-Pingback" && header="/xmlrpc.php" && body="/wp-includes/") ) && host="gov.cn"

新增==完全匹配的符号，可以加快搜索速度，比如查找qq.com所有host，可以是domain=="qq.com"



注意事项:

* 如果查询表达式有多个与或关系，尽量在外面用（）包含起来

剩下来，就是发挥你想象力的时候了 ；）""")

def shodanSearch():
    global shodanParamSearch,shodanSearchNum
    SHODAN_API_KEY = shodan_read()
    API = shodan.Shodan(SHODAN_API_KEY)
    shodan_ST.insert(END,"shodan搜索进行中，请勿关闭程序\n")
    try:
        paramSearch = shodanParamSearch.get()
        NumSearch = shodanSearchNum.get()
        fileUrlPath = str(os.getcwd()) + '\\results\\shodan\\' + time_now + '_url.txt'
        fileAllPath = str(os.getcwd()) + '\\results\\shodan\\' + time_now + '_all.txt'
        if NumSearch.isdigit():
            NumSearch = int(NumSearch)
            page_num = NumSearch / 100
            page_num += 1
            page_num = int(page_num)
        else:
            page_num = 2

        for p in range(1,page_num):
            results = API.search(paramSearch,page=p)
            for i in range(100):
                with open(fileUrlPath,'a+') as f:
                    ip_str = str(results['matches'][i]['ip_str'])
                    port = str(results['matches'][i]['port'])
                    if port is not None:
                        newUrl = 'http://' + ip_str + ':'+port +'\n'
                        f.write(newUrl)
                        shodan_ST.insert(END,newUrl)
                    else:
                        noPortUrl = 'http://' + ip_str +'\n'
                        f.write(noPortUrl)
                        shodan_ST.insert(END,noPortUrl)
        funcSuccess = lambda:Messagebox.ok(message='搜索完毕，文件保存在/results/shodan下')
        funcSuccess()
        shodan_ST.insert(END,"搜索完毕，文件保存在/results/shodan下\n"
                             "======================================================")

    except Exception as e:
        shodan_ST.insert(END,'搜索出错，请检查搜索语句和shodan配置，如果无误，请联系作者！')
        pass


#shodan布局
shodan_left = ttk.LabelFrame(
                            master=right_frame,
                            text='shodan搜索',
                            style=INFO,
                            padding=5
                            )
# shodan_left.pack(side=LEFT, anchor=NW,padx=5,pady=5)

#shodan查询标签
lab_shodan = ttk.Label(master=shodan_left, text='查询语句：')
lab_shodan.grid(row=0,column=0)


shodanParamSearch = ttk.StringVar(master=shodan_left,value="填写shodan搜索语法，具体可以参照右边")

#shodan搜索框
text_search_shodan = ttk.Entry(
                    master=shodan_left,
                    width=90,
                    font=('宋体',10),
                    textvariable=shodanParamSearch
                        )

#点击输入框，自动清除内容
def text_search_shodan_delete(event):
    text_search_shodan.delete(0,END)
    return None
text_search_shodan.bind('<Button-1>',text_search_shodan_delete)
text_search_shodan.grid(row=0,column=1,ipadx=3,ipady=3,padx=3,pady=3,sticky=W)

shodanSearchNum = ttk.StringVar(master=shodan_left,value='根据自己情况填写相应条数')

#查询条数
num_shodan = ttk.Label(
                    master=shodan_left,
                    text='查询条数：'
                    )
num_shodan.grid(row=1,column=0)
num_search_shodan = ttk.Entry(
                        master=shodan_left,
                        width=30,
                        font=('宋体',10),
                        textvariable=shodanSearchNum
                        )

def num_search_shodan_delete(event):
    num_search_shodan.delete(0,END)
    return None
num_search_shodan.bind('<Button-1>',num_search_shodan_delete)
num_search_shodan.grid(row=1,column=1,ipadx=3,ipady=3,padx=3,pady=3,sticky=W)


#查询按钮
btnSearch_shodan = ttk.Button(master=shodan_left, style=INFO, text='点击查询',width=10,command=shodanSearch)
btnSearch_shodan.grid(row=2,column=0,ipadx=3,ipady=3,padx=3,pady=3,sticky=W)

#查询结果
res_lab_shodan = ttk.Label(
                    master=shodan_left,
                    text=' 查询条数：'
                    )
res_lab_shodan.grid(row=3,column=0,sticky=N)

shodan_ST = ScrolledText(master=shodan_left, width=90, height=50,font=('楷体',10),bootstyle='danger-round')
shodan_ST.grid(row=3,column=1,sticky=W)

#shodan语法参考
shodan_right = ttk.LabelFrame(
                            master=right_frame,
                            text='shodan语法参考',
                            style=SUCCESS,
                            padding=5
                            )
# shodan_right.pack(side=LEFT, anchor=NW,padx=3,pady=3)

shodan_CMD = ScrolledText(master=shodan_right, width=90, height=55,font=('黑体',12),bootstyle='success-round')
shodan_CMD.pack(side=RIGHT,fill=BOTH)
shodan_CMD.insert(END,r"""------限定国家和城市
限定国家country:"CN"
限定城市city:"ShangHai"

------限定主机名或域名
hostname:.org
hostname:"google"
hostname:baidu.com

------限定组织或机构
org:"alibaba"

------限定系统OS版本
os:"Windows Server 2008 R2"
os:"Windows 7 or 8"
os:"Linux 2.6.x"

------限定端口
port:22
port:80

------指定网段
net:"59.56.19.0/24"

------指定使用的软件或产品
product:"Apache httpd"
product:"nginx"
product:"Microsoft IIS httpd"
product:"mysql"

------指定CVE漏洞编号
vuln:"CVE-2014-0723"

------指定网页内容
http.html:"hello world"

------指定网页标题
http.title:"hello"

------指定返回响应码
http.status:200

------指定返回中的server类型
http.server:Apache/2.4.7
http.server:PHP

------指定地理位置
geo:"31.25,121.44"

------指定ISP供应商
isp:"China Telecom"
""")


#ZoomEye布局







windows.mainloop()
