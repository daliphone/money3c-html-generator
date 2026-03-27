import streamlit as st

st.set_page_config(page_title="文章目錄 HTML 產生器", layout="wide")

st.title("📑 官網文章目錄 HTML 產生器")
st.write("適用馬尼通訊官網 CKEditor 編輯器，搭配編輯器內建錨點（旗幟）功能使用。")

# --- 輸入區塊 ---
intro_text = st.text_area("一、請輸入文章前言", "手機保險買哪家最好？本文將為您深入解析...")

st.markdown("### 二、請設定目錄樣式")
col_style1, col_style2 = st.columns(2)

with col_style1:
    has_border = st.checkbox("✅ 目錄需要外框線 (border)", value=True)
    font_size = st.slider("🔠 目錄字體大小 (px)", min_value=12, max_value=24, value=14)

with col_style2:
    spacing = st.slider("↕️ 目錄行距大小 (px)", min_value=0, max_value=30, value=8)

st.info("💡 提示：每行輸入一個標題。小標題請在開頭加上減號 `-`（例如：`- 手機險推薦品牌 1：馬尼通訊`）。")
outline_text = st.text_area(
    "三、請輸入文章大綱",
    "一、手機保險需要嗎？\n二、iPhone 手機保險怎麼選？\n三、手機保險比較：8 家品牌方案\n- 手機險推薦品牌 1：馬尼通訊\n- 手機險推薦品牌 2：Apple\n四、常見問題解答",
    height=150
)

# --- 處理與產生按鈕 ---
if st.button("🚀 產生 HTML 原始碼與操作說明", type="primary"):
    lines = outline_text.strip().split('\n')
    items = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        is_sub = line.startswith('-')
        title = line[1:].strip() if is_sub else line
        items.append({"title": title, "is_sub": is_sub, "id": str(len(items) + 1)})

    if has_border:
        table_attr = 'style="width: 100%;" border="1" cellspacing="1" cellpadding="1"'
    else:
        table_attr = 'style="width: 100%;" border="0" cellspacing="0" cellpadding="0"'

    # --- 產生目錄 HTML ---
    toc_html = f'<p><span style="font-size:{font_size}px">{intro_text}</span></p>\n<p>&nbsp;</p>\n'
    toc_html += (
        f'<table {table_attr}>\n\t<tbody>\n\t\t<tr>\n\t\t\t<td>\n'
        f'\t\t\t<p style="margin-bottom: {spacing}px;"><span style="font-size:{font_size}px">目錄：</span></p>\n'
        f'\t\t\t</td>\n\t\t</tr>\n\t\t<tr>\n\t\t\t<td>\n'
    )
    for item in items:
        indent = '&nbsp;&nbsp;&nbsp;&nbsp;' if item['is_sub'] else ''
        toc_html += (
            f'\t\t\t<p style="margin-bottom: {spacing}px;">'
            f'<span style="font-size:{font_size}px">{indent}'
            f'<a href="#{item["id"]}">{item["title"]}</a></span></p>\n'
        )
    toc_html += '\t\t\t</td>\n\t\t</tr>\n\t</tbody>\n</table>\n<p>&nbsp;</p>'

    # --- 產生內文標題 HTML（不含錨點，由編輯器手動插入）---
    content_html = ""
    for item in items:
        tag = "h3" if item['is_sub'] else "h2"
        content_html += (
            f'<p>&nbsp;</p>\n'
            f'<{tag}><strong>{item["title"]}</strong></{tag}>\n'
            f'<p>（請在此輸入【{item["title"]}】的內文...）</p>\n'
            f'<p>&nbsp;</p>\n'
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👀 實際預覽效果")
        full_preview_html = toc_html + content_html
        st.markdown(
            f'<div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; '
            f'background-color: #fafafa; color: #333;">{full_preview_html}</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.subheader("✅ HTML 原始碼")
        st.success("🎉 產生成功！依照下方步驟操作。")
        st.markdown("**1️⃣ 目錄區塊（貼在文章最上方）**")
        st.code(toc_html, language='html')
        st.markdown("**2️⃣ 內文標題架構（貼在目錄下方）**")
        st.code(content_html, language='html')

    # --- 操作說明 ---
    st.divider()
    st.subheader("📋 錨點設定操作步驟")
    st.warning("⚠️ 官網編輯器會過濾 style 屬性，錨點必須用編輯器內建的旗幟功能手動插入，不可直接寫在 HTML 裡。")

    st.markdown("""
**整體流程：**
1. 將「目錄區塊」HTML 貼入編輯器原始碼模式，放在文章最上方
2. 將「內文標題架構」HTML 貼入，放在目錄下方
3. 依照下方各標題的說明，在**上一個區塊的結尾**插入對應的錨點旗幟
4. 儲存後點目錄連結測試跳轉位置
""")

    st.markdown("**各標題錨點位置說明：**")

    for i, item in enumerate(items):
        tag_label = "小標題 h3" if item['is_sub'] else "大標題 h2"
        if i == 0:
            prev_desc = "目錄表格的最後一行（表格內最後一個連結之後）"
        else:
            prev_title = items[i-1]['title']
            prev_desc = f"「{prev_title}」區塊的內文最後一行結尾"

        st.markdown(f"""---
**🚩 錨點 `{item['id']}`　{tag_label}：{item['title']}**
- 游標移到：{prev_desc}
- 點工具列旗幟圖示，錨點名稱填：`{item['id']}`
""")

    st.markdown("---")
    st.info("💡 跳轉後如果標題還是被導覽列遮住一點，在錨點旗幟前多加一個空白段落 `<p>&nbsp;</p>` 補足距離。")
