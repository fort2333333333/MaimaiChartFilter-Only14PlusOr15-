import json
import random
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from datetime import datetime, timedelta
from rapidfuzz import fuzz

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
    st.markdown(f"**{INFO[index]["title"]}**  *{INFO[index]["type"]}  {INFO[index]["difficulty"]}*  lv.*{INFO[index]["level"]}* (*{INFO[index]["internal_level"]}*)")
    st.markdown(f"曲师: *{INFO[index]["artist"]}*  bpm: *{INFO[index]["bpm"]}*")
    st.markdown(f"谱师: *{INFO[index]["note_designer"]}*")
    st.markdown(f"日期: *{INFO[index]["released_date"]}* (*{INFO[index]["version"]}*)")
    st.markdown(f"tap: *{INFO[index]["tap"]}*  hold: *{INFO[index]["hold"]}*  slide: *{INFO[index]["slide"]}*  touch: *{INFO[index]["touch"]}*  break: *{INFO[index]["break"]}*  total: *{INFO[index]["total"]}*")

def look_chart(video_link):
    st.session_state.video_link = video_link
    st.switch_page("pages/video.py")

def show_badges(items):
    colours = {"KaleidScope":"blue", "KOP决赛曲":"yellow", "Legend曲":"orange", "完美挑战曲":"violet",
                "project_raputa":"red", "PANDORA BOXXX":"gray", "KOP预选追加曲":"green"}
    badge_str = " ".join([
        f":{colours[item]}-badge[{item}]"
        for item in items
    ])
    st.markdown(badge_str)

def print_all(index_list):
    for index in index_list:
        col1, col2 = st.columns([1,2])
        with col1:
            print_cover(index)
            if st.button("谱面确认",key=index+1000):
                if "video" in INFO[index]:
                    look_chart(INFO[index]["video"])
                else:
                    st.error("没找到喵")
        with col2:
            print_info(index)
            show_badges(INFO[index]["tag"])

@st.dialog("随机歌曲")
def random_song(songs):
    if songs:
        song = random.choice(songs)
    else:
        song = random.randint(0,87)
    print_cover(song)
    print_info(song)
    st.button("再越一首")

def crop_cover(index,x,y, cropped_size,g=False,rotate=False):
    cover = Image.open(full_cover_path(INFO[index]["cover"]))
    cropped = cover.crop((x,y,x+cropped_size,y+cropped_size))
    if g:
        cropped = cropped.convert("L")
    if rotate != -1:
        cropped = cropped.rotate(rotate*90,expand=True)
    st.image(cropped,width=300)

ALL_TITLE = ['Xaleid◆scopiX', '系ぎて', 'PANDORA PARADOXXX', '7 Wonders', "World's end BLACKBOX",
             '宙天', 'raputa', 'Latent Kingdom', "World's end loneliness", 'sølips', '躯樹の墓守', 'the EmpErroR', 'Schwarzschild', 'QZKago Requiem',
             'False Amber (from the Black Bazaar, Or by A Kervan Trader from the Lands Afar, Or Buried Beneath the Shifting Sands That Lead Everywhere but Nowhere)',
             'Customized Justice', 'FLΛME/FRΦST', 'Divide et impera!', '氷滅の135小節', 'ℝ∈Χ LUNATiCA',
             'Straight into the lights', 'VeRForTe αRtE:VEiN', 'WiPE OUT MEMORIES', 'チューリングの跡',
             'Heavenly Blast', '封焔の135秒', '雷切-RAIKIRI-', 'Alea jacta est!',
             '怒槌', 'SILENT BLUE', 'larva', 'Excalibur ～Revived resolution～', 'Our Wrenally', 'Glorious Crown',
             'Garakuta Doll Play', 'In Chaos', 'Break The Speakers', 'Sky Trails', 'ATLAS RUSH', 'Re:Unknown X',
             'Apollo', 'KHYMΞXΛ', 'LAMIA', '康莊大道', 'VIIIbit Explorer', 'Metamorphosism', 'GIGANTØMAKHIA',
             'Lia=Fail', 'Regulus', 'Valsqotch', 'TEmPTaTiON', 'End Time', 'AMAZING MIGHTYYYY!!!!', 'ガラテアの螺旋',
             'VERTeX', '零號車輛', 'ラストピースに祝福と栄光を', 'Get U ♭ack', 'Åntinomiε', '雨露霜雪', 'Cryptarithm',
             'IF:U', 'Λzure Vixen', '渦状銀河のシンフォニエッタ', '神威', '超熊猫的周遊記（ワンダーパンダートラベラー）',
             'VERTeX (rintaro soma deconstructed remix)', 'ViRTUS', 'mystique as iris', 'Yorugao',
             'BLACK SWAN', '脳天直撃', 'AMABIE', 'BREaK! BREaK! BREaK!', 'Titania',
             'TiamaT:F minor', 'Credits', 'Prophesy One', 'Fragrance', 'ジングルベル', '源平大戦絵巻テーマソング']
