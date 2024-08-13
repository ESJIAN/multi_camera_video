import cv2
import threading

# 创建一个全局标志，用于控制线程的停止
stop_capture = False


def capture_video(camera_id, output_file):
    global stop_capture
    video_capture = cv2.VideoCapture(camera_id)

    if not video_capture.isOpened():
        print(f"Error: Unable to open camera {camera_id}")
        return

    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (width, height))

    while not stop_capture:
        # 检查空格键是否被按下,按照检测在前，响应在后方的原则
        if cv2.waitKey(1) & 0xFF == ord(' '):  # 使用 ord(' ') 检查空格键
            stop_capture = True

        if stop_capture:
            # 执行完后摧毁所有的imshow窗口
            video_capture.release()
            out.release()
            # 窗口摧毁前必须得先释放占用的资源，否则会造成因为资源占用无法摧毁的窗口白屏现象
            cv2.destroyAllWindows()
            break
        else:
            ret, frame = video_capture.read()
            out.write(frame)
            cv2.imshow(f'Camera {camera_id}', frame)



def main():
    global stop_capture
    # 初始化全局线程中断标识
    stop_capture = False

    camera1 = threading.Thread(target=capture_video, args=(0, 'cam01.mp4'))
    camera2 = threading.Thread(target=capture_video, args=(1, 'cam02.mp4'))
    # 从主线程中孵化两个子线程
    camera1.start()
    camera2.start()
    # 等待两个子线程结束
    camera1.join()
    camera2.join()

if __name__ == '__main__':
    main()

# 犯错：窗口摧毁前必须得先释放占用的资源，否则会造成因为资源占用无法摧毁的窗口白屏现象

# 思考：可以边写代码边写流程图这样可以很明确我在干什么