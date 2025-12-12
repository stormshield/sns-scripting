# smc-object-cli

Simple CLI example to manipulate SMC objects.

## Install

Requires python 3.10

Optionaly, setup a virtual environment:

```bash
sudo apt install python3-venv python3-pip

python3 -m venv smc-object-cli
source smc-object-cli/bin/activate
```

Install the script requirements.

```bash
# via pip
pip3 install -r requirements.txt
```

## Configuration

In SMC, generate an API key ([documentation](https://documentation.stormshield.eu/SMC/v3/fr/Content/SMC_Administration_Guide/enabling_API.htm)).

Create a .env file in the working folder with the following content:

```
SMC_URL=https://<smc host name or ip>
API_KEY=<secret>
```

If the SMC has a certificate signed by a custom authority, add:

```
CACERT=/path/to/ca.pem
```

or SSL peer verification can be bypassed with:

```
UNSECURE=1
```

Alternatively, you can set the environment variables in your shell or use the command line options.

## Usage

```bash
# list hosts
./smc-object-cli.py host list

# list groups
./smc-object-cli.py group list --members

# create a host
./smc-object-cli.py host create myserver 1.2.3.4 --comment "My server"

# create a group with two elements
./smc-object-cli.py group create mygroup myserver myhost --comment "my first group"

# add a host to a group
./smc-object-cli.py group update add mygroup ntp1.stormshieldcs.eu

# remove a host from a group
./smc-object-cli.py group update remove mygroup ntp1.stormshieldcs.eu

# delete a host
./smc-object-cli.py host delete myhost

# delete a group
./smc-object-cli.py group delete g1

```

# Tests

Configure a test SMC server in environment or `.env` and launch `pytest`.