ALL_ARTIST = ['xi', '削除', 't+pazolite', 'sasakure.UK', 'rintaro soma', 'kanone', 'かねこちはる', '打打だいず',
              'かめりあ', 'FANTAGIRAFF', '大国奏音', 'Frums', 'TJ.hangneil', 'Team Grimoire',
              't+pazolite vs かねこちはる', 'sasakure.UK × TJ.hangneil', 'Laur vs 大国奏音', '隣の庭は青い(庭師+Aoi)',
              'Tsukasa', 'Kobaryo', 'BlackY a.k.a. WAiKURO survive', 'Kai', 'Cosmograph', 'orangentle',
              'BlackY fused with WAiKURO', '光吉猛修', 'ガリガリさむし', 'Project Grimoire', 'Hiro「Crackin’DJ」',
              'DJ Myosuke', 'La prière', 'まらしぃ', 'のらねこさい feat.ricono', 'BlackY', 'Spiegel vs Yukino',
              'Lime', 'BlackYooh vs. siromaru', 'お月さま交響曲', 'owl＊tree feat.chi＊tree', 'Cres.', 'WAiKURO',
              'Hiro「maimai」より', 'seatrus', 'cosMo＠暴走P', 'Ryo Fukuda', 'ああ…翡翠茶漬け…',
              'かねこちはる vs t+pazolite', 'MisoilePunch♪', '山本真央樹', 'Hiro／rintaro soma', 'Hiro',
              'An & Ryunosuke Kudo', 'ぺのれり', '黒沢ダイスケ VS 穴山大輔', 'OSTER project',
              'HiTECH NINJA vs Cranky', 'vox2（小野秀幸）', 'Tsukasa(Arte Refact)', 'SEGA Sound Unit [H.]',
              '新小田夢童 ＆ キラ★ロッソ']

@st.dialog("曲绘猜歌")
def random_cover(songs,CROP_SIZE,grey,rotate):
    col101, col201 = st.columns([9,1])
    with col101:
        if st.button("再猜一首"):
            if songs:
                st.session_state.song = random.choice(songs)
            else:
                st.session_state.song = random.randint(0,87)
            st.session_state.x = random.randint(0,190-CROP_SIZE)
            st.session_state.y = random.randint(0,190-CROP_SIZE)
            st.session_state.r = random.randint(0,3)
            st.session_state.hint = ""
    with col201:
        st.image("static/image/icon/1.png")
    if not rotate:
        st.session_state.r = -1
    crop_cover(st.session_state.song,st.session_state.x,st.session_state.y,CROP_SIZE,grey,st.session_state.r)
    coll1, coll2, coll3 = st.columns([4,1,1])
    check_answer = 0
    with coll1:
        guess_title = st.selectbox("检查答案",ALL_TITLE)
        st.text("")
    with coll2:
        st.text("")
        if st.button("提交答案"):
            if guess_title == INFO[st.session_state.song]["title"]:
                check_answer = 1
            else:
                check_answer = 2
    with coll3:
        st.text("")
        if check_answer == 1:
            st.success(f"对喵")
        elif check_answer == 2:
            st.error(f"错喵")
    if st.button("来个提示"):
        if st.session_state.hint:
            st.warning(st.session_state.hint)
        else:
            st.session_state.hint = get_random_hint(st.session_state.song)
            st.warning(st.session_state.hint)
    if st.button("看看答案"):
        print_cover(st.session_state.song)

