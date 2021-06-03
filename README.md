# Binance CLI

This package provides a unified command-line interface to interact with Binance API ([https://binance-docs.github.io/apidocs](https://binance-docs.github.io/apidocs))

ℹ️ **This is an unofficial package, and this project is not related or affiliated with Binance.**

🚨 **Use the package at your own risk. We highly recommend using the testnet version at the beginning.**

Jump to:
- [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Generate API Key and Secret Key](#generate-api-key-and-secret-key)
    - [Add Credentials](#add-credentials)
- [Basic Commands](#basic-commands)
- [Command Output](#command-output)
    - [JSON Format](#json-default)
    - [YAML Format](#yaml)
- [Query with JMESPath](#jmespath---query)    

# Getting started

We have released a special version of the Binance CLI package for testing purposes. It is called `bnc_testnet` and it contains the same functionality as `bnc`.

Both versions can co-exist on the same computer because they are independent and use different folders for configuration. 

The complete documentation of the Binance CLI package will refer to `bnc`. When you want to use testnet version, you have to replace `bnc` with `bnc_testnet`.

We highly recommend using `bnc_testnet` at the beginning to gain experience using the Binance CLI package and then switch to `bnc`. 

Keep in mind that use a testnet version implies not using real money.  

## Requirements

The Binance CLI package works on Python versions:
- 3.8.x and greater

## Installation

Installation of the Binance CLI and its dependencies use various packaging features provided by `pip` and `setuptools`.
It's recommended to use:

- `pip`: 21.1
- `setuptools`: 56.0

The safest way to install the Binance CLI is to use `pip` in a `virtualenv`:

```shell
$ python -m pip install bnc
```

*Testnet*

```shell
$ python -m pip install bnc_testnet
```

or, if you are not installing in a `virtualenv`, to install globally:

```shell
$ sudo python -m pip install bnc 
```

*Testnet*

```shell
$ sudo python -m pip install bnc_testnet
```

or for your user:

```shell
$ python -m pip install --user bnc 
```

*Testnet*

```shell
$ python -m pip install --user bnc_testnet
```

If you have the Binance CLI package installed and want to upgrade to the latest version, you can run:

```shell
$ python -m pip install --upgrade bnc 
```

*Testnet*

```shell
$ python -m pip install --upgrade bnc_testnet
```

**NOTE**

At this moment, we only use `pip` to install the Binance CLI package.
We are planning to add more options for the distribution and installation of the Binance CLI package.

## Generate API Key and Secret Key

You should have an active Binance account to create a valid API key and secret key.

You can follow this step-by-step guide provided by Binance:

[Create an API Key](https://www.binance.com/en/support/faq/360002502072)

For testnet you can follow:

[Generate API key for Testnet](https://dev.binance.vision/t/binance-testnet-environments/99/2)

## Add credentials

Before using BNC CLI, you need to tell it about your credentials. You can do this in several ways:

- Configuration file **(recommended)**
- Environment variables

The quickest way to get started is to run the `bnc credentials add` command:

```bash
$ bnc credentials add --api_key="YOUR_API_KEY" --secret="YOUR_SECRET_KEY"

Binance CLI's credentials added successfully.
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

The testnet version uses different environment variables:

```bash
$ export BNC_TESTNET_CLI_API_KEY=<YOUR_API_KEY>
$ export BNC_TESTNET_CLI_SECRET_KEY=<YOUR_SECRET_KEY>
```

# Basic Commands

A BNC CLI command has the following structure:

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

**YAML** format is also available to format output. You can select either style with the `--output` option at the root command `bnc.`

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

# JMESPath (--query)

Some commands have an `--query` option that allows extracting and transforming elements from a JSON. It is very useful on occasions where you need to filter a very long response from Binance API. For more information on the expression language used for this option, you can read the [JMESPath Tutorial](https://jmespath.org/tutorial.html)