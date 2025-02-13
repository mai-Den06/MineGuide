import tkinter as tk

from PIL import Image, ImageTk

from config.setting import IMAGE_SAMPLE_PATH
from modules.db_handler import get_is_visible, set_visibility

class OverlayInfo(tk.Toplevel):
    def __init__(self, parent, object_names: list, descriptions: list, alpha: float = 0.8):
        super().__init__(parent)
        
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-alpha', alpha)
        
        self.configure(bg='#161616')

        self.stop_flag = False
        self.info_frames = []

        # Stopボタンのフレーム
        top_frame = tk.Frame(self, bg='#161616')
        top_frame.pack(fill='x', padx=10, pady=5)

        self.stop_button = tk.Button(
            top_frame,
            text="⛔",
            font=('Arial', 10, 'bold'),
            command=self.set_stop_flag,
            bg='#FF4500',
            fg='white',
            relief="flat",
            width=20,
            height=1
        )
        self.stop_button.pack(padx=5)

        # メインコンテンツフレーム
        self.content_frame = tk.Frame(self, bg='#161616')
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # 各オブジェクトの情報を追加
        for obj_name, desc in zip(object_names, descriptions):
            self.add_info_frame(obj_name, desc)

        # ドラッグ用のデータ保持
        self.drag_data = {'x': 0, 'y': 0, 'moved': False}
        
        self.bind('<Button-1>', self._on_drag_start)
        self.bind('<B1-Motion>', self._on_drag_motion)

    def add_info_frame(self, object_name: str, description: str):
        """オーバーレイに新しい情報フレームを追加"""
        frame = tk.Frame(self.content_frame, bg='#2E2E2E', bd=3, relief="ridge")
        frame.pack(fill='x', padx=10, pady=5)

        # 上部：画像＋タイトル
        top_frame = tk.Frame(frame, bg='#2E2E2E')
        top_frame.pack(fill='x', padx=10, pady=5)

        # 画像を読み込む
        image_path = f"{IMAGE_SAMPLE_PATH}/{object_name}.png"
        try:
            image = Image.open(image_path)
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(top_frame, image=image, bg='#2E2E2E')
            image_label.image = image
        except FileNotFoundError:
            image_label = tk.Label(top_frame, text="No Image", fg="white", bg='#2E2E2E')
        image_label.pack(side="left", padx=10)

        # タイトルラベル
        title_label = tk.Label(
            top_frame,
            text=object_name,
            font=('Arial', 18, 'bold'),
            fg='#FF6347',
            bg='#2E2E2E',
            padx=20,
            pady=10
        )
        title_label.pack(side="left", padx=10)

        # 説明の表示/非表示ボタン
        description_visible = bool(get_is_visible(object_name))
        toggle_button = tk.Button(
            top_frame,
            text="v",
            font=('Arial', 10, 'bold'),
            bg='#FF6347',
            fg='white',
            relief="flat",
            width=3,
            height=1
        )
        toggle_button.pack(side="right", padx=10, pady=5)

        # 下部：説明文（初期状態は非表示）
        description_frame = tk.Frame(frame, bg='#2E2E2E')
        description_label = tk.Label(
            description_frame,
            text=description,
            font=('Arial', 14),
            fg='#F0E68C',
            bg='#2E2E2E',
            padx=20,
            pady=10
        )
        description_label.pack(fill='both', expand=True)

        if description_visible:
            description_frame.pack(fill='both', expand=True)
        else:
            description_frame.pack_forget()
            toggle_button.config(text="<")

        # ボタンの機能を設定
        def toggle_desc():
            if description_frame.winfo_ismapped():
                # 表示中の場合は非表示にする
                set_visibility(object_name, 0)
                description_frame.pack_forget()
                toggle_button.config(text="<")
            else:
                # 非表示の場合は表示する
                set_visibility(object_name, 1)
                description_frame.pack(fill='both', expand=True)
                toggle_button.config(text="v")

        toggle_button.config(command=toggle_desc)

        # フレーム情報をリストに保存
        self.info_frames.append((frame, title_label, description_label, image_label))

    def update_overlay(self, object_names: list, descriptions: list):
        """オーバーレイの内容を更新（新しいリストをセット）"""

        # 古いフレームを非表示にしてリストに保存
        if hasattr(self, 'old_info_frames'):
            for frame, _, _, _ in self.old_info_frames:
                frame.destroy()

        self.old_info_frames = self.info_frames
        for frame, _, _, _ in self.old_info_frames:
            frame.pack_forget()

        # 2秒後に古いフレームを削除
        self.after(2000, self._remove_old_frames)

        # 新しい情報をセット
        self.info_frames = []
        for obj_name, desc in zip(object_names, descriptions):
            self.add_info_frame(obj_name, desc)

    def _remove_old_frames(self):
        """古いフレームを削除"""
        if hasattr(self, 'old_info_frames'):
            for frame, _, _, _ in self.old_info_frames:
                frame.destroy()
            self.old_info_frames = []


    def set_stop_flag(self):
        """停止フラグを立てる"""
        self.stop_flag = True
    
    def _on_drag_start(self, event):
        """ドラッグ開始時の処理"""
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        self.drag_data['moved'] = False
    
    def _on_drag_motion(self, event):
        """ドラッグ中のウィンドウ移動処理"""
        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']
        
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        
        self.geometry(f'+{x}+{y}')
        self.drag_data['moved'] = True
