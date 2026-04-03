import streamlit as st
import json
import streamlit.components.v1 as components

@st.cache_data
def load_data():
    with open("info.json", "r", encoding="utf-8") as f:
        return json.load(f)

ALL_TITLE = ['Xaleid◆scopiX Re:MASTER', '系ぎて Re:MASTER', 'PANDORA PARADOXXX Re:MASTER',
             '7 Wonders MASTER', 'Xaleid◆scopiX MASTER', "World's end BLACKBOX MASTER", '宙天 MASTER',
             'raputa MASTER', 'Latent Kingdom MASTER', "World's end loneliness MASTER", 'sølips MASTER',
             '躯樹の墓守 MASTER', 'PANDORA PARADOXXX MASTER', 'the EmpErroR Re:MASTER', 'Schwarzschild Re:MASTER',
             'QZKago Requiem Re:MASTER', 'False Amber (from the Black Bazaar, Or by A Kervan Trader from the Lands Afar, Or Buried Beneath the Shifting Sands That Lead Everywhere but Nowhere) MASTER',
             'Customized Justice MASTER', 'FLΛME/FRΦST MASTER', 'Divide et impera! MASTER', '氷滅の135小節 MASTER',
             'ℝ∈Χ LUNATiCA MASTER', 'Straight into the lights MASTER', 'VeRForTe αRtE:VEiN MASTER',
             'WiPE OUT MEMORIES MASTER', 'チューリングの跡 MASTER', 'Heavenly Blast MASTER', '封焔の135秒 MASTER',
             'the EmpErroR MASTER', '雷切-RAIKIRI- Re:MASTER', 'Alea jacta est! Re:MASTER', 'QZKago Requiem MASTER',
             '怒槌 MASTER', 'SILENT BLUE MASTER', 'larva MASTER', 'Excalibur ～Revived resolution～ MASTER',
             'Our Wrenally MASTER', 'Glorious Crown MASTER', 'Garakuta Doll Play Re:MASTER', 'In Chaos Re:MASTER',
             'Break The Speakers MASTER', 'Sky Trails MASTER', 'ATLAS RUSH MASTER', 'Re:Unknown X MASTER',
             '系ぎて MASTER', 'Apollo MASTER', 'KHYMΞXΛ MASTER', 'LAMIA MASTER', '康莊大道 MASTER', 'VIIIbit Explorer MASTER',
             'Metamorphosism MASTER', 'GIGANTØMAKHIA MASTER', 'Lia=Fail MASTER', 'Regulus MASTER', 'Valsqotch MASTER',
             'TEmPTaTiON MASTER', 'End Time MASTER', 'AMAZING MIGHTYYYY!!!! MASTER', 'ガラテアの螺旋 Re:MASTER',
             'VERTeX MASTER', '零號車輛 MASTER', 'ラストピースに祝福と栄光を MASTER', 'Get U ♭ack MASTER', 'Åntinomiε MASTER',
             '雨露霜雪 MASTER', 'Cryptarithm MASTER', 'IF:U MASTER', 'Λzure Vixen MASTER', '渦状銀河のシンフォニエッタ MASTER',
             '神威 MASTER', '超熊猫的周遊記（ワンダーパンダートラベラー） MASTER', 'VERTeX (rintaro soma deconstructed remix) MASTER',
             'ViRTUS MASTER', 'mystique as iris MASTER', 'Yorugao MASTER', 'BLACK SWAN MASTER', '脳天直撃 MASTER',
             'AMABIE MASTER', 'BREaK! BREaK! BREaK! MASTER', 'Titania MASTER', '雷切-RAIKIRI- MASTER',
             'TiamaT:F minor MASTER', 'Credits MASTER', 'Prophesy One MASTER', 'ガラテアの螺旋 MASTER', 'Fragrance Re:MASTER',
             'ジングルベル MASTER', '源平大戦絵巻テーマソング Re:MASTER']

st.title("谱面播放室")
INFO = load_data()
choose_chart = st.selectbox("选择谱面",ALL_TITLE)
choose_chart = ALL_TITLE.index(choose_chart)
if st.button("播放"):
    if "video" in INFO[choose_chart]:
        st.session_state.video_link = INFO[choose_chart]["video"]
if "video_link" in st.session_state and st.session_state.video_link:
    st.text(f"{st.session_state.video_link}")
    components.iframe(
        st.session_state.video_link,
        height=600
    )
else:
    st.error("这首歌还没搞好")

col1, col2 = st.columns([6,1])
with col2:
    if st.button("我不看了"):
        st.switch_page("main.py")