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
Date         : 2024-10-02 14:49:13 +0800
LastEditTime : 2024-10-02 22:17:07 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /Heat-Exchanger-Calibration-Calculator/src/__main__.py
Description  : 
 -----------------------------------------------------------------------
'''

import math
from rich import print

from logger_config import setup_logger
from Nu_module import *
from Re_module import *
from config_module import ConfigParser

logger = setup_logger(True)
CP = ConfigParser() # 实例化 ConfigParser 类

def Pr_cal(cp, k, mu):
    """计算普朗特数

    :cp: 比热 jk/kg·K
    :k: 导热系数 W/(m·k)
    :mu: 动力粘度

    :returns: Pr 普朗特数

    """
    return cp*mu/k

# 计算平壁换热系数
def k_plane_cal(h_h, h_c, sigma, k_s):
    """计算平壁的换热系数

    :h_h: 热侧表面传热系数
    :h_c: 冷侧表面传热系数
    :sigma: 固体厚度
    :k_s: 固体导热率 (W/(m·k))
    :returns: k 返回平壁换热系数

    """
    k = 1 / (1 / h_h + sigma / k_s + 1 / h_c)
    return k


# 计算表面换热系数
def h_cal(Nu, k_f, D_h):
    """计算液体表面换热系数

    :Nu: 努塞尔数 
    :k_f: 液体导热率 (W/(m·k))
    :D_h: 水力直径
    :returns: h_cal 表面换热系数
    """
    return Nu * k_f / D_h


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

    def Corrugate_cal(self, L_w, d_corrugate):
        """波纹板换水力直径计算
        来源于 《热交换原理与设计》史美中 135 页
        :L_w: 板有效宽度 m
        :d_corrugate: 波纹深度 m
        :returns: D_h 水力直径 m

        """

        return 4 * L_w * d_corrugate / (2 * (d_corrugate + L_w))


def lmtd_cal(t_hin, t_hout, t_cin, t_cout):
    DeltaT_in = t_hin - t_cin
    DeltaT_out = t_hout - t_cout
    DeltaT_max = max(DeltaT_in, DeltaT_out)
    DeltaT_min = min(DeltaT_in, DeltaT_out)
    DeltaT_m = math.log((DeltaT_max - DeltaT_min) / (DeltaT_max / DeltaT_min))
    logger.info(f"LMTD 为：{DeltaT_m}")
    return DeltaT_m


# 判断获取最大和最小热容量: qc_max, qc_min
def judge(q_hm, cp_h, q_cm, cp_c):
    qc_h = q_hm * cp_h
    qc_c = q_cm * cp_c
    qc_max = max(qc_h, qc_c)
    qc_min = min(qc_h, qc_c)
    return qc_max, qc_min


# 计算 NTU
def ntu_cal(k, A, qc_min):
    res_ntu = k * A / qc_min
    logger.info(f"NTU 为：{res_ntu}")
    return res_ntu


# 计算 R_c
def R_c(qc_max, qc_min):
    return qc_min / qc_max


# 计算 epsilon
def epsilon_cal(FD_num, phase_change, ntu, R_c):
    '''
    名称 编号 英文名称
    顺流：1 parallel flow
    逆流：2 counter flow
    '''
    if FD_num == 1:
        if phase_change:
            R_c = 0
        res_epsilon = (1 - math.exp(-ntu * (1 + R_c))) / (1 + R_c)
    if FD_num == 2:
        if phase_change:
            R_c = 0
        res_epsilon = (1 - math.exp(-ntu *
                                    (1 - R_c))) / (1 - R_c * math.exp(-ntu *(1 - R_c)))
    logger.info(f"epsilon 为：{res_epsilon}")
    return res_epsilon


cd = CP.init_config_file() # 初始化配置文件，获取配置文件中的参数 config_dict : cd
t_hin = cd["BC"]["Temp_heat_inlet"]
t_hout = cd["BC"]["Temp_heat_outlet"]
t_cin = cd["BC"]["Temp_cool_inlet"]
t_cout = cd["BC"]["Temp_cool_outlet"]

q_hm = cd["BC"]["Mass_flow_heat"]
q_cm = cd["BC"]["Mass_flow_cool"]

FD = cd["SP"]["Flow_direction"]
D_h = cd["SP"]["Hydraulic_diameter"]
A = cd["SP"]["Cross_sectional_area"]
L_w = cd["SP"]["Effective_width"]
d_corrugate = cd["SP"]["Ripple_depth"]
sigma = cd["SP"]["Plate_thickness"]

k_s = cd["SPP"]["Thermal_conductivity"]

rho_h = cd["FHSPPP"]["Density"]
cp_h = cd["FHSPPP"]["Specific_heat_capacity"]
k_fh = cd["FHSPPP"]["Thermal_conductivity"]
mu_h = cd["FHSPPP"]["Dynamic_viscosity"]
rho_c = cd["FCSPPP"]["Density"]
cp_c = cd["FCSPPP"]["Specific_heat_capacity"]
k_fc = cd["FCSPPP"]["Thermal_conductivity"]
mu_c = cd["FCSPPP"]["Dynamic_viscosity"]

def run():
    qc_max, qc_min = judge(q_hm, cp_h, q_cm, cp_c)
    rc = R_c(qc_max, qc_min)
    Dh_class = D_h_class()
    D_h = Dh_class.Corrugate_cal(L_w, d_corrugate)

    Re = Re_class()
    Re_h = Re.common_cal(q_hm, A, mu_h, rho_h)
    Re_c = Re.common_cal(q_cm, A, mu_c, rho_c)

    Pr_h = Pr_cal(cp_h, k_fh, mu_h)
    Pr_c = Pr_cal(cp_c, k_fc, mu_c)
    Nu_SP = Nu_SP_class()
    Nu_h = Nu_SP.Okada(Re_h, Pr_h, 60)
    Nu_c = Nu_SP.Okada(Re_c, Pr_c, 60)

    h_h = h_cal(Nu_h, k_fh, D_h)
    h_c = h_cal(Nu_c, k_fc, D_h)
    
    k = k_plane_cal(h_h, h_c, sigma, k_s)
    ntu = ntu_cal(k, A, qc_min)
    epsilon = epsilon_cal(FD, False, ntu, rc)

    tmtd = lmtd_cal(t_hin, t_hout, t_cin, t_cout)

    Phi_res = epsilon*qc_min*(t_hin - t_cin)
    t_hout_res= t_hin - Phi_res/(q_hm*cp_h)
    t_cout_res = t_cin + Phi_res/(q_cm*cp_c)


    return Phi_res, t_hout_res, t_cout_res

Phi, t_hout, t_cout = run()

print(f"换热量：{round(Phi,4)} W")
print(f"热侧出口温度：{round(t_hout,4)} °C")
print(f"冷侧出口温度：{round(t_cout,4)} °C")