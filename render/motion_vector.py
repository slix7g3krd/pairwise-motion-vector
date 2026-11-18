"""第 51 批：角色快速挥刀时边缘拖影、残影粘在刀光上：运动矢量..."""

def skin_prev(prev_positions, weights, index):
    """用上一帧骨骼位置重算指定蒙皮顶点。"""
    raise NotImplementedError("TODO: skin_prev")

def blend_mode(mode, linear, dual):
    """按蒙皮模式返回线性或双四元数结果。"""
    raise NotImplementedError("TODO: blend_mode")

def object_motion(root_delta, prev_model, curr_model):
    """合成 root motion 与模型矩阵位移。"""
    raise NotImplementedError("TODO: object_motion")

def camera_cut(prev_view, curr_view):
    """判断当前帧是否发生相机切换。"""
    raise NotImplementedError("TODO: camera_cut")

def clamp_history(current, previous, max_delta):
    """按最大变化量钳制 TAA 历史颜色。"""
    raise NotImplementedError("TODO: clamp_history")

def reactive_mask(is_skinned, is_transparent):
    """生成 FSR 反应性掩码。"""
    raise NotImplementedError("TODO: reactive_mask")

def scale_motion(vector, render_scale):
    """按渲染分辨率比例缩放运动矢量。"""
    raise NotImplementedError("TODO: scale_motion")
