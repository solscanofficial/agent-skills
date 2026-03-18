---
name: solscan-data
description: >
  Use this skill to query Solana blockchain data via the Solscan Pro API.
  Triggers: look up wallet address, check token price, analyze NFT collection,
  inspect transaction, explore DeFi activities, get account metadata/label/tags,
  fetch block info, monitor API usage, search token by keyword.
version: 2.0.0
license: MIT
---

# Solscan Pro Skill

Empowers AI agents to retrieve professional-grade Solana on-chain data across
accounts, tokens, NFTs, transactions, blocks, markets, and programs.

## When to Use This Skill

- User asks about a Solana wallet address, balance, portfolio, or stake
- User wants token price, holders, markets, or trending tokens
- User needs to inspect a transaction signature or decode instructions
- User asks about NFT collections, items, or recent NFT activity
- User wants DeFi activity, transfer history, or reward exports
- User wants to check program analytics or popular platforms

## Authentication

All requests require an API key in the HTTP header:

```http
token: <YOUR_SOLSCAN_API_KEY>
```

Base URL: `https://pro-api.solscan.io/v2.0`

---

## Tools

### Tool 1 — Direct API CLI (Precise Data)

**Use when**: you need exact, structured on-chain data for a specific address,
signature, block, or mint.

**Syntax**: `python3 scripts/solscan.py <resource> <action> [--param value]`

### Tool 2 — MCP Natural Language Tools

**Use when**: answering general exploratory questions or when the user does not
provide a specific address.

Available MCP tools:
- `search_transaction_by_signature` — look up a transaction by its signature
- `get_account_balance` — retrieve SOL balance for a wallet
- `get_token_metadata` — get name, symbol, decimals for a token mint

---

## API Reference

### Account

| Action | Key Params | Returns |
|---|---|---|
| `account detail` | `--address` | Lamports, owner, executable flag |
| `account transfers` | `--address [filters...]` | SPL + SOL transfer history (supports activity-type, token, flow, time range filters) |
| `account defi` | `--address` | DeFi protocol interactions |
| `account balance-change` | `--address` | Historical SOL balance changes |
| `account transactions` | `--address` | Recent transactions list |
| `account portfolio` | `--address` | Token holdings with USD value |
| `account tokens` | `--address --type [--page] [--page-size] [--hide-zero]` | Associated token/NFT accounts (page-size: 10/20/30/40) |
| `account stake` | `--address [--page] [--page-size] [--sort-by] [--sort-order]` | Active stake accounts (page-size: 10/20/30/40) |
| `account reward-export` | `--address` | Staking reward history CSV |
| `account transfer-export` | `--address` | Transfer history CSV |
| `account metadata` | `--address` | Label, icon, tags, domain, funder |
| `account metadata-multi` | `--addresses` | Batch metadata (comma-separated) |
| `account leaderboard` | — | Top accounts by activity |
| `account defi-export` | `--address` | DeFi activity CSV |

> **`account metadata` response fields**: `account_address`, `account_label`,
> `account_icon`, `account_tags`, `account_type`, `account_domain`,
> `funded_by`, `tx_hash`, `block_time`

> **`account transfers` filter options**:
> - `--activity-type`: ACTIVITY_SPL_TRANSFER, ACTIVITY_SPL_BURN, ACTIVITY_SPL_MINT, ACTIVITY_SPL_CREATE_ACCOUNT, ACTIVITY_SPL_CLOSE_ACCOUNT, ACTIVITY_SPL_TOKEN_WITHDRAW_STAKE, ACTIVITY_SPL_TOKEN_SPLIT_STAKE, ACTIVITY_SPL_TOKEN_MERGE_STAKE, ACTIVITY_SPL_VOTE_WITHDRAW, ACTIVITY_SPL_SET_OWNER_AUTHORITY
> - `--token`: Filter by token address(es) (max 5, comma-separated)
> - `--flow`: in|out (transfer direction)
> - `--from`, `--to`: Filter by address(es) (max 5, comma-separated)
> - `--amount`: Amount range (min max)
> - `--value`: USD value range (min max)
> - `--from-time`, `--to-time`: Unix timestamp range
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)

> **`account stake` options**:
> - `--sort-by`: active_stake|delegated_stake (default: active_stake)
> - `--sort-order`: asc|desc
> - `--page-size`: 10, 20, 30, 40 (default: 10)

