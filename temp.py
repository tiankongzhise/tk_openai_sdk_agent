import re
from src.tk_openai_sdk_agent.objects.free_walk_new.db_models import aimodel_orm_mapping
from src.tk_openai_sdk_agent.database import Curd
from sqlalchemy import select

input_str = """ip='无期迷途' character='局长' ai_rsp='无期迷途' ai_model='DEEPSEEK-R1'
ip='崩坏3' character='阿波尼亚' ai_rsp='崩坏3' ai_model='DEEPSEEK-R1'
ip='黑神话悟空' character='哪吒' ai_rsp='黑神话:悟空' ai_model='DEEPSEEK-R1'
ip='终极的炽天使' character='克鲁鲁' ai_rsp='终结的炽天使' ai_model='DEEPSEEK-R1'
ip='崩铁' character='幼年星期日' ai_rsp='崩坏:星穹铁道' ai_model='DEEPSEEK-R1'
ip='入殓师' character='伊索卡尔' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='第五人格' character='病患稀缺病案' ai_rsp='第五人格' ai_model='DEEPSEEK-R1'
ip='第五人格' character='范无咎' ai_rsp='第五人格' ai_model='DEEPSEEK-R1'
ip='哪吒之魔童闹海' character='哪吒' ai_rsp='哪吒之魔童降世' ai_model='DEEPSEEK-R1'
ip='约会大作战' character='鸢一折纸' ai_rsp='约会大作战' ai_model='DEEPSEEK-R1'
ip='排球少年' character='孤爪研磨' ai_rsp='排球少年  ' ai_model='DEEPSEEK-R1'
ip='先知' character='黯' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='崩坏三' character='爱莉希雅 纯真梦歌' ai_rsp='崩坏3' ai_model='DEEPSEEK-R1'
ip='头七怪谈' character='离雨亭' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='头七怪谈' character='佴和' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='头七怪谈' character='白岭性转' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='地下偶像' character='luca' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='vocalidol' character='镜音铃' ai_rsp='vocaloid' ai_model='DEEPSEEK-R1'
ip='异形舞台' character='till' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='常规脱离' character='锦亚澄' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='颂乐人偶' character='若叶睦' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='manta' character='季少一' ai_rsp='paradox live' ai_model='DEEPSEEK-R1'
ip='背叛的鲁鲁修' character='cc' ai_rsp='反叛的鲁路修' ai_model='DEEPSEEK-R1'
ip='九柱神' character='奈芙蒂斯' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='2 5次元的诱惑' character='莉莉艾露' ai_rsp='2 5次元的诱惑' ai_model='DEEPSEEK-R1'
ip='我在惊悚游戏里封神' character='红桃皇后' ai_rsp='我在惊悚游戏里封神' ai_model='DEEPSEEK-R1'
ip='我在精神病院斩神' character='林七夜' ai_rsp='我在精神病院学斩神' ai_model='DEEPSEEK-R1'
ip='从零开始的异世界' character='蕾姆' ai_rsp='re:从零开始的异世界生活' ai_model='DEEPSEEK-R1'
ip='崩坏 星穹铁道' character='军礼刃' ai_rsp='崩坏:星穹铁道' ai_model='DEEPSEEK-R1'
ip='家里蹲吸血姬的苦闷' character='薇儿赫泽' ai_rsp='家里蹲吸血姬的郁闷' ai_model='DEEPSEEK-R1'
ip='更衣人偶坠入爱河' character='喜多川海梦 请假' ai_rsp='更衣人偶坠入爱河' ai_model='DEEPSEEK-R1'
ip='我在精神病院学斩神' character='倪克斯' ai_rsp='我在精神病院学斩神' ai_model='DEEPSEEK-R1'
ip='哪吒之魔童闹海' character='敖闰' ai_rsp='哪吒之魔童降世' ai_model='DEEPSEEK-R1'
ip='更衣人偶陷入爱河' character='喜多川海梦' ai_rsp='更衣人偶坠入爱河' ai_model='DEEPSEEK-R1'
ip='君死' character='日和飒' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='变身 偶像公主' character='雪森苹果' ai_rsp='变身 偶像公主' ai_model='DEEPSEEK-R1'
ip='崩铁星穹铁道' character='忘归人' ai_rsp='崩坏:星穹铁道' ai_model='DEEPSEEK-R1'
ip='degrees of lewdity' character='雷米 remy' ai_rsp='degrees of lewdity' ai_model='DEEPSEEK-R1'
ip='异型舞台' character='mizi' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='刀剑神域' character='亚丝娜 血盟骑士团' ai_rsp='刀剑神域' ai_model='DEEPSEEK-R1'
ip='赛马娘' character='米浴 花嫁' ai_rsp='赛马娘 pretty derby' ai_model='DEEPSEEK-R1'
ip='头七怪谈' character='子车甫昭' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='蔚蓝档案' character='早濑优香 体操服' ai_rsp='蔚蓝档案' ai_model='DEEPSEEK-R1'
ip='战斗女仆' character='红桃' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='崩坏星穹轨铁道' character='流萤' ai_rsp='崩坏:星穹铁道' ai_model='DEEPSEEK-R1'
ip='永雏塔菲' character='保健委员' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='战斗女仆' character='黑桃' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='食物语' character='舒心初茶女少' ai_rsp='食物语' ai_model='DEEPSEEK-R1'
ip='星穹铁道' character='饮月君' ai_rsp='崩坏:星穹铁道' ai_model='DEEPSEEK-R1'
ip='86-不存在的战区' character='芙拉蒂蕾娜·米利杰' ai_rsp='86-不存在的战区' ai_model='DEEPSEEK-R1'
ip='少女aに夜露死苦' character='魅红' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='反叛的鲁鲁修' character='c c' ai_rsp='反叛的鲁路修' ai_model='DEEPSEEK-R1'
ip='反叛的鲁路修' character='鲁路修' ai_rsp='反叛的鲁路修' ai_model='DEEPSEEK-R1'
ip='蛞蝓少女' character='夕子' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='头七怪谈' character='花堇' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='镭塔' character='李又珊' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='哪吒之魔童闹海' character='敖丙' ai_rsp='哪吒之魔童降世' ai_model='DEEPSEEK-R1'
ip='头七怪谈' character='民国子车甫昭' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='头七' character='佴和' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='哪吒魔童闹海' character='敖丙' ai_rsp='哪吒之魔童降世' ai_model='DEEPSEEK-R1'
ip='花花的甜心小厨房' character='花花' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='巴拉拉小魔仙' character='严莉莉' ai_rsp='巴啦啦小魔仙' ai_model='DEEPSEEK-R1'
ip='紫罗兰花园' character='薇尔莉特' ai_rsp='紫罗兰永恒花园' ai_model='DEEPSEEK-R1'
ip='硬核一中' character='戎星野' ai_rsp='硬核一中' ai_model='DEEPSEEK-R1'
ip='头七' character='离宇亭' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='我不是戏神' character='陈伶' ai_rsp='我不是戏神' ai_model='DEEPSEEK-R1'
ip='vtuber' character='enna' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='重返未来19999' character='梅兰妮' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='你去死吧' character='田纲丈' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='虚拟歌姬-初音未来' character='小浣熊' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='家庭教师' character='蓝波 请假' ai_rsp='家庭教师hitman reborn ' ai_model='DEEPSEEK-R1'
ip='v家' character='焚炉石镜音连' ai_rsp='vocaloid' ai_model='DEEPSEEK-R1'
ip='v家' character='初音未来 39望月' ai_rsp='vocaloid' ai_model='DEEPSEEK-R1'
ip='崩坏-星穹铁道' character='花火' ai_rsp='崩坏:星穹铁道' ai_model='DEEPSEEK-R1'
ip='头七' character='离宇亭' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='苗疆' character='祭司大人' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='地狱有什么不好' character='利维坦 自拍' ai_rsp='地狱有什么不好' ai_model='DEEPSEEK-R1'
ip='pradoxlive' character='御山京' ai_rsp='paradox live' ai_model='DEEPSEEK-R1'
ip='虚拟舞台' character='kaito小浣熊' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='第五人格-园丁' character='万圣节音乐会' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='第五人格-拉拉队员' character='荧' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='plave' character='hamin' ai_rsp='plave' ai_model='DEEPSEEK-R1'
ip='火影忍者' character='旗木卡卡西 暗部' ai_rsp='火影忍者' ai_model='DEEPSEEK-R1'
ip='东方pro ject' character='芙兰朵露' ai_rsp='东方project' ai_model='DEEPSEEK-R1'
ip='唱见' character='ado' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='明日方舟' character='泥岩' ai_rsp='明日方舟' ai_model='DEEPSEEK-R1'
ip='哭泣少女乐队' character='安和昴' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='假面骑士加布' character='井上生真' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='世界计划·多彩舞台' character='桐谷遥 zozo1' ai_rsp='世界计划 彩色舞台 feat  初音未来' ai_model='DEEPSEEK-R1'
ip='摩登三国' character='诸葛亮' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='第5人格' character='红夫人' ai_rsp='第五人格' ai_model='DEEPSEEK-R1'
ip='头七怪谈' character='仇云生' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='术力口' character='miku' ai_rsp='vocaloid' ai_model='DEEPSEEK-R1'
ip='虚拟歌姬-巡音流歌' character='小浣熊' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='拂晓的尤娜 晨曦公主' character='尤娜' ai_rsp='晨曦公主' ai_model='DEEPSEEK-R1'
ip='斩神' character='司小南' ai_rsp='我在精神病院学斩神' ai_model='DEEPSEEK-R1'
ip='颂乐人偶' character='丰川祥子' ai_rsp='未知' ai_model='DEEPSEEK-R1'
ip='idoish7' character='入殓师' ai_rsp='idolish7' ai_model='DEEPSEEK-R1'
"""


def parse_string_to_dict(input_str):
    # 正则表达式匹配所有 key='value' 键值对
    matches = re.findall(r"([^=]+)='([^']*)'", input_str)
    # 将匹配结果转换为字典
    return {key.strip(): value for key, value in matches}
# 解析为字典列表
result = []
# 按行分割字符串
for line in input_str.strip().split('\n'):
    # 跳过空行（如果有）
    if not line.strip():
        continue
    result.append(parse_string_to_dict(line))

print(len(result))
ai_model = result[0]['ai_model']
db_client = Curd()
stmt = select(aimodel_orm_mapping[ai_model])
session_func = db_client.get_session()
existing_data = set()
with session_func() as session:
    db_result = session.execute(stmt).scalars().all()
    for record in db_result:
        temp = f'{record.ip}@{record.character}'
        if temp not in existing_data:
            existing_data.add(temp)
new_list = []
for item in result:
    temp = f'{item["ip"]}@{item["character"]}'
    if temp not in existing_data:
        new_list.append(item)

print(new_list)

