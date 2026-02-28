import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 1. 网页标题和说明 (你可以在这里随意修改文字)
st.set_page_config(page_title="AI 鹰眼 - 网站 AI 友好度体检", page_icon="🦅")
st.title("🦅 AI 鹰眼：你的网站能被大模型搜到吗？")
st.markdown("输入你的网址，一键检测网站的 **AI 友好度 (GEO)** 评分！")

# 2. 输入框和按钮
url_input = st.text_input("🔗 请输入要测试的网址 (需包含 http:// 或 https://):", "https://www.apple.com.cn/")
submit_button = st.button("🚀 立即免费体检")

# 3. 当用户点击按钮后发生的事情
if submit_button:
    if not url_input.startswith("http"):
        st.error("❌ 网址格式不对哦，请加上 http:// 或 https://")
    else:
        with st.spinner('🕸️ 正在模拟 AI 爬虫扫描中，请稍候...'):
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            try:
                # 获取网页内容
                response = requests.get(url_input, headers=headers, timeout=10)
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                
                st.subheader("📊 你的专属体检报告")
                
                # --- 指标一：骨架清晰度 ---
                st.markdown("### 🔍 指标一：网页骨架清晰度 (H1/H2标签)")
                h1_tags = soup.find_all('h1')
                h2_tags = soup.find_all('h2')
                
                # 用漂亮的指标卡片显示数字
                col1, col2 = st.columns(2)
                col1.metric("H1 主标题数量", len(h1_tags))
                col2.metric("H2 副标题数量", len(h2_tags))
                
                if h1_tags:
                    st.success("✅ 优秀！找到了 <h1> 标签，AI 能秒懂你的核心主题。")
                else:
                    st.error("❌ 严重警告：缺失 <h1> 标签！AI 抓取时会找不到重点。")

                # --- 指标二：纯文本含金量 ---
                st.markdown("### 🔍 指标二：纯文本含金量 (信噪比)")
                for script in soup(["script", "style"]):
                    script.extract() # 清除无用代码
                
                pure_text = soup.get_text(strip=True)
                ratio = (len(pure_text) / len(html_content)) * 100 if len(html_content) > 0 else 0
                
                st.metric("信噪比得分 (建议大于10%)", f"{ratio:.2f}%")
                
                if ratio < 10:
                    st.warning("⚠️ 代码太臃肿！真实内容被大量无效代码淹没，AI 提取困难。")
                else:
                    st.success("✅ 信噪比健康，AI 提取正文非常轻松。")

                # --- 指标三：爬虫拦截测试 ---
                st.markdown("### 🔍 指标三：AI 爬虫大门测试 (robots.txt)")
                parsed_url = urllib.parse.urlparse(url_input)
                robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
                robots_response = requests.get(robots_url, headers=headers, timeout=5)
                
                if robots_response.status_code == 200:
                    st.info("ℹ️ 网站配置了 robots.txt，建议人工确认是否拦截了 AI 爬虫。")
                else:
                    st.success("✅ 未检测到严格的 robots.txt 拦截，AI 默认可访问。")
                    
                st.balloons() # 庆祝动画 🎉
                
            except Exception as e:
                st.error(f"❌ 扫描失败，请检查网址是否正确或网站开启了防抓取保护。")
