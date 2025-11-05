#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL分析エージェント - 参考サイトを分析してテンプレート設計データを作成
"""

import json
import os
import re
from typing import Dict, Optional
from agents.base_agent import BaseAgent
from utils.html_parser import HTMLParser
from utils.css_analyzer import CSSAnalyzer

class URLAnalyzerAgent(BaseAgent):
    """参考URLを分析してデザインパターンを抽出"""

    def __init__(self):
        super().__init__("URLAnalyzerAgent")

    def execute(self, url: str, output_dir: str = "analyzed_sites") -> Dict:
        """
        URLを分析してテンプレート設計データを生成

        Args:
            url: 分析対象のURL
            output_dir: 出力ディレクトリ

        Returns:
            テンプレート設計データ（辞書形式）
        """
        self.logger.info(f"🔍 Analyzing URL: {url}")

        # 1. HTML構造を解析
        html_parser = HTMLParser(url)
        if not html_parser.fetch():
            self.log_error(f"Failed to fetch URL: {url}")
            return self._get_default_template_data(url)

        structure = html_parser.extract_structure()
        self.log_success("HTML structure extracted")

        # 2. CSS解析
        css_analyzer = CSSAnalyzer(url)
        css_links = structure.get('links', [])[:5]  # 最初の5つのCSSファイル

        for css_link in css_links:
            css_analyzer.fetch_css(css_link)

        css_analysis = css_analyzer.analyze()
        self.log_success("CSS analysis completed")

        # 3. AIでデザインパターンを分析
        design_analysis = self._analyze_design_with_ai(structure, css_analysis)

        # 4. ページ構造を推測
        page_structure = self._infer_page_structure(structure)

        # 5. テンプレート設計データを生成
        template_data = {
            'source_url': url,
            'structure': structure,
            'css_analysis': css_analysis,
            'design_patterns': design_analysis,
            'page_structure': page_structure,
            'template_type': design_analysis.get('template_type', 'corporate')
        }

        # 6. 保存
        os.makedirs(output_dir, exist_ok=True)
        domain = url.split('//')[-1].split('/')[0].replace('.', '_').replace(':', '_')
        output_file = os.path.join(output_dir, f"{domain}_analysis.json")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)

        self.log_success(f"Template data saved: {output_file}")

        return template_data

    def _analyze_design_with_ai(self, structure: Dict, css: Dict) -> Dict:
        """AIを使ってデザインパターンを分析"""

        # ナビゲーション情報
        nav_items = structure.get('navigation', [])
        nav_text = ', '.join([item.get('text', '') for item in nav_items[:10]])

        # セクション情報
        sections = structure.get('sections', [])
        section_summary = []
        for sec in sections[:5]:
            headings = ', '.join(sec.get('headings', []))
            section_summary.append(f"- {headings[:50]}")

        # テキストコンテンツのサマリー
        text_content = structure.get('text_content', '')[:500]

        prompt = f"""
以下のWebサイトの構造とスタイル情報を分析して、デザインパターンを抽出してください。

【サイト情報】
- タイトル: {structure.get('title', 'N/A')}
- メタ説明: {structure.get('meta_description', 'N/A')[:100]}
- ナビゲーション: {nav_text}

【セクション構造】
{chr(10).join(section_summary[:5])}

【CSS情報】
- カラーパレット: {css.get('colors', {}).get('hex', [])[:5]}
- フォント: {css.get('fonts', [])[:3]}
- レスポンシブブレークポイント: {css.get('breakpoints', [])}
- レイアウト: Flexbox={css.get('layout_patterns', {}).get('uses_flexbox', False)}, Grid={css.get('layout_patterns', {}).get('uses_grid', False)}

【コンテンツサンプル】
{text_content}

以下の形式でJSON形式で回答してください（JSON以外の説明文は不要）：
{{
  "template_type": "corporate | startup | portfolio | landing | service",
  "color_scheme": {{
    "primary": "#色コード",
    "secondary": "#色コード",
    "background": "#色コード",
    "text": "#色コード",
    "accent": "#色コード"
  }},
  "layout_structure": {{
    "header_style": "固定ヘッダー with ロゴとナビゲーション",
    "hero_section": "フルワイドヒーロー with 背景画像",
    "content_layout": "2カラムまたは3カラムグリッド",
    "footer_style": "マルチカラムフッター"
  }},
  "design_characteristics": ["モダン", "クリーン", "プロフェッショナル"],
  "recommended_sections": ["hero", "services", "features", "about", "contact"],
  "typography": {{
    "heading_font": "フォント名",
    "body_font": "フォント名",
    "font_scale": "large | medium | small"
  }}
}}
"""

        system_prompt = """あなたはWebデザイン分析の専門家です。
