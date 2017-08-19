Sand artwork.

### Installation
It doesn't appear pip can install from git urls via setup.py, and `--process-dependency-links` is
deprecated, so you have to install some packages by hand.

```
git clone https://github.com/Caged/sandworks.git
cd sandworks
pip install cython==0.25.0
pip install -e git+https://github.com/Caged/fast-sand-paint.git@non-write-transfer#egg=fast-sand-paint-0.1.0

pip install -r requirements.txt
pip install .
```

### Usage

```
sandworks --help
sandworks splines --help
sandworks playground --help
sandworks playground --color '#111111'
sandworks playground --bg-color '#111111' --color '#ffb605'
sandworks splines --lines 100 --color '#cc0000' --width 1000 --height 1200 --dir vertical --margin 25
```

### Special Attribution

Much of the foundational work in this project was derived from or taken directly from [the work of Anders Hoff](https://github.com/inconvergent/sand-spline) who has graciously released his work under the MIT license in addition to [writing extensively](http://inconvergent.net/#writing) about generative art.  Without those projects and texts, I'd likely still be fumbling around with math I don't fully understand.
