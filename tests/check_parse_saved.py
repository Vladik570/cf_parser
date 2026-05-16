from parsers.coinmarketcap import collect_token_info

info = collect_token_info("saved_pages/coin1.html")
print(info["name"])
print(info["ticker"])
print(info["socials"])
print(info["website"])