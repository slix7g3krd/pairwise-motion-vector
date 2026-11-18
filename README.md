# pairwise-motion-vector

角色快速挥刀时边缘拖影、残影粘在刀光上：运动矢量只算骨骼末端，蒙皮顶点用错上一帧矩阵；双四元数插值和线性蒙皮混用；root motion 位移没进 object motion；相机切换帧没标记；alpha test 材质写了运动矢量但没裁剪；粒子用上一帧相机矩阵；TAA 历史颜色钳制过窄；FSR 反应性掩码没包含蒙皮；副屏分辨率比例不同；时间缩放时动画步长和渲染帧不同步。render/motion_vector.py 是核心，tests/test_motion_vector.py 15个红。要修的是：逐顶点上一帧蒙皮；统一蒙皮模式；object motion 加 root motion；相机切换标记；alpha test 同步裁剪；粒子矩阵校正；历史钳制按亮度；反应性掩码覆盖蒙皮；比例归一；时间缩放对齐。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：图形渲染；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。
