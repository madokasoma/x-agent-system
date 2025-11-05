#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ページ生成エージェント - HTML/CSS/JSを生成（複数ページ対応）
"""

import os
import json
import re
import shutil
from typing import Dict, List
from agents.base_agent import BaseAgent

class PageGeneratorAgent(BaseAgent):
    """HTMLページを生成（複数ページ対応）"""

    def __init__(self):
        super().__init__("PageGeneratorAgent")

    def execute(self, template_data: Dict, content_map: Dict,
               output_dir: str, pages: List[str] = None) -> Dict:
        """
        ホームページを生成（複数ページ対応）

        Args:
            template_data: テンプレート設計データ
            content_map: コンテンツマップ
            output_dir: 出力ディレクトリ
            pages: 生成するページのリスト（None なら全ページ）

        Returns:
            生成されたファイルのパス情報
        """
        self.logger.info("🎨 Generating multi-page website...")

        # 出力ディレクトリ作成
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'css'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'js'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)

        # 生成するページのリスト
        if pages is None:
            pages = list(content_map.get('pages', {}).keys())
            if not pages:
                pages = ['index', 'about', 'services', 'contact']

        # ナビゲーション情報を生成
        navigation = self._generate_navigation(pages, content_map)

        # 共通CSSを生成
        css_content = self._generate_css(template_data)
        css_file = os.path.join(output_dir, 'css', 'style.css')
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        self.log_success(f"CSS generated: {css_file}")

        # 共通JavaScriptを生成
        js_content = self._generate_js()
        js_file = os.path.join(output_dir, 'js', 'main.js')
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        self.log_success(f"JavaScript generated: {js_file}")

        # 各ページを生成
        generated_files = {}
        for page in pages:
            page_content = content_map.get('pages', {}).get(page, {})
            html_content = self._generate_html_page(
                page_name=page,
                template_data=template_data,
                content_map=content_map,
                page_content=page_content,
                navigation=navigation
            )

            html_file = os.path.join(output_dir, f'{page}.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            generated_files[page] = html_file
            self.log_success(f"HTML generated: {html_file}")

        # 画像をコピー
        self._copy_images(content_map, output_dir)

        # サマリーを表示
        self.logger.info(f"\n✨ Website generated successfully!")
        self.logger.info(f"📁 Output directory: {output_dir}")
        self.logger.info(f"📄 Generated pages: {', '.join(pages)}")

        return {
            'output_dir': output_dir,
            'pages': generated_files,
            'css': css_file,
            'js': js_file
        }

    def _generate_navigation(self, pages: List[str], content_map: Dict) -> List[Dict]:
        """ナビゲーションメニューを生成"""
        navigation = []

        page_titles = {
            'index': 'ホーム',
            'about': '会社概要',
            'services': 'サービス',
            'cases': '実績・事例',
            'contact': 'お問い合わせ'
        }

        for page in pages:
            # ページタイトルを取得（content_mapから、またはデフォルト）
            page_data = content_map.get('pages', {}).get(page, {})
            title = page_data.get('title', page_titles.get(page, page.capitalize()))

            navigation.append({
                'page': page,
                'title': title,
                'href': f'{page}.html',
                'is_index': page == 'index'
            })

        return navigation

    def _generate_html_page(self, page_name: str, template_data: Dict,
                           content_map: Dict, page_content: Dict,
                           navigation: List[Dict]) -> str:
        """個別ページのHTMLを生成（AIを使用）"""

        company_info = content_map.get('company_info', {})
        design_patterns = template_data.get('design_patterns', {})
        sections = page_content.get('sections', [])

        # セクション情報をテキストに変換
        sections_text = "\n".join([
            f"- {s.get('type')}: {s.get('title')} - {s.get('content', '')[:100]}"
            for s in sections[:5]
        ])

        # ナビゲーションHTMLを生成
        nav_html = "\n".join([
            f'          <a href="{item["href"]}" class="{"active" if item["page"] == page_name else ""}">{item["title"]}</a>'
            for item in navigation
        ])

        prompt = f"""
以下の情報を元に、プロフェッショナルな企業Webサイトの{page_name}.htmlページを生成してください。

【ページ種類】
{page_name}ページ（{navigation[next((i for i, x in enumerate(navigation) if x['page'] == page_name), 0)]['title']}）

【会社情報】
- 会社名: {company_info.get('company_name', 'Company Name')}
- キャッチコピー: {company_info.get('tagline', 'Your Success, Our Mission')}
- 説明: {company_info.get('description', 'We provide professional services.')}

【デザイン要件】
- カラースキーム: {design_patterns.get('color_scheme', {})}
- デザインスタイル: {', '.join(design_patterns.get('design_characteristics', []))}

