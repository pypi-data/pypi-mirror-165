# msqd

The `msqd` library (pronounced "em squared") is a small boilerplate library for designing, testing and spinning up trading algorithms using Python.

### Notes
- Upon class instantiation, ping database to get timestamps for which we have data, whether this is the downsampled timestamps or the timestamps we got from the database, and maybe some record of the furthest lookback would have to consider to get well-defined features.
- What data do we need to get from the database? How/where shall we cache it? For how long? Either we need to get some data and compute the feature value OR we already know (or can work out) that we won't yield any more information by pinging the database again and should just return the most recent value available.

### Design Goals
- We build up trading systems and strategies by composing functions. For example, we may have a filtering layer where we only trade a particular strategy when certain conditions are met; we may filter instruments. 
- A strategy is a function: it has some fixed parameters and it has some time-dependent inputs.
- What is the most convenient way to define strategies?
- We require full-stack control: we can spin up strategies using simple moving averages really quickly but can also do deep market-making strategies with full control over individual orders, sizes, etc.
- Pass to Rust for calculations that are really really slow. Most of the time, numpy calculations will be working fine.
- Let certain features augment multiple values, e.g. `RETURNS[-5:]` would give the most recent 5 returns (according to some frequency), even though it is just one input in the code.  