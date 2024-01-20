"""
一个用来计算简单计算题的软件
"""

#导入模块
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import math

#电学计算对象
class Oumu(object):
    def __init__(self,R=None,U=None,I=None,P=None,T=None,W=None):
        #传入六个参数
        self.R=R
        self.U=U
        self.I=I
        self.P=P
        self.W=W
        self.T=T

    #这个方法返回一个字典
    def output(self,name='R1'):

        if self.R is not None and self.U is not None:

            self.I = self.out_I(self.U,self.R)
            self.P = self.out_P(self.U,self.I)

            self.W=self.out_W()
            self.T=self.out_T()

        elif self.U is not None and self.I is not None:
            self.R = self.out_R(self.U, self.I)
            self.P = self.out_P(self.U, self.I)

            self.W=self.out_W()
            self.T=self.out_T()

        elif self.R is not None and self.I is not None:
            self.U = self.out_U(self.I, self.R)
            self.P = self.out_P(self.U, self.I)

            self.W=self.out_W()
            self.T=self.out_T()

        elif self.R is not None and self.P is not None:
            self.I = (self.P/self.R)**0.5
            self.U = self.out_U(self.I,self.R)

            self.W=self.out_W()
            self.T=self.out_T()

        elif self.U is not None and self.P is not None:
            self.R = self.U**2/self.P
            self.I = self.out_I(self.U,self.R)

            self.W=self.out_W()
            self.T=self.out_T()

        elif self.I is not None and self.P is not None:
            self.U = self.P/self.I
            self.R = self.out_R(self.U,self.I)

            self.W=self.out_W()
            self.T=self.out_T()

        elif self.I is not None and self.W is not None and self.T is not None:
            self.U = self.W/(self.I*self.T)
            self.R = self.out_R(self.U,self.I)

            self.P=self.U*self.I

        return {f'R':f'{self.R}',
                'U':f'{self.U}',
                'I':f'{self.I}',
                'P':f'{self.P}',
                'T':f'{self.T}',
                'W':f'{self.W}'
                }

    #定义根据公式求值的函数
    def out_I(self,u,r):
        return u/r

    def out_P(self,u,i):
        return u*i


    def out_R(self,u,i):
        return u/i

    def out_U(self,i,r):
        return i*r

    def out_T(self):

        if self.W is not None and self.P is not None:
            return self.W/self.P

        elif self.W is not None and self.U is not None and self.I is not None:
            return self.W/(self.U*self.I)

        elif self.W is not None and self.I is not None and self.R is not None:
            return self.W/(self.I**2*self.R)

        elif self.W is not None and self.U is not None and self.R is not None:
            return self.W/(self.U**2/self.R)

    def out_W(self):
        if self.P is not None and self.T is not None:
            return self.P * self.T

#函数解二元一次方程（传入abc）
def jie_eryuan(a,b,c):
    dt = b**2-4*a*c
    if dt < 0:
        return False
    elif dt >= 0:
        return (-b + dt**0.5) / 2*a , (-b - dt**0.5) / 2*a

#相对原子质量（正价在前）
dict_fenzi = {'K':39,'Ca':40,'Mn':55,'Ag':108,'Cu':64,'Ba':137,'Hg':201,'Fe':56,'Zn':65,
              'Na':23,'Mg':24,'Al':27,'Si':28,'P':31,'S':32,'C':12,'H':1,'NH4':18,
              'N':14,'O':16,'F':19,'Cl':35.5,
              'OH':17,'NO3':62,'SO4':96,'CO3':60}

#判断是否已知某两个值
is_ur = is_ui=is_rp=is_up=is_ip=is_iwt = False
#几个主屏幕
main_box = toga.Box()
main_box2 = toga.Box()
main_box3 = toga.Box()
main_box4 = toga.Box()
main_box5 = toga.Box()

#输出的解析式
out_jxs = toga.Label('y=?')
out_jxs.style.font_size=20

#输出的交点
jiaodian = toga.Label(' ')
jiaodian.style.font_size = 20

#输出的总电阻值
Rzong1 = toga.Label(' ')
Rzong2 = toga.Label(' ')
Rzong1.style.font_size = Rzong2.style.font_size = 16

