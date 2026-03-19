# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**agent-skills** is an AI agent skills repository that provides integration with the Solscan Pro API (v2.0). The primary skill, `solscan-data`, wraps the entire Solscan Pro API as a Python CLI tool that agents can invoke to query Solana blockchain data.

This follows the [Agent Skills](https://agentskills.io/) format for standardized agent integration.

## Architecture

### Repository Structure

```
skills/
  solscan-data/
    SKILL.md                 # Comprehensive API documentation and usage guide
    scripts/
      solscan.py            # Main CLI implementation (~488 lines)
```

### Core Implementation Pattern

**`solscan.py`** is a single Python script that:
1. Defines CLI command structure using `argparse` with main commands (account, token, transaction, nft, block, market, program, monitor)
2. Each command has subcommands mapping to API endpoints
3. Builds HTTP requests to Solscan Pro API base URL (`https://pro-api.solscan.io/v2.0`)
4. Handles authentication via `SOLSCAN_API_KEY` environment variable passed as `token` header
5. Returns JSON responses from the API

**Key architectural decisions:**
- Single-file design keeps the CLI self-contained and easy to test
- Argument validation happens at parse time (e.g., `choices`, `type` constraints)
- Parameter mapping is explicit: CLI args → query params for the API request
- All responses are printed as JSON (via `json.dumps()`)

### API Command Structure

The script provides ~50+ API endpoints organized into 8 resource types:

- **Account**: detail, tokens (with type: token|nft), transactions, transfers, stake, portfolio, defi, balance-change, metadata, leaderboard, export operations
- **Token**: meta, price, holders, markets, transfers, defi, search, trending, list, latest, historical
- **Transaction**: detail, actions, fees, last
- **NFT**: news, activities, collections, items
- **Block**: last, detail, transactions
- **Market**: list, info, volume
- **Program**: list, popular, analytics
- **Monitor**: usage

Each endpoint supports specific parameters (filters, pagination, sorting) documented in `SKILL.md`.

## Development Commands

### Validate Script Syntax

```bash
python3 -m py_compile skills/solscan-data/scripts/solscan.py
```

This is the only validation allowed in `.claude/settings.local.json`. It checks for Python syntax errors without executing the script.

### Test API Calls (manual)

With `SOLSCAN_API_KEY` environment variable set:

```bash
# Get account metadata
python3 skills/solscan-data/scripts/solscan.py account metadata --address <ADDRESS>

# Get token price
python3 skills/solscan-data/scripts/solscan.py token price --address <TOKEN_ADDRESS>

# Get transaction details
python3 skills/solscan-data/scripts/solscan.py transaction detail --signature <SIGNATURE>
```

## Key Implementation Details

### Parameter Handling

- Required parameters are marked with `required=True` in argparse
- Optional parameters use `default` values (e.g., `--page-size` defaults to 10)
- Filters support multiple values as comma-separated strings (max constraints enforced in `SKILL.md`)
- Pagination uses either `--page`/`--page-size` (offset-based) or `--before` (cursor-based for transactions)
- Amount/value ranges use `nargs=2` with min/max values

### Error Handling

- HTTP errors caught and printed to stderr with request exception details
- API response body printed on failure for debugging
- Non-zero exit code (1) on any API error
- Invalid arguments caught by argparse before API call

### API Key Management

- API key required via `SOLSCAN_API_KEY` environment variable
- Script exits with error message if not set
- Header passed as `token` (not `Authorization`)

## Common Tasks

### Adding a New API Endpoint

1. Add a new subparser in the appropriate `setup_*_parser()` function in `solscan.py`
2. Map CLI arguments to API query parameters
3. Add the endpoint handler in the main command routing
4. Update `SKILL.md` with the new endpoint documentation and parameters
5. Test with `python3 -m py_compile` to validate syntax
6. Document any new parameter constraints or pagination behavior in `SKILL.md`

### Modifying Existing Parameters

- Check `SKILL.md` first for API documentation on valid values/constraints
- Update argparse configuration (e.g., `choices`, `nargs`, defaults)
- Ensure parameter names match the API's expected query param names
- Test with example calls to confirm mapping works

### Updating API Documentation

- `SKILL.md` is the source of truth for endpoint capabilities and usage
- When adding endpoints or parameters, update the relevant sections in `SKILL.md`
- Include example filters and constraints in the parameter tables and notes
- Add new endpoints to "When to Use This Skill" section if triggering new agent use cases

## Notes for Future Work

- The script currently uses positional command structure (`account detail`, `token price`, etc.) — this maps cleanly to API endpoint organization
- All response data is raw JSON from the API — agents parse this for filtering/formatting
- Pagination varies by endpoint: some use `page`/`page-size`, transactions use cursor (`--before`), NFT uses different page-size constraints
- Rate limiting errors (429) are caught by requests library but not retried — agents should implement backoff
- API key is the sole authentication method; no session management
