# CryptOMaMa
CryptOMaMa, an acronym for Crypto Optimized Market Maker, is designed to provide liquidity in the crypto markets by maintaining a competitive spread between buy and sell orders, thereby ensuring market stability.

## Dependencies

Dependencies are listed in omama.yml
You can create an adapted conda environment with the following command : 

```bash
conda create -n omama -f omama.yml
```

## Usage

```bash
$ python main.py --help
usage: CryptOMaMa [-h] [--input_file INPUT_FILE] [--api API] [--api_key API_KEY] [--private_key PRIVATE_KEY] [--symbol SYMBOL] [--model MODEL] {run,test}

positional arguments:
  {run,test}            Specify if you want "run" or "test" a strategy.

options:
  -h, --help            show this help message and exit
  --input_file INPUT_FILE
                        Specify input files
```

## Structure

We separate this project of market making into 3 parts :

    * The first one is use get the market data from the broker. For now, we use the library 'python-binance'. For safety we have to re-code this module to remove any possible backdoors. 
    * The second one is used to calibrate the used market making model (GLFT for exemple) from the previous datas.
    * The third one is used to send the position on the broker.
  
In a first step we will code these main features separately and then, connect them with an optimized asynchronous system.

## Input file structure

```json
{
    "use_api": {
        "api": "binance",
        "api_key": "Public_key",
        "private_key": "Private_key.pem",
        "symbol": "BNBBTC",
        "duration": 120,
        "output_file_name": "historical_datas.txt"
    },
    "model": "GueantLehalleFernandezTapia"
}
```
