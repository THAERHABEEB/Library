import streamlit as st
import pandas as pd
import time

# ================== ⚙️ إعداد الصفحة ==================
st.set_page_config(page_title="📚 مكتبة الذكاء الاصطناعي", page_icon="📘", layout="wide")

# session لإدارة الواجهة
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

# ===================== 🎬 أنيميشن البداية (الكتاب المتقلب) =====================
book_animation = """
<style>
.book-loader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  
}

.book {
  width: 160px;
  height: 120px;
  background: #f1f1f1;
  border-radius: 5px;
  position: flex;
  perspective: 800px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.5);
  animation: fadeOut 1s ease 3.5s forwards;
}

.page {
  width: 80px;
  height: 100%;
  background: white;
  position: absolute;
  right: 0;
  top: 0;
  transform-origin: left;
  border-left: 1px solid #ccc;
  animation: flip 0.8s ease infinite alternate;
}

@keyframes flip {
  0% { transform: rotateY(0deg); }
  100% { transform: rotateY(-180deg); }
}

@keyframes fadeOut {
  to { opacity: 0; visibility: hidden; }
}
</style>

<div class='book-loader'>
  <div class='book'>
    <div class='page'></div>
  </div>
</div>
"""

st.markdown(book_animation, unsafe_allow_html=True)
time.sleep(4)  # وقت عرض الأنيميشن قبل الدخول
# ================== 🎨 CSS + أنيميشن + صوت ==================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Cairo', sans-serif;
}



/* ===== fade-in ===== */
.fade-in {
  position:relative;
  animation: fadeIn 2s ease;
  top:-50px;
  
  
}
@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}

/* ===== شبكة الكتب ===== */
.book-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 25px;
  padding: 20px;
}

.book-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 15px;
  text-align: center;
  transition: all 0.4s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.book-card:hover {
  transform: scale(1.05);
  background: rgba(255,255,255,0.2);
  box-shadow: 0 10px 20px rgba(255,255,255,0.3);
}

.book-card img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 12px;
  transition: all 0.5s ease;
}

.book-card img:hover {
  transform: scale(1.08);
}

.book-title {
  font-size: 18px;
  font-weight: bold;
  color: #f8f9fa;
  margin-top: 10px;
}

.book-author {
  font-size: 15px;
  color: #ccc;
}

.book-rating {
  color: gold;
  margin: 5px 0;
}

.book-buttons a {
  display: inline-block;
  margin: 6px;
  padding: 8px 14px;
  border-radius: 8px;
  text-decoration: none;
  color: white;
  font-weight: 600;
  transition: 0.3s;
}

.read-btn {
  background: #28a745;
}

.read-btn:hover {
  background: #218838;
}

.download-btn {
  background: #007bff;
}

.download-btn:hover {
  background: #0056b3;
}
</style>
""", unsafe_allow_html=True)




# ================== 📚 واجهة المكتبة ==================
st.markdown("<h1 class='fade-in' style='text-align:center;'>🤖 مكتبة الذكاء الاصطناعي وعلوم البيانات</h1>", unsafe_allow_html=True)

# تحميل بيانات الكتب
try:
    df = pd.read_csv("ai_data_books_1000.csv")
except Exception as e:
    st.error(f"⚠️ خطأ في قراءة الملف: {e}")
    st.stop()

# ✅ إضافة تصنيف لو مش موجود
if "category" not in df.columns:
    df["category"] = "ذكاء اصطناعي"
    

# 🔍 مربع البحث + قائمة الفلاتر
# col1, col2  = st.columns([3, 1])

# with col1:
search = st.text_input("🔍 ابحث عن كتاب أو مؤلف:", "").strip()

# with col2:
#     categories = ["الكل"] + sorted(df["category"].dropna().unique().tolist())
#     selected_cat = st.selectbox("📂 التصنيف", categories)

# فلترة البيانات
if search:
    df = df[df.apply(lambda row: search.lower() in str(row['title']).lower() or search.lower() in str(row['author']).lower(), axis=1)]

# if selected_cat != "الكل":
#     df = df[df["category"] == selected_cat]

# عرض الكتب
st.markdown('<div class="book-container fade-in">', unsafe_allow_html=True)

for _, row in df.iterrows():
    st.markdown(f"""
    <div class="book-card">
        <img src="{row['image']}" alt="{row['title']}">
        <div class="book-title">{row['title']}</div>
        <div class="book-author">👨‍💻 {row['author']}</div>
        <div class="book-rating">⭐ {row['rating']}/5</div>
        <div class="book-buttons">
            <a href="{row['link']}" class="read-btn" target="_blank">📖 قراءة</a>
            <a href="{row['link']}" class="download-btn" download>⬇️ تحميل</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)