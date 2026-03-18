import argparse
import sys
import json
import os
import requests

BASE_URL = "https://pro-api.solscan.io/v2.0"

def get_api_key():
    api_key = os.environ.get("SOLSCAN_API_KEY")
    if not api_key:
        print("Error: SOLSCAN_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return api_key

def make_request(endpoint, params=None):
    api_key = get_api_key()
    headers = {
        "token": api_key,
        "User-Agent": "Agent-Skill/1.0"
    }
    url = f"{BASE_URL}{endpoint}"
    # Remove None values
    if params:
        params = {k: v for k, v in params.items() if v is not None}
        
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response Body: {e.response.text}", file=sys.stderr)
        sys.exit(1)

def print_result(data):
    print(json.dumps(data, indent=2))

# --- Account Commands ---
def setup_account_parser(subparsers):
    parser = subparsers.add_parser('account', help='Account operations')
    sp = parser.add_subparsers(dest='action', required=True)

    sp.add_parser('detail', help='Get account details').add_argument('--address', required=True)
    sp.add_parser('data-decoded', help='Get decoded data').add_argument('--address', required=True)
    
    p_tokens = sp.add_parser('tokens', help='Get token accounts')
    p_tokens.add_argument('--address', required=True)
    p_tokens.add_argument('--type', required=True, choices=['token', 'nft'], help='Type of token: token or nft')
    p_tokens.add_argument('--page', type=int, default=1)
    p_tokens.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40], help='Items per page: 10, 20, 30, or 40')
    p_tokens.add_argument('--hide-zero', action='store_true', help='Filter tokens with zero amount')

    p_txs = sp.add_parser('transactions', help='Get account transactions')
    p_txs.add_argument('--address', required=True)
    p_txs.add_argument('--before', help='Cursor for pagination (transaction signature)')
    p_txs.add_argument('--limit', type=int, default=10, choices=[10, 20, 30, 40], help='Number of transactions')
    
    p_transfers = sp.add_parser('transfers', help='Get transfers')
    p_transfers.add_argument('--address', required=True)
    p_transfers.add_argument('--activity-type', help='Activity type (comma-separated): ACTIVITY_SPL_TRANSFER,ACTIVITY_SPL_BURN,ACTIVITY_SPL_MINT,etc')
    p_transfers.add_argument('--token-account', help='Filter by specific token account address')
    p_transfers.add_argument('--from', help='Filter from address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--exclude-from', help='Exclude from address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--to', help='Filter to address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--exclude-to', help='Exclude to address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--token', help='Filter by token address(es) (max 5, comma-separated)')
    p_transfers.add_argument('--amount', nargs=2, type=float, help='Amount range (min max)')
    p_transfers.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_transfers.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_transfers.add_argument('--exclude-amount-zero', action='store_true', help='Exclude zero amount transfers')
    p_transfers.add_argument('--flow', choices=['in', 'out'], help='Transfer direction: in or out')
    p_transfers.add_argument('--page', type=int, default=1)
    p_transfers.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100], help='Items per page')
    p_transfers.add_argument('--sort-order', choices=['asc', 'desc'], default='desc', help='Sort order')
    p_transfers.add_argument('--value', nargs=2, type=float, help='Value range in USD (min max)')

    p_stake = sp.add_parser('stake', help='Get stake accounts')
    p_stake.add_argument('--address', required=True)
    p_stake.add_argument('--page', type=int, default=1)
    p_stake.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40], help='Items per page')
    p_stake.add_argument('--sort-by', default='active_stake', choices=['active_stake', 'delegated_stake'], help='Sort by field')
    p_stake.add_argument('--sort-order', choices=['asc', 'desc'], help='Sort order: asc or desc')
    p_portfolio = sp.add_parser('portfolio', help='Get portfolio')
    p_portfolio.add_argument('--address', required=True)
    p_portfolio.add_argument('--exclude-low-score-tokens', action='store_true', help='Exclude low score tokens')

    p_defi = sp.add_parser('defi', help='Get DeFi activities')
    p_defi.add_argument('--address', required=True)
    p_defi.add_argument('--activity-type', help='Filter by activity type(s) (comma-separated): ACTIVITY_TOKEN_SWAP,ACTIVITY_AGG_TOKEN_SWAP,etc')
    p_defi.add_argument('--from', help='Filter from address')
    p_defi.add_argument('--platform', help='Filter by platform(s) (comma-separated, max 5)')
    p_defi.add_argument('--source', help='Filter by source(s) (comma-separated, max 5)')
    p_defi.add_argument('--token', help='Filter by token address')
    p_defi.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_defi.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_defi.add_argument('--page', type=int, default=1)
    p_defi.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    p_defi.add_argument('--sort-order', default='desc', choices=['asc', 'desc'])

    sp.add_parser('defi-export', help='Export DeFi activities').add_argument('--address', required=True)

    p_balance = sp.add_parser('balance-change', help='Get balance changes')
    p_balance.add_argument('--address', required=True)
    p_balance.add_argument('--token-account', help='Filter by token account address')
    p_balance.add_argument('--token', help='Filter by token address')
    p_balance.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_balance.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_balance.add_argument('--amount', nargs=2, type=float, help='Amount range (min max)')
    p_balance.add_argument('--flow', choices=['in', 'out'], help='Transfer direction: in or out')
    p_balance.add_argument('--remove-spam', choices=['true', 'false'], help='Remove spam transactions')
    p_balance.add_argument('--page', type=int, default=1)
    p_balance.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    p_balance.add_argument('--sort-order', default='desc', choices=['asc', 'desc'])

    sp.add_parser('reward-export', help='Export rewards').add_argument('--address', required=True)
    sp.add_parser('transfer-export', help='Export transfers').add_argument('--address', required=True)
    
    sp.add_parser('metadata', help='Get metadata').add_argument('--address', required=True)
    sp.add_parser('metadata-multi', help='Get multiple metadata').add_argument('--addresses', required=True, help='Comma separated addresses')

    p_leader = sp.add_parser('leaderboard', help='Get leaderboard')
    p_leader.add_argument('--page', type=int, default=1)
    p_leader.add_argument('--page-size', type=int, default=10)

