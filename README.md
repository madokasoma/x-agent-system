# AI Agent Homepage Builder

**参考URLを分析し、ユーザーの素材で自動的にホームページを生成するAIエージェントシステム**

## 🎯 概要

このシステムは、以下の流れでホームページを自動生成します：

1. **参考URLを分析** - 企業サイト等のデザイン・レイアウトを解析
2. **ユーザー素材を提供** - 会社名、説明文、画像などを提供
3. **AIが自動生成** - HTML/CSS/JavaScriptを完全自動生成
4. **プレビュー＆調整** - ローカルでプレビュー、必要に応じて調整

## ✨ 主な機能

- 🔍 **URL分析エージェント**: Webサイトの構造とデザインを自動解析
- 📝 **コンテンツ管理**: ユーザーの素材を整理・最適化
- 🎨 **ページ生成**: レスポンシブなHTML/CSS/JSを自動生成
- 👀 **プレビュー機能**: ローカルサーバーで即座に確認
- ♿ **アクセシビリティ対応**: WCAG準拠のセマンティックHTML
- 📱 **レスポンシブデザイン**: PC/タブレット/スマホ完全対応

## 🚀 クイックスタート

### 1. セットアップ

```bash
# リポジトリをクローン
git clone <your-repo-url>
cd x-agent-system

# 依存パッケージをインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .env ファイルを編集してAPIキーを設定
```

### 2. APIキーの設定

`.env` ファイルに以下を設定：

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx  # 必須
OPENAI_API_KEY=sk-xxxxx         # オプション
```

### 3. 使い方

#### 方法A: CLIを使う

```bash
# 1. 参考サイトを分析
python cli.py analyze https://example-company.com --output my_project

# 2. コンテンツを準備（YAMLファイルで）
# user_materials/texts/my_project.yaml を編集

# 3. ホームページを生成
python cli.py generate my_project

# 4. プレビュー
python cli.py preview my_project
# → ブラウザで http://localhost:8000 を開く
```

#### 方法B: Pythonスクリプトで使う

```python
from agents.url_analyzer import URLAnalyzerAgent
from agents.content_manager import ContentManagerAgent
from agents.page_generator import PageGeneratorAgent

# 1. 参考サイト分析
analyzer = URLAnalyzerAgent()
template_data = analyzer.execute('https://example-corporate.com')

# 2. ユーザー素材を準備
content_manager = ContentManagerAgent()
content_manager.add_text('company_name', 'マイカンパニー株式会社', category='company_info')
content_manager.add_text('tagline', 'イノベーションで未来を創る', category='company_info')
content_manager.add_image('hero_image', 'path/to/hero.jpg')

# 3. ホームページ生成
generator = PageGeneratorAgent()
site_path = generator.execute(
    template_data=template_data,
    content=content_manager.get_content_map(),
    output_dir='output/my_project'
)

print(f"✅ サイト生成完了: {site_path}")
```

## 📁 プロジェクト構造

```
x-agent-system/
├── agents/                    # AIエージェントモジュール
│   ├── base_agent.py         # ベースエージェントクラス
│   ├── url_analyzer.py       # URL分析エージェント
│   ├── content_manager.py    # コンテンツ管理
│   └── page_generator.py     # ページ生成
├── utils/                     # ユーティリティ
│   ├── html_parser.py        # HTML解析
│   └── css_analyzer.py       # CSS解析
├── templates/                 # テンプレート
├── output/                    # 生成されたサイト
├── user_materials/            # ユーザー素材
├── config/                    # 設定ファイル
├── cli.py                     # CLIインターフェース
└── requirements.txt           # 依存パッケージ
```

## 📚 ドキュメント

- **[設計書](HOMEPAGE_BUILDER_DESIGN.md)** - システム全体の設計
- **[実装ガイド](IMPLEMENTATION_GUIDE.md)** - 詳細な実装手順

## 🎨 サポートするデザインパターン

- **コーポレートサイト**: 企業の公式サイト
- **スタートアップ/SaaS**: モダンなサービスサイト
- **ポートフォリオ**: 個人/クリエイター向け
- **ランディングページ**: 1ページ完結型

## 🛠️ 技術スタック

- **Python 3.10+**: メイン言語
- **Anthropic Claude API**: AI分析・生成
- **BeautifulSoup4**: HTML解析
- **Jinja2**: テンプレートエンジン
- **Pillow**: 画像処理

## 📊 生成されるサイトの特徴

- ✅ **レスポンシブデザイン**: モバイルファースト
- ✅ **SEO最適化**: メタタグ、構造化データ
- ✅ **アクセシビリティ**: ARIA属性、セマンティックHTML
- ✅ **高速読み込み**: 最適化された画像・CSS
- ✅ **モダンCSS**: Flexbox/Grid使用

## 🔧 要件

- Python 3.10 以上
- Anthropic Claude API キー（必須）
- OpenAI API キー（オプション）

## 📝 使用例

### ユーザー素材の準備（YAML形式）

```yaml
# user_materials/texts/my_project.yaml

company_info:
  company_name: "マイカンパニー株式会社"
  tagline: "イノベーションで未来を創る"
  description: "私たちは最先端のAI技術で、ビジネスの課題を解決します。"
  address: "東京都渋谷区..."
  email: "info@example.com"

sections:
  - type: "features"
    title: "サービスの特徴"
    content: "高品質なAIソリューションを提供"

  - type: "about"
    title: "会社概要"
    content: "2020年設立。AIエンジニア30名が在籍。"
```

## 🚧 開発ロードマップ

### Phase 1: 基本機能（現在）
- [x] URL分析エージェント
- [x] コンテンツ管理
- [x] ページ生成
- [x] プレビュー機能

### Phase 2: 拡張機能
- [ ] 複数ページ生成（About、Contact等）
- [ ] お問い合わせフォーム
- [ ] 多言語対応
- [ ] CMSとの統合

### Phase 3: 高度な機能
- [ ] A/Bテスト自動生成
- [ ] アクセス解析統合
- [ ] デプロイ自動化（Netlify/Vercel）
- [ ] AI による継続的改善提案

## 🤝 コントリビューション

プルリクエスト大歓迎です！

## 📄 ライセンス

MIT License

## 🙏 謝辞

- Anthropic Claude API
- BeautifulSoup4
- その他のオープンソースライブラリ

---

**詳細な設計・実装手順は以下をご覧ください:**
- [設計書 (HOMEPAGE_BUILDER_DESIGN.md)](HOMEPAGE_BUILDER_DESIGN.md)
- [実装ガイド (IMPLEMENTATION_GUIDE.md)](IMPLEMENTATION_GUIDE.md)
