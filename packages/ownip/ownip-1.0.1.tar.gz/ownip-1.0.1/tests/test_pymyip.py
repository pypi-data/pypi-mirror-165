from ownip.ownip import OwnIp

class TestPyMyIp:
    def test_api(self):
        ip_dict = OwnIp.get_ip()
        assert type(ip_dict) is dict