def handle_account(args):
    if args.action == 'detail': return make_request("/account/detail", {"address": args.address})
    elif args.action == 'data-decoded': return make_request("/account/data-decoded", {"address": args.address})
    elif args.action == 'tokens': return make_request("/account/token-accounts", {"address": args.address, "type": args.type, "page": args.page, "page_size": args.page_size, "hide_zero": args.hide_zero})
    elif args.action == 'transactions':
        params = {"address": args.address, "limit": args.limit}
        if args.before: params["before"] = args.before
        return make_request("/account/transactions", params)
    elif args.action == 'transfers':
        params = {
            "address": args.address,
            "page": args.page,
            "page_size": args.page_size,
            "sort_order": args.sort_order
        }
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if args.token_account: params["token_account"] = args.token_account
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if args.exclude_from: params["exclude_from"] = args.exclude_from
        if getattr(args, 'to'): params["to"] = getattr(args, 'to')
        if args.exclude_to: params["exclude_to"] = args.exclude_to
        if args.token: params["token"] = args.token
        if args.amount: params["amount"] = args.amount
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        if args.exclude_amount_zero: params["exclude_amount_zero"] = args.exclude_amount_zero
        if args.flow: params["flow"] = args.flow
        if args.value: params["value"] = args.value
        return make_request("/account/transfer", params)
    elif args.action == 'stake':
        params = {
            "address": args.address,
            "page": args.page,
            "page_size": args.page_size,
            "sort_by": args.sort_by
        }
        if args.sort_order: params["sort_order"] = args.sort_order
        return make_request("/account/stake", params)
    elif args.action == 'portfolio':
        params = {"address": args.address}
        if args.exclude_low_score_tokens: params["exclude_low_score_tokens"] = args.exclude_low_score_tokens
        return make_request("/account/portfolio", params)
    elif args.action == 'defi':
        params = {"address": args.address, "page": args.page, "page_size": args.page_size, "sort_order": args.sort_order}
        if args.activity_type: params["activity_type"] = args.activity_type.split(',')
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if args.platform: params["platform"] = args.platform.split(',')
        if args.source: params["source"] = args.source.split(',')
        if args.token: params["token"] = args.token
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/account/defi/activities", params)
    elif args.action == 'defi-export': return make_request("/account/defi/activities/export", {"address": args.address})
    elif args.action == 'balance-change':
        params = {"address": args.address, "page": args.page, "page_size": args.page_size, "sort_order": args.sort_order}
        if args.token_account: params["token_account"] = args.token_account
        if args.token: params["token"] = args.token
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        if args.amount: params["amount"] = args.amount
        if args.flow: params["flow"] = args.flow
        if args.remove_spam: params["remove_spam"] = args.remove_spam
        return make_request("/account/balance_change", params)
    elif args.action == 'reward-export': return make_request("/account/reward/export", {"address": args.address})
    elif args.action == 'transfer-export': return make_request("/account/transfer/export", {"address": args.address})
    elif args.action == 'metadata': return make_request("/account/metadata", {"address": args.address})
    elif args.action == 'metadata-multi': return make_request("/account/metadata/multi", {"address": args.addresses})
    elif args.action == 'leaderboard': return make_request("/account/leaderboard", {"page": args.page, "page_size": args.page_size})

