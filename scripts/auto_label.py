import os
import shutil
from ultralytics import YOLO

# 1. 모델 로드 (범용 모델이라 얼굴만 크게 있으면 가끔 못 잡을 수 있어요)
model = YOLO('yolov8n.pt') 

base_path = './dataset'
users = ['ssafy_user1', 'ssafy_user2', 'ssafy_user3']
train_img_path = './train/images'
train_txt_path = './train/labels'

# 폴더 비우고 새로 시작 (선택 사항)
# shutil.rmtree('./train', ignore_errors=True)
# os.makedirs(train_img_path, exist_ok=True)
# os.makedirs(train_txt_path, exist_ok=True)

print("🚀 오토 라벨링을 시작합니다...")

for idx, user in enumerate(users):
    user_folder = os.path.join(base_path, user)
    if not os.path.exists(user_folder):
        print(f"⚠️ 폴더 없음: {user_folder}")
        continue
    
    # jpg, JPG, png 모두 찾기
    images = [f for f in os.listdir(user_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"📂 {user} 폴더에서 사진 {len(images)}장 발견!")

    for img_name in images:
        img_full_path = os.path.join(user_folder, img_name)
        
        # conf를 0.25로 대폭 낮췄습니다. (더 잘 잡히게)
        results = model.predict(source=img_full_path, conf=0.25, save=False, verbose=False)
        
        found = False
        for r in results:
            if len(r.boxes) > 0:
                box = r.boxes.xywhn[0].tolist()
                new_name = f"{user}_{img_name}"
                
                shutil.copy(img_full_path, os.path.join(train_img_path, new_name))
                
                txt_name = new_name.rsplit('.', 1)[0] + '.txt'
                with open(os.path.join(train_txt_path, txt_name), 'w') as f:
                    f.write(f"{idx} {box[0]} {box[1]} {box[2]} {box[3]}\n")
                found = True
        
        if not found:
            print(f"❌ {img_name}: AI가 사람을 못 찾음 (넘어감)")

print("\n✨ 작업 완료! 이제 'train/images' 폴더를 다시 확인해 보세요.")