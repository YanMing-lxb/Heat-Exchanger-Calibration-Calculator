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
Date         : 2024-10-02 15:46:58 +0800
LastEditTime : 2024-10-02 15:46:59 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /Heat-Exchanger-Calibration-Calculator/src/Re_model.py
Description  : 
 -----------------------------------------------------------------------
'''


class Re_class(object):
    """雷诺数计算类"""

    def __init__(self):
        """ 无 """
    
    def common_cal(self,q_h, A, mu, rho):
        """雷诺数通用计算方法

        :q_h: 质量流量 kg/s
        :A: 截面积 m^2
        :mu: 动力粘度 Pa·s
        :rho_l: 液态密度 kg/m^3
        returns: 雷诺数

        """
        return rho*(q_h/rho/A)*A/mu 

    def Re_eq_cal(self, q_h, A, D_h, mu_l, rho_l, rho_g, X_m):
        """Akers 等人提出的等效雷诺数
        [1] CROSSER O K. Condensing heat transfer within horizontal tubes[J/OL]. 1955[2024-10-02]. https://hdl.handle.net/1911/18229.
        
        :q_h: 质量流量 kg/s
        :A: 截面积 m^2
        :D_h: 水力直径 m
        :mu_l: 液态动力粘度 Pa·s
        :rho_l: 液态密度 kg/m^3
        :rho_g: 气态密度 kg/m^3
        :X_m: 干度 kg
        :returns: Re_eq 等效雷诺数

        @article{Akers1955CONDENSINGHT,
            title={CONDENSING HEAT TRANSFER WITHIN HORIZONTAL TUBES},
            author={William W. Akers and Harry A. Deans and Orrin K. Crosser},
            journal={Chemical Engineering Progress},
            year={1955},
            url={https://api.semanticscholar.org/CorpusID:93664455}
        }
        """

        return q_h / A * D_h/mu_l * ((1 - X_m) + X_m * (rho_l / rho_g)**0.5)
    
    def Re_L_cal(self, q_h, A, D_h, mu_l, X_m):
        """ 凝结水的雷诺数，表现为部分凝结的特征
        [1] HU S, MA X, ZHOU W. Condensation heat transfer of ethanol-water vapor in a plate heat exchanger[J/OL]. Applied Thermal Engineering, 2017, 113: 1047-1055. DOI:10.1016/j.applthermaleng.2016.11.013.

        :q_h: 质量流量 kg/s
        :A: 截面积 m^2
        :D_h: 水力直径 m
        :mu_l: 液态动力粘度 Pa·s
        :X_m: 干度 kg
        :returns: Re_eq 等效雷诺数
        """
        return q_h/A(1-X_m)*D_h/mu_l
