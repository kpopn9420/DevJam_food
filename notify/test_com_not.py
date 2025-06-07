from combine_notify import notify_user
token = "e6W_LCbYKvLHLV8XOkVx2i:APA91bG-GuudRTM8QjknsRHe4M2gkuxnxVa7RVBrSSI6trTvhnHvPStJc4_tP8KUxUOiLKpX3GjFLJL75MmIFIfigSJErxlU5FKzdKqC-QHiB3Rvje518Xw"

# 這是前端需要發送的通知範例
notify_user(
    event_type="new_food_nearby",
    user_name="小美",
    item_name="香蕉蛋糕",
    email="miracle.ylul1020@gmail.com",
    fcm_token=token
)
