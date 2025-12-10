# k6pylib

> This repository is part of [xk6-python](https://github.com/grafana/hackathon-2024-08-snake-charmers) development by the [Grafana Hackathon 10/Snake-Charmers team](https://devpost.team/grafana-bl/projects/6358).


Example remote module library for xk6-python extension.

The content of the repository is deployed with GitHub Pages and is available at https://grafana.github.io/k6pylib/. For example, the [welcome.py](welcome.py) module can be used as follows:

```python
load("https://grafana.github.io/k6pylib/welcome.py", "hello")

def default():
    hello("Joe")
```
