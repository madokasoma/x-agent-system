# AI Agent Homepage Builder

**参考URLを分析し、複数ページの企業Webサイトを自動生成するAIエージェントシステム**

## 🎯 概要

このシステムは、参考となる企業サイトのデザインを分析し、ユーザーのコンテンツで複数ページの完全なWebサイトを自動生成します。

### 主な特徴

- ✅ **完全な複数ページ対応** - トップページ、会社概要、サービス、お問い合わせ等
- ✅ **URL分析** - 参考サイトのデザイン・構造を自動解析
- ✅ **AIによる生成** - Claude APIで高品質なHTML/CSS/JSを生成
- ✅ **レスポンシブデザイン** - PC/タブレット/スマホ完全対応
- ✅ **SEO最適化** - 適切なメタタグと構造化データ
- ✅ **簡単カスタマイズ** - YAMLファイルでコンテンツ管理

## 🚀 クイックスタート

### 1. セットアップ

```bash
# 依存パッケージをインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .env ファイルを編集してAnthropicのAPIキーを設定
```

### 2. 3ステップでWebサイト生成

```bash
# Step 1: プロジェクト初期化
python cli.py init my_company

# Step 2: 参考サイトを分析（オプション）
python cli.py analyze https://example-company.com

# Step 3: Webサイト生成
python cli.py generate my_company

# プレビュー
python cli.py preview my_company
# → ブラウザで http://localhost:8000 を開く
```

### ワンライナーで生成

```bash
python main.py https://example-company.com my_company
```

## 📋 使い方

### 方法A: CLIツール（推奨）

#### 1. プロジェクト初期化

```bash
python cli.py init my_company
```

これにより `user_materials/texts/my_company.yaml` が作成されます。

#### 2. コンテンツを編集

```yaml
# user_materials/texts/my_company.yaml

company_info:
  company_name: "マイカンパニー株式会社"
  tagline: "イノベーションで未来を創る"
  description: "私たちは最先端のAI技術で、ビジネスの課題を解決します。"

pages:
  index:
    sections:
      - type: "hero"
        title: "ビジネスを次のレベルへ"
        content: "革新的なソリューションで成長を加速"

  about:
    sections:
      - type: "company"
        title: "会社概要"
        content: "2020年設立。AIエンジニア30名が在籍。"
```

#### 3. 参考サイトを分析（オプション）

```bash
python cli.py analyze https://toma.co.jp
```

#### 4. Webサイト生成

```bash
python cli.py generate my_company
```

生成されるページ:
- `index.html` - トップページ
- `about.html` - 会社概要
- `services.html` - サービス紹介
- `contact.html` - お問い合わせ

特定のページのみ生成:
```bash
python cli.py generate my_company --pages index,about
```

#### 5. プレビュー

```bash
python cli.py preview my_company
```

ブラウザで http://localhost:8000 を開きます。

#### その他のコマンド

```bash
# プロジェクト一覧
python cli.py list

# ヘルプ
python cli.py --help
```

### 方法B: Pythonスクリプト

```python
from agents.url_analyzer import URLAnalyzerAgent
from agents.content_manager import ContentManagerAgent
from agents.page_generator import PageGeneratorAgent

# 1. URL分析
analyzer = URLAnalyzerAgent()
template_data = analyzer.execute('https://example.com')

# 2. コンテンツ準備
content_mgr = ContentManagerAgent()
content_mgr.add_company_info('company_name', 'マイカンパニー株式会社')
content_mgr.add_company_info('tagline', 'Innovation for the Future')

# 各ページにセクションを追加
content_mgr.add_section('index', 'hero', 'Welcome', 'Transform your business')
content_mgr.add_section('about', 'company', 'About Us', 'We are professionals')
content_mgr.add_section('services', 'service_list', 'Services', 'Our services')
content_mgr.add_section('contact', 'contact_form', 'Contact', 'Get in touch')

# 3. Webサイト生成（複数ページ）
generator = PageGeneratorAgent()
result = generator.execute(
    template_data=template_data,
    content_map=content_mgr.get_content_map(),
    output_dir='output/my_company',
    pages=['index', 'about', 'services', 'contact']
)

print(f"✅ Generated: {result}")
```

## 📁 プロジェクト構造

```
x-agent-system/
├── agents/                    # AIエージェント（実装済み）
│   ├── base_agent.py         # ベースエージェントクラス
│   ├── url_analyzer.py       # URL分析エージェント
│   ├── content_manager.py    # コンテンツ管理
│   └── page_generator.py     # ページ生成（複数ページ対応）
├── utils/                     # ユーティリティ（実装済み）
│   ├── html_parser.py        # HTML解析
│   └── css_analyzer.py       # CSS解析
├── user_materials/            # ユーザー素材
│   ├── texts/                # テキストコンテンツ（YAML）
│   ├── images/               # 画像素材
│   └── logos/                # ロゴファイル
├── output/                    # 生成されたサイト
│   └── [project_name]/
│       ├── index.html
│       ├── about.html
│       ├── services.html
│       ├── contact.html
│       ├── css/style.css
│       ├── js/main.js
│       └── images/
├── analyzed_sites/            # 分析済みサイトデータ
├── config/                    # 設定ファイル
├── cli.py                     # CLIインターフェース ⭐
├── main.py                    # メインスクリプト ⭐
└── requirements.txt           # 依存パッケージ
```

## 🎨 生成されるWebサイトの特徴

### 対応ページ

