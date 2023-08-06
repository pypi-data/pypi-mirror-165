import json
import requests
import pandas as pd
import numpy as np
from datetime import date,timedelta
from time import sleep


def int_to_str(x: int) -> str:
    return "%06d" % x


def date_to_str(today):

    str_date = str(today)[:4] + str(today)[5:7] + str(today)[-2:]
    return str_date


def str_to_date(str_date):

    str_date = str_date.replace('-', '')
    year = int(str_date[:4])
    month = int(str_date[4:6])
    day = int(str_date[-2:])
    return date(year,month,day)


def get_trading_day(start_date, end_date):

    trading_days = pd.read_csv("data_file/korea_trading_days.csv")
    trading_days['날짜'] = trading_days['날짜'].apply(lambda x: str_to_date(x))
    trading_days = trading_days['날짜'].to_list()
    trading_days = [day for day in trading_days if start_date <= day <= end_date]
    return trading_days


def get_supply_day_price(today):

    print(today)
    # 코스피 일봉 수집
    # 인데 -> 거래일 리스트를 생성해야함 (삼성전자 데이터 수집)

    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
        'mktId': 'STK',
        'trdDd': str(today),
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
    }
    j = json.loads(requests.post(url, data).text)
    df = pd.json_normalize(j['OutBlock_1'])
    df = df.replace(',', '', regex=True)
    df = df.drop(['SECT_TP_NM','MKT_ID','FLUC_TP_CD','CMPPREVDD_PRC','FLUC_RT'],axis='columns')

    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
        'mktId': 'KSQ',
        'trdDd': str(today),
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
    }
    j = json.loads(requests.post(url, data).text)
    df2 = pd.json_normalize(j['OutBlock_1'])
    df2 = df2.replace(',', '', regex=True)
    df2 = df2.drop(['SECT_TP_NM', 'MKT_ID', 'FLUC_TP_CD', 'CMPPREVDD_PRC', 'FLUC_RT'], axis='columns')

    df = pd.concat([df,df2])

    date_index = str_to_date(today)
    df['날짜'] = date_index

    df = df.sort_values('MKTCAP', ascending=False)

    cols_map = {'ISU_SRT_CD':'종목코드', 'ISU_ABBRV':'종목명', 'MKT_NM':'마켓', '날짜':'날짜',
                'TDD_CLSPRC':'종가', 'TDD_OPNPRC':'시가', 'TDD_HGPRC':'고가', 'TDD_LWPRC':'저가',
                'ACC_TRDVOL':'거래량', 'ACC_TRDVAL':'거래대금', 'MKTCAP':'시가총액', 'LIST_SHRS':'상장주식수'
    }

    df = df.rename(columns=cols_map)
    df = df[['종목코드','종목명','날짜','마켓','종가','시가','고가','저가','거래량','거래대금','시가총액','상장주식수']]

    df['금융투자순매수'] = ''
    df['금융투자순거래대금']= ''
    df['보험순매수'] = ''
    df['보험순거래대금'] = ''
    df['투신순매수'] = ''
    df['투신순거래대금'] = ''
    df['은행순매수'] = ''
    df['은행순거래대금'] = ''
    df['기타금융순매수'] = ''
    df['기타금융순거래대금'] = ''
    df['연기금순매수'] = ''
    df['연기금순거래대금'] = ''
    df['기관순매수'] = ''
    df['기관순거래대금'] = ''
    df['기타법인순매수'] = ''
    df['기타법인순거래대금'] = ''
    df['개인순매수'] = ''
    df['개인순거래대금'] = ''
    df['외국인순매수'] = ''
    df['외국인순거래대금'] = ''
    df['기타외국인순매수'] = ''
    df['기타외국인순거래대금'] = ''

    df = pd.DataFrame(df)
    df = df.set_index('종목코드')

    dic_code = {'1000': '금융투자', '2000': '보험', '3000': '투신', '4000': '은행', '5000': '기타금융', '6000': '연기금', \
                '7050': '기관', '7100': '기타법인', '8000': '개인', '9000': '외국인', '9001': '기타외국인'}

    for code in dic_code:

        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02401',
            'locale': 'ko_KR',
            'mktId': 'STK',
            'invstTpCd': code,
            'strtDd': str(today),
            'endDd': str(today),
            'share': '1',
            'money':'1',
            'csvxls_isNo':'false'
        }

        j = json.loads(requests.post(url, data).text)
        local_df = pd.json_normalize(j['output'])
        local_df = local_df.replace(',', '', regex=True)

        local_df = local_df[['ISU_SRT_CD', 'ISU_NM', 'NETBID_TRDVOL', 'NETBID_TRDVAL']]

        for i in range(len(local_df['ISU_SRT_CD'])):

            ticker = local_df['ISU_SRT_CD'].iloc[i]
            vol = int(local_df['NETBID_TRDVOL'].iloc[i])
            tr_val = int(local_df['NETBID_TRDVAL'].iloc[i])

            df[f'{dic_code[code]}순매수'].loc[ticker] = vol
            df[f'{dic_code[code]}순거래대금'].loc[ticker] = tr_val


        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02401',
            'locale': 'ko_KR',
            'mktId': 'KSQ',
            'invstTpCd': code,
            'strtDd': str(today),
            'endDd': str(today),
            'share': '1',
            'money':'1',
            'csvxls_isNo':'false'
        }

        j = json.loads(requests.post(url, data).text)
        local_df = pd.json_normalize(j['output'])
        local_df = local_df.replace(',', '', regex=True)

        local_df = local_df[['ISU_SRT_CD', 'ISU_NM', 'NETBID_TRDVOL', 'NETBID_TRDVAL']]

        for i in range(len(local_df['ISU_SRT_CD'])):

            ticker = local_df['ISU_SRT_CD'].iloc[i]
            vol = int(local_df['NETBID_TRDVOL'].iloc[i])
            tr_val = int(local_df['NETBID_TRDVAL'].iloc[i])

            df[f'{dic_code[code]}순매수'].loc[ticker] = vol
            df[f'{dic_code[code]}순거래대금'].loc[ticker] = tr_val

        # sleep(0.5)

    df = df.replace('',0)
    df = df.reset_index()
    return df


