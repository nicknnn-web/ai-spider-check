import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 1. 网页基础设置
st.set_page_config(page_title="AI 友好度检测", page_icon="🍏", layout="centered")

# 2. 注入 Apple 风格的 CSS 魔法
st.markdown("""
<style>
    /* 隐藏默认菜单和页脚，保持极简 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 整体背景与字体 */
    .stApp {
        background-color: #f5f5f7; /* 苹果经典淡灰底色 */
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 标题样式居中 */
    .apple-title {
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        color: #1d1d1f;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }
    .apple-subtitle {
        text-align: center;
        font-weight: 400;
        font-size: 1.2rem;
        color: #86868b;
        margin-bottom: 3rem;
    }

    /* 输入框样式 */
    .stTextInput>div>div>input {
        border-radius: 14px;
        background-color: #ffffff;
        border: 1px solid #d2d2d7;
        padding: 0.8rem 1rem;
        font-size: 1.1rem;
        color: #1d1d1f;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }

    /* 按钮样式：胶囊形状 + 苹果蓝 */
    .stButton>button {
        background-color: #0071e3;
        color: white;
        border-radius: 980px;
        padding: 0.6rem 2rem;
        font-size: 17px;
        font-weight: 400;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #0077ed;
        transform: scale(1.01);
    }
    
    /* 结果提示框圆角化 */
    .stAlert {
        border-radius: 16px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# 3. 页面头部 (苹果风文案)
st.markdown('<div class="apple-title">AI 友好度检测。</div>', unsafe_allow_html=True)
st.markdown('<div class="apple-subtitle">一键洞悉，大模型眼中的你。</div>', unsafe_allow_html=True)

# 4. 核心交互区
url_input = st.text_input("", placeholder="输入网站地址 (例如：https://www.apple.com.cn)", label_visibility="collapsed")
submit_button = st.button("开始检测")

# 5. 诊断逻辑
if submit_button:
    if not url_input.startswith("http"):
        st.error("提示：网址需以 http:// 或 https:// 开头。")
    else:
        with st.spinner('正在获取结构数据...'):
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
            try:
                response = requests.get(url_input, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                st.markdown("### 诊断结果")
                
                # 指标一：骨架
                h1_tags = soup.find_all('h1')
                if h1_tags:
                    st.success(f"**结构清晰。** 发现 {len(h1_tags)} 个 H1 标签，AI 能精准捕捉页面核心主题。")
                else:
                    st.error("**缺少核心结构。** 未发现 H1 标签，AI 提取页面重点时可能产生偏差。")

                # 指标二：信噪比
                for script in soup(["script", "style"]):
                    script.extract()
                pure_text = soup.get_text(strip=True)
                html_len = len(response.text)
                ratio = (len(pure_text) / html_len) * 100 if html_len > 0 else 0
                
                if ratio >= 10:
                    st.success(f"**信噪比优良 ({ratio:.1f}%)。** 代码整洁，核心文本易于被大模型向量化。")
                else:
                    st.warning(f"**信噪比偏低 ({ratio:.1f}%)。** 页面代码较为冗余，可能降低 AI 抓取效率。")

                # 指标三：协议
                parsed_url = urllib.parse.urlparse(url_input)
                robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
                robots_response = requests.get(robots_url, headers=headers, timeout=5)
                
                if robots_response.status_code == 200:
                    st.info("**已配置爬虫协议。** 检测到 robots.txt，请确保未拦截 GPTBot 等主流 AI。")
                else:
                    st.success("**无抓取限制。** 未检测到拦截规则，大模型可畅通访问。")
                    
            except Exception as e:
                st.error("无法访问该站点。请检查网络或确认网站是否开启了反爬虫防护。")