# --- Token Commands ---
def setup_token_parser(subparsers):
    parser = subparsers.add_parser('token', help='Token operations')
    sp = parser.add_subparsers(dest='action', required=True)

    sp.add_parser('meta', help='Get metadata').add_argument('--address', required=True)
    sp.add_parser('meta-multi', help='Get multiple metadata').add_argument('--addresses', required=True)
    
    p_holders = sp.add_parser('holders', help='Get holders')
    p_holders.add_argument('--address', required=True)
    p_holders.add_argument('--page', type=int, default=1)
    p_holders.add_argument('--page-size', type=int, default=10)
    
    sp.add_parser('price', help='Get price').add_argument('--address', required=True)
    sp.add_parser('price-multi', help='Get multiple prices').add_argument('--addresses', required=True)

    p_market = sp.add_parser('markets', help='Get markets')
    p_market.add_argument('--token', required=True, help='Token address(es) (max 5, comma-separated)')
    p_market.add_argument('--page', type=int, default=1)
    p_market.add_argument('--page-size', type=int, default=10)
    p_market.add_argument('--program', help='Filter by DEX program')
    p_market.add_argument('--sort-by', help='Sort by field (e.g., created_time)')
    
    sp.add_parser('trending', help='Get trending').add_argument('--limit', type=int, default=10)

    p_list = sp.add_parser('list', help='List tokens')
    p_list.add_argument('--page', type=int, default=1)
    p_list.add_argument('--page-size', type=int, default=10)
    p_list.add_argument('--sort-by', default='holder', choices=['holder', 'market_cap', 'created_time'], help='Sort field')
    p_list.add_argument('--sort-order', default='desc', choices=['asc', 'desc'], help='Sort order')

    sp.add_parser('top', help='Get top tokens')
    p_latest = sp.add_parser('latest', help='Get latest tokens')
    p_latest.add_argument('--platform-id', help='Filter by platform', choices=['jupiter','lifinity','meteora','orca','raydium','phoenix','sanctum','kamino','pumpfun','openbook','apepro','stabble','jupiterdca','jupiter_limit_order','solfi','zerofi','letsbonkfun_launchpad','raydium_launchlab','believe_launchpad','moonshot_launchpad','jup_studio_launchpad','bags_launchpad'])
    p_latest.add_argument('--page', type=int, default=1)
    p_latest.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    
    p_transfer = sp.add_parser('transfers', help='Get token transfers')
    p_transfer.add_argument('--address', required=True)
    p_transfer.add_argument('--page', type=int, default=1)
    p_transfer.add_argument('--page-size', type=int, default=10)

    p_defi = sp.add_parser('defi', help='Get DeFi activities')
    p_defi.add_argument('--address', required=True)
    p_defi.add_argument('--page', type=int, default=1)
    p_defi.add_argument('--page-size', type=int, default=10)
    
    sp.add_parser('defi-export', help='Export DeFi activities').add_argument('--address', required=True)
    
    p_hist = sp.add_parser('historical', help='Get historical price data')
    p_hist.add_argument('--address', required=True)
    p_hist.add_argument('--range', type=int, choices=[7, 30], help='Time range in days (7 or 30)')
    p_hist.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_hist.add_argument('--to-time', type=int, help='To Unix timestamp')

    p_search = sp.add_parser('search', help='Search tokens')
    p_search.add_argument('--keyword', required=True)
    p_search.add_argument('--page', type=int, default=1)
    p_search.add_argument('--page-size', type=int, default=10)
    p_search.add_argument('--search-by', choices=['combination', 'address', 'name', 'symbol'], help='Search field')
    p_search.add_argument('--search-mode', choices=['exact', 'fuzzy'], help='Search mode')