Webサイトの構造とスタイルを分析し、再利用可能なデザインパターンを抽出します。
必ずJSON形式のみで回答してください。説明文やマークダウンは含めないでください。"""

        try:
            response = self.call_claude(prompt, system_prompt=system_prompt, max_tokens=2000)

            # JSONを抽出（マークダウンのコードブロックを除去）
            response = response.strip()
            response = re.sub(r'^```json\s*', '', response)
            response = re.sub(r'^```\s*', '', response)
            response = re.sub(r'\s*```$', '', response)

            # JSONをパース
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                design_data = json.loads(json_match.group())
                self.log_success("AI design analysis completed")
                return design_data
            else:
                self.log_warning("AI response is not valid JSON, using defaults")
                return self._get_default_design_pattern(css)

        except json.JSONDecodeError as e:
            self.log_error(f"JSON parsing failed: {e}")
            return self._get_default_design_pattern(css)
        except Exception as e:
            self.log_error(f"AI analysis failed: {e}")
            return self._get_default_design_pattern(css)

    def _infer_page_structure(self, structure: Dict) -> Dict:
        """ページ構造を推測（複数ページ対応のため）"""
        nav_items = structure.get('navigation', [])
        internal_links = structure.get('internal_links', [])

        # ナビゲーションから推測されるページ
        suggested_pages = {
            'index': {'title': 'ホーム', 'priority': 1},
        }

        # ナビゲーションアイテムから推測
        for item in nav_items:
            text = item.get('text', '').lower()
            href = item.get('href', '')

            if any(keyword in text for keyword in ['home', 'ホーム', 'トップ']):
                suggested_pages['index'] = {'title': item.get('text', 'ホーム'), 'priority': 1}
            elif any(keyword in text for keyword in ['about', '会社概要', '企業情報', '私たちについて']):
                suggested_pages['about'] = {'title': item.get('text', '会社概要'), 'priority': 2}
            elif any(keyword in text for keyword in ['service', 'サービス', '事業内容', '業務内容']):
                suggested_pages['services'] = {'title': item.get('text', 'サービス'), 'priority': 3}
            elif any(keyword in text for keyword in ['case', '実績', '事例', 'portfolio']):
                suggested_pages['cases'] = {'title': item.get('text', '実績・事例'), 'priority': 4}
            elif any(keyword in text for keyword in ['contact', 'お問い合わせ', '問合せ', '連絡']):
                suggested_pages['contact'] = {'title': item.get('text', 'お問い合わせ'), 'priority': 5}

        return {
            'suggested_pages': suggested_pages,
            'has_multi_page': len(suggested_pages) > 1,
            'navigation_items': nav_items
        }

    def _get_default_design_pattern(self, css: Dict) -> Dict:
        """デフォルトのデザインパターン（CSSから推測）"""
        color_scheme = css.get('colors', {}).get('hex', [])
        fonts = css.get('fonts', [])

        # CSSから色を取得、なければデフォルト
        primary_color = color_scheme[0] if color_scheme else '#2563eb'
        secondary_color = color_scheme[1] if len(color_scheme) > 1 else '#7c3aed'
        accent_color = color_scheme[2] if len(color_scheme) > 2 else '#f59e0b'

        return {
            'template_type': 'corporate',
            'color_scheme': {
                'primary': primary_color,
                'secondary': secondary_color,
                'background': '#ffffff',
                'text': '#1f2937',
                'accent': accent_color
            },
            'layout_structure': {
                'header_style': 'Fixed navigation with logo and menu',
                'hero_section': 'Full-width hero with image and CTA',
                'content_layout': '3-column grid layout',
                'footer_style': 'Multi-column footer with links'
            },
            'design_characteristics': ['Modern', 'Clean', 'Professional'],
            'recommended_sections': ['hero', 'features', 'services', 'about', 'contact'],
            'typography': {
                'heading_font': fonts[0] if fonts else 'sans-serif',
                'body_font': fonts[1] if len(fonts) > 1 else 'sans-serif',
                'font_scale': 'medium'
            }
        }

    def _get_default_template_data(self, url: str) -> Dict:
        """デフォルトのテンプレートデータ（フェッチ失敗時）"""
        self.log_warning("Using default template data")

        return {
            'source_url': url,
            'structure': {},
            'css_analysis': {},
            'design_patterns': self._get_default_design_pattern({}),
            'page_structure': {
                'suggested_pages': {
                    'index': {'title': 'ホーム', 'priority': 1},
                    'about': {'title': '会社概要', 'priority': 2},
                    'services': {'title': 'サービス', 'priority': 3},
                    'contact': {'title': 'お問い合わせ', 'priority': 4}
                },
                'has_multi_page': True,
                'navigation_items': []
            },
            'template_type': 'corporate'
        }


# 動作確認用
if __name__ == '__main__':
    agent = URLAnalyzerAgent()

    # テスト用URL（公開されている企業サイト）
    test_url = "https://www.example.com"

    print(f"\n🔍 Analyzing: {test_url}\n")
    result = agent.execute(test_url)

    print("\n📊 Analysis Result:")
    print(f"Template Type: {result.get('template_type')}")
    print(f"Suggested Pages: {list(result.get('page_structure', {}).get('suggested_pages', {}).keys())}")
    print(f"Color Scheme: {result.get('design_patterns', {}).get('color_scheme', {})}")
