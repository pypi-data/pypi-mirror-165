```
alias cosmd=./wasmd/build/wasmd
cosmd --home .atomkraft/nodes/node-0 init node-0 --chain-id cosmos-test
cosmd --home .atomkraft/nodes/node-1 init node-1 --chain-id cosmos-test

cosmd --home .atomkraft/nodes/node-0 add-genesis-account cosmos1grtwnw3gyr7vldnwypv95ugtvv9z7tc7x5xml6 1000000000000000000000000000stake --keyring-backend test --output json
cosmd --home .atomkraft/nodes/node-0 add-genesis-account cosmos1h3q4ewanmn3zdfrpxf2yps25xn7e9wz9as302c 1000000000000000000000000000stake --keyring-backend test --output json

cosmd --home .atomkraft/nodes/node-0 add-genesis-account cosmos1wxk5hdwvhsnk422kaqwuzfp2qljnsd23fpastt 1000000000000000000000000000stake --keyring-backend test --output json
cosmd --home .atomkraft/nodes/node-0 add-genesis-account cosmos1udk2e7c78mxulv0ps4curqsw5ul5wtp7axm62e 1000000000000000000000000000stake --keyring-backend test --output json
cosmd --home .atomkraft/nodes/node-0 add-genesis-account cosmos1cn2xuwurmdmkarsuskywh70pf4yvv335hzfyxy 1000000000000000000000000000stake --keyring-backend test --output json

cosmd --home .atomkraft/nodes/node-0 keys add validator-0 --recover --keyring-backend test --output json
essay horn nice first vibrant label garage audit frame scale kitchen nose
cosmd --home .atomkraft/nodes/node-0 gentx validator-0 1000000000000000000000stake --keyring-backend test --chain-id cosmos-test --output json

cosmd --home .atomkraft/nodes/node-1 keys add validator-1 --recover --keyring-backend test --output json
first train mistake pumpkin bounce universe offer fatal neither basic pole thank
cosmd --home .atomkraft/nodes/node-1 gentx validator-1 1000000000000000000000stake --keyring-backend test --chain-id cosmos-test --output json

cosmd --home .atomkraft/nodes/node-1 tx sign .atomkraft/nodes/node-1//config/gentx/gentx-ee394515a3acc9bca44a7e9d1246f8c7fdcb66bf.json --output-document .atomkraft/nodes/node-1//config/gentx/gentx-ee394515a3acc9bca44a7e9d1246f8c7fdcb66bf.json --chain-id cosmos-test --overwrite --offline --sequence 0 --account-number 0 --from validator-1 --keyring-backend test --output json

cosmd --home .atomkraft/nodes/node-0 collect-gentxs
cosmd --home .atomkraft/nodes/node-1 collect-gentxs
```