def handle_token(args):
    if args.action == 'meta': return make_request("/token/meta", {"address": args.address})
    elif args.action == 'meta-multi': return make_request("/token/meta/multi", {"address": args.addresses})
    elif args.action == 'holders': return make_request("/token/holders", {"address": args.address, "page": args.page, "page_size": args.page_size})
    elif args.action == 'price': return make_request("/token/price", {"address": args.address})
    elif args.action == 'price-multi': return make_request("/token/price/multi", {"address": args.addresses})
    elif args.action == 'markets':
        params = {
            "token": args.token.split(',') if args.token else [],
            "page": args.page,
            "page_size": args.page_size
        }
        if args.program: params["program"] = args.program
        if args.sort_by: params["sort_by"] = args.sort_by
        return make_request("/token/markets", params)
    elif args.action == 'trending': return make_request("/token/trending", {"limit": args.limit})
    elif args.action == 'list': return make_request("/token/list", {"page": args.page, "page_size": args.page_size, "sort_by": args.sort_by, "sort_order": args.sort_order})
    elif args.action == 'top': return make_request("/token/top")
    elif args.action == 'latest':
        params = {"page": args.page, "page_size": args.page_size}
        if args.platform_id: params["platform_id"] = args.platform_id
        return make_request("/token/latest", params)
    elif args.action == 'transfers': return make_request("/token/transfer", {"address": args.address, "page": args.page, "page_size": args.page_size})
    elif args.action == 'defi': return make_request("/token/defi/activities", {"address": args.address, "page": args.page, "page_size": args.page_size})
    elif args.action == 'defi-export': return make_request("/token/defi/activities/export", {"address": args.address})
    elif args.action == 'historical':
        params = {"address": args.address}
        if args.range: params["range"] = args.range
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/token/historical-data", params)
    elif args.action == 'search':
        params = {"keyword": args.keyword, "page": args.page, "page_size": args.page_size}
        if args.search_by: params["search_by"] = args.search_by
        if args.search_mode: params["search_mode"] = args.search_mode
        return make_request("/token/search", params)


# --- Transaction Commands ---
def setup_transaction_parser(subparsers):
    parser = subparsers.add_parser('transaction', help='Transaction operations')
    sp = parser.add_subparsers(dest='action', required=True)

    sp.add_parser('detail', help='Get details').add_argument('--signature', required=True)
    sp.add_parser('detail-multi', help='Get multiple details').add_argument('--signatures', required=True, help='Comma separated keys')
    sp.add_parser('last', help='Get last transactions').add_argument('--limit', type=int, default=10)
    
    p_actions = sp.add_parser('actions', help='Get actions')
    p_actions.add_argument('--signature', required=True)

    p_actions_m = sp.add_parser('actions-multi', help='Get multiple actions')
    p_actions_m.add_argument('--signatures', required=True)
    
    sp.add_parser('fees', help='Get network fees statistics')

def handle_transaction(args):
    if args.action == 'detail': return make_request("/transaction/detail", {"tx": args.signature})
    elif args.action == 'detail-multi': return make_request("/transaction/detail/multi", {"txs": args.signatures})
    elif args.action == 'last': return make_request("/transaction/last", {"limit": args.limit})
    elif args.action == 'actions': return make_request("/transaction/actions", {"tx": args.signature})
    elif args.action == 'actions-multi': return make_request("/transaction/actions/multi", {"txs": args.signatures})
    elif args.action == 'fees': return make_request("/transaction/fees")


