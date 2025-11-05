# AI Agent Homepage Builder - システム設計書

## 📋 概要

参考となる企業のホームページURLを分析し、ユーザーの素材（テキスト、画像等）を組み合わせて、自動的にカスタマイズされたホームページを生成するAIエージェントシステム。

## 🎯 主要機能

### 1. URL分析エージェント (URL Analyzer Agent)
- 指定されたURLからHTML/CSS/JavaScript構造を抽出
- レイアウトパターン、色使い、フォント、セクション構成を分析
- デザインの特徴をAIで理解し、テンプレート化
- レスポンシブデザインのブレークポイント検出

**主な処理:**
```
入力: 参考サイトのURL（例: https://example-company.com）
↓
HTML/CSSダウンロード・解析
↓
デザインパターン抽出
  - カラーパレット
  - フォント体系
  - レイアウト構造（ヘッダー、ヒーロー、特徴、フッター等）
  - アニメーション効果
↓
出力: テンプレート設計データ（JSON形式）
```

### 2. コンテンツ管理エージェント (Content Manager Agent)
- ユーザーの素材（テキスト、画像、会社情報等）を受け取り、管理
- 素材の種類を自動分類（会社名、キャッチコピー、サービス説明等）
- 各セクションに最適な素材を提案
- 画像の自動リサイズ・最適化

**素材の種類:**
```yaml
company_info:
  - 会社名
  - キャッチコピー
  - 会社説明
  - 所在地、連絡先

content_sections:
  - サービス/製品説明
  - 特徴・強み
  - お客様の声
  - 実績・事例

media:
  - ロゴ画像
  - メインビジュアル
  - サービス画像
  - チーム写真
```

### 3. ホームページ生成エージェント (Page Generator Agent)
- 分析したテンプレート + ユーザー素材 → 完全なHTML/CSS/JSを生成
- レスポンシブデザイン自動対応（PC/タブレット/スマホ）
- SEO最適化（メタタグ、構造化データ）
- アクセシビリティ対応（WCAG準拠）

**生成フロー:**
```
テンプレート設計データ + ユーザー素材
↓
AI が最適な配置を決定
↓
HTML/CSS/JavaScript コード生成
  - セマンティックHTML
  - モダンCSS（Flexbox/Grid）
  - バニラJavaScript（軽量）
↓
出力: 完全なWebサイト
```

### 4. プレビュー＆カスタマイズエージェント (Customizer Agent)
- 生成したサイトのリアルタイムプレビュー
- ユーザーのフィードバックに基づいた調整
- 色・フォント・レイアウトの変更提案
- A/Bテストパターンの生成

## 🛠️ 技術スタック

### バックエンド
- **Python 3.10+** - メインロジック
- **BeautifulSoup4** - HTML解析
- **requests** - HTTP通信
- **Pillow** - 画像処理
- **Anthropic Claude API** - AI分析・生成（メイン）
- **OpenAI GPT-4 API** - 補助的なAI処理
- **Jinja2** - テンプレートエンジン
- **PyYAML** - 設定管理

### フロントエンド
- **HTML5** - セマンティックマークアップ
- **CSS3** - モダンスタイリング（Flexbox/Grid）
- **Vanilla JavaScript** - インタラクション（フレームワークレス）

### Webインターフェース（オプション）
- **Flask** または **FastAPI** - Webフレームワーク
- **Tailwind CSS** - 管理画面のスタイリング

## 📁 ディレクトリ構造

