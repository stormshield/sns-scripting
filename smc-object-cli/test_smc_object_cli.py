from typer.testing import CliRunner

import random
import string
import importlib
import re

module = importlib.import_module("smc-object-cli")
app = module.app

runner = CliRunner()

def gen_str(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def gen_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def test_add_and_delete_host():
    name = gen_str(12)
    comment = gen_str(24)
    ip = gen_ip()

    # create a host
    result = runner.invoke(app, ["host", "create", name, ip, "--comment", comment])
    assert result.exit_code == 0
    assert f"Host {name} created" in result.output

    # already exists
    result = runner.invoke(app, ["host", "create", name, ip, "--comment", comment])
    assert result.exit_code == 1
    assert f"EDUPLICATE" in result.output

    # check the host is created
    result = runner.invoke(app, ["host", "list"])
    assert result.exit_code == 0
    assert ip in result.output
    assert name in result.output
    assert comment in result.output

    # delete the host
    result = runner.invoke(app, ["host", "delete", name])
    assert result.exit_code == 0
    assert f"Host {name} deleted" in result.output

    # check the host is deleted
    result = runner.invoke(app, ["host", "list"] )
    assert result.exit_code == 0
    assert name not in result.output

def test_group():
    name = gen_str(12)
    comment = gen_str(24)
    ip = gen_ip()

    name2 = gen_str(12)
    ip2 = gen_ip()

    name3 = gen_str(12)
    ip3 = gen_ip()

    gname = gen_str(12)
    comment = gen_str(24)

    # create a host
    result = runner.invoke(app, ["host", "create", name, ip, "--comment", comment])
    assert result.exit_code == 0
    assert f"Host {name} created" in result.output

    # create a second host
    result = runner.invoke(app, ["host", "create", name2, ip2])
    assert result.exit_code == 0
    assert f"Host {name2} created" in result.output

    # create a third host
    result = runner.invoke(app, ["host", "create", name3, ip3])
    assert result.exit_code == 0
    assert f"Host {name3} created" in result.output

    # create a group
    result = runner.invoke(app, ["group", "create", gname, name, "--comment", comment])
    assert result.exit_code == 0
    assert f"Group {gname} created" in result.output

    # check group list
    result = runner.invoke(app, ["group", "list"])
    assert result.exit_code == 0
    assert gname in result.output
    
    # can't delete a host already in a group
    result = runner.invoke(app, ["host", "delete", name])
    assert result.exit_code != 0

    # add hosts to group
    result = runner.invoke(app, ["group", "update", "add", gname, name2, name3])
    assert result.exit_code == 0

    # check group content
    result = runner.invoke(app, ["group", "list", "--members"])
    assert result.exit_code == 0
    assert gname in result.output
    assert name in result.output
    assert name2 in result.output

    # remove hosts from a group
    result = runner.invoke(app, ["group", "update", "remove", gname, name2, name3])
    assert result.exit_code == 0

    # remove twice is ok
    result = runner.invoke(app, ["group", "update", "remove", gname, name2, name3])
    assert result.exit_code == 0
    assert re.findall(r"nothing\s+to\s+do", result.output, re.MULTILINE) is not None

    # check group content
    result = runner.invoke(app, ["group", "list", "--members"])
    assert result.exit_code == 0
    assert name in result.output
    assert name2 not in result.output
    assert name3 not in result.output

    # delete a group
    result = runner.invoke(app, ["group", "delete", gname])
    assert result.exit_code == 0
    assert f"Group {gname} deleted" in result.output

    # delete the host
    result = runner.invoke(app, ["host", "delete", name])
    assert result.exit_code == 0
    assert f"Host {name} deleted" in result.output

    # delete the second host
    result = runner.invoke(app, ["host", "delete", name2])
    assert result.exit_code == 0
    assert f"Host {name2} deleted" in result.output

    # delete the second host
    result = runner.invoke(app, ["host", "delete", name3])
    assert result.exit_code == 0
    assert f"Host {name3} deleted" in result.output

    # check group list
    result = runner.invoke(app, ["group", "list"])
    assert result.exit_code == 0
    assert gname not in result.output