Spine artwork.

### Installation
It doesn't appear pip can install from git urls via setup.py, and `--process-dependency-links` is
deprecated, so you have to install this package by hand.

```
git clone https://github.com/Caged/splineworks.git
cd splineworks
pip install cython==0.25.0
pip install -r requirements.txt
pip install .
```

If you get an error about missing cython, you might need to manually install it first.  

### Special Attribution

Much of the foundational work in this project was derived from or taken directly from [the work of Anders Hoff](https://github.com/inconvergent/sand-spline) who has graciously released his work under the MIT license in addition to [writing extensively](http://inconvergent.net/#writing) about generative art.  Without those projects and texts, I'd likely still be fumbling around with math I don't fully understand. 