if "grey" not in st.session_state:
    st.session_state.grey = False
if "image_size" not in st.session_state:
    st.session_state.image_size = 30
if "after_rerun" not in st.session_state:
    st.session_state.after_rerun = ""
if "search_index" not in st.session_state:
    st.session_state.search_index = 80
if "random_target" not in st.session_state:
    st.session_state.random_target = False
if "random_rotate" not in st.session_state:
    st.session_state.random_rotate = False
if "colour_count" not in st.session_state:
    st.session_state.colour_count = 10

@st.dialog("设置")
def setting():
    setting_search_index = st.slider("搜索曲名:模糊搜索严格度(100=无模糊搜索)",min_value=60,max_value=100,value=st.session_state.search_index)
    setting_image_size = st.slider("曲绘猜歌:曲绘裁剪大小",min_value = 1,max_value = 100,value=st.session_state.image_size)
    setting_grey = st.toggle("曲绘猜歌:显示黑白曲绘",value=st.session_state.grey)
    setting_rotate = st.toggle("曲绘猜歌:随机翻转",value=st.session_state.random_rotate)
    setting_colour = st.slider("颜色猜歌:颜色数量",min_value=1,max_value=20,value=st.session_state.colour_count)
    if st.button("保存"):
        st.session_state.search_index = setting_search_index
        st.session_state.image_size = setting_image_size
        st.session_state.grey = setting_grey
        st.session_state.random_rotate = setting_rotate
        st.session_state.colour_count = setting_colour
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

def get_random_value(key):
    return random.choice(INFO)[key]

def get_random_hint(song):
    if "完美挑战曲" in INFO[song]["tag"]:
        target = random.randint(0,2)
    else:
        target = random.randint(0,1)
    if target == 0:
        if INFO[song]["type"] == "STD":
            return "这歌是旧框的"
        elif VERSION.index(INFO[song]["version"]) < VERSION.index("BUDDiES"):
            return "这歌是DX代的但是在BUDDiES前"
        else:
            return "这歌在FESTiVAL PLUS之后"
    elif target == 1:
        if INFO[song]["internal_level"] < "14.8":
            return "这歌定数不到14.8"
        else:
            return "这歌定数在14.7之上"
    elif target == 2:
        return "这歌是完美挑战曲"
    return "卡bug了"


