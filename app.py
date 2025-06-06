import streamlit as st  # Import thư viện Streamlit để xây dựng giao diện web
import pandas as pd  # Dùng để xử lý dữ liệu dạng bảng (DataFrame)
import requests  # Dùng để gửi yêu cầu HTTP và nhận dữ liệu từ API
import pickle  # Dùng để lưu và tải dữ liệu từ các file nhị phân
import base64  # Để mã hóa ảnh nền thành base64

# Hàm mã hóa ảnh sang base64
def get_base64(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

# Hàm đặt ảnh nền
def set_background(image_file):
    img_base64 = get_base64(image_file)
    css = f"""
    <style>
    .stApp {{
        background-image: url(data:image/png;base64,{img_base64});      # Cách nhúng trực tiếp hình ảnh vào CSS bằng Data URI với định dạng Base64.
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white; /* Màu chữ phù hợp với nền */
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Gọi hàm để đặt ảnh nền
set_background("1693150322893.jpg")  # Thay bằng đường dẫn đến file ảnh của bạn



# Tải dữ liệu đã xử lý và ma trận tương tự từ file pickle
with open('movie_data.pkl', 'rb') as file:  # Mở file 'movie_data.pkl' để đọc
    movies, cosine_sim = pickle.load(file)  # Tải dữ liệu phim và ma trận cosine similarity

# Hàm lấy đề xuất phim dựa trên tên phim đã chọn
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]  # Tìm chỉ số của phim đã chọn trong DataFrame
    sim_scores = list(enumerate(cosine_sim[idx]))  # Lấy danh sách điểm tương tự từ ma trận cosine_sim
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # Sắp xếp điểm tương tự theo thứ tự giảm dần
    sim_scores = sim_scores[1:11]  # Lấy 10 phim tương tự nhất (bỏ qua phim đã chọn)
    movie_indices = [i[0] for i in sim_scores]  # Lấy chỉ số của các bộ phim tương tự
    return movies[['title', 'movie_id']].iloc[movie_indices]  # Trả về tên phim và ID của các bộ phim tương tự

# Hàm lấy poster của bộ phim từ API TMDB
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Thay thế bằng khóa API của bạn
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'  # URL yêu cầu API để lấy thông tin phim
    response = requests.get(url)  # Gửi yêu cầu HTTP đến TMDB API
    data = response.json()  # Chuyển đổi phản hồi từ API sang định dạng JSON
    poster_path = data['poster_path']  # Lấy đường dẫn đến poster của bộ phim
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"  # Tạo URL đầy đủ của poster với kích thước 500px
    return full_path  # Trả về URL của poster

st.title("Nhóm 2 Hệ Thống Đề Xuất Phim")  # Tiêu đề phụ cho hệ thống đề xuất
# Tạo thanh điều hướng (Navbar) trên trang
st.markdown("""
<div class="navbar">
    <img src="https://ctsv.humg.edu.vn/uploads/news/2017_11/logo-truong-dai-hoc-mo-dia-chat.png" class ="img" alt="">
    <a href="#">Trang Chủ</a>
    <a href="/blog.html" target="_blank">Blog</a>
    <a href="#">Liên Hệ</a>
    <a href="#">Giới Thiệu</a>
</div>
""", unsafe_allow_html=True)  # Cho phép sử dụng HTML không an toàn

# CSS tùy chỉnh cho giao diện
st.markdown("""
    <style>
        body{
            background-color: #0000;
        }
        .navbar {
            background-color: #0000;
            # Màu nền cho thanh điều hướng
            padding: 10px;
            text-align: center;
            color: #0000;
            font-size: 18px;
        }
        .img{
                width: 64px;
                height: 64px;
        }
        .navbar a {
            color: white;  # Màu chữ của liên kết trong navbar
            padding: 14px 20px;
            text-decoration: none;
            margin: 0 15px;
            display: inline-block;
        }
        .navbar a:hover {
            background-color: blue;  # Màu nền khi di chuột qua
            color: #ffff;
        }
        .header {
            text-align: center;
            margin-top: 50px;
            font-size: 36px;
            color: white;
            font-weight: bold;
        }
        button {
            color: black !important;
            background-color: #007BFF;  # Màu nền nút bấm
            padding: 50px 20px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            padding_left:200px;
        }
        button:hover {
            background-color: pink;  # Màu nền nút khi di chuột qua
        }
        .selectbox {
            width: 100%;
            padding: 10px;
            font-size: 18px;
        }
        .movie-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            text-align: center;streamlit run movie_app.py

        }
        .movie-card {
            width: 200px;
            margin: 10px;
            color: white;
        }
        .movie-card img {
            width: 100%;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Giao diện của ứng dụng
st.markdown("<div class='header'>Chọn Phim và Xem Các Phim Đề Xuất</div>", unsafe_allow_html=True)  # Tiêu đề chính

# Hộp chọn để người dùng chọn phim
selected_movie = st.selectbox("Nhập Phim Vào Đây:", movies['title'].values, key="movie_select", label_visibility="visible")
# key="movie_select":

# Dùng để định danh (key) cho widget này. Key giúp Streamlit nhớ trạng thái của widget giữa các lần tải lại trang.
# label_visibility="visible":

# Đảm bảo nhãn "Nhập Phim Vào Đây:" luôn hiển thị (có thể ẩn với giá trị "hidden" hoặc "collapsed").

# Khi người dùng bấm nút 'Đề Xuất'
if st.button('Đề Xuất', key="recommend_button"):
    recommendations = get_recommendations(selected_movie)  # Lấy các phim đề xuất từ hàm get_recommendations
    st.write("Top 10 Phim Đề Xuất:")  # Hiển thị tiêu đề cho các phim đề xuất

    # Hiển thị các bộ phim theo dạng lưới
    movie_grid = st.container()  # Tạo container cho lưới phim
    with movie_grid:
        st.markdown('<div class="movie-grid">', unsafe_allow_html=True)  # Bắt đầu lưới phim
        for i in range(0, 10, 1):  # Duyệt qua từng hàng, mỗi hàng 1 bộ phim
            for j in range(i, i + 1):
                if j < len(recommendations):  # Kiểm tra xem phim có trong danh sách đề xuất không
                    movie_title = recommendations.iloc[j]['title']  # Lấy tên phim
                    movie_id = recommendations.iloc[j]['movie_id']  # Lấy ID phim
                    poster_url = fetch_poster(movie_id)  # Lấy URL poster của phim từ API
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="{poster_url}" alt="{movie_title}">
                            <p>{movie_title}</p>
                        </div>
                    """, unsafe_allow_html=True)  # Hiển thị poster và tên phim
        st.markdown('</div>', unsafe_allow_html=True)  # Kết thúc lưới phim