# InvestoPy

Help investors invest in certain indexes.

## Portfolios

### IBIndex
Ett index som viktar investmentbolag enligt deras substansvärde som följande:
```
viktningsvärde_bolagX = 1 + [SUBSTANSVÄRDE]
```
Här är ```0 <= SUBSTANSVÄRDE <= 1``` och är antingen positivt (substansrabatt) eller negativt (substanspremium).
Sedan divideras detta viktningsvärde med summan av alla viktningsvärden för alla investmentbolag.
```
viktningsvärde_bolagX = viktningsvärde_bolagX/SUM(viktningsvärde_bolag_i)
```