# Utils for MLExchange Platform

**mlex_utils** is a utility package designed to support the MLExchange platform by providing convenient tools and extensions for Dash Plotly and Prefect. Currently, this package focuses on facilitating job launches and monitoring workflows with Prefect, making it easier to manage and track your machine learning tasks. As the platform evolves, mlex_utils will continue to expand, incorporating additional utilities to enhance the MLExchange experience and streamline data workflows.

## Features
- Utilities for integrating Dash Plotly components to orchestrate ML jobs using Dash Bootstrap Components and Dash Mantime Components
- Prefect job management tools for launching, scheduling, and monitoring ML jobs.

## Installation

To install `mlex_utils`, you can create a new Python environment and install all the dependencies:

```
conda create -n new_env python==3.11
conda activate new_env
pip install .
```

Alternatively, you can choose to install a set of utils according to your use case. For example, to install the Prefect-related dependencies and utils:

```
pip install ".[prefect]"
```

## Copyright
MLExchange Copyright (c) 2024, The Regents of the University of California,
through Lawrence Berkeley National Laboratory (subject to receipt of
any required approvals from the U.S. Dept. of Energy). All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

(1) Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

(2) Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

(3) Neither the name of the University of California, Lawrence Berkeley
National Laboratory, U.S. Dept. of Energy nor the names of its contributors
may be used to endorse or promote products derived from this software
without specific prior written permission.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
