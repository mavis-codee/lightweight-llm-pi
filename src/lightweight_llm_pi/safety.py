from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyHint:
    level: str
    message: str


SYSTEM_PROMPT = """你是运行在本地设备上的公益轻量 AI 助手。
请用简洁、温和、可执行的中文回答。遇到医疗、法律、金融、灾害、自伤、暴力、危险操作等高风险内容时，先提示边界，并建议联系当地专业人员或紧急服务。不要编造政策、药物剂量、法律结论或危险步骤。"""


_EMERGENCY_PATTERNS = {
    "煤气": "如果闻到煤气或燃气味：不要开关电器，不要点火，立刻开窗通风，离开现场后联系燃气公司或当地紧急救援。",
    "燃气": "如果闻到煤气或燃气味：不要开关电器，不要点火，立刻开窗通风，离开现场后联系燃气公司或当地紧急救援。",
    "火灾": "遇到火灾请优先撤离，低姿前进，关闭身后门，到了安全地点后拨打当地火警电话。",
    "触电": "发现触电时不要直接接触伤者，先切断电源或用干燥绝缘物隔离，再呼叫急救。",
    "中毒": "疑似中毒请尽快离开污染源，保留可疑物品信息，并联系急救或中毒控制中心。",
    "自杀": "如果你或身边的人有自伤风险，请立刻联系可信赖的人、当地急救电话或心理危机热线，不要独自承受。",
    "不想活": "如果你或身边的人有自伤风险，请立刻联系可信赖的人、当地急救电话或心理危机热线，不要独自承受。",
    "胸痛": "突发胸痛、呼吸困难、意识不清等情况可能很危险，请立即联系急救服务。",
}

_BOUNDARY_PATTERNS = {
    "药": "我可以提供一般安全提醒，但不能替代医生诊断或给出个体化用药方案。",
    "病": "我可以提供一般健康信息，但不能替代医生诊断；症状严重或持续时请就医。",
    "合同": "我可以帮助梳理问题，但不能替代律师给出正式法律意见。",
    "起诉": "我可以帮助整理材料思路，但具体法律判断请咨询律师或当地法律援助机构。",
    "投资": "我不能替代持牌金融顾问；请结合自身风险承受能力，谨慎决策。",
    "贷款": "涉及贷款和征信请核实官方渠道，警惕要求先交钱或索要验证码的骗局。",
    "密码": "不要在对话中输入真实密码、验证码、身份证号、银行卡号等敏感信息。",
    "验证码": "不要向任何人透露验证码；正规机构通常不会索要你的短信验证码。",
}


def match_safety_hint(text: str) -> SafetyHint | None:
    normalized = text.lower()
    for keyword, message in _EMERGENCY_PATTERNS.items():
        if keyword in normalized:
            return SafetyHint(level="紧急安全提示", message=message)

    for keyword, message in _BOUNDARY_PATTERNS.items():
        if keyword in normalized:
            return SafetyHint(level="安全边界", message=message)

    return None


def safety_context(user_text: str) -> str:
    hint = match_safety_hint(user_text)
    if hint is None:
        return SYSTEM_PROMPT
    return f"{SYSTEM_PROMPT}\n\n当前用户问题触发了{hint.level}：{hint.message}"