DESC_DESIGNER = ["Luxizhel","シチミヘルツ","Jack","翠楼屋","サファ太","鳩ホルダー"]
DESC_LEVEL = ["14.6","14.7","14.8","14.9","15.0"]
DESC_TAG = ["KaleidScope","PANDORA BOXXX","project_raputa","完美挑战曲","Legend曲","KOP决赛曲","KOP预选追加曲"]
def random_description(song,target,value=None):
    if target == "designers":
        target_designer = random.choice(DESC_DESIGNER) if value == None else value
        if target_designer in INFO[song]["designers"]:
            return f"谱师是{target_designer}"
        else:
            return f"谱师不是{target_designer}"
    elif target == "internal_level":
        target_level = get_random_value("internal_level") if value == None else value
        if INFO[song]["internal_level"] > target_level:
            return f"定数大于{target_level}"
        elif INFO[song]["internal_level"] < target_level:
            return f"定数小于{target_level}"
        else:
            return f"定数是{target_level}"
    elif target == "version":
        target_version = get_random_value("version") if value == None else value
        if condition(INFO[song]["version"],"version",">",target_version):
            return f"版本在{target_version}后"
        elif condition(INFO[song]["version"],"version","<",target_version):
            return f"版本在{target_version}前"
        else:
            return f"版本是{target_version}"
    elif target == "tag":
        target_tag = random.choice(DESC_TAG) if value == None else value
        if target_tag in INFO[song]["tag"]:
            return f"曲子是{target_tag}"
        else:
            return f"曲子不是{target_tag}"
    elif target == "break":
        target_break = int(get_random_value("break")) if value == None else value
        if int(INFO[song]["break"]) > target_break:
            return f"绝赞大于{target_break}"
        elif int(INFO[song]["break"]) < target_break:
            return f"绝赞小于{target_break}"
        else:
            return f"绝赞等于{target_break}"
    elif target == "type":
        return f"曲子是{INFO[song]["type"]}曲"
    elif target == "bpm":
        target_bpm = int(get_random_value("bpm")) if value == None else value
        if int(INFO[song]["bpm"]) > target_bpm:
            return f"bpm大于{target_bpm}"
        elif int(INFO[song]["bpm"]) < target_bpm:
            return f"bpm小于{target_bpm}"
        else:
            return f"bpm等于{target_bpm}"
    elif target == "total":
        target_total = int(get_random_value("total")) if value == None else value
        if int(INFO[song]["total"]) > target_total:
            return f"物量大于{target_total}"
        elif int(INFO[song]["total"]) < target_total:
            return f"物量小于{target_total}"
        else:
            return f"物量等于{target_total}"
    elif target == "difficulty":
        return f"难度是{INFO[song]["difficulty"]}"
    elif target == "released_date":
        target_date = random_date() if value == None else value
        if target_date < INFO[song]["released_date"]:
            return f"在{target_date}后加入"
        elif target_date > INFO[song]["released_date"]:
            return f"在{target_date}前加入"
        else:
            return f"在{target_date}加入"
    elif target in ["tap","hold","slide","touch"]:
        target_count = value
        if int(INFO[song][target]) > target_count:
            return f"{target}比{target_count}多"
        elif int(INFO[song][target]) < target_count:
            return f"{target}比{target_count}少"
        else:
            return f"{target}是{target_count}"
    elif target == "title":
        target_title = value
        if INFO[song]["title"] == target_title:
            return f"是{target_title}"
        else:
            return f"不是{target_title}"
    elif target == "artist":
        target_artist = value
        if INFO[song]["artist"] == target_artist:
            return f"曲师是{target_artist}"
        else:
            return f"曲师不是{target_artist}"
    return f"卡bug了"

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

ALL_TARGET = ["designers","internal_level","version","tag","break","type","bpm","total","difficulty"]
ALL_TARGET_2 = ["designers","internal_level","version","tag","break","bpm","total"]
USER_TARGET_CHOICE = ["类型","难度","谱师","定数","版本","系列","绝赞","bpm","物量","曲师","标题","日期","tap","hold","slide","touch"]
USER_TARGET_TRANS = {"谱师":"designers","定数":"internal_level","版本":"version","系列":"tag","绝赞":"break",
                     "类型":"type","bpm":"bpm","物量":"total","难度":"difficulty","tap":"tap","hold":"hold",
                     "slide":"slide","touch":"touch","日期":"released_date","标题":"title","曲师":"artist"}
