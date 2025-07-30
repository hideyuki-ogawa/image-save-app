import streamlit as st
import os
from datetime import datetime
from PIL import Image
import io

def save_images(uploaded_files, save_directory="saved_images"):
    """画像を保存する関数"""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    saved_files = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for i, uploaded_file in enumerate(uploaded_files, 1):
        # ファイル名を生成（タイムスタンプ + 連番）
        file_extension = uploaded_file.name.split('.')[-1]
        filename = f"image_{timestamp}_{i:02d}.{file_extension}"
        filepath = os.path.join(save_directory, filename)
        
        # 画像を保存
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        saved_files.append(filepath)
    
    return saved_files

def main():
    st.title("📱 画像2枚保存アプリ")
    st.write("スマホで撮影した画像を2枚選択して保存できます")
    
    # サイドバーで設定
    with st.sidebar:
        st.header("⚙️ 設定")
        save_dir = st.text_input("保存フォルダ名", value="saved_images")
        st.info("画像は選択したフォルダに保存されます")
    
    # ファイルアップローダー
    st.header("📸 画像をアップロード")
    uploaded_files = st.file_uploader(
        "画像を選択してください（2枚まで）",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        accept_multiple_files=True,
        help="スマホのカメラで撮影した画像やギャラリーから選択できます"
    )
    
    if uploaded_files:
        # アップロードされたファイル数をチェック
        if len(uploaded_files) > 2:
            st.warning("⚠️ 2枚までしか選択できません。最初の2枚のみ処理します。")
            uploaded_files = uploaded_files[:2]
        
        # 画像プレビュー
        st.header("🖼️ プレビュー")
        
        # 2列レイアウトで画像を表示
        if len(uploaded_files) == 1:
            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_files[0], caption=f"画像1: {uploaded_files[0].name}", use_column_width=True)
            with col2:
                st.info("もう1枚画像を選択してください")
        
        elif len(uploaded_files) == 2:
            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_files[0], caption=f"画像1: {uploaded_files[0].name}", use_column_width=True)
            with col2:
                st.image(uploaded_files[1], caption=f"画像2: {uploaded_files[1].name}", use_column_width=True)
        
        # 画像情報を表示
        st.header("ℹ️ 画像情報")
        for i, file in enumerate(uploaded_files, 1):
            with st.expander(f"画像{i}の詳細"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**ファイル名:** {file.name}")
                with col2:
                    st.write(f"**サイズ:** {file.size / 1024:.1f} KB")
                with col3:
                    # 画像の解像度を取得
                    try:
                        image = Image.open(file)
                        st.write(f"**解像度:** {image.size[0]} × {image.size[1]}")
                    except:
                        st.write("**解像度:** 取得できません")
        
        # 保存ボタン
        st.header("💾 保存")
        
        if len(uploaded_files) == 2:
            if st.button("🔄 2枚の画像を保存", type="primary", use_container_width=True):
                try:
                    saved_files = save_images(uploaded_files, save_dir)
                    st.success("✅ 画像が正常に保存されました！")
                    
                    # 保存されたファイル一覧を表示
                    st.write("**保存されたファイル:**")
                    for filepath in saved_files:
                        st.write(f"- `{filepath}`")
                    
                    # 保存完了後のアクション
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ 保存中にエラーが発生しました: {str(e)}")
        else:
            st.info("📝 2枚の画像を選択してから保存ボタンが有効になります")
    
    else:
        # 初期画面の説明
        st.info("""
        ### 使い方
        1. 上のアップローダーをクリック
        2. スマホで撮影した画像を2枚選択
        3. プレビューで確認
        4. 保存ボタンをクリック
        
        ### 対応形式
        - PNG, JPG, JPEG, GIF, BMP
        
        ### 特徴
        - 📱 スマホからの直接アップロード対応
        - 🖼️ リアルタイムプレビュー
        - 📊 画像情報表示
        - 🕒 タイムスタンプ付きファイル名
        """)

if __name__ == "__main__":
    main()