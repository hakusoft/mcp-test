# mcp-test

MCP operation test playground (issue -> branch -> PR -> review workflow)

`cart.py` 自体は検証のための題材であり、コードの中身に意味はない。
このリポジトリの主眼は、**Slack / Sentry のような外部ツールの情報を Claude Code が
MCP 経由で読み取り、GitHub 上で Issue 起票から PR 作成・CI 確認・セルフレビューまでを
自律的に進められるか**を検証することにある。

## 検証しているパイプライン

外部ツール上のシグナル（人間の要望、あるいはエラー監視ツールが検知した例外）を起点に、
Claude Code が以下を一気通貫で行う。

```
Slack の投稿 ─┐
              ├─> Issue 起票 -> ブランチ作成 -> 実装 -> PR 作成
Sentry の Issue ─┘         -> CI 確認 -> セルフレビュー -> 人間にマージを引き継ぎ
```

**人間が最後に必ず行うのは approve とマージのみ。** それ以外の一連の作業（Issue の要件把握、
実装、テスト、PR説明の作成、CI失敗時の原因調査と修正、セルフレビュー）は Claude Code が
MCP 経由で完結させる。

### 起点1: Slack

Slack ワークスペースに投稿された機能要望を Claude Code が読み取り、GitHub Issue として
起票する。Issue 本文には元の Slack 投稿へのリンクを残し、要望の出所を追えるようにしている。

- 例: [#5 calculate_total に送料計算を追加してほしい](../../issues/5)
  → [#6 feat: calculate_total に送料計算を追加](../../pull/6)

### 起点2: Sentry

Sentry が検知した例外（Issue）を Claude Code が読み取り、スタックトレースと該当コードから
根本原因を特定し、再現テストを添えて修正する。コミット/PR本文に `Fixes <SENTRY-ISSUE-ID>`
を含めることで、マージ時に Sentry 側の Issue も連動して解決済みになる。

- 例: [PYTHON-1 (KeyError: 'price')](https://hakusoft.sentry.io/issues/PYTHON-1)
  → [#7 fix: calculate_total で price/quantity 欠落時に ValueError を送出](../../pull/7)

## 使っている MCP 連携

| MCP | 用途 |
|---|---|
| [Slack](https://github.com/slackapi/slack-mcp-plugin) | チャンネルの読み取り、Issue化する投稿の検出 |
| [Sentry](https://github.com/getsentry/plugin-claude) | エラー Issue の取得、スタックトレース・該当コード行の特定 |
| GitHub | Issue 起票、ブランチ作成、PR 作成、CI 状況の確認、セルフレビュー投稿 |

## 守っているルール

- **Claude Code は自分の PR を自分で approve しない。** GitHub 自身がセルフ承認を
  禁止しており、CI が green になったこと・セルフレビューで見つけた懸念を潰したことを
  確認した上で、最後は人間に判断を委ねてコメントで引き継ぐ。
- **CI の green だけが客観的な検証結果。** 手元の pytest 実行結果は自己申告に過ぎない
  という前提で、必ず GitHub Actions 上の結果を確認してから完了と報告する。
- **`main` への直接 push は禁止。** ブランチ保護により PR 経由でのマージのみを許可し、
  `pytest` の CI チェックが通らない変更はマージできない設定にしている。
