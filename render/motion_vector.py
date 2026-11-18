"""第 51 批：角色快速挥刀时边缘拖影、残影粘在刀光上的运动矢量修复。

时间抗锯齿（TAA/FSR）运动矢量管线，按测试契约提供以下修复入口：

* ``skin_prev``      —— 逐顶点用上一帧骨骼位置重算蒙皮（权重先归一化），
                        不再只取骨骼末端，修复残影粘在刀光边缘的问题；
* ``blend_mode``     —— 统一蒙皮插值入口，线性蒙皮与双四元数插值不许混用；
* ``object_motion``  —— object motion 合成时纳入 root motion 位移；
* ``camera_cut``     —— 标记相机切换帧，切换帧必须丢弃时间历史；
* ``clamp_history``  —— TAA 历史颜色在亮度邻域内对称钳制，避免钳制过窄；
* ``reactive_mask``  —— FSR 反应性掩码同时覆盖蒙皮物体与透明物体；
* ``scale_motion``   —— 副屏渲染分辨率比例不同时，对运动矢量做比例归一。
"""


def skin_prev(prev_positions, weights, index):
    """用上一帧骨骼位置重算指定蒙皮顶点。

    对第 ``index`` 个蒙皮顶点，按其骨骼权重 ``weights`` 对上一帧各骨骼
    位置 ``prev_positions`` 做加权混合。权重不要求预先归一化（例如
    ``[0.25, 0.25]``），混合前先按权重和归一化，保证快速挥刀时边缘顶点
    的上一帧位置与当前帧走同一套蒙皮结果，而不是错误地只取骨骼末端。
    """
    if not prev_positions:
        return ()

    total = sum(weights)
    if total == 0:
        return tuple(0.0 for _ in prev_positions[0])

    dim = len(prev_positions[0])
    return tuple(
        sum(pos[axis] * w for pos, w in zip(prev_positions, weights)) / total
        for axis in range(dim)
    )


def blend_mode(mode, linear, dual):
    """按蒙皮模式返回线性或双四元数结果。

    同一个物体只能走一种插值路径，禁止双四元数与线性蒙皮结果混用。
    """
    normalized = str(mode).strip().lower()
    if normalized == "linear":
        return linear
    if normalized == "dual":
        return dual
    raise ValueError(f"unknown skinning blend mode: {mode!r}")


def object_motion(root_delta, prev_model, curr_model):
    """合成 root motion 与模型矩阵位移。

    运动矢量的物体空间分量为 root motion 位移与上一帧/当前帧模型矩阵
    贡献的逐分量之和，root motion 不再被漏掉。
    """
    return tuple(
        root + prev + curr
        for root, prev, curr in zip(root_delta, prev_model, curr_model)
    )


def camera_cut(prev_view, curr_view):
    """判断当前帧是否发生相机切换。

    视图参数（位置/朝向等任意分量）发生变化即视为切换帧，返回 ``True``，
    调用方据此丢弃 TAA 历史，避免把切换前的画面重投影成鬼影。
    """
    return bool(prev_view != curr_view)


def clamp_history(current, previous, max_delta):
    """按最大变化量钳制 TAA 历史颜色。

    在实际引擎中该钳制在亮度（luma）通道、以当前像素邻域为界执行；
    这里对标量契约做对称钳制：``current`` 被限制在
    ``[previous - max_delta, previous + max_delta]`` 内，
    邻域过窄导致的拖影由此消除。
    """
    lower = previous - max_delta
    upper = previous + max_delta
    if current < lower:
        return float(lower)
    if current > upper:
        return float(upper)
    return float(current)


def reactive_mask(is_skinned, is_transparent):
    """生成 FSR 反应性掩码。

    蒙皮物体（快速形变区域）与透明物体都必须标记为反应性像素，
    掩码不再只覆盖透明通道而漏掉蒙皮网格。
    """
    return bool(is_skinned or is_transparent)


def scale_motion(vector, render_scale):
    """按渲染分辨率比例缩放运动矢量。

    副屏渲染比例与主屏幕不同时，矢量逐分量乘以 ``render_scale``
    归一到同一屏幕空间；比例为 0 时矢量归零。
    """
    return tuple(component * render_scale for component in vector)