#输出的三角函数值
print_sanjiaohanshu = toga.Label(' ')
print_sanjiaohanshu.style.font_size = 16

#输出的一元二次方程解
print_yyecfc = toga.Label(' ')
print_yyecfc.style.font_size = 16

#电学计算的输入框
u_ = toga.TextInput()
r_ = toga.TextInput()
i_ = toga.TextInput()
p_ = toga.TextInput()
w_ = toga.TextInput()
t_ = toga.TextInput()

#相对分子质量的几个部件（添加原子按钮，输出的化学式，元素符号的字典）
button_add_fz = toga.Button('添加 H ×1')
button_add_fz.style.font_size = 16
huaxueshi = toga.Label('化学式：\n')
huaxueshi.style.font_size = 20
huaxueshi.style.background_color = 'blue'
fuhao = list(dict_fenzi.keys())
dict_fuhao = {i: 0 for i in fuhao}

#关于软件
about_box1 = toga.Box()


class _112(toga.App):
    """
※※※
1. 根据著名公式1+1=2，开发者开发了这个软件.
这个软件的代码量打破了之前265行的纪录，
甚至超过了700行，达到了746行，总字符量超过22000个，
开发者认为，他之前做的那些软件都是垃圾。目前这个也是。
2. 使用过程中可能出现的问题：
(0) 首先强调一个重点：负号是-不是－！
你在手机数字键盘左侧找见的2个横杠都不是负号！
左下角的英文键盘里的那个短杠才是负号！
⑴ 崩溃。如果你在手机里安装这个软件，
在使用时突然崩溃、闪退，请不要骂开发者。
开发者的代码肯定没啥大毛病，
只不过懒得写处理异常的代码，
所以软件闪退一般是你的问题。
⑵ 计算结果有问题。
这个软件可以用来解决一些非常简单但是你实在懒得动手的数学问题。
开发者为了体现自己精益求精的伟大工匠精神，
很多部分都用自己的作业测试了好几遍，
但结果还是有0.01%的可能出错。
如果你因为软件的一个小bug被你的数学老师真实，
跟开发者没有任何关系哦。
⑶ 显示有问题。这个问题曾经使开发者内心崩溃。
因为开发者自始至终都用pycharm在计算机里敲代码。
所以根本不清楚这个软件在手机里是怎么显示的。
你在手机里可能会发现软件的字有的太大，有的太小，
有的部分甚至超出了屏幕，有的滚动条是失效的。
开发者能想到的问题就是这些。
遇到上述的这些问题，请息怒，并且联系开发者。
    """

    def startup(self):
        #主页
        mainbox = toga.Box()
        main_s = toga.ScrollContainer(content=mainbox)
        #检查更新网页
        webview = toga.WebView(url='https://zhangboyaung.github.io/112')
        webview.style.flex = 1
        web_box = toga.Box()
        web_box.add(webview)

        #打开主页
        def mainbox_open(widget):
            self.main_window.content = main_s

        #关于软件
        sc1 = toga.ScrollContainer(content=about_box1)
        l_about1 = toga.Label(self.__doc__)
        l_about1.style.font_size = 14
        about_box1.style.direction = 'column'
        about_box1.add(l_about1)

        #求函数值
        def zheng(widget):
            global out_jxs
            t = zb1_.value
            t = t.split(' ')
            k = eval(t[1])/eval(t[0])
            out_jxs.text = f'y={k}x'

        def fan(widget):
            global out_jxs
            t = zb1_fbl_.value
            t = t.split(' ')
            k = eval(t[0])*eval(t[1])
            out_jxs.text = f'y={k}/x'

        def yici(widget):
            global out_jxs
            t1 = zb_yc1.value.split(' ')
            t2 = zb_yc2.value.split(' ')
            k = (eval(t2[1]) - eval(t1[1])) / (eval(t2[0]) - eval(t1[0]))
            b = eval(t1[1]) - eval(t1[0])*k
            out_jxs.text = f'y={k}x+({b})'

        #求交点
        def qiujiaodian(widget):
            global jiaodian
            a,b,c,k,m = eval(a_vl.value),eval(b_vl.value),eval(c_vl.value),eval(k_vl.value),eval(m_vl.value)
            zx_pwx = f'直线{k}x+{m}与抛物线{a}x²+{b}x+{c}'
            x = jie_eryuan(a,(b-k),(c-m))
            if not x:
                rt_jd = f'{zx_pwx}无交点'
            elif x[0]==x[1]:
                rt_jd = f'{zx_pwx}有一个交点：\n（{x[0]},{k*x[0]+m}）.'
            elif x[0]!=x[1]:
                rt_jd = f'{zx_pwx}有两个交点：\n （{x[0]},{k*x[0]+m}）, （{x[1]},{k*x[1]+m}）.'
            jiaodian.text = rt_jd

        #正比例函数的BOX
        zb1 = toga.Label('输入1个坐标（不要输括号，逗号用空格代替）：')
        zb1_ = toga.TextInput()
        jxs = toga.Button('计算（正）！',on_press=zheng)
        zb1box = toga.Box()
        zb1box.style.direction = 'column'
        zb1box.add(zb1,zb1_,jxs)

        #反比例函数的BOX
        jxs_fbl = toga.Button('计算（反）！',on_press=fan)
        zb1_fbl = toga.Label('输入1个坐标\n（不要输括号，逗号用空格代替）：\n')
        zb1_fbl_ = toga.TextInput()
        zb_fbl = toga.Box()
        zb_fbl.style.direction = 'column'
        zb_fbl.add(zb1_fbl,zb1_fbl_,jxs_fbl)

        #一次函数的BOX
        js_yc = toga.Button('计算（一）！',on_press=yici)
        zb1_yc = toga.Label('输入第1个坐标\n（不要输括号，逗号用空格代替）：\n')
        zb2_yc = toga.Label('输入第2个坐标：')
        zb_yc1 = toga.TextInput()
        zb_yc2 = toga.TextInput()
        ychs = toga.Box()
        ychs.style.direction = 'column'
        ychs.add(zb1_yc,zb_yc1,zb2_yc,zb_yc2,js_yc)

        #二次函数的box
        l1 = toga.Label(
"""此功能仍在开发中......
开发者说：那么容易让你做出点东西来吗？""")
        l1.style.font_size = 20
        l1.style.color = 'blue'
        l2 = toga.Label("""
本来这部分的内容应该是
让你输入三个坐标，
然后通过程序将二次函数的解析式求出来。
然而问题是，
在你输入(x1,y1)(x2,y2)(x3,Y3)这三个坐标后，
程序要生成一个三元一次方程组，
ax1²+bx1+c=y1,
ax2²+bx2+c=y2,
ax3²+bx3+c=y3.
然后解出来a，b，c.
但是这个解方程部分的代码
咋写？？？？？？？？？？？？？？？
经过我的调查，
有一个专门处理数据的第三方库Numpy，
里边有个线性代数模块linalg，传入未知数的系数
就可以解三元一次方程。
等我做完这部分的代码后，我发现我错了。
经过我的研究，所有使用beeware打包的程序，
应用于移动平台时，
都不能支持包含二进制模块的依赖项
（也就是说手机软件不能用）。
要解三元一次方程还得靠初一老师教给你的原始方法。
还是上面的三个方程，
怎么用含有x1,x2,x3,y1,y2,y3的式子把a,b,c分别表示出来？
这个计算过程，我必须在纸上解决，过于复杂而且太容易出错。
反正我是解不出来，所以果断放弃。
如果说你是一位精通数学或是计算机的大佬，
并且具有伟大的无私奉献精神，知道怎么做，
请你联系我。""")
        l2.style.font_size = 15
        echs = toga.Box()
        echs.style.direction = 'column'
        echs.add(l1,l2)
        gdt = toga.ScrollContainer(content=echs)

        #求交点
        jd_ck = toga.Box()
        jd_lb = toga.Label('求直线和抛物线交点\n直线：y=kx+m\n抛物线y=ax²+bx+c')
        k_lb = toga.Label('k=')
        k_vl = toga.TextInput()
        m_lb = toga.Label('m=')
        m_vl = toga.TextInput()
        a_lb = toga.Label('a=')
        a_vl = toga.TextInput()
        b_lb = toga.Label('b=')
        b_vl = toga.TextInput()
        c_lb = toga.Label('c=')
        c_vl = toga.TextInput()
        out_jd = toga.Button('求交点！',on_press=qiujiaodian)
        out_jd.style.color = 'blue'
        jd_ck.add(jd_lb,k_lb,k_vl,m_lb,m_vl,a_lb,a_vl,b_lb,b_vl,c_lb,c_vl,out_jd,jiaodian)
        jd_ck.style.direction = 'column'

        #打开求解析式的各个小窗口
        def zbl():
            self.main_window.content = zb1box
            zb1box.add(out_jxs,backbutton)

        def fbl():
            self.main_window.content = zb_fbl
            zb_fbl.add(out_jxs,backbutton)

        def yc():
            self.main_window.content = ychs
            ychs.add(out_jxs,backbutton)

        def ec():
            self.main_window.content = gdt
            echs.add(backbutton)

        def jd():
            self.main_window.content = jd_ck
            jd_ck.add(backbutton)

        #打开各个小窗口
        def main_box2_open(widget):
            self.main_window.content = main_box2

        # 求函数解析式界面的返回按钮
        backbutton = toga.Button('返回',on_press=main_box2_open)

        def main_box3_open(widget):
            self.main_window.content = main_box3
            main_box3.add(main_page)

        def main_box4_open(widget):
            self.main_window.content = main_box4
            main_box4.add(main_page)

        def main_box5_open(widget):
            self.main_window.content = main_box5
            main_box5.add(main_page,toga.Label('注意：化学式中元素符号的排序可能是不正确的！\n这个问题开发者还没有解决。'))

        def main_box6_open(widget):
            self.main_window.content = web_box
            web_box.add(main_page)

        def main_box_open(widget):
            self.main_window.content = main_box_s
            main_box.add(main_page)

        def rzong_box_open(widget):
            self.main_window.content = rzong_box
            rzong_box.add(main_page)

        def about_box1_open(widget):
            self.main_window.content = sc1
            about_box1.add(main_page)


        #主页显示的内容
        button_rzong_box_open = toga.Button('计算并联/串联电路总电阻',on_press=rzong_box_open)
        button_rzong_box_open.style.font_size = 16
        button_main_box_open = toga.Button('电学计算', on_press=main_box_open)
        button_main_box_open.style.font_size = 16
        button_main_box2_open = toga.Button('求函数解析式',on_press=main_box2_open)
        button_main_box2_open.style.font_size = 16
        button_main_box3_open = toga.Button('三角函数',on_press=main_box3_open)
        button_main_box3_open.style.font_size = 16
        button_main_box4_open = toga.Button('一元二次方程',on_press=main_box4_open)
        button_main_box4_open.style.font_size = 16
        button_main_box5_open = toga.Button('相对分子质量',on_press=main_box5_open)
        button_main_box5_open.style.font_size = 16
        button_main_box6_open = toga.Button('检查更新',on_press=main_box6_open)
        button_main_box6_open.style.font_size = 16
        button_one = toga.Button('（使用前必读）关于这个软件_必读！__必读！！___必读！！！',on_press=about_box1_open)
        button_one.style.background_color = 'red'
        button_one.style.font_size = 16
        main_label = toga.Label("""
    软件名：1+1=2
    版本：v0.0.1
    发布日期：2024.1.20
    更新网站：https://zhangboyaung.github.io/112
    适用系统：Android;Windows(x64)
    授权类型：开源
    开源代码存储库：https://www.github.com/zhangboyaung/one
    占用空间：≤50MB
    开发者：张博洋
    邮箱：youhulu2021@outlook.com
        """)
        thanks = toga.Label('另外，需要特别感谢王楠同学的帮助。\n开发者在8天里单枪匹马手刃代码746行之后，'+
                            '\n程序的测试就是王楠同学帮忙的。\n毕竟开发者根本不清楚软件在不同环境下的运行情况，'+
                            '\n万一哪块出了问题，这些工作可就白做了。\n所以测试是个必需的环节……\n总之就是非常感谢啦！')
        main_label.style.font_size = 16
        thanks.style.font_size = 14
        thanks.style.color = 'blue'

        #添加按钮到主页
        mainbox.add(button_rzong_box_open,
                    button_main_box_open,
                    button_main_box2_open,
                    button_main_box3_open,
                    button_main_box4_open,
                    button_main_box5_open,
                    button_main_box6_open,
                    button_one,main_label,thanks)
        mainbox.style.direction = 'column'


        #求函数解析式
        xuanxiang_jxs = ['求正比例函数解析式','求反比例函数解析式','求一次函数解析式',
                                      '求二次函数解析式','求直线和抛物线的交点']

        def qiujiexishi(widget):
            if drop1.value == xuanxiang_jxs[0]:
                zbl()
            elif drop1.value == xuanxiang_jxs[1]:
                fbl()
            elif drop1.value == xuanxiang_jxs[2]:
                yc()
            elif drop1.value == xuanxiang_jxs[3]:
                ec()
            elif drop1.value == xuanxiang_jxs[4]:
                jd()


        drop1 = toga.Selection(items=xuanxiang_jxs)
        button_drop = toga.Button('确定',on_press=qiujiexishi)
        main_box2.add(drop1,button_drop)
        main_box2.add(toga.Button('返回主页',on_press=mainbox_open))
        main_box2.style.direction = 'column'

        #求总电阻
        def out_rchuan(widget):
            global Rzong1
            rlist = [eval(i) for i in r_chuan.value.split(' ')]
            a = 0
            for i in rlist: a+=i
            Rzong1.text = f'共有电阻{len(rlist)}个，总电阻={a}Ω.'

        def out_rbing(widget):
            global Rzong2
            rlist = [eval(i) for i in r_bing.value.split(' ')]
            a = 0
            for i in rlist: a+=1/i
            Rzong2.text = f'共有支路{len(rlist)}条，总电阻={1/a}Ω.'

        rzong_box = toga.Box()
        rzong_lb1 = toga.Label('求串联电路总电阻\n在下面的方框里依次输入各个电阻值，用空格隔开')
        rzong_lb1.style.font_size = 14
        r_chuan = toga.TextInput()
        suan_rchuan = toga.Button('计算',on_press=out_rchuan)

        rzong_lb2 = toga.Label('并联\n在下面的方框里依次输入各个电阻值，用空格隔开')
        rzong_lb2.style.font_size = 14
        r_bing = toga.TextInput()
        suan_rbing = toga.Button('计算',on_press=out_rbing)

        rzong_box.add(rzong_lb1,r_chuan,Rzong1,suan_rchuan,
                      rzong_lb2,r_bing,Rzong2,suan_rbing)
        rzong_box.style.direction = 'column'


        #三角函数部分
        def qiu_sjhs_zhi(widget):
            global print_sanjiaohanshu
            degree = math.radians(jd_kuang.value)
            if choice1.value == 'sin':
                out = math.sin(degree)
            elif choice1.value == 'cos':
                out = math.cos(degree)
            elif choice1.value == 'tan':
                out = math.tan(degree)
            print_sanjiaohanshu.text = f'{choice1.value}{jd_kuang.value}°={out}'

        def qiu_sjhs_jiao(widget):
            global print_sanjiaohanshu
            a = jd_kuang2a.value
            b = jd_kuang2b.value
            if choice2.value == 'sin':
                out = math.asin(a/b)
            elif choice2.value == 'cos':
                out = math.acos(a/b)
            elif choice2.value == 'tan':
                out = math.atan(a/b)
            print_sanjiaohanshu.text = f'{choice1.value}{math.degrees(out)}°={a}/{b}={a/b}'

        sjhs_lb1 = toga.Label('已知角度，求正弦、余弦、正切值。\n在下面的框子里直接输入角度（去掉单位）')
        choice1 = toga.Selection(items=['sin','cos','tan'])
        jd_kuang = toga.NumberInput()
        button_sjhs1 = toga.Button('计算',on_press=qiu_sjhs_zhi)

        sjhs_lb2 = toga.Label('已知正弦、余弦、正切值，求角度\nθ=a/b：在下面的框子里依次输入a,b的值')
        choice2 = toga.Selection(items=['sin','cos','tan'])
        jd_kuang2a = toga.NumberInput()
        jd_kuang2b = toga.NumberInput()
        button_sjhs2 = toga.Button('计算',on_press=qiu_sjhs_jiao)

        main_box3.add(sjhs_lb1,choice1,jd_kuang,button_sjhs1,
                      sjhs_lb2,choice2,jd_kuang2a,jd_kuang2b,button_sjhs2,print_sanjiaohanshu)
        main_box3.style.direction = 'column'


        #解一元二次方程部分
        def jfc(widget):
            global print_yyecfc
            abc = [eval(i) for i in fc_ipt.value.split(' ')]
            x = jie_eryuan(abc[0],abc[1],abc[2])
            if not x:
                out = '该方程无实数根！'
            else:
                out = f'x1 = {x[0]}, x2 = {x[1]}'
            print_yyecfc.text = out

        fc_lb = toga.Label('解一元二次方程ax²+bx+c=0\n在下面的方框里依次直接输入a,b,c值（用空格隔开）')
        fc_ipt = toga.TextInput()
        fc_button = toga.Button('开始解方程!',on_press=jfc)
        main_box4.style.direction = 'column'
        main_box4.add(fc_lb,fc_ipt,fc_button,print_yyecfc)


        #相对分子质量部分
        def add_fz(widget):
            global dict_fuhao,huaxueshi
            txt = '化学式：'
            m = 0
            n = choose_fz.value
            dict_fuhao[n] += 1
            for i in dict_fuhao.keys():
                if dict_fuhao[i]!=0:
                    m += dict_fenzi[i]*dict_fuhao[i]
                    txt+=f'{i if i!="OH" and len(i)<=2 else "("+i+")"}{dict_fuhao[i] if dict_fuhao[i]!=1 else ""}'
            huaxueshi.text = txt
            huaxueshi.text += '\n相对分子质量='+str(m)


        def select_fz(widget):
            global button_add_fz
            n = choose_fz.value
            button_add_fz.text = f'添加 {n} ×1'

        def zero(widget):
            global huaxueshi,dict_fuhao
            huaxueshi.text = '化学式：'
            for i in dict_fuhao.keys():
                dict_fuhao[i]=0

        button_add_fz.on_press = add_fz
        fzzl_lb = toga.Label('根据化学式计算相对分子质量.')
        it = list(dict_fenzi.keys())
        choose_fz = toga.Selection(items=it,on_select=select_fz)
        button_zero = toga.Button('归零',on_press=zero)
        main_box5.add(fzzl_lb,choose_fz,button_add_fz,huaxueshi,button_zero)

        main_box5.style.direction = 'column'

        #求电学值部分
        def ur(widget):
            global u_, r_, i_, p_, w_, t_, is_ur, is_ui, is_rp, is_up, is_ip, is_iwt
            u_.value = r_.value = ""
            t_.value = '1'
            p_.value = w_.value = i_.value = '*这里不要填！！！'

            is_ur = True
            is_ui = is_rp = is_up = is_ip = is_iwt = False

        def ui(widget):
            global u_, r_, i_, p_, w_, t_, is_ur, is_ui, is_rp, is_up, is_ip, is_iwt
            u_.value = i_.value = ""
            t_.value = '1'
            r_.value = w_.value = p_.value = '*这里不要填！！！'

            is_ui = True
            is_ur = is_rp = is_up = is_ip = is_iwt = False

        def rp(widget):
            global u_, r_, i_, p_, w_, t_, is_ur, is_ui, is_rp, is_up, is_ip, is_iwt
            r_.value = p_.value = ""
            t_.value = '1'
            u_.value = i_.value = w_.value = '*这里不要填！！！'

            is_rp = True
            is_ur = is_ui = is_up = is_ip = is_iwt = False

        def up(widget):
            global u_, r_, i_, p_, w_, t_, is_ur, is_ui, is_rp, is_up, is_ip, is_iwt
            u_.value = p_.value = ""
            t_.value = '1'
            r_.value = i_.value = w_.value = '*这里不要填！！！'

            is_up = True
            is_ur = is_ui = is_rp = is_ip = is_iwt = False

        def ip(widget):
            global u_, r_, i_, p_, w_, t_, is_ur, is_ui, is_rp, is_up, is_ip, is_iwt
            i_.value = p_.value = ""
            t_.value = '1'
            r_.value = u_.value = w_.value = '*这里不要填！！！'

            is_ip = True
            is_ur = is_ui = is_rp = is_up = is_iwt = False

        def iwt(widget):
            global u_, r_, i_, p_, w_, t_, is_ur, is_ui, is_rp, is_up, is_ip, is_iwt
            i_.value = w_.value = t_.value = ""
            r_.value = u_.value = p_.value = '*这里不要填！！！'

            is_iwt = True
            is_ur = is_ui = is_rp = is_ip = is_up = False

        def ur_out(widget):
            global u_, r_, i_, p_, w_, t_, is_ur, is_ui, is_rp, is_up, is_ip, is_iwt
            if is_ur:
                oumu = Oumu(U=float(u_.value), R=float(r_.value), T=float(t_.value))
            elif is_ui:
                oumu = Oumu(U=float(u_.value), I=float(i_.value), T=float(t_.value))
            elif is_rp:
                oumu = Oumu(R=float(r_.value), P=float(p_.value), T=float(t_.value))
            elif is_up:
                oumu = Oumu(U=float(u_.value), P=float(p_.value), T=float(t_.value))
            elif is_ip:
                oumu = Oumu(I=float(i_.value), P=float(p_.value), T=float(t_.value))
            elif is_iwt:
                oumu = Oumu(I=float(i_.value), W=float(w_.value), T=float(t_.value))

            i_.value = oumu.output()['I']
            u_.value = oumu.output()['U']
            r_.value = oumu.output()['R']
            p_.value = oumu.output()['P']
            w_.value = oumu.output()['W']
            t_.value = oumu.output()['T']

        button1 = toga.Button('已知 U,R', on_press=ur)
        main_box.add(button1)

        button2 = toga.Button('已知 U,I', on_press=ui)
        main_box.add(button2)

        button3 = toga.Button('已知 R,P', on_press=rp)
        main_box.add(button3)

        button4 = toga.Button('已知 U,P', on_press=up)
        main_box.add(button4)

        button5 = toga.Button('已知 I,P', on_press=ip)
        main_box.add(button5)

        button6 = toga.Button('已知 I,W,T', on_press=iwt)
        main_box.add(button6)

        u = toga.Label('电压（V）：')
        ubox = toga.Box()
        ubox.add(u, u_)
        main_box.add(ubox)

        r = toga.Label('电阻（Ω）：')
        rbox = toga.Box()
        rbox.add(r, r_)
        main_box.add(rbox)

        i = toga.Label('电流（A）：')
        ibox = toga.Box()
        ibox.add(i, i_)
        main_box.add(ibox)

        p = toga.Label('电功率（W）：')
        pbox = toga.Box()
        pbox.add(p, p_)
        main_box.add(pbox)

        w = toga.Label('电功（J）：')
        wbox = toga.Box()
        wbox.add(w, w_)
        main_box.add(wbox)

        t = toga.Label('时间（s）：')
        tbox = toga.Box()
        tbox.add(t, t_)
        main_box.add(tbox)
        ubox.style.direction = rbox.style.direction = ibox.style.direction = pbox.style.direction = wbox.style.direction = tbox.style.direction ='column'
        button_out = toga.Button('出结果（时间可以不填，默认为1s）', on_press=ur_out)
        main_box.add(button_out)
        main_box_s = toga.ScrollContainer(content=main_box)

        main_box.style.direction = "column"

        main_page = toga.Button('返回主页', on_press=mainbox_open)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_s
        self.main_window.size = (5000,5000)
        self.main_window.show()

def main():
    return _112()