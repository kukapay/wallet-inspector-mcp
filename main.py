import os
import httpx
import asyncio
import re
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from tabulate import tabulate
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("WalletInspector")

# Dune SIM API configuration
DUNE_SIM_API_KEY = os.getenv("DUNE_SIM_API_KEY")
DUNE_SIM_API_URL = "https://api.sim.dune.com"

if not DUNE_SIM_API_KEY:
    raise ValueError("DUNE_SIM_API_KEY environment variable is required")

# Helper function to query Dune SIM Balance API for EVM chains
async def query_evm_balance(wallet_address: str) -> Dict[str, Any]:
    """Query Dune SIM Balance API for wallet balance on EVM chains."""
    headers = {"X-Sim-Api-Key": DUNE_SIM_API_KEY}
    url = f"{DUNE_SIM_API_URL}/v1/evm/balances/{wallet_address}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}

# Helper function to query Dune SIM Balance API for SVM (Solana) chain
async def query_svm_balance(wallet_address: str) -> Dict[str, Any]:
    """Query Dune SIM Balance API for wallet balance on Solana chain."""
    headers = {"X-Sim-Api-Key": DUNE_SIM_API_KEY}
    url = f"{DUNE_SIM_API_URL}/beta/svm/balances/{wallet_address}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}

# Helper function to query Dune SIM Activity API for EVM chains
async def query_evm_activity(wallet_address: str) -> Dict[str, Any]:
    """Query Dune SIM Activity API for wallet activity on EVM chains."""
    headers = {"X-Sim-Api-Key": DUNE_SIM_API_KEY}
    url = f"{DUNE_SIM_API_URL}/v1/evm/activity/{wallet_address}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}

# Helper function to query Dune SIM Transactions API for EVM chains
async def query_evm_transactions(wallet_address: str, limit: int = 100) -> Dict[str, Any]:
    """Query Dune SIM Transactions API for wallet transactions on EVM chains."""
    headers = {"X-Sim-Api-Key": DUNE_SIM_API_KEY}
    url = f"{DUNE_SIM_API_URL}/v1/evm/transactions/{wallet_address}?limit={limit}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}

# Helper function to query Dune SIM Transactions API for SVM (Solana) chain
async def query_svm_transactions(wallet_address: str, limit: int = 100) -> Dict[str, Any]:
    """Query Dune SIM Transactions API for wallet transactions on Solana chain."""
    headers = {"X-Sim-Api-Key": DUNE_SIM_API_KEY}
    url = f"{DUNE_SIM_API_URL}/beta/svm/transactions/{wallet_address}?limit={limit}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}

def is_evm_address(address: str) -> bool:
    """Check if the address is an EVM-compatible address."""
    return bool(re.match(r"^0x[a-fA-F0-9]{40}$", address))