# --- NFT Commands ---
def setup_nft_parser(subparsers):
    parser = subparsers.add_parser('nft', help='NFT operations')
    sp = parser.add_subparsers(dest='action', required=True)
    
    p_news = sp.add_parser('news', help='Get NFT news/activities')
    p_news.add_argument('--filter', required=True, choices=['created_time'], help='Filter type (default: created_time)')
    p_news.add_argument('--page', type=int, default=1)
    p_news.add_argument('--page-size', type=int, default=12, choices=[12, 24, 36])
    
    p_act = sp.add_parser('activities', help='Get NFT activities')
    p_act.add_argument('--from', help='Filter from address')
    p_act.add_argument('--to', help='Filter to address')
    p_act.add_argument('--source', help='Filter by source')
    p_act.add_argument('--activity-type', help='Filter by activity type')
    p_act.add_argument('--token', help='Filter by token address')
    p_act.add_argument('--collection', help='Filter by collection')
    p_act.add_argument('--from-time', type=int, help='From Unix timestamp')
    p_act.add_argument('--to-time', type=int, help='To Unix timestamp')
    p_act.add_argument('--page', type=int, default=1)
    p_act.add_argument('--page-size', type=int, default=12, choices=[12, 24, 36])
    
    p_cols = sp.add_parser('collections', help='Get collections')
    p_cols.add_argument('--page', type=int, default=1)
    p_cols.add_argument('--page-size', type=int, default=10)
    
    p_items = sp.add_parser('items', help='Get collection items')
    p_items.add_argument('--address', required=True)
    p_items.add_argument('--page', type=int, default=1)
    p_items.add_argument('--page-size', type=int, default=10)

def handle_nft(args):
    if args.action == 'news': return make_request("/nft/news", {"filter": args.filter, "page": args.page, "page_size": args.page_size})
    elif args.action == 'activities':
        params = {"page": args.page, "page_size": args.page_size}
        if getattr(args, 'from'): params["from"] = getattr(args, 'from')
        if getattr(args, 'to'): params["to"] = getattr(args, 'to')
        if args.source: params["source"] = args.source
        if args.activity_type: params["activity_type"] = args.activity_type
        if args.token: params["token"] = args.token
        if args.collection: params["collection"] = args.collection
        if args.from_time: params["from_time"] = args.from_time
        if args.to_time: params["to_time"] = args.to_time
        return make_request("/nft/activities", params)
    elif args.action == 'collections': return make_request("/nft/collection/lists", {"page": args.page, "page_size": args.page_size})
    elif args.action == 'items': return make_request("/nft/collection/items", {"collection": args.address, "page": args.page, "page_size": args.page_size})


# --- Block Commands ---
def setup_block_parser(subparsers):
    parser = subparsers.add_parser('block', help='Block operations')
    sp = parser.add_subparsers(dest='action', required=True)
    
    p_last = sp.add_parser('last', help='Get last blocks')
    p_last.add_argument('--limit', type=int, default=10, help='Limit (10, 20, 30, 40, 60, 100)')
    
    sp.add_parser('detail', help='Get block detail').add_argument('--block', required=True)
    
    p_txs = sp.add_parser('transactions', help='Get block transactions')
    p_txs.add_argument('--block', required=True)
    p_txs.add_argument('--page', type=int, default=1)
    p_txs.add_argument('--page-size', type=int, default=10)
    p_txs.add_argument('--exclude-vote', action='store_true', help='Exclude voting transactions')
    p_txs.add_argument('--program', help='Filter by program')

def handle_block(args):
    if args.action == 'last': return make_request("/block/last", {"limit": args.limit})
    elif args.action == 'detail': return make_request("/block/detail", {"block": args.block})
    elif args.action == 'transactions':
        params = {"block": args.block, "page": args.page, "page_size": args.page_size}
        if args.exclude_vote: params["exclude_vote"] = args.exclude_vote
        if args.program: params["program"] = args.program
        return make_request("/block/transactions", params)