### Token

| Action | Key Params | Returns |
|---|---|---|
| `token meta` | `--address` | Name, symbol, decimals, supply |
| `token meta-multi` | `--addresses` | Batch metadata |
| `token price` | `--address` | Current USD price |
| `token price-multi` | `--addresses` | Batch prices |
| `token holders` | `--address` | Top holder list with amounts |
| `token markets` | `--address` | DEX markets trading this token |
| `token transfers` | `--address` | Transfer history |
| `token defi` | `--address` | DeFi activity |
| `token defi-export` | `--address` | DeFi activity CSV |
| `token historical` | `--address --type line` | Price history chart data |
| `token search` | `--query` | Search by keyword/name |
| `token trending` | — | Currently trending tokens |
| `token list` | — | Full token list |
| `token top` | — | Top tokens by market cap |
| `token latest` | — | Newly listed tokens |

### Transaction

| Action | Key Params | Returns |
|---|---|---|
| `transaction detail` | `--signature` | Full tx details |
| `transaction detail-multi` | `--signatures` | Batch tx details |
| `transaction last` | — | Most recent transactions |
| `transaction actions` | `--signature` | Human-readable decoded actions |
| `transaction actions-multi` | `--signatures` | Batch decoded actions |
| `transaction fees` | `--signature` | Fee breakdown |

### NFT

| Action | Key Params | Returns |
|---|---|---|
| `nft news` | — | Latest NFT activity feed |
| `nft activities` | `--address` | NFT transfer/sale history |
| `nft collections` | — | Top NFT collections |
| `nft items` | `--address` | Items inside a collection |

### Block

| Action | Key Params | Returns |
|---|---|---|
| `block last` | — | Most recent blocks |
| `block detail` | `--block` | Block metadata by slot number |
| `block transactions` | `--block` | All transactions in a block |

### Market

| Action | Key Params | Returns |
|---|---|---|
| `market list` | — | All trading pools/markets |
| `market info` | — | General market overview |
| `market volume` | — | 24h volume data |

### Program

| Action | Key Params | Returns |
|---|---|---|
| `program list` | — | All indexed programs |
| `program popular` | — | Most-used programs |
| `program analytics` | `--address` | Usage stats for a program |

### Monitor

| Action | Key Params | Returns |
|---|---|---|
| `monitor usage` | — | Your API key usage & rate limits |

---

## Error Handling

| HTTP Code | Meaning | Agent Action |
|---|---|---|
| `400` | Bad request / invalid address | Validate address format, retry |
| `401` | Authentication failed | Check `token` header is set correctly |
| `429` | Rate limit exceeded | Wait and retry with backoff |
| `500` | Internal server error | Retry once; report if persistent |

All error responses include `success: false`, `code`, and `message` fields.

---

## Example Workflows

### Wallet Research Workflow
- [ ] Step 1: `account metadata --address <ADDR>` → confirm label and type
- [ ] Step 2: `account portfolio --address <ADDR>` → get token holdings
- [ ] Step 3: `account transfers --address <ADDR>` → review recent activity
- [ ] Step 4: `account defi --address <ADDR>` → check protocol interactions

### Token Analysis Workflow
- [ ] Step 1: `token meta --address <MINT>` → confirm token identity
- [ ] Step 2: `token price --address <MINT>` → get current price
- [ ] Step 3: `token holders --address <MINT>` → check concentration risk
- [ ] Step 4: `token markets --address <MINT>` → find best liquidity pools

---

## Evaluations

| Query | Expected Behavior |
|---|---|
| "What tokens does wallet `ABC123` hold?" | Calls `account portfolio --address ABC123`, returns token list with USD values |
| "What is the current price of BONK?" | Calls `token meta` to resolve mint, then `token price`, returns USD price |
| "Decode transaction `XYZ...`" | Calls `transaction actions --signature XYZ`, returns human-readable action list |
| "Is this a known wallet?" | Calls `account metadata --address`, returns label/tags/domain if available |

---

*Resources: [Solscan Pro API Docs](https://pro-api.solscan.io/pro-api-docs/v2.0), [Solscan Pro API FAQs](https://pro-api.solscan.io/pro-api-docs/v2.0/faq.md)*
