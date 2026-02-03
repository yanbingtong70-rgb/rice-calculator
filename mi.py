import streamlit as st

st.set_page_config(page_title="🥖 酸面团实验室", page_icon="🥖")

st.title("🥖 酸面团智能助手")
st.write("将复杂的“烘焙百分比”转化为简单的“加法”")

# 创建两个功能区
tab1, tab2 = st.tabs(["🧬 酵种喂养计算", "🍞 做面包 (烘焙百分比)"])

# --- 功能 1：酵种喂养 (Starter Feeding) ---
with tab1:
    st.header("1. 酵种喂养")
    st.info("目标：按比例精准喂养，保持酵母活力")
    
    col1, col2 = st.columns(2)
    with col1:
        starter_weight = st.number_input("当前容器内酵种重量 (g)", value=50, step=5)
    with col2:
        ratio_options = ["1:1:1 (日常维护)", "1:2:2 (增强活力)", "1:3:3 (去酸/长时间)", "1:4:4 (夏季/极强)"]
        selected_ratio = st.selectbox("选择喂养比例 (种:水:粉)", ratio_options)
    
    # 解析比例字符串，例如 "1:2:2" -> [1, 2, 2]
    r_list = [int(x) for x in selected_ratio.split(" ")[0].split(":")]
    seed_ratio, water_ratio, flour_ratio = r_list[0], r_list[1], r_list[2]

    if st.button("计算喂养方案", key="feed_btn"):
        # 计算逻辑：以当前酵种为基准
        # 如果是 1:2:2，当前50g酵种，则水=50*(2/1)=100，粉=50*(2/1)=100
        needed_water = starter_weight * (water_ratio / seed_ratio)
        needed_flour = starter_weight * (flour_ratio / seed_ratio)
        total_weight = starter_weight + needed_water + needed_flour
        
        st.success(f"⚖️ 喂养目标总重：{int(total_weight)} g")
        
        c1, c2 = st.columns(2)
        c1.metric("1. 加入水", f"{int(needed_water)} g")
        c2.metric("2. 加入面粉", f"{int(needed_flour)} g")
        st.caption(f"混合搅拌均匀，并在容器上做好高度标记。")

# --- 功能 2：做面包 (Baker's Math) ---
with tab2:
    st.header("2. 欧包面团计算")
    st.info("输入面粉量，自动计算其他配料 (Baker's Percentage)")

    # 核心输入：面粉量
    flour_input = st.number_input("你想用多少面粉做面包？(g)", value=500, step=50)
    
    # 滑动条调整配方
    st.write("--- 调整配方参数 ---")
    hydration = st.slider("💧 含水量 (Hydration %)", 60, 90, 75, format="%d%%")
    salt_pct = st.slider("🧂 盐 (Salt %)", 1.0, 3.0, 2.0, 0.1, format="%.1f%%")
    starter_pct = st.slider("🧬 酵种比例 (Starter %)", 10, 40, 20, 5, format="%d%%")
    
    if st.button("生成配方表", key="bread_btn"):
        # 烘焙百分比计算逻辑：一切都是面粉的百分比
        # 注意：酵种里通常也含有水和粉（假设酵种是100%水粉比），这里做简易版计算，直接按总百分比算
        
        water_weight = flour_input * (hydration / 100)
        salt_weight = flour_input * (salt_pct / 100)
        starter_weight = flour_input * (starter_pct / 100)
        total_dough = flour_input + water_weight + salt_weight + starter_weight
        
        st.subheader(f"🥯 预计面团总重：{int(total_dough)} g")
        
        # 用表格展示，清晰明了
        recipe_data = {
            "原料": ["高筋面粉 (基准)", "水", "天然酵种", "盐"],
            "重量 (g)": [flour_input, int(water_weight), int(starter_weight), float(f"{salt_weight:.1f}")],
            "百分比": ["100%", f"{hydration}%", f"{starter_pct}%", f"{salt_pct}%"]
        }
        st.table(recipe_data)
        
        # 硬件交互模拟
        st.warning("💡 如果这是硬件产品，屏幕会依次显示：'请倒入面粉' -> '请倒入水' -> '请倒入酵种'，每一步归零。")