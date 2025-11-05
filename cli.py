#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI インターフェース - コマンドラインから使用
"""

import argparse
import os
import http.server
import socketserver
import sys
import json
from pathlib import Path

# エージェントをインポート
from agents.url_analyzer import URLAnalyzerAgent
from agents.content_manager import ContentManagerAgent
from agents.page_generator import PageGeneratorAgent


def analyze_command(args):
    """参考URLを分析"""
    print(f"\n🔍 Analyzing URL: {args.url}\n")

    agent = URLAnalyzerAgent()
    result = agent.execute(args.url, output_dir=args.output)

    print(f"\n✅ Analysis complete!")
    print(f"📁 Data saved to: {args.output}/")
    print(f"📊 Template type: {result.get('template_type')}")

    if result.get('page_structure'):
        pages = result['page_structure'].get('suggested_pages', {})
        print(f"📄 Suggested pages: {', '.join(pages.keys())}")

    print(f"\n💡 Next step: Run 'python cli.py generate {args.project}' to create the website")


def generate_command(args):
    """ホームページを生成"""
    print(f"\n🎨 Generating website for project: {args.project}\n")

    # テンプレートデータを読み込み
    analyzed_dir = Path('analyzed_sites')
    template_file = None

    if analyzed_dir.exists():
        # 最新の分析ファイルを探す
        json_files = list(analyzed_dir.glob('*.json'))
        if json_files:
            template_file = max(json_files, key=lambda p: p.stat().st_mtime)
            print(f"📄 Using template: {template_file.name}")

    if not template_file or not template_file.exists():
        print("⚠️  No analyzed template found. Using default template.")
        template_data = {
            'design_patterns': {
                'color_scheme': {
                    'primary': '#2563eb',
                    'secondary': '#7c3aed',
                    'text': '#1f2937'
                },
                'design_characteristics': ['Modern', 'Professional'],
                'layout_structure': {}
            }
        }
    else:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_data = json.load(f)

    # コンテンツを準備
    content_manager = ContentManagerAgent()

    # YAMLファイルがあれば読み込み
    content_yaml = Path('user_materials') / 'texts' / f'{args.project}.yaml'
    if content_yaml.exists():
        print(f"📝 Loading content from: {content_yaml}")
        content_manager.load_from_yaml(str(content_yaml))
    else:
        # デフォルトコンテンツ
        print("⚠️  No content YAML found. Using sample content.")
        content_manager.add_company_info('company_name', 'Your Company')
        content_manager.add_company_info('tagline', 'Your Success Partner')
        content_manager.add_section('index', 'hero', 'Welcome', 'We help your business grow')

    # ページ生成
    generator = PageGeneratorAgent()

    pages = args.pages.split(',') if args.pages else ['index', 'about', 'services', 'contact']

    output_dir = f"output/{args.project}"
    result = generator.execute(
        template_data=template_data,
        content_map=content_manager.get_content_map(),
        output_dir=output_dir,
        pages=pages
    )

    print(f"\n✅ Website generated successfully!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📄 Generated pages: {', '.join(result['pages'].keys())}")
    print(f"\n💡 Next step: Run 'python cli.py preview {args.project}' to view the website")


def preview_command(args):
    """生成したサイトをプレビュー"""
    output_dir = Path(f"output/{args.project}")

    if not output_dir.exists():
        print(f"❌ Project not found: {args.project}")
        print(f"Available projects:")
        output_path = Path('output')
        if output_path.exists():
            for proj in output_path.iterdir():
                if proj.is_dir():
                    print(f"  - {proj.name}")
        return

    PORT = args.port

    # ディレクトリを変更
    os.chdir(output_dir)

    Handler = http.server.SimpleHTTPRequestHandler

    print(f"\n🌐 Preview server starting...")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"📁 Directory: {output_dir}")
    print(f"\n⌨️  Press Ctrl+C to stop\n")

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")


def init_command(args):
    """プロジェクトを初期化"""
    project_name = args.project

    print(f"\n🚀 Initializing project: {project_name}\n")

    # コンテンツYAMLのテンプレートを作成
    yaml_dir = Path('user_materials/texts')
    yaml_dir.mkdir(parents=True, exist_ok=True)

    yaml_file = yaml_dir / f'{project_name}.yaml'

    if yaml_file.exists() and not args.force:
        print(f"⚠️  Project already exists: {yaml_file}")
        print(f"Use --force to overwrite")
        return

    yaml_content = f"""# {project_name} - Content Configuration

