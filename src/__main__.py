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
 Date         : 2024-09-28 19:47:51 +0800
 LastEditTime : 2024-09-30 15:20:37 +0800
 Github       : https://github.com/YanMing-lxb/
 FilePath     : /Heat-Exchanger-Calibration-Calculator/src/__main__.py
 Description  : 
 -----------------------------------------------------------------------
'''

import math

from rich import print

from logger_config import setup_logger

logger = setup_logger(True)


# 计算平壁换热系数
def k_plane(h_h, h_c, sigma, k_s):
    """计算平壁的换热系数

    :h_h: 热侧表面传热系数
    :h_c: 冷侧表面传热系数
    :sigma: 固体厚度
    :k_s: 固体导热率 (W/(m·k))
    :returns: k 返回平壁换热系数

    """
    k = 1 / (1 / h_h + sigma / lambda_s + 1 / h_c)
    return k


# 计算表面换热系数
def h_cal(Nu, k_f, D_h):
    """计算液体表面换热系数

    :Nu: 努塞尔数 
    :k_f: 液体导热率 (W/(m·k))
    :D_h: 水力直径
    :returns: h_cal 表面换热系数
    """
    h_cal = Nu * k_f / D_h


class D_h_class(object):
    """计算水力直径类"""

    def __init__(self):
        """无 """

    def common_cal(self, A, U):
        """水力直径通用计算方法

        :A: 截面积 m^2
        :U: 周长 m
        :returns: D_h 水力直径 m

        """
        return 4 * A / U

    def Corrugate_cal(self, L_w, h):
        """波纹板换水力直径计算
        来源于 《热交换原理与设计》史美中 135 页
        :L_w: 板有效宽度 m
        :h: 波纹深度 m
        :returns: D_h 水力直径 m

        """
        D_h = 4 * L_w * h / (2 * (h + L_w))
        return D_h


class Re_class(object):
    """雷诺数计算类"""

    def __init__(self):
        """ 无 """

    def eq_cal(self, q_h, A, D_h, mu, rho_l, rho_g, X_m):
        """Akers 等人提出的等效雷诺数
        
        :q_h: 质量流量 kg/s
        :A: 截面积 m^2
        :D_h: 水力直径 m
        :mu: 动力粘度 Pa·s
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

        return q_h / A * mu / (1 - X_m) + X_m * rho_l * rho_g**0.5


def lmtd_calt_hin(t_hout, t_lin, t_lout):
    DeltaT_in = t_hin - t_lin
    DeltaT_out = t_hout - t_lout
    DeltaT_max = max(DeltaT_in, DeltaT_out)
    DeltaT_min = min(DeltaT_in, DeltaT_out)
    DeltaT_m = math.log((DeltaT_max - DeltaT_min) / (DeltaT_max / DeltaT_min))
    logger.info(f"LMTD 为：{DeltaT_m}")
    return DeltaT_m


# 判断获取最大和最小热容量: qc_max, qc_min
def judge(q_hm, c_h, q_cm, c_c):
    qc_h = q_hm * c_h
    qc_c = q_cm * c_c
    qc_max = max(qc_h, qc_c)
    qc_min = min(qc_h, qc_c)
    return qc_max, qc_min


# 计算 NTU
def ntu(k, A, qc_min):
    res_ntu = k * A / qc_min
    logger.info(f"NTU 为：{res_ntu}")
    return res_ntu


# 计算 R_c
def rc(qc_max, qc_min):
    return qc_min / qc_max


# 计算 epsilon
def epsilon(FD_num, phase_change, ntu, rc):
    '''
    名称 编号 英文名称
    顺流：1 parallel flow
    逆流：2 counter flow
    '''
    if FD_num == 1:
        if phase_change:
            rc = 0
        res_epsilon = (1 - math.exp(-ntu * (1 + rc))) / (1 + rc)
    if FD_num == 2:
        if phase_change:
            rc = 0
        res_epsilon = (1 - math.exp(-ntu *
                                    (1 - rc))) / (1 - rc * math.exp(-ntu *
                                                                    (1 - rc)))
    logger.info(f"epsilon 为：{res_epsilon}")
    return res_epsilon


epsilon(1, False, 2, 2)
epsilon(2, False, 2, 2)
