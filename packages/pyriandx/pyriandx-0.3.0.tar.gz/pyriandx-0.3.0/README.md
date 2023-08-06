# pyriandx

![Pull Request Build Status](https://github.com/umccr/pyriandx/workflows/Pull%20Request%20Build/badge.svg)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyriandx?style=flat)](https://pypistats.org/packages/pyriandx) 
[![PyPI](https://img.shields.io/pypi/v/pyriandx?style=flat)](https://pypi.org/project/pyriandx)
[![PyPI - License](https://img.shields.io/pypi/l/pyriandx?style=flat)](https://opensource.org/licenses/MIT)


`pyriandx` is CLI client and Python SDK/Library for PierianDx Clinical Genomics Workspace (CGW) web services -- https://umccr.github.io/pyriandx/

* [Test Coverage](https://umccr.github.io/pyriandx/coverage/)
* [PyDoc](https://umccr.github.io/pyriandx/pyriandx/)
* https://github.com/umccr/pyriandx


## TL;DR

- Install through `pip` like so
    ```
    pip install pyriandx
    ```

- Export `PDX_` environment variables
    ```
    export PDX_USERNAME=<YOUR_PierianDx_CGW_LOGIN_EMAIL>
    export PDX_PASSWORD=<YOUR_PierianDx_CGW_LOGIN_PASSWORD>
    export PDX_INSTITUTION=<ASK_YOUR_PierianDx_CGW_ACCOUNT_MANAGER>
    export PDX_BASE_URL=https://app.pieriandx.com/cgw-api/v2.0.0
    ```

- Print CLI command help
    ```
    pyriandx version
    pyriandx help
    pyriandx case help
    pyriandx list help
    pyriandx create help
    pyriandx upload help
    pyriandx run help
    pyriandx job help
    pyriandx poll help
    pyriandx report help
    ```

- More examples/tutorials available at [User Guide](https://umccr.github.io/pyriandx/user.html)


## License

MIT License and DISCLAIMER

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
