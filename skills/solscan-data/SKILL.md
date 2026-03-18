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
| `account defi` | `--address [filters...]` | DeFi protocol interactions (activity-type, from, platform, source, token, time range) |
| `account balance-change` | `--address [filters...]` | Historical balance changes (token, flow, amount, time range, remove-spam) |
| `account transactions` | `--address [--before] [--limit]` | Recent transactions list (cursor-based pagination) |
| `account portfolio` | `--address [--exclude-low-score-tokens]` | Token holdings with USD value |
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

> **`account transactions` pagination**:
> - Uses cursor-based pagination with `--before` (transaction signature)
> - `--limit`: 10, 20, 30, 40 (default: 10)
> - No page/page_size parameters

> **`token search` parameters**:
> - `--keyword`: Search term (required)
> - `--search-by`: combination|address|name|symbol
> - `--search-mode`: exact|fuzzy
> - `--page`, `--page-size`: Standard pagination

> **`nft activities` parameters** (all optional):
> - `--from`, `--to`: Filter by address
> - `--activity-type`: Type of activity
> - `--token`: Token address
> - `--collection`: Collection address
> - `--from-time`, `--to-time`: Unix timestamp range
> - `--page-size`: 12, 24, 36 (default: 12)

> **`token markets` parameters**:
> - `--token`: Token address(es) - REQUIRED (max 5, comma-separated)
> - `--program`: Filter by DEX program
> - `--sort-by`: Sort field (e.g., created_time)
> - `--page`, `--page-size`: Standard pagination

> **`program analytics` parameters**:
> - `--address`: Program address (required)
> - `--range`: 7 or 30 days (required)

> **`token historical` parameters**:
> - `--address`: Token address (required)
> - `--range`: 7 or 30 days
> - `--from-time`, `--to-time`: Unix timestamp range

> **`account defi` filter options**:
> - `--activity-type`: ACTIVITY_TOKEN_SWAP, ACTIVITY_AGG_TOKEN_SWAP, ACTIVITY_TOKEN_ADD_LIQ, ACTIVITY_TOKEN_REMOVE_LIQ, ACTIVITY_POOL_CREATE, ACTIVITY_SPL_TOKEN_STAKE, ACTIVITY_LST_STAKE, ACTIVITY_SPL_TOKEN_UNSTAKE, ACTIVITY_LST_UNSTAKE, ACTIVITY_TOKEN_DEPOSIT_VAULT, ACTIVITY_TOKEN_WITHDRAW_VAULT, ACTIVITY_SPL_INIT_MINT, ACTIVITY_ORDERBOOK_ORDER_PLACE, ACTIVITY_BORROWING, ACTIVITY_REPAY_BORROWING, ACTIVITY_LIQUIDATE_BORROWING, ACTIVITY_BRIDGE_ORDER_IN, ACTIVITY_BRIDGE_ORDER_OUT
> - `--from`: Filter by source address
> - `--platform`, `--source`: Filter by platform/source (comma-separated, max 5)
> - `--token`: Filter by token address
> - `--from-time`, `--to-time`: Unix timestamp range
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)

> **`account balance-change` filter options**:
> - `--token-account`: Filter by specific token account
> - `--token`: Filter by token address
> - `--amount`: Amount range (min max)
> - `--flow`: in|out
> - `--remove-spam`: true|false
> - `--from-time`, `--to-time`: Unix timestamp range
> - `--page-size`: 10, 20, 30, 40, 60, 100 (default: 10)

> **`token latest` platforms**:
> - `--platform-id`: jupiter, lifinity, meteora, orca, raydium, phoenix, sanctum, kamino, pumpfun, openbook, apepro, stabble, jupiterdca, jupiter_limit_order, solfi, zerofi, letsbonkfun_launchpad, raydium_launchlab, believe_launchpad, moonshot_launchpad, jup_studio_launchpad, bags_launchpad

### Token

| Action | Key Params | Returns |
|---|---|---|
| `token meta` | `--address` | Name, symbol, decimals, supply |
| `token meta-multi` | `--addresses` | Batch metadata |
| `token price` | `--address` | Current USD price |
| `token price-multi` | `--addresses` | Batch prices |
| `token holders` | `--address` | Top holder list with amounts |
| `token markets` | `--token [--page] [--page-size] [--program] [--sort-by]` | DEX markets for token(s) (max 5 tokens, comma-separated) |
| `token transfers` | `--address` | Transfer history |
| `token defi` | `--address` | DeFi activity |
| `token defi-export` | `--address` | DeFi activity CSV |
| `token historical` | `--address [--range] [--from-time] [--to-time]` | Historical price data (range: 7 or 30 days) |
| `token search` | `--keyword [--page] [--page-size] [--search-by] [--search-mode]` | Search tokens by keyword/address/name/symbol |
| `token trending` | — | Currently trending tokens |
| `token list` | `[--page] [--page-size] [--sort-by] [--sort-order]` | Full token list (sort: holder|market_cap|created_time) |
| `token top` | — | Top tokens by market cap |
| `token latest` | `[--platform-id] [--page] [--page-size]` | Newly listed tokens (page-size: 10/20/30/40/60/100) |

### Transaction

| Action | Key Params | Returns |
|---|---|---|
| `transaction detail` | `--signature` | Full tx details |
| `transaction detail-multi` | `--signatures` | Batch tx details |
| `transaction last` | — | Most recent transactions |
| `transaction actions` | `--signature` | Human-readable decoded actions |
| `transaction actions-multi` | `--signatures` | Batch decoded actions |
| `transaction fees` | — | Network fees statistics (no parameters) |

### NFT

| Action | Key Params | Returns |
|---|---|---|
| `nft news` | `--filter [--page] [--page-size]` | Latest NFT activity feed (filter: created_time, page-size: 12/24/36) |
| `nft activities` | `[filters...]` | NFT activities (all filters optional: from, to, activity-type, token, collection, etc.) |
| `nft collections` | — | Top NFT collections |
| `nft items` | `--address` | Items inside a collection |

### Block

| Action | Key Params | Returns |
|---|---|---|
| `block last` | — | Most recent blocks |
| `block detail` | `--block` | Block metadata by slot number |
| `block transactions` | `--block [--page] [--page-size] [--exclude-vote] [--program]` | Transactions in block (exclude voting tx optional) |

### Market

| Action | Key Params | Returns |
|---|---|---|
| `market list` | `[--page] [--page-size] [--program] [--token-address] [--sort-by] [--sort-order]` | All trading pools/markets (sort: created_time\|volumes_24h\|trades_24h) |
| `market info` | `--address` | Market pool details by address |
| `market volume` | `--address [--time]` | Market volume data |

### Program

| Action | Key Params | Returns |
|---|---|---|
| `program list` | `[--sort-by] [--sort-order] [--page] [--page-size]` | All indexed programs (sort: num_txs\|num_txs_success\|interaction_volume\|success_rate\|active_users_24h) |
| `program popular` | — | Most-used programs |
| `program analytics` | `--address --range` | Program analytics (range: 7 or 30 days, required) |

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
- [ ] Step 4: `token markets --token <MINT>` → find best liquidity pools

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
