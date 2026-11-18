import pytest
from render import motion_vector as mod

CASES = [
    ("skin_mid", "m.skin_prev([(0.0, 0.0), (2.0, 0.0)], [0.5, 0.5], 0) == (1.0, 0.0)"),
    ("skin_normalized", "m.skin_prev([(0.0, 0.0), (2.0, 0.0)], [0.25, 0.25], 0) == (1.0, 0.0)"),
    ("blend_dual", "m.blend_mode('dual', 1.0, 2.0) == 2.0"),
    ("blend_linear", "m.blend_mode('linear', 1.0, 2.0) == 1.0"),
    ("object_sum", "m.object_motion((1.0, 0.0), (2.0, 3.0), (4.0, 5.0)) == (7.0, 8.0)"),
    ("camera_cut_true", "m.camera_cut((0.0, 0.0), (1.0, 0.0)) is True"),
    ("camera_cut_false", "m.camera_cut((0.0, 0.0), (0.0, 0.0)) is False"),
    ("clamp_inside", "m.clamp_history(5.0, 4.5, 1.0) == 5.0"),
    ("clamp_outside", "m.clamp_history(10.0, 5.0, 2.0) == 7.0"),
    ("mask_skinned", "m.reactive_mask(True, False) is True"),
    ("mask_transparent", "m.reactive_mask(False, True) is True"),
    ("scale_motion", "m.scale_motion((1.0, 2.0), 2.0) == (2.0, 4.0)"),
    ("scale_zero", "m.scale_motion((1.0, 2.0), 0.0) == (0.0, 0.0)"),
    ("skin_single", "m.skin_prev([(3.0, 1.0)], [1.0], 0) == (3.0, 1.0)"),
    ("camera_same_view", "m.camera_cut((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)) is False")
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
