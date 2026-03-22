import json
import random
import streamlit as st

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
    st.text(f"曲师: {INFO[index]["artist"]}")
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
        st.button("再来一首")
    else:
        st.image("static/image/cover/-1.jpg")
        st.text("鍠滄�㈣糠浣犱笘鐣� 浣犳槸 杩欎釜 lv.浠�涔� (鎯冲共.鍟�)")
        st.text("鏇插笀: 杩欐槸璋� 脳 鏄�涓�浜虹墿")
        st.text("璋卞笀: 涓嶆槸涔濋笩")
        st.text("鏃ユ湡: 鍝堝搱-涓栫晫-浣犲ソ (鍢诲樆)")
        st.text("瀹炲湪: 缂栦笉涓�  鍘讳簡: 鎵�浠� 鍒板簳鍐�: 浠� 涔堝ソ鍛�:閿� 鏂ゆ嫹: 锟斤拷�� 鎯冲悆: 閿熸枻鎷�")

st.title("请您越级")
songs = list(range(0, 88))
col3, col4 = st.columns(2)
with col3:
    filter_level = st.multiselect("筛选定数",["14.6","14.7","14.8","14.9","15.0"])
    filter_version = st.multiselect("筛选版本",VERSION)
filter_level_list = []
filter_version_list = []
for level in filter_level:
    filter_level_list += find_all("internal_level","==",level)
for version in filter_version:
    filter_version_list += find_all("version","==",version)
songs = [
    s for s in songs
    if (not filter_level or s in filter_level_list)
    and (not filter_version or s in filter_version_list)]

with col4:
    condition_code = st.text_area("筛选其他", height=153, help="语法为 类别 运算符 数值 例如bpm>180, released_date<2026-01-01, break==100")
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

col1, col2 = st.columns(2)
with col1:
    sort_method = st.selectbox("排序",["定数","bpm","版本","日期","tap","hold","slide","touch","break","物量"])
with col2:
    sort_reverse = st.selectbox("顺序",["倒序","正序"])
TRANSLATE = {"定数":"internal_level","bpm":"bpm","版本":"version","日期":"released_date","tap":"tap","hold":"hold",
             "slide":"slide","touch":"touch","break":"break","物量":"total","正序":False,"倒序":True}
songs = sort_by(TRANSLATE[sort_method],TRANSLATE[sort_reverse],songs)

if st.button("随机抽取"):
    random_song(songs)
try:
    print_all(songs)
except Exception as e:
    st.error(e)