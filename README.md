# Orion SDK for Python

This project contains a python client for interacting with the SolarWinds Orion API

## API Documentation

For documentation about the SolarWinds Orion API, please see the [wiki](https://github.com/solarwinds/OrionSDK/wiki), [tools](https://github.com/solarwinds/OrionSDK/releases), and sample code (in languages other than Python) in the main [OrionSDK project](https://github.com/solarwinds/OrionSDK).

## Install

```
pip install orionsdk
```

## Usage

```python
import orionsdk

swis = orionsdk.SwisClient("server", "username", "password")

aliases = swis.invoke('Metadata.Entity', 'GetAliases', 'SELECT B.Caption FROM Orion.Nodes B')

print(aliases)
```

## SSL Certificate Verification

Initial support for SSL certificate valuation was added in 0.0.4. To
enable this, you will need to save the self-signed cert to a file. One
way of doing this is with OpenSSL:

```bash
openssl s_client -connect server:17774
```

> **Note:** The default `SolarWinds-Orion` certificate used to secure the SWIS REST endpoint (port 17774) does not contain a Subject Alternative Name (SAN) extension. Newer versions of Python/OpenSSL require a valid SAN for certificate verification to succeed. To use certificate verification, replace the endpoint certificate with a custom certificate that includes a valid SAN, then provide that certificate (or its CA) via the `verify` parameter.

```python
import orionsdk
swis = orionsdk.SwisClient("server", "username", "password", verify="server.pem")  # "server" must match the hostname in the custom certificate's SAN
swis.query("SELECT NodeID from Orion.Nodes")
```

## Setting Timeout

By default, requests timeout after 30 seconds. You can customize this by passing the `timeout` parameter (in seconds) to `SwisClient`:

```python
import orionsdk

swis = orionsdk.SwisClient("server", "username", "password", timeout=30, verify="server.pem")
swis.query("SELECT NodeID from Orion.Nodes")
```

## Setting Retry 

```python
import orionsdk
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def retry_session(retries=3,
                  backoff_factor=0.3,
                  status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


swis = orionsdk.SwisClient(
    "server",
    "username",
    "password",
    verify="server.pem",
    session=retry_session())
swis.query("SELECT NodeID from Orion.Nodes")
```

## License

	This software is licensed under the Apache License, version 2 ("ALv2"), quoted below.

	Copyright © 2015 SolarWinds Worldwide, LLC.  All rights reserved.

	Licensed under the Apache License, Version 2.0 (the "License"); you may not
	use this file except in compliance with the License. You may obtain a copy of
	the License at

	    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
	WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
	License for the specific language governing permissions and limitations under
	the License.

## Related Projects

### Solarwinds Interface Traffic Forecaster

[SolarwindsInterfaceTrafficPrediction](https://github.com/andrewbury/SolarwindsInterfaceTrafficPrediction) is an example of using the Orion SDK for Python and machine learning techniques to predict network interface traffic.
