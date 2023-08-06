import datetime
import os

import pandas as pd
import pyarrow.parquet as pq

from .client import BaseClient

extract_list = ['EXPOSURE', 'RETURN', 'COVARIANCE', 'IDIOSYNCRATIC_VOLATILITY']


def load_table(table: str, storage_dir: str, start_year: int, end_year: int):
    years = list(map(str, range(start_year, end_year+1)))
    file_list = [os.path.join(storage_dir, f'{table}_{year}.parquet') for year in years]
    if len(file_list) == 0:
        raise Exception(f"文件不存在，无法加载数据")
    for file in file_list:
        if not os.path.isfile(file):
            raise Exception(f"{file}文件不存在,无法加载全部数据")
    print("\n正在加载文件：")
    for file in file_list:
        print(f"    {file}")
    dataset = pq.ParquetDataset(file_list, use_legacy_dataset=True)
    print("加载数据完毕")
    df = dataset.read().to_pandas()
    return df


def validate_date(date_text):
    if len(date_text) == 8:
        try:
            datetime.datetime.strptime(date_text, '%Y%m%d')
        except ValueError:
            raise ValueError("数据格式不正确，应该是YYYYMMDD")
    else:
        raise ValueError("数据格式不正确，应该是YYYYMMDD")


def validate_class(param):
    if len(param["class"]) == 0:
        raise Exception(f"class不能为空")
    elif len(param["class"]) > 0 and param["class"][0:17] == "feature_exposure_":
        param["class"] = param["class"].split('feature_exposure_')[1]
    elif len(param["class"]) > 0 and param["class"][0:24] == "characteristic_exposure_":
        param["class"] = param["class"].split('characteristic_exposure_')[1]
    else:
        raise Exception(f"class输入错误")
    return f"FACTOR_{param.get('class').upper()}"


def validate_fields(param, start_date, end_date):
    where = f"TRADE_DT >= {start_date} and TRADE_DT <= {end_date}"
    if len(param["fields"]) > 0 and param["fields"] not in extract_list:
        where += f" & STK_CODE in {param['fields']}"
    return where


class LocalClient(BaseClient):
    def __init__(self, path):
        super().__init__()
        if not os.path.isdir(path):
            raise Exception(f"{path}该目录不存在")
        self.storage_path = path

    def extract_feature_exposure(self, param) -> pd.DataFrame:
        """直接取得特征暴露"""
        # todo 需要对参数校验
        table_name = "Features_Data"
        dir_name = "feature-exposure"
        storage_idr = os.path.join(self.storage_path, dir_name)
        if not os.path.isdir(storage_idr):
            raise Exception(f"{storage_idr}该目录不存在")
        """校验class"""
        factor_name = validate_class(param)

        """校验date"""
        validate_date(param.get("start_date"))
        validate_date(param.get("end_date"))

        start_date = int(param.get("start_date"))
        end_date = int(param.get("end_date"))
        start_year = int(str(start_date)[0:4])
        end_year = int(str(end_date)[0:4])
        df = load_table(table_name, storage_idr, start_year, end_year)  # 加载数据
        df["TRADE_DT"] = pd.to_datetime(df['TRADE_DT'])
        # todo 增加筛选项
        where = validate_fields(param, start_date, end_date)
        try:
            res = df.query(where)[["TRADE_DT", "STK_CODE", factor_name]]
        except KeyError:
            raise KeyError(factor_name + "不存在")
        return res

    def query(self, param):
        pass

    def extract(self, param):
        if param.get("domain") == "descriptor" and param.get("phylum") == "direct":
            return self.extract_feature_exposure(param)
        else:
            raise Exception("domain或phylum参数错误")
