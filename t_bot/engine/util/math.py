def clamp(value: float, min_val: float, max_val: float) -> float:
    """将 value 钳制在 [min_val, max_val] 范围内。"""
    return max(min_val, min(value, max_val))
