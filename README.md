"""
1.测试时间：2019-04-17
2.demo作用：使用selenium + numpy + cv2完成geetest3登录界面滑块拖动
3.1. origin_img：原图保存文件夹。原图来源于自己手动拼接，一共6张（还行）
3.2. test_img: 程序测试10次的完成情况截图。实际测试远不止10次，除滑动距离在110px左右时出现失败，其他时候均成功。如果有误，那多数是更新了（还行）
3.3. jietu.py: 手动截图的遗留物
3.4. koutu.py: 手动拼图的遗留物
3.5. login.py: 主程序，可直接运行（可能出现cv2版本问题，自行百度）
"""