1. **index.html** (トップページ)
   - ヒーローセクション
   - サービス概要
   - 特徴・強み
   - CTAボタン

2. **about.html** (会社概要)
   - 会社情報
   - ビジョン・ミッション
   - 沿革
   - チーム紹介

3. **services.html** (サービス)
   - サービス一覧
   - 詳細説明
   - 料金プラン

4. **contact.html** (お問い合わせ)
   - お問い合わせフォーム
   - 連絡先情報
   - アクセス情報

### デザインの特徴

- ✅ **レスポンシブデザイン**: モバイルファースト、768px/1024px/1280pxブレークポイント
- ✅ **モダンCSS**: Flexbox/Grid使用
- ✅ **SEO最適化**: 適切なメタタグ、セマンティックHTML
- ✅ **アクセシビリティ**: ARIA属性対応
- ✅ **統一されたナビゲーション**: 全ページで共通のヘッダー・フッター
- ✅ **スムーズなアニメーション**: ホバーエフェクト、トランジション

## 🛠️ 技術スタック

### バックエンド
- **Python 3.10+** - メイン言語
- **Anthropic Claude API** - AI分析・HTML/CSS生成
- **BeautifulSoup4** - HTML解析
- **Pillow** - 画像処理
- **PyYAML** - 設定管理
- **Jinja2** - テンプレートエンジン（将来拡張用）

### フロントエンド
- **HTML5** - セマンティックマークアップ
- **CSS3** - モダンスタイリング（Flexbox/Grid）
- **Vanilla JavaScript** - インタラクション（フレームワークレス）

## 📊 実装済み機能

### ✅ 完全実装済み

1. **URL分析エージェント** (`agents/url_analyzer.py`)
   - HTML構造解析
   - CSS解析（色、フォント、レイアウト）
   - デザインパターン抽出（AI使用）
   - 複数ページ構造の推測

2. **コンテンツ管理エージェント** (`agents/content_manager.py`)
   - YAMLファイルからの読み込み
   - ページごとのコンテンツ管理
   - 画像の最適化
   - セクション管理

3. **ページ生成エージェント** (`agents/page_generator.py`)
   - **複数ページ対応** (index, about, services, contact)
   - AIによるHTML/CSS生成
   - 統一されたナビゲーション
   - レスポンシブCSS
   - お問い合わせフォーム

4. **ユーティリティ** (`utils/`)
   - HTML解析 (`html_parser.py`)
   - CSS解析 (`css_analyzer.py`)

5. **CLIツール** (`cli.py`)
   - `init` - プロジェクト初期化
   - `analyze` - URL分析
   - `generate` - サイト生成
   - `preview` - プレビューサーバー
   - `list` - プロジェクト一覧

## 🔧 要件

- Python 3.10 以上
- Anthropic Claude API キー（必須）
- インターネット接続（URL分析時）

### APIキーの取得

1. [Anthropic Console](https://console.anthropic.com/) でアカウント作成
2. API Keyを生成
3. `.env` ファイルに設定:
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## 💡 使用例

### 例1: 企業サイトの生成

```bash
# プロジェクト初期化
python cli.py init tech_company

# コンテンツ編集
# user_materials/texts/tech_company.yaml を編集

# 参考サイト分析
python cli.py analyze https://www.apple.com

# サイト生成
python cli.py generate tech_company

# プレビュー
python cli.py preview tech_company
```

### 例2: コンサルティング会社のサイト

```bash
python main.py https://www.mckinsey.com consulting_firm
```

### 例3: カスタムページ構成

```bash
# index と about のみ生成
python cli.py generate my_company --pages index,about
```

## 🚧 今後の拡張機能（将来）

- [ ] ブログ機能（記事一覧・詳細ページ）
- [ ] お問い合わせフォームのバックエンド連携
- [ ] 多言語対応（英語/日本語切り替え）
- [ ] CMSとの統合（WordPress、microCMS等）
- [ ] デプロイ自動化（Netlify/Vercel/GitHub Pages）
- [ ] A/Bテスト用のバリエーション生成
- [ ] アクセス解析コード埋め込み（Google Analytics等）

## 📚 ドキュメント

- **[README.md](README.md)** - 本ドキュメント
- **[HOMEPAGE_BUILDER_DESIGN.md](HOMEPAGE_BUILDER_DESIGN.md)** - システム設計書
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - 実装手順ガイド

## 🤝 コントリビューション

プルリクエスト大歓迎です！

## 📄 ライセンス

MIT License

## 🙏 謝辞

- Anthropic Claude API
- BeautifulSoup4
- Pillow
- PyYAML
- その他のオープンソースライブラリ

---

## 🎉 まとめ

**AI Agent Homepage Builder** は、参考サイトを分析して複数ページの企業Webサイトを自動生成する、完全に動作するシステムです。

### ✅ 実装済み
- URL分析エージェント
- コンテンツ管理エージェント
- ページ生成エージェント（**複数ページ対応**）
- HTML/CSS/JavaScript自動生成
- CLIツール
- プレビューサーバー

### 🚀 今すぐ使える
```bash
pip install -r requirements.txt
cp .env.example .env
# .env にAPIキーを設定

python cli.py init my_company
python cli.py generate my_company
python cli.py preview my_company
```

**参考サイトのレベル**: TOMAコンサルタンツグループ等の企業サイトに対応
**生成されるページ**: トップ、会社概要、サービス、お問い合わせ + 必要に応じて追加可能

質問やサポートが必要な場合は、Issueを作成してください！