# --- Market Commands ---
def setup_market_parser(subparsers):
    parser = subparsers.add_parser('market', help='Market operations')
    sp = parser.add_subparsers(dest='action', required=True)
    
    p_mlist = sp.add_parser('list', help='List markets')
    p_mlist.add_argument('--page', type=int, default=1)
    p_mlist.add_argument('--page-size', type=int, default=10, choices=[10, 20, 30, 40, 60, 100])
    p_mlist.add_argument('--program', help='Filter by program')
    p_mlist.add_argument('--token-address', help='Filter by token address')
    p_mlist.add_argument('--sort-by', default='volumes_24h', choices=['created_time', 'volumes_24h', 'trades_24h'])
    p_mlist.add_argument('--sort-order', default='desc', choices=['asc', 'desc'])

    sp.add_parser('info', help='Market info').add_argument('--address', required=True)

    p_mvol = sp.add_parser('volume', help='Market volume')
    p_mvol.add_argument('--address', required=True)
    p_mvol.add_argument('--time', nargs=2, help='Time range as YYYYMMDD (start end)')

def handle_market(args):
    if args.action == 'list':
        params = {"page": args.page, "page_size": args.page_size, "sort_by": args.sort_by, "sort_order": args.sort_order}
        if args.program: params["program"] = args.program
        if args.token_address: params["token_address"] = args.token_address
        return make_request("/market/list", params)
    elif args.action == 'info': return make_request("/market/info", {"address": args.address})
    elif args.action == 'volume':
        params = {"address": args.address}
        if args.time: params["time"] = args.time
        return make_request("/market/volume", params)

# --- Program Commands ---
def setup_program_parser(subparsers):
    parser = subparsers.add_parser('program', help='Program operations')
    sp = parser.add_subparsers(dest='action', required=True)
    
    p_list = sp.add_parser('list', help='List programs')
    p_list.add_argument('--page', type=int, default=1)
    p_list.add_argument('--page-size', type=int, default=10)
    p_list.add_argument('--sort-by', default='num_txs', choices=['num_txs','num_txs_success','interaction_volume','success_rate','active_users_24h'])
    p_list.add_argument('--sort-order', default='desc', choices=['asc', 'desc'])
    
    sp.add_parser('popular', help='Popular platforms')
    
    p_analytics = sp.add_parser('analytics', help='Program analytics')
    p_analytics.add_argument('--address', required=True)
    p_analytics.add_argument('--range', type=int, required=True, choices=[7, 30], help='Analytics range in days (7 or 30)')

def handle_program(args):
    if args.action == 'list': return make_request("/program/list", {"page": args.page, "page_size": args.page_size, "sort_by": args.sort_by, "sort_order": args.sort_order})
    elif args.action == 'popular': return make_request("/program/popular/platforms")
    elif args.action == 'analytics': return make_request("/program/analytics", {"address": args.address, "range": args.range})

# --- Monitor Commands ---
def setup_monitor_parser(subparsers):
    parser = subparsers.add_parser('monitor', help='Monitor operations')
    sp = parser.add_subparsers(dest='action', required=True)
    
    sp.add_parser('usage', help='Get API usage')

def handle_monitor(args):
    if args.action == 'usage': return make_request("/monitor/usage")

def main():
    parser = argparse.ArgumentParser(description="Solscan Pro CLI Tool")
    subparsers = parser.add_subparsers(dest='resource', required=True)

    setup_account_parser(subparsers)
    setup_token_parser(subparsers)
    setup_transaction_parser(subparsers)
    setup_nft_parser(subparsers)
    setup_block_parser(subparsers)
    setup_market_parser(subparsers)
    setup_program_parser(subparsers)
    setup_monitor_parser(subparsers)

    args = parser.parse_args()

    data = {}
    if args.resource == 'account': data = handle_account(args)
    elif args.resource == 'token': data = handle_token(args)
    elif args.resource == 'transaction': data = handle_transaction(args)
    elif args.resource == 'nft': data = handle_nft(args)
    elif args.resource == 'block': data = handle_block(args)
    elif args.resource == 'market': data = handle_market(args)
    elif args.resource == 'program': data = handle_program(args)
    elif args.resource == 'monitor': data = handle_monitor(args)

    print_result(data)

if __name__ == "__main__":
    main()