【このページのセクション】
{sections_text if sections_text else '（標準的な' + page_name + 'ページ構成を使用）'}

【ナビゲーションメニュー】
{nav_html}

【要件】
1. セマンティックHTML5を使用
2. レスポンシブデザイン（モバイルファースト）
3. 外部CSS（css/style.css）と外部JS（js/main.js）を読み込み
4. ナビゲーションは上記のHTMLをそのまま使用
5. {page_name}ページに適したセクション構成
   - index: ヒーロー、サービス概要、特徴、CTA
   - about: 会社概要、ビジョン、沿革、チーム
   - services: サービス一覧、詳細、料金
   - contact: お問い合わせフォーム、連絡先情報
6. プロフェッショナルで洗練されたデザイン
7. SEO最適化（適切なメタタグ）

完全なHTMLコードのみを出力してください（説明やマークダウン記号は不要）。
"""

        system_prompt = """あなたはプロのWebデザイナー・フロントエンドエンジニアです。
モダンで美しく、SEOに最適化されたHTMLコードを生成します。
コードのみを出力し、説明やマークダウンは含めないでください。"""

        try:
            html = self.call_claude(prompt, system_prompt=system_prompt, max_tokens=8000)

            # マークダウンのコードブロックを除去
            html = re.sub(r'^```html\s*', '', html.strip(), flags=re.MULTILINE)
            html = re.sub(r'^```\s*', '', html.strip(), flags=re.MULTILINE)
            html = re.sub(r'\s*```$', '', html.strip(), flags=re.MULTILINE)

            return html

        except Exception as e:
            self.log_error(f"HTML generation failed for {page_name}: {e}")
            return self._get_fallback_html(page_name, content_map, navigation)

    def _generate_css(self, template_data: Dict) -> str:
        """CSSを生成（AIを使用）"""

        design = template_data.get('design_patterns', {})
        color_scheme = design.get('color_scheme', {})

        prompt = f"""
以下のデザイン要件を満たす、プロフェッショナルな企業Webサイト用のCSSコードを生成してください。

【カラースキーム】
{json.dumps(color_scheme, indent=2, ensure_ascii=False)}

【デザイン特性】
{', '.join(design.get('design_characteristics', ['Modern', 'Clean', 'Professional']))}

【レイアウト要件】
{json.dumps(design.get('layout_structure', {}), indent=2, ensure_ascii=False)}

【要件】
1. モダンCSS（Flexbox/Grid使用）
2. レスポンシブデザイン（768px, 1024px, 1280pxブレークポイント）
3. スムーズなアニメーション・トランジション
4. 読みやすいタイポグラフィ
5. アクセシブルなコントラスト比
6. ホバーエフェクト
7. 共通スタイル:
   - ヘッダー（固定、ロゴ+ナビゲーション）
   - ヒーローセクション
   - コンテンツセクション
   - フッター
   - ボタン
   - フォーム
8. プロフェッショナルで洗練された見た目

完全なCSSコードのみを出力してください（説明不要）。
"""

        system_prompt = """あなたはプロのCSSデザイナーです。
モダンで美しく、パフォーマンスの良いCSSコードを生成します。
コードのみを出力してください。"""

        try:
            css = self.call_claude(prompt, system_prompt=system_prompt, max_tokens=6000)

            # マークダウンのコードブロックを除去
            css = re.sub(r'^```css\s*', '', css.strip(), flags=re.MULTILINE)
            css = re.sub(r'^```\s*', '', css.strip(), flags=re.MULTILINE)
            css = re.sub(r'\s*```$', '', css.strip(), flags=re.MULTILINE)

            return css

        except Exception as e:
            self.log_error(f"CSS generation failed: {e}")
            return self._get_fallback_css(color_scheme)

    def _generate_js(self) -> str:
        """基本的なJavaScriptを生成"""
        return """// Main JavaScript

// スムーズスクロール
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// モバイルメニュートグル
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const nav = document.querySelector('nav');
const navMenu = document.querySelector('nav ul');

if (mobileMenuBtn && navMenu) {
    mobileMenuBtn.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
    });
}

// フォームバリデーション（contactページ用）
const contactForm = document.querySelector('#contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // 簡易バリデーション
        const name = this.querySelector('[name="name"]').value;
        const email = this.querySelector('[name="email"]').value;
        const message = this.querySelector('[name="message"]').value;

        if (!name || !email || !message) {
            alert('すべての項目を入力してください。');
            return;
        }

        if (!email.includes('@')) {
            alert('正しいメールアドレスを入力してください。');
            return;
        }

        // 実際の送信処理（バックエンドが必要）
        alert('お問い合わせありがとうございます。後ほど担当者よりご連絡いたします。');
        this.reset();
    });
}