def is_solana_address(address: str) -> bool:
    """Check if the address is a Solana-compatible address (Base58, 32-44 characters)."""
    return bool(re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", address))

@mcp.tool()
async def get_wallet_balance(wallet_address: str) -> str:
    """
    Query the balance of a specified wallet address across supported EVM and Solana blockchains.
    
    Parameters:
        wallet_address (str): The wallet address to query (e.g., '0x123...' for EVM chains like Ethereum, 
                             Polygon, BSC, or 'DYw8jCT...' for Solana). Must be a valid address for the target chain.
    
    Returns:
        str: Formatted table with balance information (chain, token amount, USD value) for supported chains or an error message.
    """
    if not wallet_address:
        return "Error: Wallet address is required."
    
    balance_data = []
    supported_evm_chains = ["ethereum", "polygon", "bsc"]
    
    if is_evm_address(wallet_address):
        result = await query_evm_balance(wallet_address)
        if "error" in result:
            return f"Error querying EVM balance: {result['error']}"
        
        balances = result.get("balances", [])
        if not balances:
            return f"No balance data found for wallet {wallet_address}."
        
        for balance in balances:
            chain = balance.get("chain", "").lower()
            if chain not in supported_evm_chains:
                continue
            amount = int(balance.get("amount", "0"))
            decimals = balance.get("decimals", 18)
            symbol = balance.get("symbol", "Unknown")
            value_usd = float(balance.get("value_usd", 0))
            # Convert amount to human-readable token quantity
            token_amount = amount / (10 ** decimals)
            balance_data.append([chain, f"{token_amount:.6f} {symbol}", f"${value_usd:.2f}"])
    
    elif is_solana_address(wallet_address):
        result = await query_svm_balance(wallet_address)
        if "error" in result:
            return f"Error querying Solana balance: {result['error']}"
        
        balances = result.get("balances", [])
        if not balances:
            return f"No balance data found for wallet {wallet_address}."
        
        for balance in balances:
            chain = balance.get("chain", "").lower()
            if chain != "solana":
                continue
            token_amount = float(balance.get("balance", "0"))
            symbol = balance.get("symbol", "Unknown")
            value_usd = float(balance.get("value_usd", 0))
            balance_data.append([chain, f"{token_amount:.6f} {symbol}", f"${value_usd:.2f}"])
    
    else:
        return "Error: Invalid wallet address format. Use EVM (0x...) or Solana (Base58) address."
    
    if not balance_data:
        return f"No supported chain balances found for wallet {wallet_address}."
    
    # Generate ASCII table
    headers = ["Chain", "Token Amount", "USD Value"]
    table = tabulate(balance_data, headers=headers, tablefmt="grid")
    return f"Wallet {wallet_address} balances:\n\n{table}"

@mcp.tool()
async def get_wallet_activity(wallet_address: str) -> str:
    """
    Query the activity of a specified wallet address on supported EVM blockchains.
    
    Parameters:
        wallet_address (str): The wallet address to query (e.g., '0x123...'). 
                             Must be a valid EVM-compatible address for chains like Ethereum, Polygon, or BSC.
    
    Returns:
        str: Formatted text with activity information (chain_id, block_time, tx_hash, type, asset_type, value, value_usd) 
             or an error message.
    """
    if not wallet_address:
        return "Error: Wallet address is required."
    
    if not is_evm_address(wallet_address):
        return "Error: Invalid EVM wallet address. Use a valid EVM address (0x...)."
    
    result = await query_evm_activity(wallet_address)
    if "error" in result:
        return f"Error querying EVM activity: {result['error']}"
    
    activities = result.get("activity", [])
    if not activities:
        return f"No activity data found for wallet {wallet_address}."
    
    activity_lines = []
    for activity in activities:
        chain_id = activity.get("chain_id", "")
        block_time = activity.get("block_time", "")
        tx_hash = activity.get("tx_hash", "")
        activity_type = activity.get("type", "").capitalize()
        asset_type = activity.get("asset_type", "").upper()
        value = int(activity.get("value", "0"))
        token_metadata = activity.get("token_metadata", {})
        decimals = token_metadata.get("decimals", 18)
        symbol = token_metadata.get("symbol", "Unknown")
        value_usd = float(activity.get("value_usd", 0))
        # Convert value to human-readable token quantity
        token_amount = value / (10 ** decimals)
        # Format activity line
        activity_line = (
            f"Chain ID: {chain_id}\n"
            f"Block Time: {block_time}\n"
            f"Tx Hash: {tx_hash}\n"
            f"Type: {activity_type}\n"
            f"Asset Type: {asset_type}\n"
            f"Value: {token_amount:.6f} {symbol}\n"
            f"USD Value: ${value_usd:.2f}\n"
        )
        activity_lines.append(activity_line)
    
    return f"Wallet {wallet_address} activity:\n\n" + "\n".join(activity_lines)

@mcp.tool()
async def get_wallet_transactions(wallet_address: str, limit: int = 100) -> str:
    """
    Query the transactions of a specified wallet address on supported EVM and Solana blockchains.
    
    Parameters:
        wallet_address (str): The wallet address to query (e.g., '0x123...' for EVM chains like Ethereum, 
                             Polygon, BSC, or 'DYw8jCT...' for Solana). Must be a valid address for the target chain.
        limit (int): Maximum number of transactions to return (default: 100).
    
    Returns:
        str: Formatted text with transaction information (chain, block_time, tx_hash, from, to, value, value_usd) 
             or an error message.
    """
    if not wallet_address:
        return "Error: Wallet address is required."
    
    if limit < 1:
        return "Error: Limit must be a positive integer."
    
    transaction_lines = []
    
    if is_evm_address(wallet_address):
        result = await query_evm_transactions(wallet_address, limit)
        if "error" in result:
            return f"Error querying EVM transactions: {result['error']}"
        
        transactions = result.get("transactions", [])
        if not transactions:
            return f"No transaction data found for wallet {wallet_address}."
        
        for tx in transactions:
            chain = tx.get("chain", "Unknown")
            block_time = tx.get("block_time", "")
            tx_hash = tx.get("hash", "")
            from_addr = tx.get("from", "")
            to_addr = tx.get("to", "")
            value = int(tx.get("value", "0"), 16)  # Convert hex to int
            # Assume native token (e.g., ETH) with 18 decimals
            decimals = 18
            symbol = "ETH" if chain.lower() == "ethereum" else "Unknown"
            token_amount = value / (10 ** decimals)
            value_usd = "N/A"  # No USD value in response
            # Format transaction line
            transaction_line = (
                f"Chain: {chain}\n"
                f"Block Time: {block_time}\n"
                f"Tx Hash: {tx_hash}\n"
                f"From: {from_addr}\n"
                f"To: {to_addr}\n"
                f"Value: {token_amount:.6f} {symbol}\n"
            )
            transaction_lines.append(transaction_line)
    
    elif is_solana_address(wallet_address):
        result = await query_svm_transactions(wallet_address, limit)
        if "error" in result:
            return f"Error querying Solana transactions: {result['error']}"
        
        transactions = result.get("transactions", [])
        if not transactions:
            return f"No transaction data found for wallet {wallet_address}."
        
        for tx in transactions:
            chain = tx.get("chain", "solana")
            block_time = tx.get("block_time", 0)
            # Convert block_time (UNIX timestamp in nanoseconds) to readable format
            if block_time:
                block_time = datetime.fromtimestamp(block_time / 1_000_000_000).strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                block_time = ""
            raw_tx = tx.get("raw_transaction", {})
            tx_hash = raw_tx.get("transaction", {}).get("signatures", [""])[0]
            account_keys = raw_tx.get("transaction", {}).get("message", {}).get("accountKeys", [])
            from_addr = account_keys[0] if len(account_keys) > 0 else ""
            to_addr = account_keys[1] if len(account_keys) > 1 else ""
            # Calculate value from balance changes
            pre_balances = raw_tx.get("meta", {}).get("preBalances", [])
            post_balances = raw_tx.get("meta", {}).get("postBalances", [])
            value = 0
            if len(pre_balances) > 1 and len(post_balances) > 1:
                value = abs(post_balances[1] - pre_balances[1])  # Value transferred to 'to' address
            decimals = 9  # Solana uses 9 decimals for SOL
            symbol = "SOL"
            token_amount = value / (10 ** decimals)
            value_usd = "N/A"  # No USD value in response
            # Format transaction line
            transaction_line = (
                f"Chain: {chain}\n"
                f"Block Time: {block_time}\n"
                f"Tx Hash: {tx_hash}\n"
                f"From: {from_addr}\n"
                f"To: {to_addr}\n"
                f"Value: {token_amount:.6f} {symbol}\n"
            )
            transaction_lines.append(transaction_line)
    
    else:
        return "Error: Invalid wallet address format. Use EVM (0x...) or Solana (Base58) address."
    
    return f"Wallet {wallet_address} transactions:\n\n" + "\n".join(transaction_lines) if transaction_lines else f"No transactions found for wallet {wallet_address}."

# Run the server
if __name__ == "__main__":
    mcp.run()
    