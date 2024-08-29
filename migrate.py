import os
import re
import requests
import json
from logger import getLogger
from MatchInfo import MatchInfo
import yaml

logger = getLogger()
# 读取配置文件
config = None
with open("config.yml", "r", encoding="utf-8") as yaml_file:
    config = yaml.safe_load(yaml_file)
yaml_file.close()
picgo_server_url = config["migrate"]["picgo"]["server_url"]
result_filepath = config["scan"]["match"]["result_filepath"]

def upload_by_picgo(match_info):
    """
    批量上传图片到图床，失败使用原链接
    :param match_info:
    :return:
    """
    name = match_info.filepath
    new_urls = []

    for url in match_info.pic_urls:
        data = {
            "list": [url]
        }
        logger.info(f"{name}: 开始上传 {url}")
        res = requests.post(picgo_server_url, json=data)
        res_obj = json.loads(res.text)

        if res.status_code != 200 or res_obj["success"] == False:
            logger.error(f"{name}: 上传失败, {res}")
            new_urls.append(url)
        else:
            logger.info(f"{name}: 上传成功, {res.text}")
            new_urls.append(res_obj["result"][0])

    return new_urls


def replace():
    """
    :return:
    """
    # 反序列化
    output_file = open(result_filepath, "r", encoding="utf-8")

    load_data = json.load(output_file)
    matches = [MatchInfo.from_dict(data) for data in load_data]
    logger.info("开始执行, 可能会耗费较长时间, 请勿关闭程序!!")
    # 按文件分组上传图片并替换原始url
    for match in matches:
        # 上传文件内所有图片
        pics_new = upload_by_picgo(match)
        # 批量替换
        with open(match.filepath, "r", encoding="utf-8") as f:
            content = f.read()
            for search_text, replace_text in zip(match.pic_urls, pics_new):
                content = content.replace(search_text, replace_text)
            with open(match.filepath, "w", encoding="utf-8") as ff:
                ff.write(content)
            ff.close()
            logger.info(f"{match.filepath}: 替换完成")
        f.close()
    logger.info("全部替换完成!!")


if __name__ == "__main__":
    replace()