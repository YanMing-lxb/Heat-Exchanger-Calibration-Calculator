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
Date         : 2024-10-02 16:01:55 +0800
LastEditTime : 2024-10-04 18:19:50 +0800
Github       : https://github.com/YanMing-lxb/
FilePath     : /Heat-Exchanger-Calibration-Calculator/src/config_module.py
Description  : 
 -----------------------------------------------------------------------
'''

import toml
import logging
from pathlib import Path


# 默认配置文件
default_config = """ # 参数设置
# 结构参数 Structural parameters
[SP]
Flow_direction = 2 # 顺流：1 parallel flow  逆流：2 counter flow
Hydraulic_diameter = 0.5 # 水力直径 m
Effective_width = 0.2 # 板有效宽度 m
Ripple_depth = 0.01 # 波纹深度 m
Plate_thickness = 0.001 # 板厚度 m
Cross_sectional_area = 1 # 截面积 m^2

# 边界条件 Boundary_condition
[BC]
Temp_heat_inlet = 80 # 热侧入口温度 摄氏度
# Temp_heat_outlet = 89 # 热侧出口温度 摄氏度
Temp_cool_inlet = 25 # 冷侧入口温度 摄氏度
# Temp_cool_outlet = 26 # 冷侧出口温度 摄氏度
Mass_flow_heat = 0.15 # 热侧流量 kg/s
Mass_flow_cool = 0.1 # 冷侧流量 kg/s

# 固体物性参数 solid physical parameter
[SPP] 
Density = 135 # 密度 kg/m^3
Specific_heat_capacity = 1350 # 比热容
Thermal_conductivity = 21 # 导热率

# 冷侧单相液体物性参数 fluid heat single phase physical parameter
[FHSPPP]
Density = 135 # 密度 kg/m^3
Specific_heat_capacity = 1350 # 比热容
Thermal_conductivity = 21 # 导热率
Dynamic_viscosity = 0.01 # 动力粘度

# 单相热侧液体物性参数 fluid cool single phase physical parameter
[FCSPPP]
Density = 135 # 密度 kg/m^3
Specific_heat_capacity = 1350 # 比热容
Thermal_conductivity = 21 # 导热率
Dynamic_viscosity = 0.01 # 动力粘度
"""

class ConfigParser:
    """
    配置解析器类, 用于处理系统配置和本地配置文件的加载和生成。
    """
    def __init__(self):
        """
        初始化配置解析器, 设置日志记录器, 获取边界参数路径。
        """
        self.logger = logging.getLogger(__name__)  # 加载日志记录器
        self.local_config_path = Path.cwd() / '参数设置文件.toml'  # 获取参数文件路径
        self.logger.info("边界参数初始化完成")

    def _load_toml(self, path):
        """
        加载指定路径的 TOML 配置文件。
        参数:
            path (Path): 配置文件路径。
        返回:
            dict: 配置字典。
        """
        if not path.exists():
            self.logger.warning("边界参数文件不存在: " + str(path))
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = toml.load(f)
            self.logger.info("边界参数文件加载成功: " + str(path))
            return config
        except Exception as e:
            self.logger.error("边界参数文件加载失败: " + f"{path} --> {e}")
            return None

    def init_default_config(self, path, config):
        """
        生成默认边界参数文件。
        参数:
            path (Path): 边界参数文件路径。
            config (str): 边界参数内容。
        """
        if not path.exists():
            try:
                self.logger.info("创建默认边界参数文件: " + str(path))
                path.parent.mkdir(parents=True, exist_ok=True)  # 创建父目录
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(config)
            except Exception as e:
                self.logger.error("创建默认边界参数文件失败: " + f"{path} --> {e}")
    
    def init_config_file(self):
        """
        初始化边界参数文件。
        加载边界参数文件
        返回:
            dict: 最终的配置字典。
        """
        self.init_default_config(self.local_config_path, default_config)
        
        local_config = self._load_toml(self.local_config_path)  # 加载本地配置文件

        return local_config