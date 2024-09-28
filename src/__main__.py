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
Date         : 2024-09-28 09:15:23 +0800
LastEditTime : 2024-09-28 10:24:28 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /Heat-Exchanger-Calibration-Calculator/src/__main__.py
Description  : 
 -----------------------------------------------------------------------
'''

import math
from rich import print

from logger_config import setup_logger

logger = setup_logger(True)

def lmtd_cal(t_hin, t_hout, t_lin, t_lout):
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
    res_ntu = k*A/qc_min
    logger.info(f"NTU 为：{res_ntu}")
    return res_ntu

# 计算 R_c
def rc(qc_max,qc_min):
    return qc_min/qc_max

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
        res_epsilon = (1 - math.exp(- ntu * (1 + rc)))/(1 + rc)
    if FD_num ==2:
        if phase_change:
            rc = 0
        res_epsilon = (1 - math.exp(- ntu * (1 - rc)))/(1 - rc * math.exp(-ntu * (1 - rc)))
    logger.info(f"epsilon 为：{res_epsilon}")
    return res_epsilon


epsilon(1,False, 2, 2)
epsilon(2,False, 2, 2)









