company_info:
  company_name: "Your Company Name"
  tagline: "Your Success Partner"
  description: "We provide professional services to help your business grow."
  address: "Tokyo, Japan"
  email: "info@example.com"
  phone: "03-1234-5678"

global:
  copyright: "© 2024 Your Company. All rights reserved."
  social_media:
    twitter: "https://twitter.com/yourcompany"
    linkedin: "https://linkedin.com/company/yourcompany"

pages:
  index:
    title: "ホーム"
    sections:
      - type: "hero"
        title: "Welcome to Your Company"
        content: "We help businesses succeed with innovative solutions."
        cta_text: "Get Started"
        cta_link: "#contact"

      - type: "features"
        title: "Our Services"
        content: "We offer comprehensive solutions tailored to your needs."
        items:
          - "Service 1"
          - "Service 2"
          - "Service 3"

      - type: "about_preview"
        title: "About Us"
        content: "With years of experience, we deliver exceptional results."

  about:
    title: "会社概要"
    sections:
      - type: "company_info"
        title: "Company Profile"
        content: "Founded in 2020, we are a leading provider of..."

      - type: "vision"
        title: "Our Vision"
        content: "To be the most trusted partner for businesses worldwide."

  services:
    title: "サービス"
    sections:
      - type: "service_list"
        title: "Our Services"
        content: "We offer a wide range of professional services."
        items:
          - title: "Consulting"
            description: "Expert advice for your business"
          - title: "Development"
            description: "Custom solutions tailored to your needs"
          - title: "Support"
            description: "24/7 customer support"

  contact:
    title: "お問い合わせ"
    sections:
      - type: "contact_form"
        title: "Get in Touch"
        content: "We'd love to hear from you. Send us a message!"

# Image paths (optional)
images:
  hero_image: "user_materials/images/hero.jpg"
  logo: "user_materials/logos/logo.png"

image_pages:
  hero_image: "index"
  logo: "index"
"""

    with open(yaml_file, 'w', encoding='utf-8') as f:
        f.write(yaml_content)

    print(f"✅ Project initialized: {yaml_file}")
    print(f"\n📝 Next steps:")
    print(f"1. Edit the content file: {yaml_file}")
    print(f"2. Analyze a reference website: python cli.py analyze <URL>")
    print(f"3. Generate the website: python cli.py generate {project_name}")


def list_command(args):
    """プロジェクト一覧を表示"""
    print("\n📁 Available Projects:\n")

    output_path = Path('output')
    if not output_path.exists() or not any(output_path.iterdir()):
        print("  No projects found.")
        print("\n💡 Create a new project with: python cli.py init <project_name>")
        return

    for proj in sorted(output_path.iterdir()):
        if proj.is_dir():
            index_file = proj / 'index.html'
            status = "✅" if index_file.exists() else "⚠️ "
            print(f"  {status} {proj.name}")

    print("\n💡 Preview a project with: python cli.py preview <project_name>")


def main():
    parser = argparse.ArgumentParser(
        description='AI Agent Homepage Builder - Multi-page Website Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize a new project
  python cli.py init my_company

  # Analyze a reference website
  python cli.py analyze https://example.com

  # Generate website
  python cli.py generate my_company

  # Preview website
  python cli.py preview my_company

  # List all projects
  python cli.py list
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # init コマンド
    parser_init = subparsers.add_parser('init', help='Initialize a new project')
    parser_init.add_argument('project', help='Project name')
    parser_init.add_argument('--force', action='store_true', help='Overwrite existing project')

    # analyze コマンド
    parser_analyze = subparsers.add_parser('analyze', help='Analyze a reference URL')
    parser_analyze.add_argument('url', help='URL to analyze')
    parser_analyze.add_argument('--output', default='analyzed_sites', help='Output directory')
    parser_analyze.add_argument('--project', default='analyzed', help='Project name')

    # generate コマンド
    parser_generate = subparsers.add_parser('generate', help='Generate website')
    parser_generate.add_argument('project', help='Project name')
    parser_generate.add_argument('--pages', help='Comma-separated list of pages (default: index,about,services,contact)')

    # preview コマンド
    parser_preview = subparsers.add_parser('preview', help='Preview generated website')
    parser_preview.add_argument('project', help='Project name')
    parser_preview.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')

    # list コマンド
    parser_list = subparsers.add_parser('list', help='List all projects')

    args = parser.parse_args()

    if args.command == 'init':
        init_command(args)
    elif args.command == 'analyze':
        analyze_command(args)
    elif args.command == 'generate':
        generate_command(args)
    elif args.command == 'preview':
        preview_command(args)
    elif args.command == 'list':
        list_command(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
