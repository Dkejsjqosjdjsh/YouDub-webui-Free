import asyncio
import edge_tts
from loguru import logger
import os

async def _generate_edge_tts(text, output_path, voice="zh-CN-XiaoxiaoNeural"):
    """
    使用 Edge-TTS 生成語音
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        logger.info(f"Edge-TTS 成功生成語音: {output_path}")
    except Exception as e:
        logger.error(f"Edge-TTS 生成失敗: {e}")

def edge_tts_generate(text, output_path, voice="zh-CN-XiaoxiaoNeural"):
    """
    同步包裝器，用於調用異步的 Edge-TTS
    """
    if os.path.exists(output_path):
        logger.info(f"語音已存在: {output_path}")
        return
    
    asyncio.run(_generate_edge_tts(text, output_path, voice))

def get_edge_voices():
    """
    獲取常用的中文語音列表
    """
    return [
        "zh-CN-XiaoxiaoNeural",
        "zh-CN-YunxiNeural",
        "zh-CN-YunjianNeural",
        "zh-CN-XiaoyiNeural",
        "zh-CN-YunyangNeural",
        "zh-CN-XiaochenNeural",
        "zh-CN-XiaohanNeural",
        "zh-CN-XiaomengNeural",
        "zh-CN-XiaomoNeural",
        "zh-CN-XiaoqiuNeural",
        "zh-CN-XiaoruiNeural",
        "zh-CN-XiaoshuangNeural",
        "zh-CN-XiaoxuanNeural",
        "zh-CN-XiaozhenNeural",
        "zh-TW-HsiaoChenNeural",
        "zh-TW-NanamiNeural",
        "zh-TW-HsiaoYuNeural",
        "zh-HK-HiuGaaiNeural",
        "zh-HK-HiuMaanNeural",
        "zh-HK-WanLungNeural",
    ]
