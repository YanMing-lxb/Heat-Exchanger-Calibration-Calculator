'''
 =======================================================================
 ·······································································
 ·······································································
 ····Y88b···d88P················888b·····d888·d8b·······················
 ·····Y88b·d88P·················8888b···d8888·Y8P·······················
 ······Y88o88P··················88888b·d88888···························
 ·······Y888P··8888b···88888b···888Y88888P888·888·88888b·····d88b·······
 ········888······"88b·888·"88b·888·Y888P·888·888·888·"88b·d88P"88b·····
 ········888···d888888·888··888·888··Y8P··888·888·888··888·888··888·····
 ········888··888··888·888··888·888···"···888·888·888··888·Y88b·888·····
 ········888··"Y888888·888··888·888·······888·888·888··888··"Y88888·····
 ·······························································888·····
 ··························································Y8b·d88P·····
 ···························································"Y88P"······
 ·······································································
 =======================================================================

 -----------------------------------------------------------------------
Author       : 焱铭
Date         : 2024-10-02 15:46:12 +0800
LastEditTime : 2024-10-16 22:11:02 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /Heat-Exchanger-Calibration-Calculator/src/Nu_module.py
Description  : 
 -----------------------------------------------------------------------
'''
import logging
import math
import sys


class Nu_SP_class(object):

    """单相努塞尔数计算类"""

    def __init__(self):
        """无 """
        self.logger = logging.getLogger(__name__)  # 调用_setup_logger方法设置日志记录器

    def YL_cal(self, Re, Pr, mu_f, mu_w):
        """Yan和Li拟合的努塞尔计算公式

        :Re: 雷诺数
        :Pr: 普朗特数
        :mu_f: 不确定 
        :mu_w: 不确定
        :returns: TODO

        不能用     
        [1] YAN Y Y, LIN T F. Evaporation Heat Transfer and Pressure Drop of Refrigerant R-134a in a Plate Heat Exchanger[J/OL]. Journal of Heat Transfer, 1999, 121(1): 118-127. DOI:10.1115/1.2825924.
        """

        return 0.2121*Re**0.78*Pr**(1/3)*(mu_f/mu_w)**0.14

    def Okada_cal(self, Re, Pr, ang_corrugated):
        """Okada拟合的努塞尔计算公式
        适用范围: Re=700-25000

        :Re: 雷诺数
        :Pr: 普朗特数
        :ang_corrugated: 波纹角 ° 可选值有: 30、45、60、75
        :returns: TODO
        """

        if ang_corrugated == 30:
            Nu = 0.157 * Re**0.66*Pr**0.4
        elif ang_corrugated == 45:
            Nu = 0.249 * Re**0.64*Pr**0.4
        elif ang_corrugated == 60:
            Nu = 0.327 * Re**0.65*Pr**0.4
        elif ang_corrugated == 75:
            Nu = 0.478 * Re**0.62*Pr**0.4
        else:
            self.logger.error("Okada 努塞尔拟合公式仅适用于波纹角为30°、45°、60°、75°")
            sys.exit()
        return Nu

    def Gulenoglu_C_1_cal(self, Re, Pr, mu, mu_w, phi):
        """Gulenoglu-C 努塞尔计算公式
        适用范围: Re=300-5000,波纹角30°,工质为水

        :Re: 雷诺数   300~5000
        :Pr: 普朗特数
        :phi: 放大系数
        :mu: 平均温度下的动力粘度
        :mu_w: 壁面温度下的黏度

        来源：[25] Gulenoglu C, Akturk F, Aradag S, et al.
        Experimental comparison of performances of three different plates for gasketed plate heat exchangers[J]. 
        International Journal of Thermal Sciences, 2014, 75: 249-256.
        """
        if 300 < Re < 5000:
            if phi == 1.17:
                Nu = 0.32867*Re**0.68*Pr**(0.1/3)*(mu/mu_w)**0.14
            elif phi == 1.288:
                Nu = 0.17422*Re**0.7*Pr**(0.1/3)*(mu/mu_w)**0.14
            else:
                self.logger.error("Gulenoglu-C 努塞尔计算公式仅适用于phi=1.17或1.288")
                sys.exit()
        else:
            self.logger.error("Gulenoglu-C 努塞尔计算公式仅适用于Re=300-5000,波纹角30°,工质为水")
            sys.exit()
        return Nu

    def Gulenoglu_C_2_cal(self, Re, Pr, mu, mu_w, phi):
        """Gulenoglu-C 努塞尔计算公式
        适用范围: Re=300-5000,波纹角30°,工质为水

        :Re: 雷诺数   300~5000
        :Pr: 普朗特数
        :phi: 放大系数
        :mu: 平均温度下的动力粘度值
        :mu_w: 壁面温度下的动力黏度值

        来源：[25] Gulenoglu C, Akturk F, Aradag S, et al.
        Experimental comparison of performances of three different plates for gasketed plate heat exchangers[J]. 
        International Journal of Thermal Sciences, 2014, 75: 249-256.
        """
        if 300 < Re < 5000:
            if phi == 1.17:
                Nu = 0.3277*Re**0.675*Pr**(0.1/3)*(mu/mu_w)**0.14
            elif phi == 1.288:
                Nu = 0.17422*Re**0.7*Pr**(0.1/3)*(mu/mu_w)**0.14
        else:
            self.logger.error("Gulenoglu-C 努塞尔计算公式仅适用于Re=300-5000,波纹角30°,工质为水")
            sys.exit()

        return Nu

    def LinJunYU_cal(self, Re, Pr, mu_m, mu_w):
        """Lin-Jun-YU 努塞尔计算公式
        适用范围: Re=1000-3000,工质为水/r245fa,v型角度 β SPHE 50° BPHE 60°,
        表面放大系数φ SPHE 1.16 BPHE 1.14,波纹纵横比ʘ SPHE 0.27 BPHE 0.25

        :Re: 雷诺数   1000-3000
        :Pr: 普朗特数
        :mu_m: 平均温度下的动力粘度
        :mu_w: 壁面温度下的动力黏度

        来源：[4] Junyub Lim, Kang Sub Song, Dongwoo Kim, DongChan Lee, Yongchan Kim,
        Condensation heat transfer characteristics of R245fa in a shell and plate heat exchanger for high-temperature heat pumps,
        International Journal of Heat and Mass Transfer, 127, 2018, 730-739.
        """
        if 1000 < Re < 3000:
            return 0.0508*Re**0.7304*Pr**0.33(mu_m/mu_w)**0.14
        else:
            self.logger.error(
                "Lin-Jun-YU 努塞尔计算公式仅适用于Re=1000-3000,工质为水/r245fa,v型角度 β SPHE 50° BPHE 60°,表面放大系数φ SPHE 1.16 BPHE 1.14,波纹纵横比ʘ SPHE 0.27 BPHE 0.25")
            sys.exit()

    def Alklaibi_cal(self, Re, Pr, phi):
        """Alklaibi 努塞尔计算公式
            适用范围 Re 300~1000, Pr 5.5~6.5, φ 0~0.3%, β 30°， 工作介质制冷剂（MWCNT/水纳米流体）/水的板式换热器

            :Re: 雷诺数   300~1000
            :Pr: 普朗特数
            :phi: 颗粒体积浓度

            来源：[8] A.M. Alklaibi, L. Syam Sundar, Kotturu V.V. Chandra Mouli,
            Experimental investigation on the performance of hybrid Fe3O4 coated MWCNT/Water nanofluid as a coolant of a Plate heat exchanger,
            International Journal of Thermal Sciences, 171,2022.
            """
        if 300 < Re < 1000:
            return 0.1735*Re**0.4655*Pr**0.4*(1+phi)**0.692
        else:
            self.logger.error(
                "Alklaibi 努塞尔计算公式仅适用于Re 300~1000,Pr 5.5~6.5,φ 0~0.3%,β 30°， 工作介质制冷剂（MWCNT/水纳米流体）/水的板式换热器")
            sys.exit()

    # def Tapacob_cal(self,Re,Pr,h,L_s,T_in,T_out,d_e,d_0):
    #     """Tapacob 努塞尔计算公式
    #     适用范围：适于任何流道断面的传热通式,对大多数波纹板片都可得出满意的结果

    #     :Re: 雷诺数
    #     :Pr: 普朗特数
    #     :y,x,m,Z中间量
    #     :h: 波纹高度
    #     :L_s: 波纹间距
    #     :T_in: 进口温度
    #     :T_out: 出口温度
    #     :d_e: 当量直径
    #     :d_0: 1mm

    #     来源：未检索到原文
    #     """
    #     y=(1.2+(3+3.15*Z)*d_e/d_0)/(7+(4-4*Z)*d_e/d_0)
    #     x=0.1+0.0189*(T_out-T_in)
    #     m=0.025+Z
    #     n=(0.26-0.065*Z)*(T_out-T_in )**0.186
    #     Z=h/L_s
    #     e=math.e
    #     return 1.5*Re**n*Pr**0.4*y*e**(-x)*e**m

    def He_Qing_Qiong_cold(self, Re, Pr, mu_f, mu_w):
        """He-Qing-Qiong 努塞尔计算公式
        适用范围：波纹夹角45°，横波波距30mm，纵波波距16mm，纵波波高1.5mm，工质为水、油
        适用于冷侧

        :Re: 雷诺数
        :Pr: 普朗特数
        :mu_f: 平均温度下的动力粘度
        :mu_w: 壁面温度下的动力黏度

        来源：[12] 何庆琼.复合波纹板式换热器换热与阻力特性研究[D].山东大学,2007.
        """
        if Re < 500 and Re > 50:
            Nu = 0.3942*Re**0.5473*Pr**0.4*(mu_f/mu_w)**0.14
        elif Re < 20000 and Re > 2000:
            Nu = 0.1579*Re**0.6463*Pr**0.4
        else:
            self.logger.error("He-Qing-Qiong 努塞尔计算公式仅适用于Re 50~500, 2000~20000")
            sys.exit()
        return Nu

    def HeQQ_hot_cal(self, Re, Pr, mu_f, mu_w):
        """He-Qing-Qiong 努塞尔计算公式
        适用范围：波纹夹角45°，横波波距30mm，纵波波距16mm，纵波波高1.5mm，工质为水、油
        适用于热侧

        :Re: 雷诺数
        :Pr: 普朗特数
        :mu_f: 平均温度下的动力粘度
        :mu_w: 壁面温度下的动力黏度

        来源：[12] 何庆琼.复合波纹板式换热器换热与阻力特性研究[D].山东大学,2007.
        """
        if Re < 500 and Re > 50:
            Nu = 0.3942*Re**0.5473*Pr**0.3*(mu_f/mu_w)**0.14
        elif Re < 20000 and Re > 2000:
            Nu = 0.1579*Re**0.6463*Pr**0.3
        else:
            self.logger.error(
                "He-Qing-Qiong 努塞尔计算公式仅适用于Re 50~500, 2000~20000 波纹夹角45°，横波波距30mm，纵波波距16mm，纵波波高1.5mm，工质为水、油")
            sys.exit()
        return Nu

    def Saranmanduh_Borjigin_cal(self, Re, Pr, Lambda, ff):
        """
        Saranmanduh Borjigin nu 计算公式
        适用范围：Re 3000~100000,气-气板式换热器

        :Re: 雷诺数
        :Pr: 普朗特数
        :Lambda: 导热系数
        :ff: 摩擦因数

        来源：[14] Saranmanduh Borjigin, Suritu Bai, Keqilao Meng, Hexi Baoyin,
        Heat recovery from kitchen by using range hood with gas-gas plate heat exchanger,
        Case Studies in Thermal Engineering, 49,2023.
        """
        if 3000 < Re < 100000:
            return (0.5*ff*(Re-1000)*Pr)/(1.07+12.7*(0.5*ff)**0.5*(Pr**(2/3)-1))
        else:
            self.logger.error("Saranmanduh Borjigin nu 计算公式仅适用于Re 3000~100000")
            sys.exit()

    def Pantzali_MN_cal(self, Re, Pr):
        """
        Pantzali, M.N. 等人努塞尔数计算公式
        适用范围：纳米流体作为冷却剂在板式换热器，

        :Re: 雷诺数
        :Pr: 普朗特数

        来源：[22] Pantzali M N, Mouza A A, Paras S V. 
        Investigating the efficacy of nanofluids as coolants in plate heat exchangers (PHE)[J]. 
        Chemical Engineering Science, 2009, 64(14): 3290-3300.
        """
        return 0.247*Re**(0.66)*Pr**0.4

    def MM_cal(self, Re, Pr, ang_corrugated, projection_coefficient, mu_f, mu_w):
        """Muley和Manglik拟合的努塞尔计算公式
        适用范围:Re>1000

        :Re: 雷诺数
        :Pr:普朗克数
        :ang_corrugated: 波纹角 ° 范围:30°~60°
        :projection_coefficient: 面积投影系数
        :mu_f: 不确定
        :mu_w: 不确定
        :returns: TODO
        """
        if 30< ang_corrugated < 60:
            return (0.2668-0.006967*ang_corrugated+7.244e-5*ang_corrugated**2)*(20.78-50.94*projection_coefficient+41.16*projection_coefficient**2-10.15*projection_coefficient**3)*Re**{0.728+0.0543*math.sin[(math.pi*ang_corrugated)/45+3.7]}*Pr**(1/3)*(mu_f/mu_w)*0.14
        else:
            self.logger.error("Muley和Manglik拟合的努塞尔计算公式仅适用于波纹角30°~60°")
            sys.exit()

    def Nu_SK_cal(self, C1, C2, Re, Pr, Refrigerant, State):
        """Song和Kim拟合的努塞尔计算公式
        适用条件：1.制冷剂：R-32和R-410A；2.单相流冷凝板式换热器

        :C1:系数1
        :C2:系数2
        :Re:单相流体的Re
        :Pr:液态普朗特数
        :returns:TODO
        """
        if Refrigerant == 'R-32':
            if State == 'Vapor':
                if 2935 < Re < 6311 and 1.414 < Pr < 1.446:
                    C1 = 0.07109
                    C2 = 0.7775
                else:
                    self.logger.error("输入参数不在适用范围内")
                    sys.exit()
            elif State == 'Liquid':
                if 364.9 < Re < 911.9 and 1.841 < Pr < 1.861:
                    C1 = 0.01801
                    C2 = 0.9495
                else:
                    self.logger.error("输入参数不在适用范围内")
                    sys.exit()
        elif Refrigerant == 'R-410A':
            if State == 'Vapor':
                if 3189 < Re < 6136 and 1.678 < Pr < 1.696:
                    C1 = 0.01068
                    C2 = 0.09907
                else:
                    self.logger.error("输入参数不在适用范围内")
                    sys.exit()
            elif State == 'Liquid':
                if 346.1 < Re < 975.4 and 2.374 < Pr < 2.384:
                    C1 = 0.0151
                    C2 = 0.9477
                else:
                    self.logger.error("输入参数不在适用范围内")
                    sys.exit()
        else:
            self.logger.error("制冷剂输入错误")
            sys.exit()

        return C1*Re**C2*Pr**(1/3)

    def Nu_Chisholm_cal(self, Re, Pr, ang_corrugated, projection_coefficient):
        """Chisholm拟合的努塞尔计算公式
        适用范围: 1.1000<Re<40000 2. 波纹角30°~80°

        :Re: 雷诺数
        :Pr: 普朗特数   
        :ang_corrugated: 波纹角 ° 范围:30°~80°
        :projection_coefficient: 面积投影系数   
        :returns: TODO
        """
        if 30< ang_corrugated < 80 and 1000 < Re < 40000:
            return 0.72*Re**0.59*projection_coefficient**0.41*(ang_corrugated/30)**0.66*Pr**0.4
        else:
            self.logger.error("Chisholm nu 计算公式仅适用于Re 1000~40000 波纹角30°~80°")
            sys.exit()

    def Nu_R_D_V_cal(self, Re, Pr):
        """ Ray D R,Das D K,Vajjha R S拟合的努塞尔计算公式
        适用范围: 1. Al2O3/EG:Water(~5 vol.%) 2. 4<Pr<27 3. 150<Re<1500
        :Re: 雷诺数
        :Pr: 普朗特数
        :returns: TODO
        """
        if 150 < Re < 1500 and 4 < Pr < 27:
            return 0.3053*Re**0.75*Pr**0.3
        else:
            self.logger.error("Ray D R,Das D K,Vajjha R S nu 计算公式仅适用于Re 150~1500 4<Pr<27")
            sys.exit()

