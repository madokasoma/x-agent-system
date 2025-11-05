#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ベースエージェントクラス - すべてのエージェントの基底クラス
"""

import os
import logging
from abc import ABC, abstractmethod
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseAgent(ABC):
    """すべてのAIエージェントの基底クラス"""

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)

        # Anthropic Claude クライアント
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            self.anthropic = Anthropic(api_key=anthropic_key)
            self.logger.info(f"✅ Anthropic Claude API initialized")
        else:
            self.anthropic = None
            self.logger.warning(f"⚠️  Anthropic API key not found")

        # OpenAI クライアント（オプション）
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            self.openai = OpenAI(api_key=openai_key)
            self.logger.info(f"✅ OpenAI API initialized")
        else:
            self.openai = None

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        エージェントのメイン処理
        各エージェントで実装が必要
        """
        pass

    def call_claude(self, prompt: str, system_prompt: str = None,
                   model: str = "claude-3-5-sonnet-20241022",
                   max_tokens: int = 4096) -> str:
        """Claude APIを呼び出し"""
        if not self.anthropic:
            raise ValueError("Anthropic API key not configured")

        try:
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": model,
                "max_tokens": max_tokens,
                "messages": messages
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = self.anthropic.messages.create(**kwargs)
            return response.content[0].text

        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise

    def call_openai(self, prompt: str, system_prompt: str = None,
                   model: str = "gpt-4-turbo-preview",
                   max_tokens: int = 2048) -> str:
        """OpenAI APIを呼び出し（オプション）"""
        if not self.openai:
            raise ValueError("OpenAI API key not configured")

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise

    def log_success(self, message: str):
        """成功ログ"""
        self.logger.info(f"✅ {message}")

    def log_error(self, message: str):
        """エラーログ"""
        self.logger.error(f"❌ {message}")

    def log_warning(self, message: str):
        """警告ログ"""
        self.logger.warning(f"⚠️  {message}")
