from ownip import get

class TestOwnIp:
    def test_api(self):
        ip_dict = get()
        assert type(ip_dict) is dict
