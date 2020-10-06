import logging
import random
import urllib.request, json

import azure.functions as func
import pandas as pd


def judgebyjson(json_dict):
    RES_LIST = []

    THRES_HR = 75
    THRES_VOLUME = 600
    GET_DATA_NUM = 12
    if not len(json_dict)==0: # json fileの中身が存在する時
        # json formatをpd.DataFrameにcast
        df_json = pd.DataFrame(json_dict)

        # DBの中からhr, volumeが共に、-1のレコードを抽出 →　終了時間候補を抽出
        df_end_candinate = df_json[(df_json['hr'].astype(int).values==-1.) & (df_json['volume'].astype(int).values==-1)]
        # print(df_end_candinate)
        # DBの中からhr, volumeが共に、-1以外のレコードを抽出 → 終了時間以外を抽出
        df_json2 = df_json[(df_json['hr'].astype(int).values!=-1.) | (df_json['volume'].astype(int).values!=-1)]

        # 終了時間以外を時間基準に降べきにソート
        df_json_sort = df_json2.sort_values('time', ascending=False).head(GET_DATA_NUM)
        # print(df_json_sort)
        # 最新時間を取得
        df_now = df_json_sort.head(1)

        if not len(df_end_candinate)==0:
            # まだ未到達の終了時間( 終了時間候補 > 最新時間 )
            # 複数分の退出時間がある時には、時間で昇べきにソートし、先頭を取得（現在に近い方を取得）。
            df_end_candinate2  = df_end_candinate[df_end_candinate['time'].values > df_now['time'].values].sort_values('time').head(1)
            # print(df_end_candinate2)

            if not len(df_end_candinate2)==0:
                # 終了時間候補 - 最新時間:  https://note.nkmk.me/python-pandas-datetime-timestamp/
                #  df_end_candinate2['time']が datatime型の場合
                end2now_time = (pd.to_datetime(df_end_candinate2['time']).map(pd.Timestamp.timestamp).astype(int).values[0]
                                - pd.to_datetime(df_now['time']).map(pd.Timestamp.timestamp).astype(int).values[0])

                #  df_end_candinate2['time']が unixtime：数値型の場合
                # end2now_time = df_end_candinate2['time'].values[0] - df_now['time'].values[0]

                # print(end2now_time)

                if end2now_time <= 60: # 誰かの指定した終了時間候補まで1分以内
                    RES_LIST.append({'name':df_end_candinate2['name'].values[0], 'behave':2})

            else: # 終了時間候補を抽出できない場合
                contain_member = False
                kumamon = df_json_sort[df_json_sort['name']=='kumamon']
                hachan = df_json_sort[df_json_sort['name']=='hachan']
                sanosan = df_json_sort[df_json_sort['name']=='sanosan']
                otomo= df_json_sort[df_json_sort['name']=='otomo']

                # judge whether behave ==1 or !=1  for each person?
                if kumamon['hr'].astype(int).values.mean() > THRES_HR and kumamon['volume'].astype(int).values.mean() < THRES_VOLUME:
                    contain_member = True
                    RES_LIST.append({'name':'kumamon', 'behave':1})
                if hachan['hr'].astype(int).values.mean() > THRES_HR and hachan['volume'].astype(int).values.mean() < THRES_VOLUME:
                    contain_member = True
                    RES_LIST.append({'name':'hachan', 'behave':1})
                if sanosan['hr'].astype(int).values.mean() > THRES_HR and sanosan['volume'].astype(int).values.mean() < THRES_VOLUME:
                    contain_member = True
                    RES_LIST.append({'name':'sanosan', 'behave':1})
                if otomo['hr'].astype(int).values.mean() > THRES_HR and otomo['volume'].astype(int).values.mean() < THRES_VOLUME:
                    contain_member = True
                    RES_LIST.append({'name':'otomo', 'behave':1})

                if not contain_member: # behave1の条件に当てはまらなかった場合
                    RES_LIST.append({'name':'stranger', 'behave':0})

        else: # 終了時間候補を抽出できない場合
            contain_member = False
            kumamon = df_json_sort[df_json_sort['name']=='kumamon']
            hachan = df_json_sort[df_json_sort['name']=='hachan']
            sanosan = df_json_sort[df_json_sort['name']=='sanosan']
            otomo= df_json_sort[df_json_sort['name']=='otomo']

            # judge whether behave ==1 or !=1  for each person?
            if kumamon['hr'].astype(int).values.mean() > THRES_HR and kumamon['volume'].astype(int).values.mean() < THRES_VOLUME:
                contain_member = True
                RES_LIST.append({'name':'kumamon', 'behave':1})
            if hachan['hr'].astype(int).values.mean() > THRES_HR and hachan['volume'].astype(int).values.mean() < THRES_VOLUME:
                contain_member = True
                RES_LIST.append({'name':'hachan', 'behave':1})
            if sanosan['hr'].astype(int).values.mean() > THRES_HR and sanosan['volume'].astype(int).values.mean() < THRES_VOLUME:
                contain_member = True
                RES_LIST.append({'name':'sanosan', 'behave':1})
            if otomo['hr'].astype(int).values.mean() > THRES_HR and otomo['volume'].astype(int).values.mean() < THRES_VOLUME:
                contain_member = True
                RES_LIST.append({'name':'otomo', 'behave':1})

            if not contain_member: # behave1の条件に当てはまらなかった場合
                RES_LIST.append({'name':'stranger', 'behave':0})

        # behave1の条件に当てはまる人が複数存在する場合に１人に絞る
        select_res_list = RES_LIST[random.randrange(len(RES_LIST))]
        return select_res_list

    else: # json fileの中身が空の時
        return {'name':'stranger', 'behave':0}

def make_slack_msg(result_json):
    name_dict = {"kumamon":"くまモン", "hachan":"はーさん", "sanosan": "さのさん", "otomo":"おおとも", "stranger":"皆の者"}
    behave_list = ["リモを楽しみたまへ", "喋るが良い", "帰るが良いぞ"]
    name = name_dict[result_json["name"]]
    behave = behave_list[result_json["behave"]]
    msg_obj = {"text":"{} {}".format(name, behave)}
    return msg_obj

def send_slack(obj):
    url = "SLACKのURL"
    method = "POST"
    headers = {"Content-Type" : "application/json"}
    # PythonオブジェクトをJSONに変換する
    json_data = json.dumps(obj).encode("utf-8")
    # httpリクエストを準備してPOST
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")

def main(req: func.HttpRequest, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('judge!!')

    # jsonの取得
    params = req.get_json()
    logging.info(params)

    # 結果登録
    judge_result = judgebyjson(params)
    logging.info({"result":judge_result}, judge_result)
    outputDocument.set(func.Document.from_dict({"result":judge_result}))

    msg_obj = make_slack_msg(judge_result)
    send_slack(msg_obj)

    if params:
        return func.HttpResponse(f"PARAMS: {params}")
    else:
        return func.HttpResponse(
             "RUN!!",
             status_code=200
        )
