#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSS解析ユーティリティ
"""

import re
import requests
from typing import Dict, List, Set
from urllib.parse import urljoin

class CSSAnalyzer:
    """CSS を解析して主要なスタイル情報を抽出"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.css_content = ""

    def fetch_css(self, css_url: str) -> bool:
        """CSSファイルを取得"""
        try:
            # 相対URLを絶対URLに変換
            full_url = urljoin(self.base_url, css_url)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(full_url, headers=headers, timeout=10)
            response.raise_for_status()

            self.css_content += response.text + "\n"
            return True

        except Exception as e:
            print(f"⚠️  CSS fetch error ({css_url}): {e}")
            return False

    def extract_colors(self) -> Dict[str, List[str]]:
        """色情報を抽出"""
        colors = {
            'hex': [],
            'rgb': [],
            'rgba': [],
            'hsl': []
        }

        # HEX色 (#fff, #ffffff)
        hex_colors = re.findall(r'#[0-9a-fA-F]{3,6}\b', self.css_content)
        colors['hex'] = list(dict.fromkeys(hex_colors))[:15]  # 重複除去、最初の15個

        # RGB色
        rgb_colors = re.findall(r'rgb\([^)]+\)', self.css_content)
        colors['rgb'] = list(dict.fromkeys(rgb_colors))[:10]

        # RGBA色
        rgba_colors = re.findall(r'rgba\([^)]+\)', self.css_content)
        colors['rgba'] = list(dict.fromkeys(rgba_colors))[:10]

        # HSL色
        hsl_colors = re.findall(r'hsl\([^)]+\)', self.css_content)
        colors['hsl'] = list(dict.fromkeys(hsl_colors))[:5]

        return colors

    def extract_fonts(self) -> List[str]:
        """フォント情報を抽出"""
        font_families = re.findall(r'font-family:\s*([^;}]+)', self.css_content)

        # クリーンアップ
        fonts = []
        for font in font_families:
            font = font.strip().replace('"', '').replace("'", '')
            fonts.append(font)

        return list(dict.fromkeys(fonts))[:10]  # 重複除去、最初の10個

    def extract_breakpoints(self) -> List[int]:
        """レスポンシブのブレークポイントを抽出"""
        # メディアクエリからブレークポイントを抽出
        media_queries = re.findall(
            r'@media[^{]+\((?:min|max)-width:\s*(\d+)px\)',
            self.css_content
        )

        breakpoints = [int(bp) for bp in media_queries]
        return sorted(list(dict.fromkeys(breakpoints)))[:10]

    def extract_common_classes(self) -> List[str]:
        """よく使われるクラス名を抽出"""
        # クラスセレクタを抽出
        class_selectors = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{', self.css_content)

        # 頻度をカウント
        from collections import Counter
        class_counts = Counter(class_selectors)

        # 頻度の高い順に取得
        common_classes = [cls for cls, _ in class_counts.most_common(20)]
        return common_classes

    def extract_layout_patterns(self) -> Dict[str, bool]:
        """レイアウトパターンを検出"""
        patterns = {
            'uses_flexbox': bool(re.search(r'display:\s*flex', self.css_content)),
            'uses_grid': bool(re.search(r'display:\s*grid', self.css_content)),
            'uses_float': bool(re.search(r'float:\s*(left|right)', self.css_content)),
            'uses_position': bool(re.search(r'position:\s*(absolute|fixed|relative)', self.css_content)),
            'uses_transitions': bool(re.search(r'transition:', self.css_content)),
            'uses_animations': bool(re.search(r'@keyframes|animation:', self.css_content)),
        }
        return patterns

    def analyze(self) -> Dict:
        """CSS全体を分析"""
        return {
            'colors': self.extract_colors(),
            'fonts': self.extract_fonts(),
            'breakpoints': self.extract_breakpoints(),
            'common_classes': self.extract_common_classes(),
            'layout_patterns': self.extract_layout_patterns(),
            'total_size': len(self.css_content),
            'total_rules': len(re.findall(r'\{[^}]+\}', self.css_content))
        }

    def infer_color_scheme(self) -> Dict[str, str]:
        """主要な色を推測してカラースキームを作成"""
        colors = self.extract_colors()
        all_colors = colors['hex'] + colors['rgb']

        # デフォルトのカラースキーム
        color_scheme = {
            'primary': '#2563eb',
            'secondary': '#7c3aed',
            'background': '#ffffff',
            'text': '#1f2937',
            'accent': '#f59e0b'
        }

        # 実際の色から推測（簡易版）
        if all_colors:
            if len(all_colors) >= 1:
                color_scheme['primary'] = all_colors[0]
            if len(all_colors) >= 2:
                color_scheme['secondary'] = all_colors[1]
            if len(all_colors) >= 3:
                color_scheme['accent'] = all_colors[2]

        return color_scheme
