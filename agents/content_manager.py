#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コンテンツ管理エージェント - ユーザーの素材を管理
"""

import os
import json
import yaml
from typing import Dict, List, Optional
from PIL import Image
from agents.base_agent import BaseAgent

class ContentManagerAgent(BaseAgent):
    """ユーザー素材の管理とマッピング"""

    def __init__(self):
        super().__init__("ContentManagerAgent")
        self.content_map = {
            'company_info': {},
            'pages': {
                'index': {'sections': []},
                'about': {'sections': []},
                'services': {'sections': []},
                'contact': {'sections': []}
            },
            'images': {},
            'global': {}  # サイト全体で使う情報（コピーライト等）
        }

    def add_company_info(self, key: str, value: str):
        """会社情報を追加"""
        self.content_map['company_info'][key] = value
        self.log_success(f"Company info added: {key}")

    def add_text(self, key: str, value: str, page: str = 'index', category: str = 'texts'):
        """テキストコンテンツを追加"""
        if category == 'company_info':
            self.content_map['company_info'][key] = value
        elif category == 'global':
            self.content_map['global'][key] = value
        else:
            # ページ固有のコンテンツ
            if page not in self.content_map['pages']:
                self.content_map['pages'][page] = {'sections': []}

            # ページのセクションに追加
            if 'texts' not in self.content_map['pages'][page]:
                self.content_map['pages'][page]['texts'] = {}

            self.content_map['pages'][page]['texts'][key] = value

        self.log_success(f"Text added: {key} to {page}/{category}")

    def add_image(self, key: str, image_path: str, page: str = 'index', optimize: bool = True):
        """画像を追加（最適化オプション付き）"""
        if not os.path.exists(image_path):
            self.log_error(f"Image not found: {image_path}")
            return False

        # 画像最適化
        if optimize:
            try:
                optimized_path = self._optimize_image(image_path)
                self.content_map['images'][key] = {
                    'path': optimized_path,
                    'original': image_path,
                    'page': page
                }
            except Exception as e:
                self.log_warning(f"Image optimization failed: {e}, using original")
                self.content_map['images'][key] = {
                    'path': image_path,
                    'original': image_path,
                    'page': page
                }
        else:
            self.content_map['images'][key] = {
                'path': image_path,
                'original': image_path,
                'page': page
            }

        self.log_success(f"Image added: {key} to {page}")
        return True

    def add_section(self, page: str, section_type: str, title: str, content: str, **kwargs):
        """セクションを追加"""
        if page not in self.content_map['pages']:
            self.content_map['pages'][page] = {'sections': []}

        section = {
            'type': section_type,
            'title': title,
            'content': content,
            **kwargs
        }
        self.content_map['pages'][page]['sections'].append(section)
        self.log_success(f"Section added: {section_type} to {page}")

    def load_from_yaml(self, yaml_file: str) -> bool:
        """YAMLファイルからコンテンツを読み込み"""
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # 会社情報
            if 'company_info' in data:
                for key, value in data['company_info'].items():
                    self.add_company_info(key, str(value))

            # グローバル情報
            if 'global' in data:
                self.content_map['global'] = data['global']

            # ページごとのコンテンツ
            if 'pages' in data:
                for page_name, page_data in data['pages'].items():
                    if 'sections' in page_data:
                        for section in page_data['sections']:
                            self.add_section(
                                page=page_name,
                                section_type=section.get('type', 'content'),
                                title=section.get('title', ''),
                                content=section.get('content', ''),
                                **{k: v for k, v in section.items() if k not in ['type', 'title', 'content']}
                            )

            # 画像
            if 'images' in data:
                for key, path in data['images'].items():
                    page = data.get('image_pages', {}).get(key, 'index')
                    self.add_image(key, path, page=page, optimize=True)

            self.log_success(f"Content loaded from: {yaml_file}")
            return True

        except Exception as e:
            self.log_error(f"Failed to load YAML: {e}")
            return False

    def _optimize_image(self, image_path: str, max_width: int = 1920,
                       quality: int = 85) -> str:
        """画像を最適化"""
        try:
            img = Image.open(image_path)

            # RGBに変換（RGBA対応）
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # リサイズ
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # 保存
            base, ext = os.path.splitext(image_path)
            optimized_path = f"{base}_optimized.jpg"

            img.save(optimized_path, 'JPEG', quality=quality, optimize=True)

            self.log_success(f"Image optimized: {optimized_path}")
            return optimized_path

        except Exception as e:
            self.log_error(f"Image optimization failed: {e}")
            return image_path

    def get_content_map(self) -> Dict:
        """コンテンツマップを取得"""
        return self.content_map

    def get_page_content(self, page: str) -> Dict:
        """特定のページのコンテンツを取得"""
        return self.content_map['pages'].get(page, {'sections': []})

    def save_content_map(self, output_file: str):
        """コンテンツマップを保存"""
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.content_map, f, ensure_ascii=False, indent=2)

        self.log_success(f"Content map saved: {output_file}")

    def execute(self, yaml_file: str = None, **kwargs) -> Dict:
        """
        メイン実行メソッド

        Args:
            yaml_file: YAMLファイルパス（オプション）
            **kwargs: 個別のコンテンツ

        Returns:
            コンテンツマップ
        """
        if yaml_file and os.path.exists(yaml_file):
            self.load_from_yaml(yaml_file)
        else:
            # kwargsから直接追加
            for key, value in kwargs.items():
                if key.startswith('company_'):
                    self.add_company_info(key.replace('company_', ''), value)
                else:
                    self.add_text(key, value)

        return self.get_content_map()


# 使用例
if __name__ == '__main__':
    agent = ContentManagerAgent()

    # 会社情報
    agent.add_company_info('company_name', 'マイカンパニー株式会社')
    agent.add_company_info('tagline', 'イノベーションで未来を創る')
    agent.add_company_info('description', '私たちは最先端のAI技術で、ビジネスの課題を解決します。')

    # トップページのセクション
    agent.add_section('index', 'hero', 'トップページヒーロー',
                     'あなたのビジネスを次のレベルへ')
    agent.add_section('index', 'features', 'サービスの特徴',
                     '高品質なAIソリューションを提供')

    # 会社概要ページ
    agent.add_section('about', 'company', '会社概要',
                     '2020年設立。AIエンジニア30名が在籍。')

    # サービスページ
    agent.add_section('services', 'service_list', 'サービス一覧',
                     'AI開発、コンサルティング、DX支援')

    # コンテンツマップを表示
    print(json.dumps(agent.get_content_map(), indent=2, ensure_ascii=False))