@st.dialog("提示猜歌")
def random_info(songs):
    col301, col401 = st.columns([9,1])
    with col301:
        if st.button("再猜一首"):
            if songs:
                st.session_state.song = random.choice(songs)
            else:
                st.session_state.song = random.randint(0, 87)
            st.session_state.description = ""
            st.session_state.description_target = ALL_TARGET.copy()
    with col401:
        st.image(r"static/image/icon/1.png")
    if st.session_state.random_target:
        if st.session_state.description_target == ALL_TARGET:
            st.session_state.description += ("\n" + random_description(st.session_state.song,st.session_state.description_target.pop(random.randint(0,len(st.session_state.description_target) - 1))))
        if st.button("继续提示"):
            if st.session_state.description_target:
                st.session_state.description += ("\n"+random_description(st.session_state.song,st.session_state.description_target.pop(random.randint(0,len(st.session_state.description_target)-1))))
            else:
                st.session_state.description_target = ALL_TARGET_2.copy()
                st.session_state.description += ("\n" + random_description(st.session_state.song,st.session_state.description_target.pop(random.randint(0,len(st.session_state.description_target) - 1))))
    else:
        col33, col34 = st.columns(2)
        with col33:
            user_target = st.selectbox("筛选问题",USER_TARGET_CHOICE)
        with col34:
            if user_target == "谱师":
                USER_VALUE_CHOICE = CHARTER.copy()
                user_value = st.selectbox("谱面谁写的",USER_VALUE_CHOICE)
            elif user_target == "定数":
                USER_VALUE_CHOICE = ["14.6","14.7","14.8","14.9","15.0"]
                user_value = st.selectbox("定数是什么", USER_VALUE_CHOICE)
            elif user_target == "版本":
                USER_VALUE_CHOICE = VERSION.copy()
                user_value = st.selectbox("何版本", USER_VALUE_CHOICE)
            elif user_target == "系列":
                USER_VALUE_CHOICE = TAG.copy()
                user_value = st.selectbox("啥系列", USER_VALUE_CHOICE)
            elif user_target == "绝赞":
                user_value = st.slider("绝赞数",min_value=2,max_value=222)
            elif user_target == "类型":
                user_value = st.selectbox("什么类型",["STD","DX"])
            elif user_target == "bpm":
                user_value = st.slider("bpm多少",min_value=88,max_value=339)
            elif user_target == "物量":
                user_value = st.slider("物量多少",min_value=655,max_value=2222)
            elif user_target == "难度":
                user_value = st.selectbox("哪个难度",["BASIC","ADVANCED","EXPERT","MASTER","Re:MASTER"])
            elif user_target == "tap":
                user_value = st.slider("tap数",min_value=1590,max_value=377)
            elif user_target == "hold":
                user_value = st.slider("hold数",min_value=0,max_value=173)
            elif user_target == "slide":
                user_value = st.slider("slide数",min_value=1,max_value=211)
            elif user_target == "touch":
                user_value = st.slider("touch数",min_value=0,max_value=302)
            elif user_target == "日期":
                user_value = str(st.date_input("追加日期"))
            elif user_target == "标题":
                user_value = st.selectbox("曲子叫什么",ALL_TITLE)
            elif user_target == "曲师":
                user_value = st.selectbox("曲师是谁(没那么智能)",ALL_ARTIST)
            else:
                USER_VALUE_CHOICE = ["卡BUG了"]
                user_value = st.selectbox("问个问题", USER_VALUE_CHOICE)
        if st.button("那我问你"):
            st.session_state.description += ("\n" + random_description(st.session_state.song,USER_TARGET_TRANS[user_target],user_value))
    if st.session_state.description:
        st.text(st.session_state.description)
    else:
        st.text("(问个问题获取提示)")
    if st.button("到底是什么"):
        col111, col222 = st.columns([1,2])
        with col111:
            print_cover(st.session_state.song)
            show_badges(INFO[st.session_state.song]["tag"])
        with col222:
            print_info(st.session_state.song)

if st.session_state.after_rerun:
    st.toast(st.session_state.after_rerun)
    st.session_state.after_rerun = ""

@st.dialog("颜色猜歌")
def random_colours(songs):
    col999, col998 = st.columns([9,1])
    with col999:
        if st.button("再来一首"):
            if songs:
                st.session_state.song = random.choice(songs)
            else:
                st.session_state.song = random.randint(0,87)
            st.session_state.xx = [random.randint(0, 189) for j in range(st.session_state.colour_count)]
            st.session_state.yy = [random.randint(0, 189) for j in range(st.session_state.colour_count)]
            st.session_state.hint = ""
    with col998:
        st.image("static/image/icon/1.png")
    colc1, colc2, colc3, colc4, colc5 = st.columns(5)
    for j in range(st.session_state.colour_count):
        if j%5 == 0:
            with colc1:
                crop_cover(st.session_state.song,st.session_state.xx[j],st.session_state.yy[j],1)
        if j%5 == 1:
            with colc2:
                crop_cover(st.session_state.song,st.session_state.xx[j],st.session_state.yy[j],1)
        if j%5 == 2:
            with colc3:
                crop_cover(st.session_state.song,st.session_state.xx[j],st.session_state.yy[j],1)
        if j%5 == 3:
            with colc4:
                crop_cover(st.session_state.song,st.session_state.xx[j],st.session_state.yy[j],1)
        if j%5 == 4:
            with colc5:
                crop_cover(st.session_state.song,st.session_state.xx[j],st.session_state.yy[j],1)

    colll1, colll2, colll3 = st.columns([4, 1, 1])
    check_answer = 0
    with colll1:
        guess_title = st.selectbox("检查答案", ALL_TITLE)
        st.text("")
    with colll2:
        st.text("")
        if st.button("提交答案"):
            if guess_title == INFO[st.session_state.song]["title"]:
                check_answer = 1
            else:
                check_answer = 2
    with colll3:
        st.text("")
        if check_answer == 1:
            st.success(f"对喵")
        elif check_answer == 2:
            st.error(f"错喵")
    if st.button("来个提示"):
        if st.session_state.hint:
            st.warning(st.session_state.hint)
        else:
            st.session_state.hint = get_random_hint(st.session_state.song)
            st.warning(st.session_state.hint)
    if st.button("看看答案"):
        print_cover(st.session_state.song)