// アクティブナビゲーションのハイライト
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('nav a').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
        link.classList.add('active');
    }
});

// スクロールでヘッダーに影を追加
const header = document.querySelector('header');
if (header) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

console.log('✅ Website loaded successfully');
"""

    def _copy_images(self, content_map: Dict, output_dir: str):
        """画像ファイルをコピー"""
        images = content_map.get('images', {})
        images_dir = os.path.join(output_dir, 'images')

        for key, image_info in images.items():
            if isinstance(image_info, dict):
                source_path = image_info.get('path', '')
            else:
                source_path = image_info

            if source_path and os.path.exists(source_path):
                filename = os.path.basename(source_path)
                dest_path = os.path.join(images_dir, filename)

                try:
                    shutil.copy2(source_path, dest_path)
                    self.log_success(f"Image copied: {filename}")
                except Exception as e:
                    self.log_warning(f"Failed to copy image {filename}: {e}")

    def _get_fallback_html(self, page_name: str, content_map: Dict,
                          navigation: List[Dict]) -> str:
        """フォールバックHTML（AI生成失敗時）"""
        company_name = content_map.get('company_info', {}).get('company_name', 'My Company')
        tagline = content_map.get('company_info', {}).get('tagline', 'Your Success Partner')

        nav_html = "\n".join([
            f'          <a href="{item["href"]}" class="{"active" if item["page"] == page_name else ""}">{item["title"]}</a>'
            for item in navigation
        ])

        page_titles = {
            'index': 'ホーム',
            'about': '会社概要',
            'services': 'サービス',
            'contact': 'お問い合わせ'
        }

        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{company_name} - {tagline}">
    <title>{page_titles.get(page_name, page_name.capitalize())} | {company_name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">
                <h1>{company_name}</h1>
            </div>
            <nav>
{nav_html}
            </nav>
        </div>
    </header>

    <main>
        <section class="hero">
            <div class="container">
                <h2>{page_titles.get(page_name, page_name.capitalize())}</h2>
                <p>{tagline}</p>
            </div>
        </section>

        <section class="content">
            <div class="container">
                <p>このページは現在構築中です。</p>
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

    def _get_fallback_css(self, color_scheme: Dict) -> str:
        """フォールバックCSS（AI生成失敗時）"""
        primary = color_scheme.get('primary', '#2563eb')
        secondary = color_scheme.get('secondary', '#7c3aed')
        text = color_scheme.get('text', '#1f2937')

        return f"""/* Reset & Base Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: {text};
    background: #ffffff;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Header */
header {{
    background: #ffffff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
    padding: 1rem 0;
}}

header .container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

header .logo h1 {{
    color: {primary};
    font-size: 1.5rem;
}}

nav {{
    display: flex;
    gap: 2rem;
}}

nav a {{
    text-decoration: none;
    color: {text};
    font-weight: 500;
    transition: color 0.3s;
}}

nav a:hover,
nav a.active {{
    color: {primary};
}}

/* Hero */
.hero {{
    background: linear-gradient(135deg, {primary}, {secondary});
    color: white;
    padding: 6rem 0;
    text-align: center;
}}

.hero h2 {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.hero p {{
    font-size: 1.25rem;
    opacity: 0.9;
}}

/* Content */
.content {{
    padding: 4rem 0;
}}

/* Footer */
footer {{
    background: #1f2937;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 4rem;
}}

/* Responsive */
@media (max-width: 768px) {{
    nav {{
        flex-direction: column;
        gap: 1rem;
    }}

    .hero h2 {{
        font-size: 2rem;
    }}
}}
"""


# 動作確認
if __name__ == '__main__':
    from agents.url_analyzer import URLAnalyzerAgent
    from agents.content_manager import ContentManagerAgent

    print("\n🎨 Page Generator Agent - Test\n")

    # テストデータ
    template_data = {
        'design_patterns': {
            'color_scheme': {
                'primary': '#2563eb',
                'secondary': '#7c3aed',
                'text': '#1f2937'
            },
            'design_characteristics': ['Modern', 'Clean'],
            'layout_structure': {}
        }
    }

    content_mgr = ContentManagerAgent()
    content_mgr.add_company_info('company_name', 'テスト株式会社')
    content_mgr.add_company_info('tagline', 'Innovation for the Future')
    content_mgr.add_section('index', 'hero', 'ヒーロー', 'Welcome')

    generator = PageGeneratorAgent()
    result = generator.execute(
        template_data=template_data,
        content_map=content_mgr.get_content_map(),
        output_dir='output/test_multi_page',
        pages=['index', 'about', 'services', 'contact']
    )

    print(f"\n✅ Generated: {result}")
