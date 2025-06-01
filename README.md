# Wallet Inspector MCP

An MCP server  that empowers AI agents to inspect any wallet’s balance and onchain activity across major EVM chains and Solana chain.

![GitHub License](https://img.shields.io/github/license/kukapay/wallet-inspector-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Multi-Chain Support**: Queries Solana, Ethereum, Polygon, Binance Smart Chain (BSC), Base, Arbitrum and more.
- **Flexible Output**: Balances in ASCII tables, activities and transactions in structured text.

## Installation

### Prerequisites

- **Python**: Version 3.10 or higher.
- **Dune SIM API Key**: Obtain from [Dune Analytics](https://dune.com).
- **Dependency Manager**: `uv` (recommended) or `pip`.

### Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/kukapay/wallet-inspector-mcp.git
   cd wallet-inspector-mcp
   ```

2. **Install Dependencies**:

   Using `uv` (recommended):

   ```bash
   uv async
   ```

   Or using `pip`:

   ```bash
   pip install mcp[cli] python-dotenv tabulate
   ```

3. **Installing to Claude Desktop**:

    Install the server as a Claude Desktop application:
    ```bash
    uv run mcp install cli.py --name "Wallet Inspector"
    ```

    Configuration file as a reference:

    ```json
    {
       "mcpServers": {
           "Wallet Inspector": {
               "command": "uv",
               "args": [ "--directory", "/path/to/wallet-inspector-mcp", "run", "main.py" ],
               "env": { "DUNE_SIM_API_KEY": "your_dune_sim_api_key_here"},               
           }
       }
    }
    ```
    Replace `/path/to/wallet-inspector-mcp` with your actual installation path, and `your_dune_sim_api_key_here` with your Dune SIM API key.

## Usage

### Interacting with the Server

Use an MCP-compatible client (e.g., Claude Desktop CLI) to query the server. Example natural language queries:

- **Balance Queries**:
  - "Check the balance of wallet 0xd8da6bf26964af9d7eed9e03e53415d37aa96045."
  - "What is the balance for wallet DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK?"
  - "Get balances for 0x1234567890abcdef1234567890abcdef12345678 on EVM chains."

- **Activity Queries** (EVM only):
  - "Show activity for wallet 0xd8da6bf26964af9d7eed9e03e53415d37aa96045."
  - "Get transaction history for 0x1234567890abcdef1234567890abcdef12345678 on EVM chains."

- **Transaction Queries**:
  - "List transactions for wallet 0xd8da6bf26964af9d7eed9e03e53415d37aa96045 with limit 50."
  - "Show transaction history for wallet DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK."
  - "Get the latest 10 transactions for 0x1234567890abcdef1234567890abcdef12345678."

### Example Outputs

- **Balance Output**:

  ```
  Wallet 0xd8da6bf26964af9d7eed9e03e53415d37aa96045 balances:

  +----------+-----------------+-------------+
  | Chain    | Token Amount    | USD Value   |
  +==========+=================+=============+
  | ethereum | 605.371497 ETH  | $1842034.66 |
  +----------+-----------------+-------------+
  | polygon  | 100.500000 MATIC| $50.25      |
  +----------+-----------------+-------------+
  | bsc      | 10.000000 BNB   | $600.00     |
  +----------+-----------------+-------------+

  Wallet DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK balances:

  +----------+---------------+-------------+
  | Chain    | Token Amount  | USD Value   |
  +==========+===============+=============+
  | solana   | 1.000000 SOL  | $20.50      |
  +----------+---------------+-------------+
  ```

- **Activity Output** (EVM only):

  ```
  Wallet 0xd8da6bf26964af9d7eed9e03e53415d37aa96045 activity:

  Chain ID: 8453
  Block Time: 2025-02-20T13:52:29+00:00
  Tx Hash: 0x184544c8d67a0cbed0a3f04abe5f958b96635e8c743c070f70e24b1c06cd1aa6
  Type: Receive
  Asset Type: ERC20
  Value: 123.069653 ENT
  USD Value: $0.14
  ```

- **Transaction Output**:

  ```
  Wallet 0xd8da6bf26964af9d7eed9e03e53415d37aa96045 transactions:

  Chain: ethereum
  Block Time: 2023-11-07T05:31:56Z
  Tx Hash: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
  From: 0xd8da6bf26964af9d7eed9e03e53415d37aa96045
  To: 0x1234567890abcdef1234567890abcdef12345678
  Value: 0.000320 ETH

  Wallet DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK transactions:

  Chain: solana
  Block Time: 2023-03-28T09:20:00Z
  Tx Hash: 5SzSbWKM9yZC7cCGMhUhvnYdWQytrk9NBaWwug1gQBKKwNEBvBKqPSfVeYYnZwUuUyvcCHgYhDkTRrB6YBfwzfv8
  From: DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK
  To: 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin
  Value: 0.010000 SOL
  ```

## Tools
### `get_wallet_balance`

- **Description**: Retrieves the balance of a specified wallet address across supported EVM and Solana blockchains.
- **Parameters**:
  - `wallet_address` (str): The wallet address to query (e.g., '0x123...' for EVM chains or 'DYw8jCT...' for Solana).
- **Returns**: An ASCII table with balance details (chain, token amount, USD value) or an error message.
- **Supported Chains**: Solana,arbitrum,arbitrum,avalanche_c,base,berachain,bnb,ethereum and more.

### `get_wallet_activity`

- **Description**: Queries transaction activity for a specified wallet address on supported EVM blockchains.
- **Parameters**:
  - `wallet_address` (str): The EVM-compatible wallet address to query (e.g., '0x123...').
- **Returns**: Formatted text with activity details (chain_id, block_time, tx_hash, type, asset_type, value, value_usd) or an error message.
- **Supported Chains**: Arbitrum,arbitrum,avalanche_c,base,berachain,bnb,ethereum and more.

### `get_wallet_transactions`

- **Description**: Fetches the transaction history of a specified wallet address on supported EVM and Solana blockchains.
- **Parameters**:
  - `wallet_address` (str): The wallet address to query (e.g., '0x123...' for EVM chains or 'DYw8jCT...' for Solana).
  - `limit` (int, optional): Maximum number of transactions to return (default: 100).
- **Returns**: Formatted text with transaction details (chain, block_time, tx_hash, from, to, value) or an error message.
- **Supported Chains**: Solana,arbitrum,arbitrum,avalanche_c,base,berachain,bnb,ethereum and more.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
