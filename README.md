
# Triangle Arbitrage Detection

## Problem Statement
Design an online triangle arbitrage detection algorithm.

---
## Data \& Terminology

**Trading Pair**
- A trading pair is a pair of assets that can be traded for each other on an exchange. 
Data for a trading pair includes `<pair_sybmol>', <base_asset>, <quote_asset>`. 
Example, in the trading pair `BTCUSDT, BTC, USDT`.

**Bid price** ( $P_{AB}^{bid}$ )
- The price at which the market is wiling to buy the base asset in exchange for the quote asset.
**Ask price** ( $P_{AB}^{ask}$ )
- The price at which the market is wiling to sell the base asset in exchange for the quote asset.
Ex. `Symbol: usdttry, Bid: 33.12, Ask: 33.13`
- One can sell 1 USDT for 33.12 TRY
- One can buy 1 USDT for 33.13 TRY
--- 
## Data Representation
We represent each asset as a node in a graph ($u,v$). 
Each trading pair exchange rate is represented as two directed edges:
1. $u \rightarrow v$ with weight $P_{AB}^{bid}$
2. $v \rightarrow u$ with weight $1/P_{AB}^{ask}$

The interpretation of the edges is as follows:
If we have an edge $u \rightarrow v$ with weight $w$, starting with 1 unit of $u$, we can get $w$ units of $v$.

--- 
## Arbitrage Detection
A triangle arbitrage instance is a cycle of length 3, $u \rightarrow v \rightarrow w \rightarrow u$, such that the product of the weights of the edges in the cycle is greater than 1.
In other words, if we start with 1 unit of $u$, we can end up with more than 1 unit of $u$ after going through the cycle.


## Algorithm
- The algorithm runs in an online fashion, processing trading pairs data as it arrives.
- We maintain a graph of exchange rates, and for each new trading pair, we update the graph and check for arbitrage instances.
- When a new price update for pair $uv$ arrives, we update the $u \rightarrow v$ and $v \rightarrow u$ edges in the graph.
- After updating $u \rightarrow v$ weight, we check for all neighbors of $v$, $w$ where $w \rightarrow u$ exists, and check if the product of the weights of the edges $u \rightarrow v$, $v \rightarrow w$, $w \rightarrow u$ is greater than 1. If so, we have an arbitrage instance.
- We carry out the same process after updating $v \rightarrow u$ weight.
- In actual implementation, we take the logarithm of weights and check if the sum of the weights is greater than 0.
- Detected arbitrage instances are kept in a dictionary of $(u,v,w) : < \text{arbitrage-factor}>$. Where arbitrage factor is the product of the weights of the edges in the cycle. Using $x$ amount of the bases asset, we can make $x * \text{arbitrage-factor}$ amount of the base asset after going through the cycle.
- Complexity" $O(V)$ per update, where $V$ is the max degree of the graph.

---

## Possible Improvements
- [ ] Detecting arbitrage instances with arbitrary cycle length. 
    - This problem is can be reduced to the negative cycle detection problem in a directed graph. 
    - Floyd-Warshall can solve this offline, is there a more efficient online algorithm?
- [ ] How to choose a good subset of trading pairs to monitor? 
