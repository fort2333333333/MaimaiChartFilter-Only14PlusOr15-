import json
import random
import streamlit as st
from PIL import Image
from datetime import datetime, timedelta

@st.cache_data
def load_data():
    with open("info.json", "r", encoding="utf-8") as f:
        return json.load(f)

INFO = load_data()

def merge(list1,list2):
    index_list = []
    for i in list2:
        if i in list1:
            index_list.append(i)
    return index_list

def find(key,value):
    for index, song in enumerate(INFO):
        if song[key] == value:
            return index
    return -1

def find_all(key,operator,value,index_list=None):
    find_all_result = []
    for index, song in enumerate(INFO):
        if condition(song[key],key,operator,value):
            find_all_result.append(index)
    if index_list != None:
        find_all_result = merge(find_all_result,index_list)
    return find_all_result

VERSION = ["maimai","maimai+","GreeN","GreeN+",
           "ORANGE","ORANGE+","PiNK","PiNK+",
           "MURASAKi","MURASAKi+","MiLK","MiLK+",
           "FiNALE",
           "でらっくす","でらっくす+","Splash","Splash+",
           "UNiVERSE","UNiVERSE+","FESTiVAL","FESTiVAL+",
           "BUDDiES","BUDDiES+","PRiSM","PRiSM+",
           "CiRCLE","CiRCLE+"]
def condition(song_value,key,operator,value):
    if key == "version":
        song_value = VERSION.index(song_value)
        value = VERSION.index(value)
    elif key == "internal_level":
        song_value = float(song_value)
        value = float(value)
    elif key == "No." or key == "bpm" or key == "tap" or key == "hold" or key == "slide" \
    or key == "touch" or key == "break" or key == "total" or key == "value":
        song_value = int(song_value)
        value = int(value)
    if operator == ">":
        return song_value > value
    elif operator == "<":
        return song_value < value
    elif operator == ">=":
        return song_value >= value
    elif operator == "<=":
        return song_value <= value
    elif operator == "==":
        return song_value == value
    elif operator == "!=":
        return song_value != value
    else:
        raise KeyError

def sort_by(sort_method,reverse=True,index_list=None):
    if index_list == None:
        index_list = list(range(0,88))
    n = len(index_list)
    for i in range(n):
        for j in range(n-1-i):
            if condition(INFO[index_list[j]][sort_method],sort_method,">=",INFO[index_list[j+1]][sort_method]):
                index_list[j], index_list[j+1] = index_list[j+1], index_list[j]
    if reverse:
        index_list = index_list[::-1]
    return index_list

cover_folder_path = "static/image/cover/"
def full_cover_path(cover):
    return cover_folder_path + cover

def print_cover(index):
    st.image(full_cover_path(INFO[index]["cover"]))

def print_info(index):
    st.text(f"{INFO[index]["title"]}  {INFO[index]["type"]}  {INFO[index]["difficulty"]}  lv.{INFO[index]["level"]} ({INFO[index]["internal_level"]})")
    st.text(f"曲师: {INFO[index]["artist"]}  bpm: {INFO[index]["bpm"]}")
    st.text(f"谱师: {INFO[index]["note_designer"]}")
    st.text(f"日期: {INFO[index]["released_date"]} ({INFO[index]["version"]})")
    st.text(f"tap: {INFO[index]["tap"]}  hold: {INFO[index]["hold"]}  slide: {INFO[index]["slide"]}  touch: {INFO[index]["touch"]}  break: {INFO[index]["break"]}  total: {INFO[index]["total"]}")

def print_all(index_list):
    for index in index_list:
        col1, col2 = st.columns([1,2])
        with col1:
            print_cover(index)
        with col2:
            print_info(index)

@st.dialog("随机歌曲")
def random_song(songs):
    if songs:
        song = random.choice(songs)
        print_cover(song)
        print_info(song)
        st.button("再越一首")
    else:
        st.image("static/image/cover/-1.jpg")
        st.text("鍠滄�㈣糠浣犱笘鐣� 浣犳槸 杩欎釜 lv.浠�涔� (鎯冲共.鍟�)")
        st.text("鏇插笀: 杩欐槸璋� 脳 鏄�涓�浜虹墿")
        st.text("璋卞笀: 涓嶆槸涔嬩腑 濋笩: 鍍忔繃绋")
        st.text("鏃ユ湡: 鍝堝搱-涓栫晫-浣犲ソ (鍢诲樆)")
        st.text("瀹炲湪: 缂栦笉涓�  鍘讳簡: 鎵�浠� 鍒板簳鍐�: 浠� 涔堝ソ鍛�:閿� 鏂ゆ嫹: 锟斤拷�� 鎯冲悆: 閿熸枻鎷�")
        st.button("浠ヨ繖鏍")

