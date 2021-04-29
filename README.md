# Binance CLI

[![Run tests](https://github.com/mpetrinidev/bnc-cli/actions/workflows/python-app.yml/badge.svg)](https://github.com/mpetrinidev/bnc-cli/actions/workflows/python-app.yml) [![codecov](https://codecov.io/gh/mpetrinidev/bnc-cli/branch/main/graph/badge.svg?token=ION6F3XIA1)](https://codecov.io/gh/mpetrinidev/bnc-cli)

This package provides a unified command-line interface to interact with Binance API ([https://binance-docs.github.io/apidocs](https://binance-docs.github.io/apidocs))

> ℹ️ *This is an unofficial package, and this project is not related or affiliated with Binance. Use at your own risk.*

# Getting started

## Generate API Key and Secret Key

You should have an active binance account in order to create a valid API key and secret key.

You can follow this step by step guide provided by Binance:

[https://www.binance.com/en/support/faq/360002502072](https://www.binance.com/en/support/faq/360002502072)

## Add credentials

Before using BNC CLI, you need to tell it about your credentials. You can do this in several ways:

- Configuration file **(recommended)**
- Environment variables

The quickest way to get started is to run the `bnc credentials add` command:

```bash
$ bnc credentials add --api_key="YOUR_API_KEY" --secret="YOUR_SECRET_KEY"

Binance CLI's credentials added successfully
```

When you add your credentials using the previous command, it will create an INI formatted file called `credentials` under `~/.bnc` directory with the following structure:

```
[api_credentials]
bnc_cli_api_key = <YOUR_API_KEY>
bnc_cli_secret_key = <YOUR_SECRET_KEY>
```

To use environment variables, do the following:

```bash
$ export BNC_CLI_API_KEY=<YOUR_API_KEY>
$ export BNC_CLI_SECRET_KEY=<YOUR_SECRET_KEY>
```

# Basic Commands

An BNC CLI command has the following structure:

```bash
$ bnc <command> [options and parameters]
$ bnc <command> <group_commands> <command> [options and parameters]
```

To view help documentation, use one of the following:

```bash
$ bnc --help
$ bnc <command> --help
$ bnc <command> <group_commands> --help
$ bnc <command> <group_commands> <command> --help
```

To get the version of the BNC CLI:

```bash
$ bnc --version
```

To turn on verbose output:

```bash
$ bnc --verbose <command>
$ bnc --verbose <group_commands> <command>
```

# Command Output

The default output for commands is currently JSON. 

**YAML** format is also available to format output. You can select either styles with the `--output` option at the root command `bnc`

## Example

### JSON (Default)

```bash
$ bnc spot account_info
```

```json
{
  "makerCommission": 0,
  "takerCommission": 0,
  "buyerCommission": 0,
  "sellerCommission": 0,
  "canTrade": true,
  "canWithdraw": false,
  "canDeposit": false,
  "updateTime": 1616376905442,
  "accountType": "SPOT",
  "balances": [
    {
      "asset": "BNB",
      "free": "1000.00000000",
      "locked": "0.00000000"
    },
    {
      "asset": "BTC",
      "free": "0.98181601",
      "locked": "0.00000000"
    }
  ],
  "permissions": [
    "SPOT"
  ]
}
```

### YAML

```bash
$ bnc --output=yaml spot account_info
```

```yaml
makerCommission: 0
takerCommission: 0
buyerCommission: 0
sellerCommission: 0
canTrade: true
canWithdraw: false
canDeposit: false
updateTime: 1616376905442
accountType: SPOT
balances:
- asset: BNB
  free: '1000.00000000'
  locked: '0.00000000'
- asset: BTC
  free: '0.98181601'
  locked: '0.00000000'
permissions:
- SPOT
```

For more information:

[Binance CLI](https://github.com/mpetrinidev/bnc-cli/wiki)