def generate_day_price(day):

    bef_day_price = pd.read_csv(f"data_file/수급데이터_2022_to_{day.year}.csv", index_col=0)

    try:
        bef_day_price['날짜'] = bef_day_price['날짜'].apply(lambda day: str_to_date(day))
        bef_day_price['종목코드'] = bef_day_price['종목코드'].apply(lambda x: int_to_str(x))
    except:
        pass

    start_date = bef_day_price['날짜'].iloc[-1]
    start_date = start_date + timedelta(days=1)

    end_date = day

    if start_date > end_date:
        print("수집할 가격데이터가 없습니다")

    trading_days = get_trading_day(start_date, end_date)


    if len(trading_days) == 0:

        print("수집할 가격데이터가 없습니다")

    else:

        trading_days = [date_to_str(day) for day in trading_days]

        aft_day_price = get_supply_day_price(trading_days[0])

        for i,now_day in enumerate(trading_days):

            if i == 0:
                continue

            df2 = get_supply_day_price(now_day)
            aft_day_price = pd.concat([aft_day_price,df2])

        try:
            day_price = pd.concat([bef_day_price, aft_day_price])
            day_price = day_price.reset_index()
        except:
            pass
        # ,level_0,index,종목코드,종목명,날짜,마켓,종가,시가,고가,저가,거래량,거래대금,시가총액,상장주식수,금융투자순매수,금융투자순거래대금,보험순매수,보험순거래대금,투신순매수,투신순거래대금,은행순매수,은행순거래대금,기타금융순매수,기타금융순거래대금,연기금순매수,연기금순거래대금,기관순매수,기관순거래대금,기타법인순매수,기타법인순거래대금,개인순매수,개인순거래대금,외국인순매수,외국인순거래대금,기타외국인순매수,기타외국인순거래대금

        day_price = day_price[['종목코드','종목명','날짜','마켓','종가','시가','고가','저가','거래량','거래대금','시가총액'\
            ,'상장주식수','금융투자순매수','금융투자순거래대금','보험순매수','보험순거래대금','투신순매수','투신순거래대금','은행순매수'\
            ,'은행순거래대금','기타금융순매수','기타금융순거래대금','연기금순매수','연기금순거래대금','기관순매수','기관순거래대금'\
            ,'기타법인순매수','기타법인순거래대금','개인순매수','개인순거래대금','외국인순매수','외국인순거래대금','기타외국인순매수','기타외국인순거래대금']]

        day_price.to_csv(f"data_file/수급데이터_2022_to_{day.year}.csv")