def crop_cover(index,x,y, cropped_size,g):
    cover = Image.open(full_cover_path(INFO[index]["cover"]))
    cropped = cover.crop((x,y,x+cropped_size,y+cropped_size))
    if g:
        cropped = cropped.convert("L")
    st.image(cropped,width=300)

@st.dialog("曲绘猜歌")
def random_cover(songs,CROP_SIZE,grey):
    if st.button("再猜一首"):
        if songs:
            st.session_state.song = random.choice(songs)
        else:
            st.session_state.song = random.randint(0,87)
        st.session_state.x = random.randint(0,190-CROP_SIZE)
        st.session_state.y = random.randint(0,190-CROP_SIZE)
    crop_cover(st.session_state.song,st.session_state.x,st.session_state.y,CROP_SIZE,grey)
    if st.button("看看答案"):
        print_cover(st.session_state.song)

if "grey" not in st.session_state:
    st.session_state.grey = False
if "image_size" not in st.session_state:
    st.session_state.image_size = 30
if "after_rerun" not in st.session_state:
    st.session_state.after_rerun = ""

@st.dialog("设置")
def setting():
    setting_image_size = st.slider("曲绘猜歌:曲绘裁剪大小",min_value = 10,max_value = 50,value=st.session_state.image_size)
    setting_grey = st.toggle("曲绘猜歌:显示黑白曲绘",value=st.session_state.grey)
    if st.button("保存"):
        st.session_state.image_size = setting_image_size
        st.session_state.grey = setting_grey
        st.session_state.after_rerun = "保存成功!"
        st.rerun()

def random_date():
    start = datetime.strptime("2013/01/01", "%Y/%m/%d")
    end = datetime.strptime("2025/12/31", "%Y/%m/%d")
    delta_days = (end - start).days
    random_days = random.randint(0, delta_days)
    random_date = start + timedelta(days=random_days)
    date_str = random_date.strftime("%Y/%m/%d")
    return date_str

DESC_DESIGNER = ["Luxizhel","シチミヘルツ","Jack","翠楼屋","サファ太","鳩ホルダー"]
DESC_LEVEL = ["14.6","14.7","14.8","14.9","15.0"]
DESC_TAG = ["KaleidScope","PANDORA BOXXX","project_raputa","完美挑战曲","Legend曲","KOP决赛曲","KOP预选追加曲"]
def random_description(song,target):
    if target == "designers":
        random.shuffle(DESC_DESIGNER)
        if DESC_DESIGNER[0] in INFO[song]["designers"]:
            return f"谱师是 {DESC_DESIGNER[0]}"
        elif DESC_DESIGNER[1] in INFO[song]["designers"]:
            return f"谱师是 {DESC_DESIGNER[1]}"
        else:
            return f"谱师不是 {DESC_DESIGNER[0]} 或 {DESC_DESIGNER[1]}"
    elif target == "internal_level":
        target_level = random.choice(DESC_LEVEL)
        if INFO[song]["internal_level"] > target_level:
            return f"定数大于{target_level}"
        elif INFO[song]["internal_level"] < target_level:
            return f"定数小于{target_level}"
        else:
            return f"定数是{target_level}"
    elif target == "version":
        target_version = random.choice(VERSION)
        if condition(INFO[song]["version"],"version",">",target_version):
            return f"版本在{target_version}后"
        elif condition(INFO[song]["version"],"version","<",target_version):
            return f"版本在{target_version}前"
        else:
            return f"版本是{target_version}"
    elif target == "tag":
        random.shuffle(DESC_TAG)
        if DESC_TAG[0] in INFO[song]["tag"]:
            return f"曲子是{DESC_TAG[0]}"
        elif DESC_TAG[1] in INFO[song]["tag"]:
            return f"曲子是{DESC_TAG[1]}"
        else:
            return f"曲子不是{DESC_TAG[0]}或{DESC_TAG[1]}"
    elif target == "break":
        target_break = random.randint(20,100)
        if int(INFO[song]["break"]) > target_break:
            return f"绝赞大于{target_break}"
        elif int(INFO[song]["break"]) < target_break:
            return f"绝赞小于{target_break}"
        else:
            return f"绝赞等于{target_break}"
    elif target == "type":
        return f"曲子是{INFO[song]["type"]}曲"
    elif target == "bpm":
        target_bpm = random.randint(100,200)
        if int(INFO[song]["bpm"]) > target_bpm:
            return f"bpm大于{target_bpm}"
        elif int(INFO[song]["bpm"]) < target_bpm:
            return f"bpm小于{target_bpm}"
        else:
            return f"bpm等于{target_bpm}"
    elif target == "total":
        target_total = random.randint(900,1200)
        if int(INFO[song]["total"]) > target_total:
            return f"物量大于{target_total}"
        elif int(INFO[song]["total"]) < target_total:
            return f"物量小于{target_total}"
        else:
            return f"物量等于{target_total}"
    elif target == "difficulty":
        return f"难度是{INFO[song]["difficulty"]}"
    elif target == "released_date":
        target_date = random_date()
        if target_date < INFO[song]["released_date"]:
            return f"在{target_date}后加入"
        elif target_date > INFO[song]["released_date"]:
            return f"在{target_date}前加入"
        else:
            return f"在{target_date}加入"
    return f"卡bug了"