```
x-agent-system/
├── agents/                           # AIエージェントモジュール
│   ├── __init__.py
│   ├── base_agent.py                # ベースエージェントクラス
│   ├── url_analyzer.py              # URL分析エージェント
│   ├── content_manager.py           # コンテンツ管理エージェント
│   ├── page_generator.py            # ページ生成エージェント
│   └── customizer.py                # カスタマイズエージェント
│
├── templates/                        # HTMLテンプレート
│   ├── base/                        # 基本テンプレート
│   │   ├── modern_corporate.html
│   │   ├── startup_style.html
│   │   └── minimal_design.html
│   └── generated/                   # 生成されたテンプレート（保存用）
│
├── static/                          # 静的ファイル（管理画面用）
│   ├── css/
│   │   └── admin.css
│   ├── js/
│   │   └── preview.js
│   └── images/
│
├── user_materials/                  # ユーザー素材置き場
│   ├── texts/                       # テキストコンテンツ
│   │   └── content.yaml
│   ├── images/                      # 画像素材
│   └── logos/                       # ロゴファイル
│
├── analyzed_sites/                  # 分析済みサイトデータ
│   └── [domain_name]/
│       ├── structure.json           # サイト構造
│       ├── styles.json              # スタイル情報
│       └── screenshots/             # スクリーンショット
│
├── output/                          # 生成されたサイト
│   └── [project_name]/
│       ├── index.html
│       ├── about.html
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── main.js
│       └── images/
│
├── config/                          # 設定ファイル
│   ├── config.yaml                  # メイン設定
│   └── api_keys.yaml                # APIキー（.gitignore）
│
├── utils/                           # ユーティリティ
│   ├── __init__.py
│   ├── image_processor.py           # 画像処理
│   ├── html_parser.py               # HTML解析
│   └── css_analyzer.py              # CSS解析
│
├── main.py                          # メインエントリーポイント
├── cli.py                           # CLIインターフェース
├── web_app.py                       # Webアプリ（オプション）
├── requirements.txt                 # 依存パッケージ
├── .env.example                     # 環境変数サンプル
├── .gitignore
└── README.md                        # プロジェクトドキュメント
```

## 🔄 システムワークフロー

### フェーズ1: 参考サイト分析
```
ユーザー: 参考URLを入力
    ↓
URL Analyzer Agent:
  1. サイトにアクセスしてHTML/CSS取得
  2. レイアウト構造を解析
  3. デザインパターンを抽出
  4. AIでデザインの特徴を理解
    ↓
出力: テンプレート設計データ（structure.json）
```

### フェーズ2: ユーザー素材の準備
```
ユーザー: 素材を提供
  - 会社名、キャッチコピー
  - サービス説明文
  - 画像ファイル
    ↓
Content Manager Agent:
  1. 素材を分類・整理
  2. 画像を最適化
  3. テキストの適切な配置を提案
    ↓
出力: コンテンツマッピング（content_map.json）
```

### フェーズ3: ホームページ生成
```
テンプレート設計データ + コンテンツマッピング
    ↓
Page Generator Agent:
  1. HTML構造を生成
  2. CSS（参考サイトのスタイルを適用）
  3. JavaScript（必要なインタラクション）
  4. SEO最適化
    ↓
出力: 完全なWebサイト（output/[project_name]/）
```

### フェーズ4: プレビュー＆調整
```
生成されたサイト
    ↓
Customizer Agent:
  1. ローカルサーバーで表示
  2. ユーザーのフィードバック受付
  3. 色・レイアウト調整
  4. 再生成
    ↓
最終出力: 本番環境用サイト
```

## 🎨 サポートするデザインパターン

### 1. コーポレートサイト
- ヘッダー（ロゴ + ナビゲーション）
- ヒーローセクション（大きなビジュアル + キャッチコピー）
- サービス紹介（3〜4カラム）
- 実績・事例
- お問い合わせフォーム
- フッター

### 2. スタートアップ/SaaS
- モダンなヒーローセクション
- 機能紹介（アイコン + 説明）
- デモ動画・スクリーンショット
- 料金プラン
- CTA（Call to Action）ボタン

### 3. ポートフォリオ
- フルスクリーンヒーロー
- プロジェクトギャラリー（グリッドレイアウト）
- スキル紹介
- 経歴・プロフィール
- お問い合わせ

## 🚀 実装手順（次のステップ）

### ステップ1: 基礎セットアップ（1日目）
- [ ] プロジェクト構造の作成
- [ ] 依存パッケージのインストール
- [ ] 環境変数・設定ファイルのセットアップ
- [ ] ベースエージェントクラスの実装

### ステップ2: URL分析エージェント実装（2日目）
- [ ] HTML/CSSダウンロード機能
- [ ] BeautifulSoupでの構造解析
- [ ] CSSパーサーでスタイル抽出
- [ ] Claude APIでデザインパターン分析
- [ ] テンプレート設計データの生成

### ステップ3: コンテンツ管理エージェント実装（3日目）
- [ ] ユーザー素材の入力インターフェース
- [ ] 素材の分類・検証
- [ ] 画像処理（リサイズ、圧縮）
- [ ] コンテンツマッピングの生成

