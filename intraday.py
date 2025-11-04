"""
version2策略可以控制换手率
"""
from wtpy import BaseCtaStrategy
from wtpy import CtaContext
from wtpy.apps import WtBtAnalyst
import numpy as np
import pandas as pd
import os
import time as ti
import sys            

class bt1(BaseCtaStrategy):
    
    def __init__(self, 
                 name:str, # 策略名
                 factor_name:str, # 因子名
                 N:int, # 持有股票数量
                 factor_path:str, # 因子路径
                 type:int, # 股票池
                 turnover_rate:float = 1.0, #换手率，默认设置为1.0
                 ascending:bool = True, # ascending = True 持有因子值较小的股票; ascending = False
                 del_ST:bool = True, # 不买入ST股票
                 ):
        
        BaseCtaStrategy.__init__(self, name)
        
        self.factor_name = factor_name
        self.factor_path = factor_path

        self.type = type
        
        # 确定回测池
        storage_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"storage") #"/data/guanxuyang/Mywtpy_storage/storage"
        # 中证1000
        if type == 1:
            zz1000 = pd.read_csv(os.path.join(storage_path,"index","zz1000.csv"),dtype={"consTickerSymbol":str})
            self.__codes__ = list("SSE.STK." + zz1000["consTickerSymbol"])
        # 中证500   
        elif type == 2:
            zz500 = pd.read_csv(os.path.join(storage_path,"index","zz500.csv"),dtype={"consTickerSymbol":str})
            self.__codes__ = list("SSE.STK." + zz500["consTickerSymbol"])
        # 中证2000
        elif type == 3:
            zz2000 = pd.read_csv(os.path.join(storage_path,"index","zz2000.csv"),dtype={"consTickerSymbol":str})
            self.__codes__ = list("SSE.STK." + zz2000["consTickerSymbol"])
        # 全标的回测    
        elif type == 4:
            self.__codes__ = sorted([x[:14] for x in os.listdir(os.path.join(storage_path,'csv'))])
        
        elif type == 5:
            tickers = ['000009', '000012', '000032', '000034', '000100', '000409', '000505', '000516', '000568', '000571', '000596', '000607', '000636', '000639', '000700', '000710', '000733', '000786', '000801', '000818', '000848', '000887', '000903', '000915', '000921', '000929', '000976', '000980', '000995', '001914', '002006', '002010', '002015', '002026', '002030', '002050', '002055', '002065', '002072', '002074', '002092', '002107', '002126', '002129', '002152', '002164', '002213', '002216', '002221', '002223', '002230', '002245', '002261', '002286', '002301', '002319', '002323', '002326', '002328', '002331', '002353', '002356', '002371', '002373', '002402', '002405', '002409', '002414', '002429', '002432', '002434', '002460', '002472', '002474', '002484', '002489', '002497', '002498', '002505', '002516', '002534', '002544', '002563', '002568', '002576', '002578', '002584', '002585', '002594', '002597', '002614', '002635', '002648', '002650', '002666', '002675', '002683', '002695', '002696', '002702', '002703', '002706', '002747', '002758', '002759', '002760', '002766', '002772', '002777', '002785', '002791', '002799', '002803', '002810', '002812', '002821', '002824', '002833', '002850', '002859', '002870', '002873', '002896', '002905', '002908', '002912', '002916', '002918', '002919', '002920', '002930', '002940', '002956', '002967', '002968', '002984', '003025', '300001', '300014', '300031', '300032', '300035', '300037', '300040', '300048', '300054', '300068', '300069', '300073', '300074', '300075', '300083', '300086', '300093', '300094', '300100', '300109', '300129', '300130', '300132', '300137', '300143', '300144', '300145', '300150', '300152', '300160', '300161', '300166', '300179', '300182', '300187', '300192', '300207', '300218', '300222', '300228', '300234', '300236', '300237', '300250', '300261', '300270', '300274', '300286', '300298', '300307', '300308', '300314', '300316', '300323', '300324', '300327', '300331', '300339', '300345', '300346', '300352', '300353', '300357', '300359', '300366', '300375', '300381', '300384', '300390', '300393', '300394', '300396', '300397', '300398', '300409', '300410', '300415', '300416', '300420', '300421', '300435', '300438', '300439', '300442', '300446', '300450', '300452', '300454', '300465', '300467', '300468', '300471', '300475', '300476', '300480', '300486', '300489', '300496', '300500', '300502', '300511', '300517', '300520', '300522', '300529', '300533', '300537', '300539', '300540', '300559', '300561', '300566', '300570', '300573', '300576', '300580', '300593', '300598', '300602', '300603', '300605', '300608', '300613', '300617', '300623', '300624', '300632', '300634', '300638', '300642', '300645', '300649', '300651', '300652', '300655', '300659', '300661', '300662', '300663', '300665', '300666', '300667', '300668', '300674', '300679', '300680', '300683', '300685', '300687', '300694', '300702', '300705', '300707', '300709', '300721', '300724', '300725', '300726', '300736', '300746', '300750', '300751', '300755', '300757', '300759', '300763', '300767', '300769', '300782', '300801', '300806', '300811', '300813', '300819', '300821', '300823', '300830', '300840', '300859', '300861', '300863', '300864', '300870', '300873', '300879', '300880', '300893', '300911', '300927', '300955', '300971', '300979', '301012', '301029', '301032', '301058', '600055', '600060', '600079', '600084', '600110', '600112', '600114', '600127', '600129', '600192', '600197', '600198', '600229', '600235', '600238', '600258', '600300', '600306', '600336', '600378', '600382', '600399', '600409', '600433', '600436', '600480', '600536', '600550', '600563', '600573', '600588', '600616', '600618', '600724', '600732', '600739', '600745', '600754', '600763', '600809', '600817', '600821', '600845', '600866', '600875', '600877', '600885', '600963', '600970', '600976', '601058', '601238', '601566', '601615', '601633', '601636', '601689', '601718', '601789', '601799', '601877', '601919', '601965', '601966', '603010', '603013', '603015', '603019', '603020', '603022', '603026', '603027', '603031', '603033', '603035', '603038', '603063', '603076', '603098', '603103', '603108', '603110', '603127', '603129', '603138', '603158', '603160', '603179', '603180', '603186', '603187', '603203', '603208', '603218', '603229', '603232', '603236', '603258', '603259', '603267', '603283', '603305', '603311', '603313', '603336', '603338', '603345', '603351', '603355', '603358', '603369', '603378', '603393', '603456', '603477', '603486', '603501', '603516', '603517', '603520', '603558', '603579', '603583', '603588', '603596', '603601', '603605', '603613', '603626', '603628', '603633', '603636', '603659', '603660', '603686', '603690', '603698', '603700', '603701', '603707', '603713', '603718', '603722', '603728', '603730', '603733', '603737', '603777', '603786', '603788', '603799', '603801', '603806', '603809', '603818', '603833', '603859', '603877', '603882', '603888', '603890', '603938', '603956', '603960', '603985', '603987', '603989', '605117', '605499', '688001', '688005', '688006', '688008', '688012', '688015', '688016', '688018', '688019', '688020', '688023', '688026', '688036', '688037', '688039', '688058', '688068', '688078', '688087', '688088', '688099', '688100', '688111', '688116', '688118', '688133', '688155', '688159', '688169', '688196', '688198', '688202', '688222', '688258', '688266', '688268', '688299', '688305', '688357', '688363', '688365', '688369', '688388', '688389', '688390', '688399', '688501', '688516', '688550', '688558', '688561', '688577', '688580', '688599', '688607', '688609', '688626']
            self.__codes__ = ["SSE.STK." + x for x in tickers]
        self.__codes__ = list(set(self.__codes__))
        
        """
        self.limits = dict()
        for code in self.__codes__:
            if code[-6:-4] in ["30","68"]:
                self.limits[code] = 19.5
            else:
                self.limits[code] = 9.5
        """
        
        self.__period__ = "m15"
        self.__bar_cnt__ = 1
        self.__capital__ = 10000000
        
        self.N = N
        self.ascending = ascending
        self.turnover_rate = turnover_rate  
        self.del_ST = del_ST
        self.flag = 0

        # 第一天各期买入数
        self.init_buy_num = dict(zip[tuple[str, int]](["945","1000","1015","1030","1045","1100","1115","1130",
                                      "1315","1330","1345","1400","1415","1430","1445"],
                                     [0]+[N // 12]*11+[N - 11 * (N // 12)]+[0]*2))
        # 每天各期换仓数
        N = int(N*turnover_rate)
        self.change_num = dict(zip(["945","1000","1015","1030","1045","1100","1115","1130",
                                      "1315","1330","1345","1400","1415","1430","1445","1500"],
                                     [0]+[N // 12]*11+[N - 11 * (N // 12)]+[0]*3))
        
        self.cur = [] # 当日买入名单
        self.pre = [] # 昨日买入仍持有名单
        self.sell = [] # 当日卖出名单
        self.execution = set() # 跌停未卖出名单，第二天优先卖出
        self.ratio = 0.99
        
        # # 加载DDB
        # self.s = ddb.session()
        # self.s.connect("localhost", 8881, "guanxuyang", "guanxuyang")
        # self.factor_tb = self.s.loadTable(tableName=self.table_name, 
        #                                   dbPath=self.db_path)
        
        # self.timelabel_dict = pd.read_csv("/data/guanxuyang/Mywtpy_storage/storage/TimeLabel_dict.csv").set_index("TradeLabel")["TimeLabel"]
        # self.index_path = os.path.join(storage_path,"index") #"/data/guanxuyang/Mywtpy_storage/storage/index"
        
        # 第一天会买入12次
        self.trade_nums = 0
        for value in self.init_buy_num.values():
            if value >0:
                self.trade_nums +=1
    
    # 确定是否涨停
    def if_limit(self,date,code):
        if code[-6:-4] in ["00","60"]:
            return 9.5
        elif code[-6:-4] == "68":
            return 19.5
        # 2020年8月24日之后创业板允许±20%涨跌幅
        elif code[-6:-4] == "30":
            if date < "20200824":
                return 9.5
            else:
                return 19.5
        
    
    # 读取因子值
    def read_factor_rank(self,date,time):
        time = time.zfill(4)
        tradelabel = date + time
        try:
            df = pd.read_csv(os.path.join(self.factor_path,"%s.csv"%date),
                        usecols = ["ticker","tradelabel",self.factor_name],
                        dtype = {"ticker":str,"tradelabel":str})
        except:
            print(os.path.join(self.factor_path,"%s.csv"%date))
            print(self.factor_name)
            raise Exception("factor_name错误！")
        
        df = df.query("tradelabel == @tradelabel")[["ticker",self.factor_name]]
        df["ticker"] = df["ticker"].apply(lambda x : x.zfill(6))
        df = df.dropna()
        df.sort_values(by=df.columns[1],inplace=True,ascending=self.ascending)
        df = df["ticker"].apply(lambda x: "SSE.STK.%s"%x)
        df = df[df.isin(self.__codes__)]
        return df

    # 加载回测程序
    def on_init(self, context:CtaContext):
        
        codes = self.__codes__
        
        if self.type == 1:
            context.stra_log_text("股票池：中证1000")
        elif self.type == 2:
            context.stra_log_text("股票池：中证500")    
        elif self.type == 3:
            context.stra_log_text("股票池：沪深300")
        elif self.type == 4:
            context.stra_log_text("股票池：全A")
        
        for i in range(0,len(codes)):
            if i == 0:
                context.stra_prepare_bars(codes[i], self.__period__, self.__bar_cnt__, isMain=True) # 设置第一支股票为主要品种
            else:
                context.stra_prepare_bars(codes[i], self.__period__, self.__bar_cnt__, isMain=False)
                
        context.stra_log_text("Strategy inited")

        #读取存储的数据
        self.xxx = context.user_load_data('xxx',1)
    
    # 回测主程序
    def on_calculate(self, context:CtaContext):
        
        date,time = str(context.stra_get_date()),str(context.stra_get_time())
        context.stra_log_text("%s %s"%(date,time))
        
        trdUnit = 10
        
        # 第一天分散买入股票
        if self.flag == 0:
            buy_ticker_nums = self.init_buy_num[time]
            if buy_ticker_nums > 0:
                rank = self.read_factor_rank(date,time)
                # 已持仓股票不买
                buy_list = rank[~rank.isin(self.cur)]
                buy_value = (self.__capital__ / self.trade_nums) * self.ratio / buy_ticker_nums
                
                cnt = 0
                for code in buy_list:

                    if self.del_ST:
                        st = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).lows[-1]
                        if st == 0:
                            context.stra_log_text("%s状态为ST无法买入"%code)
                            continue
                        
                    # 买入股价正常且非涨停的股票
                    ret = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).highs[-1]
                    if context.stra_get_price(code) > 0:
                        if ret < self.if_limit(date,code):
                            next_price = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).closes[-1]
                            buy_num = int(buy_value / next_price / trdUnit)
                            if buy_num > 0:
                                context.stra_enter_long(code, 
                                                        buy_num*trdUnit, 
                                                        'enterlong')
                                context.stra_log_text("买入%s"%code)
                                self.cur.append(code)
                                cnt += 1
                            else:
                                #context.stra_log_text("资金不足无法买入%s"%code)
                                pass
                        else:
                            context.stra_log_text("%s涨停无法买入"%code)
                    # 买入股票数量已达目标，停止交易
                    if cnt == buy_ticker_nums:
                        break

            if time == "1445":
                self.flag = 1

        # 换仓
        else:
            change_num = self.change_num[time]
            if change_num > 0:
                rank = self.read_factor_rank(date,time)
                # 因跌停无法卖出股票名单
                execution_list = rank[rank.isin(list(self.execution))]
                
                # 计算当前持仓总价值
                equity = sum(context.stra_get_position(code) * context.stra_get_price(code) for code in self.pre + self.cur)
                # 当前可用现金 = 初始资本 - 总平仓盈亏 - 总手续费 - 持仓总价值
                cur_cash = self.__capital__ + context.stra_get_fund_data(1) + context.stra_get_fund_data(2) - context.stra_get_fund_data(3) - equity
                context.stra_log_text(str(cur_cash))
                # 卖出sell_list中的股票，并预估下一期可用现金
                # 卖出和买入将在下一期完成，Wondertrader不支持按比例下单，只能通过这种方式预估可用现金计算可买入份额
                cnt = 0
                
                # 优先卖出之前因跌停无法卖出的股票
                for code in execution_list[::-1]:
                    ret = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).highs[-1]
                    position = context.stra_get_position(code)
                    if position > 0 and context.stra_get_price(code) > 0:
                        
                        if ret > -self.if_limit(date,code): 
                            context.stra_exit_long(code,
                                                position,
                                                'exitlong') 
                            context.stra_log_text("卖出%s"%code)
                            self.pre.remove(code)
                            self.sell.append(code)
                            self.execution.remove(code)
                            
                            next_price = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).closes[-1]
                            cur_cash += position * next_price
                            cnt += 1
                        else:
                            context.stra_log_text("%s跌停无法卖出"%code)
                    if cnt == change_num:
                        break
                
                # 可卖出股票名单
                sell_list = rank[rank.isin(self.pre) & ~rank.isin(list(self.execution))]
                # 正常卖出排名靠后的股票
                if cnt < change_num:
                    for code in sell_list[::-1]:
                        ret = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).highs[-1]
                        position = context.stra_get_position(code)
                        if position > 0 and context.stra_get_price(code) > 0:
                            if ret > -self.if_limit(date,code): 
                                context.stra_exit_long(code,
                                                    position,
                                                    'exitlong') 
                                context.stra_log_text("卖出%s"%code)
                                self.pre.remove(code)
                                self.sell.append(code)
                                
                                next_price = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).closes[-1]
                                cur_cash += position * next_price
                                cnt += 1
                            else:
                                context.stra_log_text("%s跌停无法卖出"%code)
                                self.execution.add(code)
                        if cnt == change_num:
                            break
                if cur_cash < 0:
                    context.stra_log_text("资金不足！")
                # 买入排名在前的股票，已持仓股票和已卖出股票不买入
                if cnt > 0:
                    buy_list = rank[~rank.isin(self.cur + self.pre + self.sell)]
                    buy_value = cur_cash * self.ratio / cnt
                    for code in buy_list:
                        
                        if self.del_ST:
                            st = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).lows[-1]
                            if st == 0:
                                context.stra_log_text("%s状态为ST无法买入"%code)
                                continue
                        
                        ret = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).highs[-1]
                        if context.stra_get_price(code) > 0:
                            if ret < self.if_limit(date,code):
                                next_price = context.stra_get_bars(code, self.__period__, self.__bar_cnt__).closes[-1]
                                buy_num = int(buy_value / next_price / trdUnit)
                                if buy_num > 0:
                                    context.stra_enter_long(code, 
                                                            buy_num*trdUnit, 
                                                            'enterlong')
                                    context.stra_log_text("买入%s"%code)
                                    self.cur.append(code)
                                    cnt -=1
                                else:
                                    #context.stra_log_text("资金不足无法买入%s"%code)
                                    pass
                            else:
                                context.stra_log_text("%s涨停无法买入"%code)
                        
                        if cnt == 0:
                            break
        
        # 每天14:45下完单进行持仓表格重整
        if time == "1445":
            self.pre = self.pre + self.cur
            self.cur = []
            self.sell = []
            context.stra_log_text("持仓表重整")
        