ALL_TARGET = ["designers","internal_level","version","tag","break","type","bpm","total","difficulty",
              "released_date"]
ALL_TARGET_2 = ["designers","internal_level","version","tag","break","bpm","total",
              "released_date"]
@st.dialog("提示猜歌")
def random_info(songs):
    if st.button("再猜一首"):
        if songs:
            st.session_state.song = random.choice(songs)
        else:
            st.session_state.song = random.randint(0, 87)
        st.session_state.description = ""
        st.session_state.description_target = ALL_TARGET.copy()
    if st.session_state.description_target == ALL_TARGET:
        st.session_state.description += ("\n" + random_description(st.session_state.song,st.session_state.description_target.pop(random.randint(0,len(st.session_state.description_target) - 1))))
    if st.button("继续提示"):
        if st.session_state.description_target:
            st.session_state.description += ("\n"+random_description(st.session_state.song,st.session_state.description_target.pop(random.randint(0,len(st.session_state.description_target)-1))))
        else:
            st.session_state.description_target = ALL_TARGET_2.copy()
            st.session_state.description += ("\n" + random_description(st.session_state.song,st.session_state.description_target.pop(random.randint(0,len(st.session_state.description_target) - 1))))
    st.text(st.session_state.description)
    if st.button("到底是什么"):
        col111, col222 = st.columns([1,2])
        with col111:
            print_cover(st.session_state.song)
        with col222:
            print_info(st.session_state.song)

if st.session_state.after_rerun:
    st.toast(st.session_state.after_rerun)
    st.session_state.after_rerun = ""

CHARTER = ['サファ太', '小鳥遊さん', 'Luxizhel', 'Jack', 'シチミヘルツ', 'はっぴー', 'チャン@DP皆伝',
           '鳩ホルダー', '翠楼屋', '隅田川星人', '合作だよ', '譜面ボーイズからの挑戦状', '某S氏', 'ロシェ@ペンギン',
           'カマボコ君', 'ぴちネコ', '譜面-100号', '華火職人', '玉子豆腐', '柠檬', 'ロシェ',
           'アミノハバキリ', 'せめんともり', 'あまくちジンジャ一', 'rintaro soma', 'maimai TEAM DX',
           'maimai Fumen All-Stars', 'Xaleid◆scopiX', 'Revo@LC', 'Redarrow', 'PANDORA PARADOXXX',
           'PANDORA BOXXX', 'Licorice Gunjyo', 'KALEIDXSCOPE', 'Garakuta Scramble!', 'BEYOND THE MEMORIES',
           'KOP7th -FiNAL BATTLE- by 7.3GHz', '7sRef -DOVE-', 'BELiZHEL vs Safari', 'project_raputa',
           'Safata.GHz', '翡翠マナ', '7.3GHz -Før The Legends-', '超七味星人', '-ZONE- SaFaRi',
           '"H"ack underground', 'Safari', 'サファ太 vs じゃこレモン', 'SΛFΛRI/RΦCHER', 'The Dove',
           'BELiZHEL vs 7.3GHz', 'BELiZHEL', '翡翠マナ -Memoir-', 'The ALiEN', '7.3GHz vs Phoenix',
           'Phoenix', '小鳥遊さん fused with Phoenix', '原田ひろゆき', 'Luxizhel+カマボコ君+はっぴー',
           'EL DiABLO', '鳩サファzhel', 'ボコ太', 'KOP3rd with 翡翠マナ', '-ZONE-Phoenix', '7.3GHz',
           'jacK on Phoenix', 'SAFARI☆CAT', 'サファ太 vs Luxizhel', 'Safazhel',
           'jacK on Phoenix vs -ZONE- SaFaRi', 'red phoenix', 'Jack & Licorice Gunjyo',
           '小鳥遊さん vs 華火職人', 'サファ太 vs -ZONE- SaFaRi', '舞舞10年ズ ～ファイナル～', '舞舞10年ズ (チャンとはっぴー)']
TAG = ["KaleidScope","PANDORA BOXXX","project_raputa","完美挑战曲","Legend曲","KOP决赛曲","KOP预选追加曲"]

col5, col6 = st.columns([9,1])
with col5:
    st.title("请您越级")
with col6:
    st.text("")
    st.text("")
    if st.button("设置"):
        setting()
