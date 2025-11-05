#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Agent Homepage Builder - メインスクリプト

完全な複数ページWebサイトを生成します
"""

import sys
import os
from pathlib import Path

# エージェントをインポート
from agents.url_analyzer import URLAnalyzerAgent
from agents.content_manager import ContentManagerAgent
from agents.page_generator import PageGeneratorAgent


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     AI Agent Homepage Builder                             ║
║     複数ページWebサイト自動生成システム                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

    # 使い方を表示
    if len(sys.argv) < 2:
        print("""
使い方:
  python main.py <reference_url> <project_name>

例:
  python main.py https://example.com my_company

または CLIツールを使用:
  python cli.py init my_company         # プロジェクト初期化
  python cli.py analyze <URL>           # URL分析
  python cli.py generate my_company     # サイト生成
  python cli.py preview my_company      # プレビュー

詳細: python cli.py --help
        """)
        return

    reference_url = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) > 2 else 'my_website'

    print(f"\n🚀 Starting website generation...")
    print(f"📍 Reference URL: {reference_url}")
    print(f"📁 Project: {project_name}\n")

    # Step 1: URL分析
    print("=" * 60)
    print("Step 1/3: Analyzing reference website...")
    print("=" * 60 + "\n")

    analyzer = URLAnalyzerAgent()
    template_data = analyzer.execute(reference_url)

    if not template_data or not template_data.get('design_patterns'):
        print("\n⚠️  Warning: Analysis incomplete. Using default template.")

    # Step 2: コンテンツ準備
    print("\n" + "=" * 60)
    print("Step 2/3: Preparing content...")
    print("=" * 60 + "\n")

    content_manager = ContentManagerAgent()

    # サンプルコンテンツ
    content_manager.add_company_info('company_name', 'Your Company Name')
    content_manager.add_company_info('tagline', 'Your Success Partner')
    content_manager.add_company_info('description',
                                     'We provide professional services to help your business succeed.')

    # 各ページのセクション
    content_manager.add_section('index', 'hero', 'Welcome',
                               'Transform your business with our innovative solutions')
    content_manager.add_section('index', 'features', 'Our Services',
                               'Comprehensive solutions tailored to your needs')

    content_manager.add_section('about', 'company', 'About Us',
                               'We are a team of dedicated professionals')

    content_manager.add_section('services', 'service_list', 'Our Services',
                               'Expert consulting, development, and support')

    content_manager.add_section('contact', 'contact_form', 'Get in Touch',
                               'We would love to hear from you')

    print("✅ Sample content created")

    # Step 3: サイト生成
    print("\n" + "=" * 60)
    print("Step 3/3: Generating website...")
    print("=" * 60 + "\n")

    generator = PageGeneratorAgent()

    output_dir = f"output/{project_name}"
    result = generator.execute(
        template_data=template_data,
        content_map=content_manager.get_content_map(),
        output_dir=output_dir,
        pages=['index', 'about', 'services', 'contact']
    )

    # 完了メッセージ
    print("\n" + "=" * 60)
    print("🎉 Website Generation Complete!")
    print("=" * 60)
    print(f"\n📁 Output directory: {output_dir}")
    print(f"📄 Generated pages:")
    for page, path in result['pages'].items():
        print(f"   - {page}.html")

    print(f"\n🌐 Preview your website:")
    print(f"   python cli.py preview {project_name}")
    print(f"\n   Or open directly:")
    print(f"   file://{Path(output_dir).absolute()}/index.html")

    print(f"\n💡 Customize your content:")
    print(f"   1. Edit: user_materials/texts/{project_name}.yaml")
    print(f"   2. Regenerate: python cli.py generate {project_name}")

    print("\n✨ Thank you for using AI Agent Homepage Builder!\n")


if __name__ == '__main__':
    main()
