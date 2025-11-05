#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML解析ユーティリティ
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re
from urllib.parse import urljoin, urlparse

class HTMLParser:
    """HTML構造を解析"""

    def __init__(self, url: str, timeout: int = 30):
        self.url = url
        self.timeout = timeout
        self.soup: Optional[BeautifulSoup] = None
        self.html: Optional[str] = None

    def fetch(self) -> bool:
        """URLからHTMLを取得"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=self.timeout, allow_redirects=True)
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
            'meta_keywords': self._get_meta_keywords(),
            'sections': self._extract_sections(),
            'navigation': self._extract_navigation(),
            'header': self._extract_header(),
            'footer': self._extract_footer(),
            'images': self._extract_images(),
            'links': self._extract_css_links(),
            'internal_links': self._extract_internal_links(),
            'text_content': self._extract_text_content(),
        }

        return structure

    def _get_meta_description(self) -> str:
        """メタディスクリプションを取得"""
        meta = self.soup.find('meta', attrs={'name': 'description'})
        if not meta:
            meta = self.soup.find('meta', attrs={'property': 'og:description'})
        return meta['content'] if meta and 'content' in meta.attrs else ''

    def _get_meta_keywords(self) -> str:
        """メタキーワードを取得"""
        meta = self.soup.find('meta', attrs={'name': 'keywords'})
        return meta['content'] if meta and 'content' in meta.attrs else ''

    def _extract_header(self) -> Dict:
        """ヘッダー情報を抽出"""
        header = self.soup.find('header')
        if not header:
            # headerタグがない場合、ページ上部を探す
            header = self.soup.find(['div'], class_=re.compile(r'header', re.I))

        if not header:
            return {}

        return {
            'has_logo': bool(header.find('img')),
            'has_nav': bool(header.find('nav')),
            'text': header.get_text(strip=True)[:200]
        }

    def _extract_sections(self) -> List[Dict]:
        """主要セクションを抽出"""
        sections = []

        # header, main, section, article, aside などを探す
        for tag in self.soup.find_all(['main', 'section', 'article', 'div'], class_=re.compile(r'section|content|hero|feature|service', re.I), limit=20):
            section_data = {
                'tag': tag.name,
                'id': tag.get('id', ''),
                'class': ' '.join(tag.get('class', [])),
                'text_preview': tag.get_text(strip=True)[:150],
                'has_image': bool(tag.find('img')),
                'has_button': bool(tag.find(['button', 'a'], class_=re.compile(r'btn|button', re.I))),
                'headings': [h.get_text(strip=True) for h in tag.find_all(['h1', 'h2', 'h3'], limit=3)]
            }
            sections.append(section_data)

        return sections[:10]  # 最初の10セクション

    def _extract_navigation(self) -> List[Dict]:
        """ナビゲーションメニューを抽出"""
        nav_items = []
        nav = self.soup.find('nav')

        if not nav:
            # navタグがない場合、メニューっぽいものを探す
            nav = self.soup.find(['div', 'ul'], class_=re.compile(r'nav|menu', re.I))

        if nav:
            for link in nav.find_all('a', limit=15):
                text = link.get_text(strip=True)
                href = link.get('href', '')
                if text and href:
                    nav_items.append({
                        'text': text,
                        'href': href,
                        'is_external': href.startswith('http') and urlparse(self.url).netloc not in href
                    })

        return nav_items

    def _extract_footer(self) -> Dict:
        """フッター情報を抽出"""
        footer = self.soup.find('footer')
        if not footer:
            footer = self.soup.find(['div'], class_=re.compile(r'footer', re.I))

        if not footer:
            return {}

        links = [{'text': a.get_text(strip=True), 'href': a.get('href', '')}
                for a in footer.find_all('a', limit=20)]

        return {
            'text': footer.get_text(strip=True)[:300],
            'links': links,
            'has_copyright': bool(re.search(r'©|copyright', footer.get_text(), re.I))
        }

    def _extract_images(self) -> List[Dict]:
        """画像情報を抽出"""
        images = []
        for img in self.soup.find_all('img', limit=20):
            src = img.get('src', '') or img.get('data-src', '')
            if src:
                # 相対URLを絶対URLに変換
                absolute_url = urljoin(self.url, src)
                images.append({
                    'src': absolute_url,
                    'alt': img.get('alt', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', ''),
                    'title': img.get('title', '')
                })
        return images

    def _extract_css_links(self) -> List[str]:
        """外部スタイルシートのリンクを抽出"""
        links = []
        for link in self.soup.find_all('link', rel='stylesheet'):
            href = link.get('href', '')
            if href:
                # 相対URLを絶対URLに変換
                absolute_url = urljoin(self.url, href)
                links.append(absolute_url)
        return links

    def _extract_internal_links(self) -> List[Dict]:
        """内部リンクを抽出（他のページ構造を理解するため）"""
        internal_links = []
        base_domain = urlparse(self.url).netloc

        for link in self.soup.find_all('a', href=True, limit=50):
            href = link.get('href', '')
            text = link.get_text(strip=True)

            # 相対URLまたは同じドメインの絶対URL
            if not href.startswith('http') or base_domain in href:
                absolute_url = urljoin(self.url, href)
                if absolute_url != self.url:  # 自分自身へのリンクは除外
                    internal_links.append({
                        'text': text,
                        'url': absolute_url,
                        'href': href
                    })

        # 重複を除去
        seen = set()
        unique_links = []
        for link in internal_links:
            if link['url'] not in seen:
                seen.add(link['url'])
                unique_links.append(link)

        return unique_links[:20]  # 最初の20件

    def _extract_text_content(self) -> str:
        """主要なテキストコンテンツを抽出"""
        # スクリプトとスタイルを除去
        for script in self.soup(['script', 'style', 'nav', 'footer']):
            script.decompose()

        # メインコンテンツを取得
        main = self.soup.find('main') or self.soup.find('body')
        if main:
            text = main.get_text(separator=' ', strip=True)
            # 複数の空白を1つに
            text = re.sub(r'\s+', ' ', text)
            return text[:2000]  # 最初の2000文字
        return ''
