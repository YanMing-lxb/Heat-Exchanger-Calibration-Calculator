"""
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
 Data         : 2024-10-04 19:09:19 +0800
 LastEditTime : 2024-10-04 19:24:27 +0800
 Github       : https://github.com/YanMing-lxb/
 File Path    : src/F_module.py
 Description  :
 -----------------------------------------------------------------------
"""

import logging
import sys

class f_SP_class(object):
    """单相波纹板换摩擦因子计算类"""

    def __init__(self):
        """TODO: to be defined. """
        self.logger = logging.getLogger(__name__)  # 调用_setup_logger方法设置日志记录器

    def YY_Hsich_cal(self, Re):
        """Y.Y Hsich 等人提出的立式板式换热器中 R410A 的摩擦因子计算公式
        适用范围：立式板式换热器，R410A 制冷剂，Re 10～400
        
        :Re: 雷诺数 10～400
        :returns: 摩擦因子
        
        来源：[1] Saturated flow boiling heat transfer and pressure drop of refrigerant R-410A in a vertical plate heat exchanger[J/OL]. International Journal of Heat and Mass Transfer, 2002, 45(5): 1033-1044. DOI:10.1016/S0017-9310(01)00219-8.
        """
        if 10< Re < 400:
            return 61000 * Re**(-1.25)
        else:
            self.logger.error("YY_Hsich 仅适用于Re：10～400 立式板式换热器，R410A 制冷剂")
            sys.exit()

    def LJY_cal(self, Re_eq, Re_f):
        """林俊宇提出的高温热泵板换 R245fa 摩擦因子计算公式
        适用范围：R245fa 制冷剂，波纹板换，Re：1000～3000

        :Re_eq: TODO
        :Re_f: TODO
        :returns: TODO
        
        来源：[1] LIM J, SONG K S, KIM D, 等. Condensation heat transfer characteristics of R245fa in a shell and plate heat exchanger for high-temperature heat pumps[J/OL]. International Journal of Heat and Mass Transfer, 2018, 127: 730-739. DOI:10.1016/j.ijheatmasstransfer.2018.06.143.
        """
        return 24502 * Re_eq**(-0.8521) * Re_f**(-0.1856)
    
    def Gulenoglu_C_1_cal(self, Re,phi):
        """
        Gulenoglu 等人三种垫片板式换热器中使用的的摩擦因子计算公式1（φ=1.17与2相同）

        适用范围：波纹角30°，工质为水
        :Re: 雷诺数 300～5000
        :phi: 放大系数
        :returns: 摩擦因子

        来源：[25] Gulenoglu C, Akturk F, Aradag S, et al. 
            Experimental comparison of performances of three different plates for gasketed plate heat exchangers[J]. 
            International Journal of Thermal Sciences, 2014, 75: 249-256.
        """
        if 300 < Re < 5000:
            if phi==1.17:
                F=259.9*Re**(-0.9227)+1.246
            elif phi==1.288:
                F=0.00374*Re**(0.5981)+0.9132
        else:
            self.logger.error("Gulenoglu_C_1 仅适用于Re：300～5000 波纹角30°，工质为水")
            sys.exit()
        return F
    
    def Gulenoglu_C_2_cal(self, Re,phi):
        """
        Gulenoglu 等人三种垫片板式换热器中使用的摩擦因子计算公式2（φ=1.288与1相同）

        适用范围：波纹角30°，工质为水
        :Re: 雷诺数 300～5000
        :phi: 放大系数
        :returns: 摩擦因子

        来源：[25] Gulenoglu C, Akturk F, Aradag S, et al. 
            Experimental comparison of performances of three different plates for gasketed plate heat exchangers[J]. 
            International Journal of Thermal Sciences, 2014, 75: 249-256.
        """
        if 300 < Re < 5000:
            if phi==1.288:
                F=0.00374*Re**(0.5981)+0.9132
            elif phi==1.17:
                F=1371*Re**(-1.146)+1.139
        else:
            self.logger.error("Gulenoglu_C_2 仅适用于Re：300～5000 波纹角30°，工质为水")
            sys.exit()
        return F
    
    def Alklaibi_cal(self, Re, phi):
        """
        Alklaibi 等人提出的垫片板式换热器中使用的摩擦因子计算公式
        适用范围：Re：300~1000， φ 0~0.3%, β 30°， 工作介质制冷剂（MWCNT/水纳米流体）/水的板式换热器

        :Re: 雷诺数   300~1000
        :phi: 颗粒体积浓度

        来源：[8] A.M. Alklaibi, L. Syam Sundar, Kotturu V.V. Chandra Mouli,
        Experimental investigation on the performance of hybrid Fe3O4 coated MWCNT/Water nanofluid as a coolant of a Plate heat exchanger,
        International Journal of Thermal Sciences, 171,2022.
        """
        if 300<Re<1000:
            if 0<phi<0.3:
                return (69.96/Re)/(1+phi)**(-0.24)
            else:
                self.logger.error("Alklaibi 仅适用于φ：0~0.3%")
                sys.exit()
        else:
            self.logger.error("Alklaibi 仅适用于Re：300~1000")
            sys.exit()
        
    
    def He_Qing_Qiong_cal(self,Re):
        """
        He-Qing-Qiong 等人提出的摩擦因子计算公式
        适用范围：波纹夹角45°，横波波距30mm，纵波波距16mm，纵波波高1.5mm，工质为水、油

        :Re: 雷诺数

        来源：[12] 何庆琼.复合波纹板式换热器换热与阻力特性研究[D].山东大学,2007.
        """
        if Re<500 and Re>50:
            F=27.487*Re**(-0.5785)
        elif Re<20000 and Re>2000:
            F=4.9772*Re**(-0.31550)
        else:
            self.logger.error("He-Qing-Qiong 仅适用于Re：50～20000")
            sys.exit()
        return F

    def Amooie_FMM_cal(self,Re,phi):
        """
        Amooie, F.M.M. 等人摩擦因子计算公式
        适用范围：Re：0.8~2220，流动工质是水的水平波纹板式换热器

        :Re: 雷诺数
        :phi: 未知

        来源：[18] Amooie, F.M.M., Flow distribution in plate heat exchanger [D]. PhD Thesis, University of Bradford, UK, 1997.
        """
        if 0.8<Re<1000:
            return phi*(26*phi/Re+0.16)
        else:
            self.logger.error("Anooie_FMM 仅适用于Re：0.8~2220")
            sys.exit()
    
    def Pantzali_MN_cal(self,Re):
        """
        Pantzali, M.N. 等人摩擦因子计算公式
        适用范围：纳米流体作为冷却剂在板式换热器，

        :Re: 雷诺数

        来源：[22] Pantzali M N, Mouza A A, Paras S V. 
        Investigating the efficacy of nanofluids as coolants in plate heat exchangers (PHE)[J]. 
        Chemical Engineering Science, 2009, 64(14): 3290-3300.
        """
        return 14.5*Re**(-0.135)
    
    def MM_cal(self, Re, ang_corrugated, projection_coefficient):
        """Muley和Manglik提出的板式换热器摩擦因子经验公式
        适用范围： ang_corrugated:30°~80°, Re:1000~40000
        :Re:雷诺数 1000~40000
        :ang_corrugated: 波纹角° 范围：30°~80°
        :projection_coefficient：面积投影系数 范围：不确定
        :returns: 摩擦因子
        
        来源：[1] Muley, A., Manglik, P.M., Experimental study of turbulent flow transfer and pressure drop in a plate heat exchanger with Chevron plates [J]. Journal of Heat Transfer. 1999.121 (1): 110-117.
        """
        return (2.917-0.1277*ang_corrugated+2.016e-3*ang_corrugated**2)*(5.474-19.02*projection_coefficient+18.93*projection_coefficient**2-5.341*projection_coefficient**3)*Re**{-0.2+0.0577*math.sin[(math.pi*ang_corrugated)/45+2.1]}

    def Talik_cal(self, Re):
        """Talik 提出的板式换热器摩擦因子计算公式
        适用范围：1.流动工质是水 2.Re：1450～11460
        
        :Re: 雷诺数 1450～11460
        :returns: 摩擦因子
        来源：[1] Pages 1033-1044,Talik, A. C., Fletcher, L. S., Anand. N. K., Swanson, L. M., Heat transfer and pressure drop characteristics of a plate heat exchanger [A]. Proceedings of the ASME/JSME Thermal Engineering Conference, ASME, New York, 1995,4. 321-329.
        """
        return 0.3323* Re**(-0.042)
    
    def Pantzali_cal(self, Re):
        """Pantzali等人提出的板式换热器摩擦因子计算公式
        适用范围：1.纳米流体是冷却剂 2.CuO/water(6.0 vol.%) 3.水作为冷却剂 4.层流/紊流

        :Re: 雷诺数 
        :returns: 摩擦因子

        来源：[1] Pantzali M N, Mouza A A, Paras S V. Investigating the efficacy of nanofluids as coolants in plate heat exchangers (PHE)[J]. Chemical Engineering Science, 2009, 64(14): 3290-3300.
        """
        return 14.5* Re**(-0.135)
    
    def R_D_V_cal(self, Re):
        """ Ray D R,Das D K,Vajjha R S提出的板式换热器摩擦因子计算公式
        适用范围：1. Al2O3/EG:Water(~5 vol.%) 2. 4<Pr<27 3. 120<Re<1000

        :Re: 雷诺数 
        :returns: 摩擦因子

        来源：[1] Ray D R, Das D K, Vajjha R S. Experimental and numerical investigations of nanofluids performance in a compact minichannel plate heat exchanger[J]. International Journal of Heat and Mass Transfer, 2014, 71: 732-746.
        """
        return 13.64*Re**(-0.2719)
    

class f_TP_class(object):
    """双相波纹板换摩擦因子计算类"""
    def __init__(self):
        """TODO: to be defined. """
        self.logger = logging.getLogger(__name__)  # 调用_setup_logger方法设置日志记录器

    def Behrozifard_cal(self, Kp, Re, m):
        """Behrozifard 等人提出的纳米流体与水的板式换热器的摩擦因子计算公式
        适用范围：1.Re<2300 2.换热器采用M6 Alfa Laval 垫片型板式换热器 3.换热介质为纳米流体和水
        
        :Re: 雷诺数 <2300
        :returns: 摩擦因子
        
        来源：[1] A. Behrozifard, Hamid Reza Goshayeshi, Iman Zahmatkesh, Issa Chaer, Soheil Salahshour, D. Toghraie,Experimental optimization of the performance of a plate heat exchanger with Graphene oxide/water and Al₂O₃/water nanofluids,Case Studies in Thermal Engineering, 59,2024.
        """
        return Kp/(Re**m)
    
f_TP = f_TP_class()
a=f_TP.Behrozifard_cal(1.5, 1000,1)
print(a)