def match_song(song_name: str, query: str, threshold: int = 60) -> bool:
    song = song_name.lower()
    q = query.lower()
    if q in song:
        return True
    score = fuzz.partial_ratio(q, song)
    return score >= threshold

#temp = []
#for s in INFO:
#    temp.append(f"{s["title"]} {s["difficulty"]}")
#st.text(temp)

st.caption("(使用电脑或者横屏访问以获得最佳体验)")
col5, col6, coll = st.columns([3,6,1])
with col5:
    st.title("请您越级")
with coll:
    st.text("")
    st.text("")
    if st.button("设置"):
        setting()
with col6:
    st.image(r"static/image/icon/0.png",width=80)
songs = list(range(0, 88))
col3, col4 = st.columns(2)
with col3:
    filter_level = st.multiselect("筛选定数",["14.6","14.7","14.8","14.9","15.0"])
    filter_version = st.multiselect("筛选版本",VERSION)
    filter_charter = st.multiselect("筛选谱师",CHARTER)
    filter_tag = st.multiselect("筛选系列",TAG)
with col4:
    condition_code = st.text_area("筛选其他", height=236, help="语法为 类别 运算符 数值 例如bpm>=180, released_date<2026-01-01, break==100")
    filter_name = st.text_input("搜索曲名(曲师)")
VALID_KEY = ["bpm","released_date","break","tap","hold","slide","touch","total","version","internal_level","type"]
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
    and (not filter_name or (match_song(INFO[s]["title"],filter_name,st.session_state.search_index) or match_song(INFO[s]["artist"],filter_name,st.session_state.search_index)))]

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
with col11:
    if st.button("曲绘猜歌"):
        if songs:
            st.session_state.song = random.choice(songs)
        else:
            st.session_state.song = random.randint(0,87)
        st.session_state.x = random.randint(0, 190 - st.session_state.image_size)
        st.session_state.y = random.randint(0, 190 - st.session_state.image_size)
        st.session_state.r = random.randint(0,3)
        st.session_state.hint = ""
        random_cover(songs,st.session_state.image_size,st.session_state.grey,st.session_state.random_rotate)
with col12:
    if st.button("颜色猜歌"):
        if songs:
            st.session_state.song = random.choice(songs)
        else:
            st.session_state.song = random.randint(0,87)
        st.session_state.xx = [random.randint(0, 189) for i in range(st.session_state.colour_count)]
        st.session_state.yy = [random.randint(0, 189) for i in range(st.session_state.colour_count)]
        st.session_state.hint = ""
        random_colours(songs)
with col13:
    if st.button("提示猜歌"):
        if songs:
            st.session_state.song = random.choice(songs)
        else:
            st.session_state.song = random.randint(0,87)
        st.session_state.description = ""
        st.session_state.description_target = ALL_TARGET.copy()
        random_info(songs)
try:
    st.divider()
    if songs:
        st.caption(f"找到了:green[{len(songs)}]个谱面")
    else:
        st.caption("找到了:red[0]个谱面")
    print_all(songs)
except Exception as e:
    st.error(e)