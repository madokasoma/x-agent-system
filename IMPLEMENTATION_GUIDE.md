# AI Agent Homepage Builder - 実装ガイド

## 📚 目次

1. [セットアップ](#セットアップ)
2. [ステップ1: プロジェクト基礎構築](#ステップ1-プロジェクト基礎構築)
3. [ステップ2: URL分析エージェント](#ステップ2-url分析エージェント)
4. [ステップ3: コンテンツ管理エージェント](#ステップ3-コンテンツ管理エージェント)
5. [ステップ4: ページ生成エージェント](#ステップ4-ページ生成エージェント)
6. [ステップ5: プレビュー機能](#ステップ5-プレビュー機能)
7. [テスト方法](#テスト方法)
8. [トラブルシューティング](#トラブルシューティング)

---

## セットアップ

### 1. 必要な環境

```bash
# Python 3.10以上
python3 --version

# pip アップデート
pip install --upgrade pip
```

### 2. 依存パッケージのインストール

```bash
# requirements.txt を作成
cat > requirements.txt << 'EOF'
# Core Dependencies
anthropic>=0.18.0
openai>=1.10.0
beautifulsoup4>=4.12.0
requests>=2.31.0
Pillow>=10.0.0
Jinja2>=3.1.2
PyYAML>=6.0

# Web Framework (Optional)
flask>=3.0.0

# Development Tools
python-dotenv>=1.0.0
pytest>=7.4.0
black>=23.0.0
EOF

# インストール
pip install -r requirements.txt
```

### 3. 環境変数の設定

```bash
# .env ファイルを作成
cat > .env << 'EOF'
# Anthropic Claude API
ANTHROPIC_API_KEY=your_api_key_here

# OpenAI API (Optional)
OPENAI_API_KEY=your_api_key_here

# Settings
DEBUG=True
OUTPUT_DIR=output
EOF

# .gitignore に追加
echo ".env" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "output/" >> .gitignore
echo "analyzed_sites/" >> .gitignore
echo "user_materials/" >> .gitignore
```

---

## ステップ1: プロジェクト基礎構築

### 1-1. ディレクトリ構造の作成

```bash
# プロジェクトディレクトリを作成
mkdir -p agents utils templates/base templates/generated static/{css,js,images}
mkdir -p user_materials/{texts,images,logos} analyzed_sites output config

# __init__.py を作成
touch agents/__init__.py utils/__init__.py
```

### 1-2. 設定ファイル作成

**config/config.yaml**
```yaml
# AI Agent Homepage Builder - 設定ファイル

# API設定
api:
  anthropic:
    model: "claude-3-5-sonnet-20241022"
    max_tokens: 4096
    temperature: 0.7

  openai:
    model: "gpt-4-turbo-preview"
    max_tokens: 2048

# 出力設定
output:
  directory: "output"
  image_quality: 85
  image_max_width: 1920
  image_format: "webp"

# 分析設定
analysis:
  timeout: 30
  user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  max_retries: 3

# 生成設定
generation:
  responsive_breakpoints:
    mobile: 768
    tablet: 1024
    desktop: 1280

  seo:
    generate_sitemap: true
    generate_robots_txt: true
    add_structured_data: true
```

### 1-3. ベースエージェントクラス作成

**agents/base_agent.py**
```python
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
```

---

## ステップ2: URL分析エージェント

### 2-1. ユーティリティ: HTML/CSS解析

**utils/html_parser.py**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML解析ユーティリティ
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import re

class HTMLParser:
    """HTML構造を解析"""

    def __init__(self, url: str, timeout: int = 30):
        self.url = url
        self.timeout = timeout
        self.soup = None
        self.html = None

    def fetch(self) -> bool:
        """URLからHTMLを取得"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            self.html = response.text
            self.soup = BeautifulSoup(self.html, 'html.parser')
            return True

        except Exception as e:
            print(f"❌ Error fetching URL: {e}")
            return False

    def extract_structure(self) -> Dict:
        """サイト構造を抽出"""
        if not self.soup:
            return {}

        structure = {
            'title': self.soup.title.string if self.soup.title else '',
            'meta_description': self._get_meta_description(),
            'sections': self._extract_sections(),
            'navigation': self._extract_navigation(),
            'footer': self._extract_footer(),
            'images': self._extract_images(),
            'links': self._extract_links(),
        }

        return structure

    def _get_meta_description(self) -> str:
        """メタディスクリプションを取得"""
        meta = self.soup.find('meta', attrs={'name': 'description'})
        return meta['content'] if meta and 'content' in meta.attrs else ''

    def _extract_sections(self) -> List[Dict]:
        """主要セクションを抽出"""
        sections = []

        # header, main, section, article, aside, footer などを探す
        for tag in self.soup.find_all(['header', 'main', 'section', 'article']):
            section_data = {
                'tag': tag.name,
                'id': tag.get('id', ''),
                'class': ' '.join(tag.get('class', [])),
                'text_preview': tag.get_text(strip=True)[:100],
                'has_image': bool(tag.find('img')),
                'headings': [h.get_text(strip=True) for h in tag.find_all(['h1', 'h2', 'h3'])]
            }
            sections.append(section_data)

        return sections

    def _extract_navigation(self) -> List[str]:
        """ナビゲーションメニューを抽出"""
        nav_items = []
        nav = self.soup.find('nav')

        if nav:
            for link in nav.find_all('a'):
                text = link.get_text(strip=True)
                if text:
                    nav_items.append(text)

        return nav_items

    def _extract_footer(self) -> Dict:
        """フッター情報を抽出"""
        footer = self.soup.find('footer')
        if not footer:
            return {}

        return {
            'text': footer.get_text(strip=True)[:200],
            'links': [a.get_text(strip=True) for a in footer.find_all('a')]
        }

    def _extract_images(self) -> List[Dict]:
        """画像情報を抽出"""
        images = []
        for img in self.soup.find_all('img')[:10]:  # 最初の10枚
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'width': img.get('width', ''),
                'height': img.get('height', '')
            })
        return images

    def _extract_links(self) -> List[str]:
        """外部スタイルシートのリンクを抽出"""
        links = []
        for link in self.soup.find_all('link', rel='stylesheet'):
            href = link.get('href', '')
            if href:
                links.append(href)
        return links
```

**utils/css_analyzer.py**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSS解析ユーティリティ
"""

import re
import requests
from typing import Dict, List
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

            response = requests.get(full_url, timeout=10)
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
            'named': []
        }

        # HEX色 (#fff, #ffffff)
        hex_colors = re.findall(r'#[0-9a-fA-F]{3,6}', self.css_content)
        colors['hex'] = list(set(hex_colors))[:10]

        # RGB色
        rgb_colors = re.findall(r'rgb\([^)]+\)', self.css_content)
        colors['rgb'] = list(set(rgb_colors))[:10]

        # 名前付き色
        named_pattern = r'\b(red|blue|green|white|black|gray|yellow|orange|purple|pink)\b'
        named_colors = re.findall(named_pattern, self.css_content, re.IGNORECASE)
        colors['named'] = list(set(named_colors))

        return colors

    def extract_fonts(self) -> List[str]:
        """フォント情報を抽出"""
        font_families = re.findall(r'font-family:\s*([^;}]+)', self.css_content)

        # クリーンアップ
        fonts = []
        for font in font_families:
            font = font.strip().replace('"', '').replace("'", '')
            fonts.append(font)

        return list(set(fonts))[:5]

    def extract_breakpoints(self) -> List[int]:
        """レスポンシブのブレークポイントを抽出"""
        media_queries = re.findall(r'@media[^{]+\((?:min|max)-width:\s*(\d+)px\)', self.css_content)

        breakpoints = [int(bp) for bp in media_queries]
        return sorted(list(set(breakpoints)))

    def analyze(self) -> Dict:
        """CSS全体を分析"""
        return {
            'colors': self.extract_colors(),
            'fonts': self.extract_fonts(),
            'breakpoints': self.extract_breakpoints(),
            'total_size': len(self.css_content)
        }
```

### 2-2. URL分析エージェント実装

**agents/url_analyzer.py**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL分析エージェント - 参考サイトを分析してテンプレート設計データを作成
"""

import json
import os
from typing import Dict
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
            return {}

        structure = html_parser.extract_structure()
        self.log_success("HTML structure extracted")

        # 2. CSS解析
        css_analyzer = CSSAnalyzer(url)
        for css_link in structure.get('links', []):
            css_analyzer.fetch_css(css_link)

        css_analysis = css_analyzer.analyze()
        self.log_success("CSS analysis completed")

        # 3. AIでデザインパターンを分析
        design_analysis = self._analyze_design_with_ai(structure, css_analysis)

        # 4. テンプレート設計データを生成
        template_data = {
            'source_url': url,
            'structure': structure,
            'css_analysis': css_analysis,
            'design_patterns': design_analysis,
            'template_type': design_analysis.get('template_type', 'corporate')
        }

        # 5. 保存
        os.makedirs(output_dir, exist_ok=True)
        domain = url.split('//')[-1].split('/')[0].replace('.', '_')
        output_file = os.path.join(output_dir, f"{domain}_analysis.json")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)

        self.log_success(f"Template data saved: {output_file}")

        return template_data

    def _analyze_design_with_ai(self, structure: Dict, css: Dict) -> Dict:
        """AIを使ってデザインパターンを分析"""

        prompt = f"""
以下のWebサイトの構造とスタイル情報を分析して、デザインパターンを抽出してください。

【サイト構造】
- タイトル: {structure.get('title', 'N/A')}
- セクション数: {len(structure.get('sections', []))}
- ナビゲーション: {', '.join(structure.get('navigation', []))}

【CSS情報】
- カラーパレット: {css.get('colors', {}).get('hex', [])[:5]}
- フォント: {css.get('fonts', [])}
- レスポンシブブレークポイント: {css.get('breakpoints', [])}

以下の形式でJSON形式で回答してください：
{{
  "template_type": "corporate | startup | portfolio | landing",
  "color_scheme": {{
    "primary": "#色コード",
    "secondary": "#色コード",
    "background": "#色コード",
    "text": "#色コード"
  }},
  "layout_structure": {{
    "header_style": "説明",
    "hero_section": "説明",
    "content_layout": "説明",
    "footer_style": "説明"
  }},
  "design_characteristics": ["特徴1", "特徴2", "特徴3"],
  "recommended_sections": ["section1", "section2", "section3"]
}}
"""

        system_prompt = """あなたはWebデザイン分析の専門家です。
Webサイトの構造とスタイルを分析し、再利用可能なデザインパターンを抽出します。
常にJSON形式で回答してください。"""

        try:
            response = self.call_claude(prompt, system_prompt=system_prompt)

            # JSONを抽出
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                self.log_warning("AI response is not valid JSON, using defaults")
                return self._get_default_design_pattern()

        except Exception as e:
            self.log_error(f"AI analysis failed: {e}")
            return self._get_default_design_pattern()

    def _get_default_design_pattern(self) -> Dict:
        """デフォルトのデザインパターン"""
        return {
            'template_type': 'corporate',
            'color_scheme': {
                'primary': '#2563eb',
                'secondary': '#7c3aed',
                'background': '#ffffff',
                'text': '#1f2937'
            },
            'layout_structure': {
                'header_style': 'Fixed navigation with logo',
                'hero_section': 'Full-width hero with image and CTA',
                'content_layout': '3-column grid layout',
                'footer_style': 'Multi-column footer with links'
            },
            'design_characteristics': ['Modern', 'Clean', 'Professional'],
            'recommended_sections': ['hero', 'features', 'about', 'contact']
        }


# 動作確認用
if __name__ == '__main__':
    import re

    agent = URLAnalyzerAgent()

    # テスト用URL
    test_url = "https://www.example.com"

    result = agent.execute(test_url)
    print("\n📊 Analysis Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

## ステップ3: コンテンツ管理エージェント

**agents/content_manager.py**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コンテンツ管理エージェント - ユーザーの素材を管理
"""

import os
import json
from typing import Dict, List
from PIL import Image
from agents.base_agent import BaseAgent

class ContentManagerAgent(BaseAgent):
    """ユーザー素材の管理とマッピング"""

    def __init__(self):
        super().__init__("ContentManagerAgent")
        self.content_map = {
            'company_info': {},
            'texts': {},
            'images': {},
            'sections': []
        }

    def add_text(self, key: str, value: str, category: str = 'texts'):
        """テキストコンテンツを追加"""
        if category == 'company_info':
            self.content_map['company_info'][key] = value
        else:
            self.content_map['texts'][key] = value

        self.log_success(f"Text added: {key}")

    def add_image(self, key: str, image_path: str, optimize: bool = True):
        """画像を追加（最適化オプション付き）"""
        if not os.path.exists(image_path):
            self.log_error(f"Image not found: {image_path}")
            return False

        # 画像最適化
        if optimize:
            optimized_path = self._optimize_image(image_path)
            self.content_map['images'][key] = optimized_path
        else:
            self.content_map['images'][key] = image_path

        self.log_success(f"Image added: {key}")
        return True

    def add_section(self, section_type: str, title: str, content: str):
        """セクションを追加"""
        section = {
            'type': section_type,
            'title': title,
            'content': content
        }
        self.content_map['sections'].append(section)
        self.log_success(f"Section added: {section_type}")

    def _optimize_image(self, image_path: str, max_width: int = 1920,
                       quality: int = 85) -> str:
        """画像を最適化"""
        try:
            img = Image.open(image_path)

            # リサイズ
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # 保存
            base, ext = os.path.splitext(image_path)
            optimized_path = f"{base}_optimized{ext}"

            img.save(optimized_path, quality=quality, optimize=True)

            self.log_success(f"Image optimized: {optimized_path}")
            return optimized_path

        except Exception as e:
            self.log_error(f"Image optimization failed: {e}")
            return image_path

    def get_content_map(self) -> Dict:
        """コンテンツマップを取得"""
        return self.content_map

    def save_content_map(self, output_file: str):
        """コンテンツマップを保存"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.content_map, f, ensure_ascii=False, indent=2)

        self.log_success(f"Content map saved: {output_file}")

    def execute(self, content_file: str) -> Dict:
        """
        YAMLまたはJSONファイルからコンテンツを読み込み

        Args:
            content_file: コンテンツファイルのパス

        Returns:
            コンテンツマップ
        """
        # 実装は省略（YAMLパーサーを追加する必要がある）
        pass


# 使用例
if __name__ == '__main__':
    agent = ContentManagerAgent()

    # 会社情報
    agent.add_text('company_name', 'マイカンパニー株式会社', category='company_info')
    agent.add_text('tagline', 'イノベーションで未来を創る', category='company_info')
    agent.add_text('description', '私たちは最先端のAI技術で、ビジネスの課題を解決します。')

    # セクション
    agent.add_section('features', 'サービスの特徴', '高品質なAIソリューションを提供')

    # コンテンツマップを表示
    print(json.dumps(agent.get_content_map(), indent=2, ensure_ascii=False))
```

---

## ステップ4: ページ生成エージェント

**agents/page_generator.py**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ページ生成エージェント - HTML/CSS/JSを生成
"""

import os
import json
from typing import Dict
from jinja2 import Template
from agents.base_agent import BaseAgent

class PageGeneratorAgent(BaseAgent):
    """HTMLページを生成"""

    def __init__(self):
        super().__init__("PageGeneratorAgent")

    def execute(self, template_data: Dict, content_map: Dict,
               output_dir: str) -> str:
        """
        ホームページを生成

        Args:
            template_data: テンプレート設計データ
            content_map: コンテンツマップ
            output_dir: 出力ディレクトリ

        Returns:
            生成されたindex.htmlのパス
        """
        self.logger.info("🎨 Generating homepage...")

        # 出力ディレクトリ作成
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'css'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'js'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)

        # 1. HTMLを生成
        html_content = self._generate_html(template_data, content_map)
        html_file = os.path.join(output_dir, 'index.html')

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        self.log_success(f"HTML generated: {html_file}")

        # 2. CSSを生成
        css_content = self._generate_css(template_data)
        css_file = os.path.join(output_dir, 'css', 'style.css')

        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)

        self.log_success(f"CSS generated: {css_file}")

        # 3. JavaScriptを生成（オプション）
        js_content = self._generate_js()
        js_file = os.path.join(output_dir, 'js', 'main.js')

        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)

        self.log_success(f"JavaScript generated: {js_file}")

        return html_file

    def _generate_html(self, template_data: Dict, content_map: Dict) -> str:
        """HTMLを生成（AIを使用）"""

        prompt = f"""
以下の情報を元に、モダンでレスポンシブなHTML5のホームページを生成してください。

【デザインパターン】
{json.dumps(template_data.get('design_patterns', {}), indent=2, ensure_ascii=False)}

【コンテンツ】
会社名: {content_map.get('company_info', {}).get('company_name', '')}
キャッチコピー: {content_map.get('company_info', {}).get('tagline', '')}
説明: {content_map.get('texts', {}).get('description', '')}

【要件】
- セマンティックHTML5を使用
- レスポンシブデザイン（モバイルファースト）
- アクセシビリティ対応（ARIA属性）
- 外部CSS（css/style.css）と外部JS（js/main.js）を読み込み
- 必要なセクション: ヘッダー、ヒーロー、特徴、フッター

完全なHTML コードのみを出力してください（説明不要）。
"""

        system_prompt = """あなたはプロのフロントエンドエンジニアです。
モダンで美しく、SEOに最適化されたHTMLコードを生成します。
コードのみを出力し、説明やマークダウンは含めないでください。"""

        try:
            html = self.call_claude(prompt, system_prompt=system_prompt, max_tokens=8000)

            # マークダウンのコードブロックを除去
            html = html.replace('```html', '').replace('```', '').strip()

            return html

        except Exception as e:
            self.log_error(f"HTML generation failed: {e}")
            return self._get_default_html(content_map)

    def _generate_css(self, template_data: Dict) -> str:
        """CSSを生成（AIを使用）"""

        design = template_data.get('design_patterns', {})
        color_scheme = design.get('color_scheme', {})

        prompt = f"""
以下のデザイン要件を満たすCSSコードを生成してください。

【カラースキーム】
{json.dumps(color_scheme, indent=2)}

【デザイン特性】
{', '.join(design.get('design_characteristics', []))}

【要件】
- モダンCSS（Flexbox/Grid使用）
- レスポンシブデザイン（768px, 1024pxブレークポイント）
- スムーズなアニメーション
- 読みやすいタイポグラフィ
- アクセシブルなコントラスト比

完全なCSSコードのみを出力してください（説明不要）。
"""

        system_prompt = """あなたはプロのCSSデザイナーです。
モダンで美しく、パフォーマンスの良いCSSコードを生成します。
コードのみを出力してください。"""

        try:
            css = self.call_claude(prompt, system_prompt=system_prompt, max_tokens=6000)

            # マークダウンのコードブロックを除去
            css = css.replace('```css', '').replace('```', '').strip()

            return css

        except Exception as e:
            self.log_error(f"CSS generation failed: {e}")
            return self._get_default_css()

    def _generate_js(self) -> str:
        """基本的なJavaScriptを生成"""
        return """
// スムーズスクロール
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// ハンバーガーメニュー
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const nav = document.querySelector('nav');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        nav.classList.toggle('active');
    });
}

console.log('✅ Homepage loaded successfully');
"""

    def _get_default_html(self, content_map: Dict) -> str:
        """デフォルトHTML（フォールバック）"""
        company_name = content_map.get('company_info', {}).get('company_name', 'My Company')
        tagline = content_map.get('company_info', {}).get('tagline', 'Welcome')

        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav>
            <div class="container">
                <h1>{company_name}</h1>
            </div>
        </nav>
    </header>

    <main>
        <section class="hero">
            <div class="container">
                <h2>{tagline}</h2>
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 {company_name}. All rights reserved.</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""

    def _get_default_css(self) -> str:
        """デフォルトCSS（フォールバック）"""
        return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

header {
    background: #2563eb;
    color: white;
    padding: 1rem 0;
}

.hero {
    padding: 4rem 0;
    text-align: center;
    background: #f3f4f6;
}

footer {
    background: #1f2937;
    color: white;
    text-align: center;
    padding: 2rem 0;
}
"""


# 動作確認
if __name__ == '__main__':
    agent = PageGeneratorAgent()

    # テストデータ
    template_data = {
        'design_patterns': {
            'color_scheme': {
                'primary': '#2563eb',
                'secondary': '#7c3aed'
            },
            'design_characteristics': ['Modern', 'Clean']
        }
    }

    content_map = {
        'company_info': {
            'company_name': 'テスト株式会社',
            'tagline': 'テストサイトへようこそ'
        }
    }

    output = agent.execute(template_data, content_map, 'output/test_site')
    print(f"✅ Generated: {output}")
```

---

## ステップ5: プレビュー機能

**cli.py - コマンドラインインターフェース**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI インターフェース - コマンドラインから使用
"""

import argparse
import os
import http.server
import socketserver
from agents.url_analyzer import URLAnalyzerAgent
from agents.content_manager import ContentManagerAgent
from agents.page_generator import PageGeneratorAgent

def analyze_command(args):
    """参考URLを分析"""
    agent = URLAnalyzerAgent()
    result = agent.execute(args.url, output_dir='analyzed_sites')
    print(f"\n✅ Analysis complete! Data saved to: analyzed_sites/")

def generate_command(args):
    """ホームページを生成"""
    # テンプレートデータを読み込み
    # コンテンツマップを作成
    # ページ生成
    print(f"🎨 Generating homepage for project: {args.project}")
    # 実装...

def preview_command(args):
    """生成したサイトをプレビュー"""
    output_dir = f"output/{args.project}"

    if not os.path.exists(output_dir):
        print(f"❌ Project not found: {args.project}")
        return

    PORT = 8000

    os.chdir(output_dir)

    Handler = http.server.SimpleHTTPRequestHandler

    print(f"\n🌐 Preview server starting...")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"📁 Directory: {output_dir}")
    print(f"\n⌨️  Press Ctrl+C to stop\n")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

def main():
    parser = argparse.ArgumentParser(description='AI Agent Homepage Builder')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # analyze コマンド
    parser_analyze = subparsers.add_parser('analyze', help='Analyze a reference URL')
    parser_analyze.add_argument('url', help='URL to analyze')
    parser_analyze.add_argument('--output', default='analyzed_sites', help='Output directory')

    # generate コマンド
    parser_generate = subparsers.add_parser('generate', help='Generate homepage')
    parser_generate.add_argument('project', help='Project name')

    # preview コマンド
    parser_preview = subparsers.add_parser('preview', help='Preview generated site')
    parser_preview.add_argument('project', help='Project name')

    args = parser.parse_args()

    if args.command == 'analyze':
        analyze_command(args)
    elif args.command == 'generate':
        generate_command(args)
    elif args.command == 'preview':
        preview_command(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

---

## テスト方法

### 1. URL分析のテスト
```bash
python cli.py analyze https://www.example.com
```

### 2. ホームページ生成のテスト
```python
# test_generation.py
from agents.url_analyzer import URLAnalyzerAgent
from agents.content_manager import ContentManagerAgent
from agents.page_generator import PageGeneratorAgent

# 1. URL分析
analyzer = URLAnalyzerAgent()
template_data = analyzer.execute('https://www.example.com')

# 2. コンテンツ準備
content_mgr = ContentManagerAgent()
content_mgr.add_text('company_name', 'マイカンパニー', category='company_info')
content_mgr.add_text('tagline', 'Innovation for the Future', category='company_info')

# 3. ページ生成
generator = PageGeneratorAgent()
output = generator.execute(
    template_data=template_data,
    content_map=content_mgr.get_content_map(),
    output_dir='output/my_project'
)

print(f"✅ Generated: {output}")
```

### 3. プレビュー
```bash
python cli.py preview my_project
# ブラウザで http://localhost:8000 を開く
```

---

## トラブルシューティング

### APIキーエラー
```
❌ Anthropic API key not configured
```
**解決策**: `.env` ファイルに正しいAPIキーを設定

### 画像最適化エラー
```
❌ Image optimization failed
```
**解決策**: Pillow が正しくインストールされているか確認

### CSS/HTML生成失敗
```
❌ AI analysis failed
```
**解決策**: プロンプトを調整するか、デフォルトテンプレートを使用

---

## 次のステップ

1. **基本実装の完了**: 上記コードを実装
2. **テスト**: 複数の参考サイトで動作確認
3. **改善**: 生成品質の向上
4. **拡張機能**: 複数ページ、フォーム機能等を追加

詳細な設計は `HOMEPAGE_BUILDER_DESIGN.md` を参照してください。
