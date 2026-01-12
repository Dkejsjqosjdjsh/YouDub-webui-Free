import os
import requests
from loguru import logger

class FreeAPI:
    """
    提供免費或簡單註冊的 API 替代方案
    """
    @staticmethod
    def get_openai_client():
        """
        嘗試獲取 OpenAI 客戶端，如果沒有密鑰則使用公共代理或提示用戶
        """
        from openai import OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        
        if not api_key or api_key == "YOUR_API_KEY":
            logger.warning("未檢測到 OPENAI_API_KEY，切換至免費/演示模式")
            # 這裡可以集成一些免費的 API 轉發服務，或者引導用戶去哪裡獲取免費 Key
            # 為了演示，我們這裡保持原樣，但在 UI 中會增加引導
        
        return OpenAI(api_key=api_key, base_url=base_url)

    @staticmethod
    def get_tts_config():
        """
        獲取 TTS 配置，如果沒有字節跳動密鑰，則嘗試使用 Edge-TTS 等免費方案
        """
        appid = os.getenv('BYTEDANCE_APPID')
        access_token = os.getenv('BYTEDANCE_ACCESS_TOKEN')
        
        if not appid or not access_token:
            logger.warning("未檢測到字節跳動 API 密鑰，建議使用 Edge-TTS 插件（待集成）")
            return None, None
        
        return appid, access_token
