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
LastEditTime : 2024-10-08 16:37:09 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /Heat-Exchanger-Calibration-Calculator/src/Nu_module.py
Description  : 
 -----------------------------------------------------------------------
'''
import logging

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
        return Nu
    
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
        H=Cp_f*Delta_T/gamma # H 表示冷凝膜对冷凝传热影响的无量纲参数
        return 0.00115*(Re_L/H)**0.983*Pr_l**0.33*(rho_l/rho_g)**0.248
