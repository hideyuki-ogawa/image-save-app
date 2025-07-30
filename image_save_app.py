import streamlit as st
import os
from datetime import datetime
from PIL import Image
import io

def save_image_from_camera(image_data, save_directory="saved_images", image_number=1):
    """カメラで撮影した画像を保存する関数"""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"camera_image_{timestamp}_{image_number:02d}.jpg"
    filepath = os.path.join(save_directory, filename)
    
    # 画像を保存
    with open(filepath, "wb") as f:
        f.write(image_data.getbuffer())
    
    return filepath

def save_images_from_upload(uploaded_files, save_directory="saved_images"):
    """アップロードした画像を保存する関数"""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    saved_files = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for i, uploaded_file in enumerate(uploaded_files, 1):
        file_extension = uploaded_file.name.split('.')[-1]
        filename = f"upload_image_{timestamp}_{i:02d}.{file_extension}"
        filepath = os.path.join(save_directory, filename)
        
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        saved_files.append(filepath)
    
    return saved_files

def main():
    st.title("📱 カメラ撮影 & 画像保存アプリ")
    st.write("カメラで直接撮影、またはファイルをアップロードして保存できます")
    
    # サイドバーで設定
    with st.sidebar:
        st.header("⚙️ 設定")
        save_dir = st.text_input("保存フォルダ名", value="saved_images")
        st.info("画像は選択したフォルダに保存されます")
        
        # 撮影モードの選択
        st.header("📷 撮影モード")
        mode = st.radio(
            "撮影方法を選択:",
            ["カメラで直接撮影", "ファイルをアップロード"],
            help="カメラ撮影ではリアルタイムで写真を撮れます"
        )
    
    # セッション状態の初期化
    if 'camera_images' not in st.session_state:
        st.session_state.camera_images = []
    if 'saved_camera_files' not in st.session_state:
        st.session_state.saved_camera_files = []
    
    if mode == "カメラで直接撮影":
        st.header("📸 カメラ撮影モード")
        
        # 現在の撮影枚数を表示
        current_count = len(st.session_state.camera_images)
        st.write(f"**撮影済み: {current_count}/2枚**")
        
        if current_count < 2:
            st.write(f"📷 {current_count + 1}枚目を撮影してください")
            
            # カメラ入力
            camera_image = st.camera_input(
                f"📸 写真{current_count + 1}を撮影",
                help="シャッターボタンを押して撮影してください"
            )
            
            if camera_image is not None:
                # 撮影した画像をセッション状態に保存
                if len(st.session_state.camera_images) == current_count:  # 新しい画像の場合
                    st.session_state.camera_images.append(camera_image)
                    st.success(f"✅ {len(st.session_state.camera_images)}枚目の撮影完了！")
                    if len(st.session_state.camera_images) < 2:
                        st.info("🔄 次の写真を撮影するために、もう一度シャッターを押してください")
                    st.rerun()
        
        # 撮影した画像のプレビューと保存
        if st.session_state.camera_images:
            st.header("🖼️ 撮影した画像")
            
            # 画像プレビュー
            if len(st.session_state.camera_images) == 1:
                col1, col2 = st.columns(2)
                with col1:
                    st.image(st.session_state.camera_images[0], caption="📸 撮影画像 1", use_column_width=True)
                with col2:
                    if current_count < 2:
                        st.info("2枚目を撮影してください")
                    
            elif len(st.session_state.camera_images) == 2:
                col1, col2 = st.columns(2)
                with col1:
                    st.image(st.session_state.camera_images[0], caption="📸 撮影画像 1", use_column_width=True)
                with col2:
                    st.image(st.session_state.camera_images[1], caption="📸 撮影画像 2", use_column_width=True)
            
            # 操作ボタン
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🗑️ すべてクリア", type="secondary", use_container_width=True):
                    st.session_state.camera_images = []
                    st.session_state.saved_camera_files = []
                    st.rerun()
            
            with col2:
                if len(st.session_state.camera_images) > 0:
                    if st.button("📤 最後の1枚を削除", type="secondary", use_container_width=True):
                        st.session_state.camera_images.pop()
                        st.rerun()
            
            with col3:
                if len(st.session_state.camera_images) == 2:
                    if st.button("💾 2枚まとめて保存", type="primary", use_container_width=True):
                        try:
                            saved_files = []
                            for i, img in enumerate(st.session_state.camera_images, 1):
                                filepath = save_image_from_camera(img, save_dir, i)
                                saved_files.append(filepath)
                            
                            st.session_state.saved_camera_files = saved_files
                            st.success("✅ 2枚の画像が正常に保存されました！")
                            st.balloons()
                            
                            # 保存されたファイル一覧を表示
                            st.write("**保存されたファイル:**")
                            for filepath in saved_files:
                                st.write(f"- `{filepath}`")
                            
                            # ダウンロードボタンを追加
                            st.write("**📥 ダウンロード:**")
                            for i, (img, filepath) in enumerate(zip(st.session_state.camera_images, saved_files), 1):
                                filename = os.path.basename(filepath)
                                st.download_button(
                                    label=f"📱 画像{i}をダウンロード",
                                    data=img.getbuffer(),
                                    file_name=filename,
                                    mime="image/jpeg",
                                    key=f"download_camera_{i}"
                                )
                            
                        except Exception as e:
                            st.error(f"❌ 保存中にエラーが発生しました: {str(e)}")
    
    else:  # ファイルアップロードモード
        st.header("📁 ファイルアップロードモード")
        
        # ファイルアップローダー
        uploaded_files = st.file_uploader(
            "画像を選択してください（2枚まで）",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            accept_multiple_files=True,
            help="ギャラリーから画像を選択できます"
        )
        
        if uploaded_files:
            # アップロードされたファイル数をチェック
            if len(uploaded_files) > 2:
                st.warning("⚠️ 2枚までしか選択できません。最初の2枚のみ処理します。")
                uploaded_files = uploaded_files[:2]
            
            # 画像プレビュー
            st.header("🖼️ プレビュー")
            
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
                        saved_files = save_images_from_upload(uploaded_files, save_dir)
                        st.success("✅ 画像が正常に保存されました！")
                        
                        st.write("**保存されたファイル:**")
                        for filepath in saved_files:
                            st.write(f"- `{filepath}`")
                        
                        # ダウンロードボタンを追加
                        st.write("**📥 ダウンロード:**")
                        for i, (uploaded_file, filepath) in enumerate(zip(uploaded_files, saved_files), 1):
                            filename = os.path.basename(filepath)
                            st.download_button(
                                label=f"📱 画像{i}をダウンロード",
                                data=uploaded_file.getbuffer(),
                                file_name=filename,
                                mime=f"image/{uploaded_file.type.split('/')[-1]}",
                                key=f"download_upload_{i}"
                            )
                        
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ 保存中にエラーが発生しました: {str(e)}")
            else:
                st.info("📝 2枚の画像を選択してから保存ボタンが有効になります")
    
    # 使い方説明
    with st.expander("💡 使い方ガイド"):
        st.markdown("""
        ### 📷 カメラ撮影モード
        1. サイドバーで「カメラで直接撮影」を選択
        2. シャッターボタンを押して1枚目を撮影
        3. もう一度シャッターボタンを押して2枚目を撮影
        4. 「2枚まとめて保存」ボタンをクリック
        
        ### 📁 ファイルアップロードモード
        1. サイドバーで「ファイルをアップロード」を選択
        2. ギャラリーから画像を2枚選択
        3. プレビューで確認
        4. 「2枚の画像を保存」ボタンをクリック
        
        ### 📝 注意事項
        - カメラ撮影では画像はJPG形式で保存されます
        - アップロードでは元の形式が保持されます
        - ファイル名にはタイムスタンプが自動で付きます
        """)

if __name__ == "__main__":
    main()