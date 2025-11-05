#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Agent Homepage Builder - デモスクリプト

このスクリプトは、システムの基本的な使い方を示すデモです。
実際に動作させるには、.env ファイルにAPIキーを設定してください。
"""

import os
import sys

def print_banner():
    """バナーを表示"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     AI Agent Homepage Builder - デモ                      ║
║                                                           ║
║  参考URLを分析し、自動的にホームページを生成します        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

def check_setup():
    """セットアップを確認"""
    print("\n📋 セットアップチェック...\n")

    issues = []

    # .env ファイルの存在確認
    if not os.path.exists('.env'):
        issues.append("❌ .env ファイルが見つかりません")
        print("⚠️  .env ファイルを作成してください:")
        print("   cp .env.example .env")
        print("   # その後、APIキーを設定してください\n")
    else:
        print("✅ .env ファイルが存在します")

    # 依存パッケージの確認
    try:
        import anthropic
        print("✅ anthropic パッケージがインストールされています")
    except ImportError:
        issues.append("❌ anthropic パッケージがインストールされていません")
        print("⚠️  依存パッケージをインストールしてください:")
        print("   pip install -r requirements.txt\n")

    try:
        import bs4
        print("✅ beautifulsoup4 パッケージがインストールされています")
    except ImportError:
        issues.append("❌ beautifulsoup4 パッケージがインストールされていません")

    try:
        import PIL
        print("✅ Pillow パッケージがインストールされています")
    except ImportError:
        issues.append("❌ Pillow パッケージがインストールされていません")

    # ディレクトリ構造の確認
    required_dirs = ['agents', 'utils', 'templates', 'config']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ ディレクトリが存在します")
        else:
            issues.append(f"❌ {dir_name}/ ディレクトリが見つかりません")

    return len(issues) == 0

def show_usage():
    """使い方を表示"""
    print("\n📚 使い方\n")

    print("【方法1: Pythonスクリプトで使う】")
    print("-" * 60)
    print("""
from agents.url_analyzer import URLAnalyzerAgent
from agents.content_manager import ContentManagerAgent
from agents.page_generator import PageGeneratorAgent

# 1. 参考サイト分析
analyzer = URLAnalyzerAgent()
template_data = analyzer.execute('https://example.com')

# 2. コンテンツ準備
content_mgr = ContentManagerAgent()
content_mgr.add_text('company_name', 'マイ企業', category='company_info')
content_mgr.add_text('tagline', 'Innovation', category='company_info')

# 3. ホームページ生成
generator = PageGeneratorAgent()
output = generator.execute(
    template_data=template_data,
    content_map=content_mgr.get_content_map(),
    output_dir='output/my_project'
)

print(f"✅ 生成完了: {output}")
""")

    print("\n【方法2: CLIで使う】")
    print("-" * 60)
    print("""
# 1. 参考サイトを分析
python cli.py analyze https://example.com

# 2. コンテンツを準備（YAMLファイルで）
# user_materials/texts/my_project.yaml を編集

# 3. ホームページ生成
python cli.py generate my_project

# 4. プレビュー
python cli.py preview my_project
""")

def show_next_steps():
    """次のステップを表示"""
    print("\n🚀 次のステップ\n")
    print("1. .env ファイルにAnthropicのAPIキーを設定")
    print("   ANTHROPIC_API_KEY=sk-ant-xxxxx")
    print()
    print("2. 依存パッケージをインストール")
    print("   pip install -r requirements.txt")
    print()
    print("3. 実装ガイドを確認")
    print("   cat IMPLEMENTATION_GUIDE.md")
    print()
    print("4. 参考URLを分析してみる")
    print("   python cli.py analyze https://example.com")
    print()

def show_docs():
    """ドキュメントへのリンクを表示"""
    print("\n📖 ドキュメント\n")
    print("- README.md               : 概要と使い方")
    print("- HOMEPAGE_BUILDER_DESIGN.md : システム設計書")
    print("- IMPLEMENTATION_GUIDE.md    : 実装手順ガイド")
    print()

def main():
    """メイン処理"""
    print_banner()

    # セットアップチェック
    setup_ok = check_setup()

    if setup_ok:
        print("\n✨ セットアップは完了しています！")
        show_usage()
    else:
        print("\n⚠️  セットアップが完了していません。")
        show_next_steps()

    show_docs()

    print("\n" + "=" * 60)
    print("🎉 AI Agent Homepage Builder へようこそ！")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
