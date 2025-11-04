from wtpy import WtBtEngine,EngineType
from wtpy.apps import WtBtAnalyst
import sys
import os 
import time
from intraday import bt1

if __name__ == "__main__":
    
    factor_name = "factor" # 因子名字，必须与csv文件中的因子名字完全一致
    name = "factor测试" # 策略名字，需与因子名字不同
    factor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim_signals") # 因子存放路径文件夹
    N = 20 # 持仓数
    ascending = False # 因子方向，False为取因子值大的股票（正向），True相反（负向）
    turnover_rate = 0.1 # 换手率
    startdate = 202401020930 # 回测开始时间
    enddate = 202406281500 # 回测结束时间
    universe_type = 4 # 1-中证1000；2-中证500；3-沪深300；4-全A

    # 以下语句不需要修改！
    # 以下语句不需要修改！
    t1 = time.time()
    engine = WtBtEngine(EngineType.ET_CTA,logCfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Mywtpy_storage', 'logcfgbt.yaml'))
    engine.init(folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Mywtpy_storage', 'common'), 
                cfgfile=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Mywtpy_storage', 'configbt.yaml'))
    engine.configBacktest(startdate,enddate)
    engine.configBTStorage(mode="csv")
    engine.commitBTConfig()

    straInfo = bt1(name = name, factor_path = factor_path, factor_name = factor_name,N = N, ascending = ascending,
                   type = universe_type, turnover_rate = turnover_rate)
    engine.set_cta_strategy(straInfo,slippage=0,isRatioSlp=False) # 滑点单位是万分之一

    engine.run_backtest()

    #绩效分析
    analyst = WtBtAnalyst()
    analyst.add_strategy(name, folder="./outputs_bt/", init_capital=10000000,) # 不要修改init_capital
    analyst.run()
    engine.release_backtest()
    t2 = time.time()
    print("总用时：%.2fs"%(t2-t1))
