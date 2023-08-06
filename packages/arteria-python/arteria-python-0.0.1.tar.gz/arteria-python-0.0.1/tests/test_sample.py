import arteria


def test_hosts_arteria():
    assert arteria.session.host == 'api.arteria.xyz'
    arteria.configure(sandbox=True)
    assert arteria.session.host == 'sandbox-api.arteria.xyz'