class NU_TP_class(object):

    """两相努塞尔计算类"""

    def __init__(self):
        """TODO: to be defined. """

    def Nu_Wang_cal(self, Cp_f, Delta_T, gamma, Re_L, Pr_l, rho_l, rho_g):
        """ Wang 将拟合的怒塞尔计算公式
        适用条件: 1. 2500 < Re < 5000 2. 冷凝
        [1] HU S, MA X, ZHOU W. Condensation heat transfer of ethanol-water vapor in a plate heat exchanger[J/OL]. Applied Thermal Engineering, 2017, 113: 1047-1055. DOI:10.1016/j.applthermaleng.2016.11.013.

        :Delta_T: 换热温差 K
        :Cp_f: 液态比热 jk/kg·K
        :gamma: 汽化潜热 j/kg
        :Re_L: 对应 Re_class.Re_L_cal 方法
        :Pr: 液态普朗特数
        :rho_l: 液态密度 kg/m^3
        :rho_g: 气态密度 kg/m^3
        """
        if 2500 < Re_L < 5000:
            H = Cp_f*Delta_T/gamma  # H 表示冷凝膜对冷凝传热影响的无量纲参数
            return 0.00115*(Re_L/H)**0.983*Pr_l**0.33*(rho_l/rho_g)**0.248
        else:
            self.logger.error("Wang nu 计算公式仅适用于Re 2500~5000")
            sys.exit()

    def Nu_SK_cal(self, C1, C2, C3, Re_eq, Pr_l, Co, Refrigerant):
        """Song和Kim拟合的努塞尔计算公式
        适用条件：1.制冷剂：R-32和R-410A；2.两相流冷凝板式换热器

        :C1:系数1
        :C2:系数2
        :C3:系数3
        :Re——eq:TP流体的等效Re
        :Pr_l:
        :Co:制冷量
        :Refrigerant:制冷剂
        :returns:TODO
        """
        if Refrigerant == 'R-32':

            if 732.1 < Re_eq < 3797 and 1.855 < Pr_l < 1.988 and 0.042 < Co < 0.889:
                C1 = 0.4514
                C2 = 0.7442
                C3 = 0.5059
            else:
                self.logger.error("输入参数不在适用范围内")
                sys.exit()

        elif Refrigerant == 'R-410A':
            if 732.1 < Re_eq < 3797 and 1.855 < Pr_l < 1.988 and 0.042 < Co < 0.889:
                C1 = 0.9237
                C2 = 0.6316
                C3 = 0.5927
            else:
                self.logger.error("输入参数不在适用范围内")
                sys.exit()

        else:
            self.logger.error("制冷剂输入错误")
            sys.exit()
        return C1*Re_eq**C2*Co**C3 * Pr_l**(1/3)

    def Nu_Behrozifard_cal(self, D, L, Re, Pr):
        """Behrozifard拟合的努塞尔计算公式
        适用范围: 1.Re<2300 

        :D: 水力直径 m
        :L: 通道长度 m
        :Re: 雷诺数
        :Pr: 普朗特数
        :returns: TODO
        """
        if Re < 2300:
            return 3.66+[0.0668*(D/L)*Re*Pr]/{1+0.04[(D/L)*Pr]**(2/3)}
        else:
            self.logger.error("Behrozifard nu 计算公式仅适用于Re < 2300")
            sys.exit()

    def Nu_Wang_zq_cal(self, Re_eq, Re_lo, Pr, Fr, Bd):
        """王志奇拟合的努塞尔计算公式
        适用范围: 1.100<Re<1000 

        :Re_eq: 等效Re
        :Re_lo: 低压端Re
        :Pr: 普朗特数
        :Fr: 
        :Bd: 表面张力对传热的影响系数
        :returns: TODO
        """
        if 100 < Re_eq < 1000:
            return 2.2891*Re_eq**1.44*Re_lo**(-0.84)*Pr**(1/3)*Fr**(-0.478)*Bd**(0.757)
        else:
            self.logger.error("王志奇 nu 计算公式仅适用于Re 100~1000")
            sys.exit()