### ステップ4: ページ生成エージェント実装（4-5日目）
- [ ] Jinja2テンプレートエンジン統合
- [ ] HTML生成ロジック
- [ ] CSS生成（レスポンシブ対応）
- [ ] JavaScript生成（最小限のインタラクション）
- [ ] SEOメタタグ生成

### ステップ5: プレビュー機能実装（6日目）
- [ ] ローカルHTTPサーバー
- [ ] プレビュー表示機能
- [ ] フィードバック受付機能

### ステップ6: テスト＆改善（7日目）
- [ ] 複数の参考サイトでテスト
- [ ] 生成品質の確認
- [ ] エラーハンドリング強化
- [ ] ドキュメント整備

### ステップ7: オプション機能（追加）
- [ ] Webインターフェース（Flask/FastAPI）
- [ ] 複数ページ生成（About、Contact等）
- [ ] お問い合わせフォーム統合
- [ ] デプロイ機能（Netlify/Vercel連携）

## 💡 使用例

### コマンドライン（CLI）での使用
```bash
# 1. 参考サイトを分析
python cli.py analyze https://example-corporate.com --output my_project

# 2. ユーザー素材を準備
python cli.py prepare-content my_project

# 3. ホームページを生成
python cli.py generate my_project

# 4. プレビュー
python cli.py preview my_project
```

### Pythonスクリプトでの使用
```python
from agents.url_analyzer import URLAnalyzerAgent
from agents.content_manager import ContentManagerAgent
from agents.page_generator import PageGeneratorAgent

# 1. 参考サイト分析
analyzer = URLAnalyzerAgent()
template_data = analyzer.analyze('https://example-corporate.com')

# 2. ユーザー素材を準備
content_manager = ContentManagerAgent()
content_manager.add_text('company_name', 'マイカンパニー株式会社')
content_manager.add_text('tagline', 'イノベーションで未来を創る')
content_manager.add_image('hero_image', 'path/to/hero.jpg')

# 3. ホームページ生成
generator = PageGeneratorAgent()
site = generator.generate(
    template_data=template_data,
    content=content_manager.get_content_map(),
    output_dir='output/my_project'
)

print(f"✅ サイト生成完了: {site.url}")
```

## 🔧 必要なAPIキー

### Anthropic Claude API（推奨）
- サイト分析、デザイン理解に使用
- 高品質なHTML/CSS生成

### OpenAI GPT-4 API（オプション）
- 補助的なテキスト生成
- コンテンツの最適化提案

### 設定方法
```bash
# .envファイルに記載
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx  # オプション
```

## 📊 期待される成果物

### 生成されるファイル
```
output/my_project/
├── index.html              # メインページ（レスポンシブ対応）
├── css/
│   ├── style.css          # カスタムスタイル
│   └── responsive.css     # レスポンシブ対応
├── js/
│   └── main.js            # インタラクション
├── images/
│   ├── hero.jpg           # 最適化済み画像
│   ├── service1.jpg
│   └── logo.png
└── README.md              # サイト説明書
```

### HTML の特徴
- ✅ セマンティックHTML5
- ✅ レスポンシブデザイン（モバイルファースト）
- ✅ SEO最適化（メタタグ、構造化データ）
- ✅ アクセシビリティ対応（ARIA属性）
- ✅ 高速読み込み（最適化された画像・CSS）

## 🎯 成功基準

1. **デザインの再現性**: 参考サイトの雰囲気を70%以上再現
2. **カスタマイズ性**: ユーザー素材が自然に統合されている
3. **レスポンシブ**: PC/タブレット/スマホで正常に表示
4. **パフォーマンス**: Google PageSpeed Insights で80点以上
5. **生成速度**: 1サイトあたり3分以内

## 🔮 将来の拡張機能

- [ ] 複数ページサイト生成（About、Services、Contact等）
- [ ] CMSとの統合（WordPress、Shopify等）
- [ ] お問い合わせフォーム機能（バックエンド連携）
- [ ] 多言語対応サイト生成
- [ ] A/Bテストバリエーション自動生成
- [ ] アクセス解析コード埋め込み（Google Analytics等）
- [ ] デプロイ自動化（Netlify/Vercel/GitHub Pages）
- [ ] AIによる継続的な改善提案

## 📝 ライセンス

MIT License

---

**次のステップ**: `IMPLEMENTATION_GUIDE.md` で詳細な実装手順を確認してください。
