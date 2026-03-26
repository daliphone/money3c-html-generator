import streamlit as st

st.set_page_config(page_title="文章目錄 HTML 產生器", layout="wide")

st.title("📑 官網文章目錄 HTML 產生器 (純物理防護版)")
st.write("利用插入「隱形空白行」的方式，徹底解決導覽列遮擋與編輯器過濾 CSS 的問題！")

# --- 輸入區塊 ---
intro_text = st.text_area("一、請輸入文章前言", "手機保險買哪家最好？本文將為您深入解析...")

st.markdown("### 二、請設定目錄樣式")
col_style1, col_style2 = st.columns(2)

with col_style1:
    has_border = st.checkbox("✅ 目錄需要外框線 (border)", value=True)
    font_size = st.slider("🔠 目錄字體大小 (px)", min_value=12, max_value=24, value=14)

with col_style2:
    spacing = st.slider("↕️ 目錄行距大小 (px)", min_value=0, max_value=30, value=8)
    # 【全新防禦機制】改為插入空白行數量
    buffer_lines = st.slider("🛡️ 導覽列防遮擋：插入空白行數", min_value=1, max_value=5, value=2, help="在標題上方安插空白行來承受導覽列的遮擋。通常 2 到 3 行就足夠。")

st.info("💡 提示：每行輸入一個標題。如果是「小標題」，請在該行開頭加上一個減號 `-` (例如：`- 手機險推薦品牌 1：馬尼通訊`)。")
outline_text = st.text_area(
    "三、請輸入文章大綱", 
    "一、手機保險需要嗎？\n二、iPhone 手機保險怎麼選？\n三、手機保險比較：8 家品牌方案\n- 手機險推薦品牌 1：馬尼通訊\n- 手機險推薦品牌 2：Apple\n四、常見問題解答", 
    height=150
)

# --- 處理與產生按鈕 ---
if st.button("🚀 產生 HTML 原始碼與預覽", type="primary"):
    lines = outline_text.strip().split('\n')
    
    if has_border:
        table_attr = 'style="width: 100%;" border="1" cellspacing="1" cellpadding="1"'
    else:
        table_attr = 'style="width: 100%;" border="0" cellspacing="0" cellpadding="0"'

    toc_html = f'<p><span style="font-size:{font_size}px">{intro_text}</span></p>\n<p>&nbsp;</p>\n'
    toc_html += f'<table {table_attr}>\n\t<tbody>\n\t\t<tr>\n\t\t\t<td>\n\t\t\t<p style="margin-bottom: {spacing}px;"><span style="font-size:{font_size}px">目錄：</span></p>\n\t\t\t</td>\n\t\t</tr>\n\t\t<tr>\n\t\t\t<td>\n'
    
    content_html = ""
    counter = 1

    # 產生空白緩衝行的 HTML
    buffer_html = '<p>&nbsp;</p>\n' * buffer_lines

    for line in lines:
        line = line.strip()
        if not line: 
            continue

        anchor_id = f"{counter}" 

        if line.startswith('-'):
            title = line[1:].strip()
            toc_html += f'\t\t\t<p style="margin-bottom: {spacing}px;"><span style="font-size:{font_size}px">&nbsp;&nbsp;&nbsp;&nbsp;<a href="#{anchor_id}">{title}</a></span></p>\n'
            
            # 【關鍵修改】ID 綁在最上方的空段落，接著插入空白行，最後才是真正的標題
            content_html += f'<p id="{anchor_id}">&nbsp;</p>\n'
            content_html += buffer_html
            content_html += f'<h3><strong>{title}</strong></h3>\n<p>（請在此輸入【{title}】的內文...）</p>\n<p>&nbsp;</p>\n'
        else:
            title = line
            toc_html += f'\t\t\t<p style="margin-bottom: {spacing}px;"><span style="font-size:{font_size}px"><a href="#{anchor_id}">{title}</a></span></p>\n'
            
            # 【關鍵修改】ID 綁在最上方的空段落，接著插入空白行，最後才是真正的標題
            content_html += f'<p id="{anchor_id}">&nbsp;</p>\n'
            content_html += buffer_html
            content_html += f'<h2><strong>{title}</strong></h2>\n<p>（請在此輸入【{title}】的內文...）</p>\n<p>&nbsp;</p>\n'

        counter += 1

    toc_html += '\t\t\t</td>\n\t\t</tr>\n\t</tbody>\n</table>\n<p>&nbsp;</p>'

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👀 實際預覽效果")
        st.info("💡 這是模擬在網頁上顯示的視覺效果。段落之間會有明顯的空白，這是為了抵抗導覽列遮擋的設計。")
        full_preview_html = toc_html + content_html
        st.markdown(f'<div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; background-color: #fafafa; color: #333;">{full_preview_html}</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("✅ HTML 原始碼")
        st.success("🎉 產生成功！請點擊右上角複製圖示，貼上至官網編輯器中。")
        st.markdown("**1️⃣ 目錄區塊 (放在文章最上方)**")
        st.code(toc_html, language='html')
        st.markdown("**2️⃣ 內文標題架構 (放在目錄下方)**")
        st.code(content_html, language='html')
