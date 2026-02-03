import streamlit as st
import pandas as pd

# 1. 基础配置
st.set_page_config(page_title="Sourdough Pro", page_icon="🥖")

st.title("🥖 酸面团实验室")
st.write("从喂养到烘焙的全流程计算")

# --- 创建两个功能标签页 ---
tab_feed, tab_bake = st.tabs(["🧬 1. 酵种喂养 (日常)", "🍞 2. 做面包 (主面团)"])

# ==========================================
# 功能区 1：酵种喂养 (Feeding)
# ==========================================
with tab_feed:
    st.header("酵种喂养计算")
    st.caption("目标：按比例精准喂养，保持酵母活力")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        # 输入：瓶子里现在的酵种重
        starter_now = st.number_input("瓶内剩余酵种 (g)", value=50, step=10, key="feed_input")
    with col_f2:
        # 选择：喂养比例
        feed_ratio = st.selectbox(
            "喂养比例 (种:水:粉)", 
            ["1:1:1 (日常维护)", "1:2:2 (增强活力)", "1:3:3 (去酸/长时间)", "1:4:4 (夏季/极强)"],
            key="feed_select"
        )
    
    # 解析比例字符串 (例如 "1:2:2" -> 1, 2, 2)
    # 简单的文本处理技巧
    r_str = feed_ratio.split(" ")[0] # 拿到 "1:2:2"
    r_parts = [int(x) for x in r_str.split(":")]
    r_seed, r_water, r_flour = r_parts[0], r_parts[1], r_parts[2]

    # 计算
    # 逻辑：以瓶内剩余为基准。如果有50g种，比例1:2:2，则需要水=50*(2/1)=100g
    need_water = starter_now * (r_water / r_seed)
    need_flour = starter_now * (r_flour / r_seed)
    total_feed_weight = starter_now + need_water + need_flour

    st.divider()
    
    # 结果展示
    st.subheader(f"⚖️ 喂养后总重: {int(total_feed_weight)} g")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("💧 加入水", f"{int(need_water)} g")
    with c2:
        st.metric("🌾 加入面粉", f"{int(need_flour)} g")
        
    st.info(f"💡 操作提示：先往瓶里倒水搅拌均匀，再倒面粉。")

# ==========================================
# 功能区 2：做面包 (Baking - V3.0逻辑)
# ==========================================
with tab_bake:
    st.header("主面团配方计算")
    
    # --- 配方库 ---
    RECIPES = {
        "🔰 新手入门 (65%水)": {
            "hydration": 65, "salt": 2.0, "starter": 20, 
            "desc": "面团较硬，不粘手，适合第一次尝试"
        },
        "🍞 经典乡村 (75%水)": {
            "hydration": 75, "salt": 2.0, "starter": 20,
            "desc": "外壳硬脆，内部气孔适中"
        },
        "☁️ 云朵夏巴塔 (85%水)": {
            "hydration": 85, "salt": 2.2, "starter": 25,
            "desc": "极软，大孔洞，操作难度高"
        },
        "🍕 披萨底 (60%水)": {
            "hydration": 60, "salt": 2.5, "starter": 15,
            "desc": "低含水，薄脆"
        }
    }

    # --- 交互逻辑 (状态管理) ---
    selected_name = st.selectbox("选择配方风格", list(RECIPES.keys()), key="bake_select")
    preset = RECIPES[selected_name]
    st.caption(f"ℹ️ {preset['desc']}")

    # 状态初始化 & 强制更新逻辑
    if "last_recipe" not in st.session_state:
        st.session_state.last_recipe = selected_name
        st.session_state.val_hydro = preset["hydration"]
        st.session_state.val_salt = preset["salt"]
        st.session_state.val_starter = preset["starter"]

    # 检测切换，强制同步滑块
    if st.session_state.last_recipe != selected_name:
        st.session_state.val_hydro = preset["hydration"]
        st.session_state.val_salt = preset["salt"]
        st.session_state.val_starter = preset["starter"]
        st.session_state.last_recipe = selected_name

    # 输入面粉
    flour = st.number_input("面粉总量 (g)", value=400, step=50, key="bake_flour")

    # 参数滑块 (绑定 Session State)
    with st.expander("⚙️ 调整比例 (已自动同步)", expanded=True):
        hydration = st.slider("含水量 %", 50, 100, key="val_hydro")
        salt_pct = st.slider("盐 %", 0.0, 5.0, 0.1, key="val_salt")
        starter_pct = st.slider("酵种 %", 0, 50, 5, key="val_starter")

    # --- 计算 ---
    w_water = flour * (hydration / 100)
    w_starter = flour * (starter_pct / 100)
    w_salt = flour * (salt_pct / 100)
    w_total = flour + w_water + w_starter + w_salt

    st.divider()
    
    # --- 结果 ---
    st.subheader(f"⚖️ 面团总重: {int(w_total)} g")

    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1: bc2.metric("高筋面粉", f"{int(flour)}", "100%") # Layout tweak
    with bc2: bc2.metric("水", f"{int(w_water)}", f"{hydration}%")
    with bc3: bc3.metric("天然酵种", f"{int(w_starter)}", f"{starter_pct}%")
    with bc4: bc4.metric("盐", f"{float(f'{w_salt:.1f}')}", f"{salt_pct}%")

    # 清单
    st.write("📄 **操作清单**")
    df = pd.DataFrame({
        "原料": ["面粉", "水", "酵种", "盐"],
        "重量 (g)": [int(flour), int(w_water), int(w_starter), float(f"{w_salt:.1f}")],
        "百分比": ["100%", f"{hydration}%", f"{starter_pct}%", f"{salt_pct}%"]
    })
    st.table(df)