songs = list(range(0, 88))
col3, col4 = st.columns(2)
with col3:
    filter_level = st.multiselect("筛选定数",["14.6","14.7","14.8","14.9","15.0"])
    filter_version = st.multiselect("筛选版本",VERSION)
    filter_charter = st.multiselect("筛选谱师",CHARTER)
    filter_tag = st.multiselect("筛选标签",TAG)
with col4:
    condition_code = st.text_area("筛选其他", height=236, help="语法为 类别 运算符 数值 例如bpm>=180, released_date<2026-01-01, break==100")
    filter_name = st.text_input("搜索曲名")
VALID_KEY = ["bpm","released_date","break","tap","hold","slide","touch","total","version","internal_level"]
if condition_code:
    try:
        for index, line in enumerate(condition_code.split("\n")):
            line.replace(" ","")
            if not line:
                continue
            if ">=" in line:
                line = line.split(">=")
                if line[0] in VALID_KEY:
                    songs = find_all(line[0], ">=", line[1], songs)
                else:
                    raise KeyError(f"第{index + 1}行: {line[0]}")
            elif "<=" in line:
                line = line.split("<=")
                if line[0] in VALID_KEY:
                    songs = find_all(line[0], "<=", line[1], songs)
                else:
                    raise KeyError(f"第{index + 1}行: {line[0]}")
            elif "!=" in line:
                line = line.split("!=")
                if line[0] in VALID_KEY:
                    songs = find_all(line[0], "!=", line[1], songs)
                else:
                    raise KeyError(f"第{index + 1}行: {line[0]}")
            elif "==" in line:
                line = line.split("==")
                if line[0] in VALID_KEY:
                    songs = find_all(line[0], "==", line[1], songs)
                else:
                    raise KeyError(f"第{index + 1}行: {line[0]}")
            elif ">" in line:
                line = line.split(">")
                if line[0] in VALID_KEY:
                    songs = find_all(line[0], ">", line[1], songs)
                else:
                    raise KeyError(f"第{index + 1}行: {line[0]}")
            elif "<" in line:
                line = line.split("<")
                if line[0] in VALID_KEY:
                    songs = find_all(line[0], "<", line[1], songs)
                else:
                    raise KeyError(f"第{index + 1}行: {line[0]}")
            else:
                raise KeyError(f"第{index + 1}行: 没有符号")
    except Exception as e:
        st.error(e)
filter_level_list = []
filter_version_list = []
filter_charter_list = []
filter_tag_list = []
for level in filter_level:
    filter_level_list += find_all("internal_level","==",level)
for version in filter_version:
    filter_version_list += find_all("version","==",version)
for charter in filter_charter:
    for i in range(0,88):
        if charter in INFO[i]["designers"] and i not in filter_charter_list:
            filter_charter_list.append(i)
        elif charter == INFO[i]["note_designer"] and i not in filter_charter_list:
            filter_charter_list.append(i)
for tag in filter_tag:
    for i in range(0,88):
        if tag in INFO[i]["tag"] and i not in filter_tag_list:
            filter_tag_list.append(i)
songs = [
    s for s in songs
    if (not filter_level or s in filter_level_list)
    and (not filter_version or s in filter_version_list)
    and (not filter_charter or s in filter_charter_list)
    and (not filter_tag or s in filter_tag_list)
    and (not filter_name or filter_name.lower() in INFO[s]["title"].lower())]

col1, col2 = st.columns(2)
with col1:
    sort_method = st.selectbox("排序",["定数","bpm","版本","日期","tap","hold","slide","touch","break","物量"])
with col2:
    sort_reverse = st.selectbox("顺序",["倒序","正序"])
TRANSLATE = {"定数":"internal_level","bpm":"bpm","版本":"version","日期":"released_date","tap":"tap","hold":"hold",
             "slide":"slide","touch":"touch","break":"break","物量":"total","正序":False,"倒序":True}
songs = sort_by(TRANSLATE[sort_method],TRANSLATE[sort_reverse],songs)

col10, col11, col12, col13 = st.columns(4)
with col10:
    if st.button("随机抽取"):
        random_song(songs)
with col11  :
    if st.button("曲绘猜歌"):
        if songs:
            st.session_state.song = random.choice(songs)
        else:
            st.session_state.song = random.randint(0,87)
        st.session_state.x = random.randint(0, 190 - st.session_state.image_size)
        st.session_state.y = random.randint(0, 190 - st.session_state.image_size)
        random_cover(songs,st.session_state.image_size,st.session_state.grey)
with col12:
    if st.button("提示猜歌"):
        if songs:
            st.session_state.song = random.choice(songs)
        else:
            st.session_state.song = random.randint(0,87)
        st.session_state.description = ""
        st.session_state.description_target = ALL_TARGET.copy()
        random_info(songs)
try:
    print_all(songs)
except Exception as e:
    st.error(e)