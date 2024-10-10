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
        return 61000 * Re**(-1.25)

    def LJY_cal(self, Re_eq, Re_f):
        """林俊宇提出的高温热泵板换 R245fa 摩擦因子计算公式
        适用范围：R245fa 制冷剂，波纹板换，Re：1000～3000

        :Re_eq: TODO
        :Re_f: TODO
        :returns: TODO
        
        来源：[1] LIM J, SONG K S, KIM D, 等. Condensation heat transfer characteristics of R245fa in a shell and plate heat exchanger for high-temperature heat pumps[J/OL]. International Journal of Heat and Mass Transfer, 2018, 127: 730-739. DOI:10.1016/j.ijheatmasstransfer.2018.06.143.
        """
        return 24502 * Re_eq**(-0.8521) * Re_f**(-0.1856)
    def Gulenoglu_C_1_cal(self, Re,fai):
        """
        Gulenoglu 等人三种垫片板式换热器中使用的的摩擦因子计算公式1（φ=1.17与2相同）

        适用范围：波纹角30°，工质为水
        :Re: 雷诺数 300～5000
        :fai: 放大系数
        :returns: 摩擦因子

        来源：[25] Gulenoglu C, Akturk F, Aradag S, et al. 
            Experimental comparison of performances of three different plates for gasketed plate heat exchangers[J]. 
            International Journal of Thermal Sciences, 2014, 75: 249-256.
        """
        if fai==1.17:
            F=259.9*Re**(-0.9227)+1.246
        elif fai==1.288:
            F=0.00374*Re**(0.5981)+0.9132
        return F
    
    def Gulenoglu_C_2_cal(self, Re,fai):
        """
        Gulenoglu 等人三种垫片板式换热器中使用的摩擦因子计算公式2（φ=1.288与1相同）

        适用范围：波纹角30°，工质为水
        :Re: 雷诺数 300～5000
        :fai: 放大系数
        :returns: 摩擦因子

        来源：[25] Gulenoglu C, Akturk F, Aradag S, et al. 
            Experimental comparison of performances of three different plates for gasketed plate heat exchangers[J]. 
            International Journal of Thermal Sciences, 2014, 75: 249-256.
        """
        if fai==1.288:
            F=0.00374*Re**(0.5981)+0.9132
        elif fai==1.17:
            F=1371*Re**(-1.146)+1.139
        return F
    def Alklaibi_cal(self, Re, fai):
        """
        Alklaibi 等人提出的垫片板式换热器中使用的摩擦因子计算公式
        适用范围：Re：300~1000， φ 0~0.3%, β 30°， 工作介质制冷剂（MWCNT/水纳米流体）/水的板式换热器
         
        :Re: 雷诺数   300~1000
        :fai: 颗粒体积浓度

        来源：[8] A.M. Alklaibi, L. Syam Sundar, Kotturu V.V. Chandra Mouli,
        Experimental investigation on the performance of hybrid Fe3O4 coated MWCNT/Water nanofluid as a coolant of a Plate heat exchanger,
        International Journal of Thermal Sciences, 171,2022.
        """
        return (69.96/Re)/(1+fai)**(-0.24)