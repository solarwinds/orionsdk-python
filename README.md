# Orion SDK for Python

This project contains a python client for interacting with the SolarWinds Orion API

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
openssl s_client -connect server:17778
```

Then add an entry to your hosts file for ``SolarWinds-Orion`` and you
will be able to verify via doing the following:

```python
import orionsdk
swis = orionsdk.SwisClient("SolarWinds-Orion", "username", "password", verify="server.pem")
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
