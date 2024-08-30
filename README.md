# Python-Digikala-SSD-Ranker
A python script to get digikala SSD devices and rank them by size/price formula.
I used firefox > [digikala.com ssd](https://www.digikala.com/search/category-internal-ssd/) > Right Click anywhere > inspect > console > xhr > searching api.digikala.com 
to detect api url of digikala and than copy them in raw mode to this site:
https://jsongrid.com/json-grid

than find the values I need (name,price) and extracted the size from the name
and than calculated size/price to rank the storages and sort them from biggest to smallest.
to find most cheap and most expencive ssd storages of digikala

## Run with this command: 
```bash
$ python python.digikala.api
```
