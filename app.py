import streamlit as st

st.set_page_config(page_title="文章目錄 HTML 產生器", layout="wide")

st.title("📑 官網文章目錄 HTML 產生器 (精準錨點偏移版)")
st.write("利用 `padding-top` + `margin-top` 的 inline 樣式，精準抵消導覽列遮擋，不依賴不穩定的空白行！")

# --- 輸入區塊 ---
intro_text = st.text_area("一、請輸入文章前言", "手機保險買哪家最好？本文將為您深入解析...")

st.markdown("### 二、請設定目錄樣式")
col_style1, col_style2 = st.columns(2)

with col_style1:
    has_border = st.checkbox("✅ 目錄需要外框線 (border)", value=True)
    font_size = st.slider("🔠 目錄字體大小 (px)", min_value=12, max_value=24, value=14)

with col_style2:
    spacing = st.slider("↕️ 目錄行距大小 (px)", min_value=0, max_value=30, value=8)
    nav_height = st.slider(
        "🛡️ 導覽列高度 (px)",
        min_value=40,
        max_value=150,
        value=80,
        step=5,
        help="輸入你的網站固定導覽列高度（px）。錨點會自動往下偏移這個距離，讓標題完整顯示在導覽列下方。"
    )

st.info("💡 提示：每行輸入一個標題。如果是「小標題」，請在該行開頭加上一個減號 `-` (例如：`- 手機險推薦品牌 1：馬尼通訊`)。")
outline_text = st.text_area(
    "三、請輸入文章大綱",
    "一、手機保險需要嗎？\n二、iPhone 手機保險怎麼選？\n三、手機保險比較：8 家品牌方案\n- 手機險推薦品牌 1：馬尼通訊\n- 手機險推薦品牌 2：Apple\n四、常見問題解答",
    height=150
)

# --- 說明原理 ---
with st.expander("🔍 為什麼這個方法比「空白行」更可靠？"):
    st.markdown(f"""
**舊方法：插入空白行**  
空白行的實際高度取決於字體大小、行高、裝置解析度等，**每個環境都不同**，難以精準對齊。

**新方法：`padding-top` + `margin-top` inline 樣式**  
直接把導覽列高度（目前設定：`{nav_height}px`）寫進錨點元素的 style 裡：

```html
<p id="1" style="padding-top: {nav_height}px; margin-top: -{nav_height}px; display: block;">&nbsp;</p>
```

- `padding-top: {nav_height}px` → 讓瀏覽器跳錨點時，停在導覽列下方 {nav_height}px 處  
- `margin-top: -{nav_height}px` → 把多出來的空間往回收，**視覺上不產生額外空隙**  
- `display: block` → 確保偏移樣式生效（部分編輯器預設 `<p>` 為 inline 會失效）

這個方法即使 `<style>` 標籤被過濾掉，因為是 inline style 也完全有效。
""")

# --- 處理與產生按鈕 ---
if st.button("🚀 產生 HTML 原始碼與預覽", type="primary"):
    lines = outline_text.strip().split('\n')

    if has_border:
        table_attr = 'style="width: 100%;" border="1" cellspacing="1" cellpadding="1"'
    else:
        table_attr = 'style="width: 100%;" border="0" cellspacing="0" cellpadding="0"'

    # 錨點偏移 inline style（核心技巧）
    anchor_style = f'style="padding-top: {nav_height}px; margin-top: -{nav_height}px; display: block;"'

    toc_html = f'<p><span style="font-size:{font_size}px">{intro_text}</span></p>\n<p>&nbsp;</p>\n'
    toc_html += (
        f'<table {table_attr}>\n\t<tbody>\n\t\t<tr>\n\t\t\t<td>\n'
        f'\t\t\t<p style="margin-bottom: {spacing}px;"><span style="font-size:{font_size}px">目錄：</span></p>\n'
        f'\t\t\t</td>\n\t\t</tr>\n\t\t<tr>\n\t\t\t<td>\n'
    )

    content_html = ""
    counter = 1

    for line in lines:
        line = line.strip()
        if not line:
            continue

        anchor_id = f"{counter}"

        if line.startswith('-'):
            title = line[1:].strip()
            toc_html += (
                f'\t\t\t<p style="margin-bottom: {spacing}px;">'
                f'<span style="font-size:{font_size}px">&nbsp;&nbsp;&nbsp;&nbsp;'
                f'<a href="#{anchor_id}">{title}</a></span></p>\n'
            )
            # 錨點直接用 inline padding-top / margin-top 偏移，不用空白行
            content_html += (
                f'<p id="{anchor_id}" {anchor_style}>&nbsp;</p>\n'
                f'<h3><strong>{title}</strong></h3>\n'
                f'<p>（請在此輸入【{title}】的內文...）</p>\n'
                f'<p>&nbsp;</p>\n'
            )
        else:
            title = line
            toc_html += (
                f'\t\t\t<p style="margin-bottom: {spacing}px;">'
                f'<span style="font-size:{font_size}px">'
                f'<a href="#{anchor_id}">{title}</a></span></p>\n'
            )
            content_html += (
                f'<p id="{anchor_id}" {anchor_style}>&nbsp;</p>\n'
                f'<h2><strong>{title}</strong></h2>\n'
                f'<p>（請在此輸入【{title}】的內文...）</p>\n'
                f'<p>&nbsp;</p>\n'
            )

        counter += 1

    toc_html += '\t\t\t</td>\n\t\t</tr>\n\t</tbody>\n</table>\n<p>&nbsp;</p>'

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👀 實際預覽效果")
        st.info(f"💡 預覽中導覽列高度設定為 {nav_height}px。錨點偏移已套用，不會產生明顯額外空隙。")
        full_preview_html = toc_html + content_html
        st.markdown(
            f'<div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; '
            f'background-color: #fafafa; color: #333;">{full_preview_html}</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.subheader("✅ HTML 原始碼")
        st.success("🎉 產生成功！請點擊右上角複製圖示，貼上至官網編輯器中。")
        st.markdown("**1️⃣ 目錄區塊 (放在文章最上方)**")
        st.code(toc_html, language='html')
        st.markdown("**2️⃣ 內文標題架構 (放在目錄下方)**")
        st.code(content_html, language='html')

        # 顯示單一錨點的說明，讓使用者能快速理解
        st.markdown("---")
        st.markdown("**📌 錨點原理速查**")
        st.code(
            f'<!-- 每個錨點都是這個結構 -->\n'
            f'<p id="1" style="padding-top: {nav_height}px; margin-top: -{nav_height}px; display: block;">&nbsp;</p>\n'
            f'<h2><strong>標題文字</strong></h2>',
            language='html'
        )
        st.caption(f"導覽列高度 = {nav_height}px。如果跳轉後標題還是被遮住，請把數值調大；如果標題顯示位置太低，請調小。")
