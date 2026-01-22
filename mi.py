import streamlit as st

# 1. 标题与说明
st.title("🍚 完美煮饭计算器")
st.write("解决“洗米后不知道加多少水”的痛点")

# 2. 预设数据 (米种数据库)
rice_db = {
    "东北米/珍珠米 (1:1.3)": 1.3,
    "丝苗米/泰国米 (1:1.5)": 1.5,
    "糙米/五谷米 (1:2.0)": 2.0,
    "自定义": 0.0
}

# 3. 用户输入区
col1, col2 = st.columns(2)
with col1:
    pot_weight = st.number_input("1. 空锅/内胆重量 (g)", min_value=0, value=300, step=10)
with col2:
    rice_weight = st.number_input("2. 干米重量 (g)", min_value=0, value=200, step=10)

# 选择米种
rice_type = st.selectbox("3. 选择米种", list(rice_db.keys()))

# 处理自定义比例
if rice_type == "自定义":
    ratio = st.slider("设置水米比", 1.0, 3.0, 1.3, 0.1)
else:
    ratio = rice_db[rice_type]

# 核心步骤：洗米
st.info("💦 请去洗米，沥干水分后，将内胆放回秤上")

# 输入洗米后的总重
current_weight = st.number_input("4. 洗完米后的当前称重 (内胆+湿米) (g)", min_value=0, value=520, step=10)

# 4. 核心算法计算
if st.button("计算加水量"):
    # 理论需水量
    target_water = rice_weight * ratio
    
    # 理论目标总重 (最关键的数值：用户只需把秤加到这个数)
    final_target_weight = pot_weight + rice_weight + target_water
    
    # 算出还需要加多少水
    # 当前锅里已经含有的水 = 当前总重 - 空锅 - 干米
    water_absorbed = current_weight - pot_weight - rice_weight
    water_to_add = target_water - water_absorbed
    
    # 5. 结果展示
    st.success(f"🚰 请加水，直到电子秤显示：{int(final_target_weight)} g")
    st.metric(label="还需要倒入", value=f"{int(water_to_add)} g 水")
    
    st.caption(f"计算逻辑：目标总重 {int(final_target_weight)}g = 锅{pot_weight} + 米{rice_weight} + 水{int(target_water)}")