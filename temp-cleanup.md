#Instructions for cleaning up filesystem

Removing .pyc files:
from /qhord
```
find . -name "*.pyc" -exec git rm -f "{}" \;
```
Removing v0.1:
```
git rm -rf v0.1
```

Making v0.2 default:
```
git mv v0.2/* .
git rm -r v0.2/
```
