# Mint Sankey

Mint Sankey is a tool to create Sankey Diagram from your [Intuit Mint](https://mint.intuit.com) data. It will generate image, interactive webpage(html) or Sankeymatic data, which can be used at [SankeyMatic](http://sankeymatic.com).

Read more about the project: [Create Personal Financial Sankey Diagram from Intuit Mint Data - Frank's Weblog](https://nyan.im/p/sankey-diagram-mint)

Example output:
![](https://blog-nyan-im-static.azureedge.net/img/2023/01/sankeymatic_20230106_224858_2000x1200.png!s)

### Get started

![](https://blog-nyan-im-static.azureedge.net/img/2023/01/howto.png)

1. Log in to [Intuit Mint](https://mint.intuit.com).
2. Select "Transactions".
3. Select the accounts.
4. Apply filters to filter transactions based on time or categories.
5. Click the gear icon, then click "Export x transactions", a csv file will be exported.
6. Go to [Mint Sankey](http://mintsankey.nyan.im), upload the csv file.

### Run or deploy from source

Copy `config-sample.toml` to `config.toml` and edit.

Then
```
docker build -t mintsankey .
docker run -p 80:80 mintsankey
```

## License

MIT License

## Acknowledgements

* [nowthis](https://github.com/nowthis) for creating [SankeyMatic tool](https://github.com/nowthis/sankeymatic)
* [bradysalz/mint-sankey: generate Sankey diagrams from Mint budgets](https://github.com/bradysalz/mint-sankey)
