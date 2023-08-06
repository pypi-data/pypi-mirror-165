# astral-projection

Like it's real-world counterpart (if you can call it that), this package allows
your code to have out-of-body experiences. Its effectiveness is also disputed
by experts.


## Usage:

```python
import sys
import os
from astral_projection import host

x = 23

with host("l3vi.de"):
    os.system("hostname")
    print("hello!", x)
    for i in range(10):
        print("hi", i, file=sys.stderr)
    x += 1

print("x is now", x)
```
