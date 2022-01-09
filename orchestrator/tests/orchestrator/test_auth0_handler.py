import unittest

from orchestrator import settings
from orchestrator.auth0_handler import management_api
from orchestrator.models import AppType


class ManagementAPITests(unittest.TestCase):
    def tearDown(self) -> None:
        if hasattr(self, "created_client_id"):
            management_api.delete_client(self.created_client_id)

    def test_should_create_client_app_type_regular_web(self):
        # Arrange
        name = "Tests - Temporary App A"
        app_type = AppType.REGULAR_WEB
        # Act
        client_details = management_api.create_client(name, app_type)
        # Assert
        self.created_client_id = client_details["client_id"]
        assert client_details["name"] == name
        assert client_details["app_type"] == app_type.name.lower()
        # I'm leaving this here just as example
        # assert client_details == {
        #     "tenant": "jsm-sandbox-dev1",
        #     "global": False,
        #     "is_token_endpoint_ip_header_trusted": False,
        #     "name": "Tests - Temporary App A",
        #     "cross_origin_auth": False,
        #     "is_first_party": True,
        #     "sso_disabled": False,
        #     "oidc_conformant": False,
        #     "refresh_token": {
        #         "expiration_type": "non-expiring",
        #         "leeway": 0,
        #         "infinite_token_lifetime": True,
        #         "infinite_idle_token_lifetime": True,
        #         "token_lifetime": 2592000,
        #         "idle_token_lifetime": 1296000,
        #         "rotation_type": "non-rotating",
        #     },
        #     "encrypted": True,
        #     "signing_keys": [
        #         {
        #             "cert": "-----BEGIN CERTIFICATE-----\r\nMIIDFTCCAf2gAwIBAgIJYYMdy7j3myj2MA0GCSqGSIb3DQEBCwUAMCgxJjAkBgNV\r\nBAMTHWpzbS1zYW5kYm94LWRldjEudXMuYXV0aDAuY29tMB4XDTIyMDEwNTIxNTAz\r\nNFoXDTM1MDkxNDIxNTAzNFowKDEmMCQGA1UEAxMdanNtLXNhbmRib3gtZGV2MS51\r\ncy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC6rM87\r\n1u1GRjWdk/UdrD3d9eLVAVDXvwjtslr2qmJ1gRerNcKLwtLoD6fkgD72DmghapS6\r\nwn2TzBqEBBIia6kuS86jZRrsrpPAQBB2MhJbSruU9UCjMdRhXgZYfxaZLj15MYzg\r\nuCU4ay+dTFd68vZlfei4j+yA5egBrAkKh7Pd0tkNLp55TPQzuVOOuf4kj1bdkaFn\r\nFDyuaFM4w5TzHPTmx3FF98OlGPPfTPvafGsWBob1LpWBhMRS29yw1ENCcMgyb58m\r\nmIj1s943+UV1+rCSTSRtaVislj7+7ihRC903ZTk1SwtHotKEXIJVDyzZYB/Q3PkQ\r\nKDgxift2h+Ii/DxbAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYE\r\nFCrEt1U4NJpwTT/1RhfKnS+7My9lMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0B\r\nAQsFAAOCAQEACLxexo+KVCh583HqchgqTT7fA7S8MfvEXCh9yl7eS5NJ0G5KOe7T\r\n7/nJkXLh8lmx0lGtORLq1gP1Z2FLG5gjp3MQeOPB8qIXexY03c2NsI2IWYhp2FQO\r\nnBTzLI39taxjSAZdNUniEvg+OPBX623NNnPmo9WMENdqD0tuJ+/aKAjgxN8AXJhU\r\ndy1iAA4TjOSlEcBz5l4brf7rcN/3LP+WWsCWHq/R01Of4fA7GHyCG7ZTTMJtG2YI\r\n7ngXA3hLqPrsEofeByfoSwWgtbtPGUj/5uaCuf1QWq0At1EGgPkjZutHeQOkWN2b\r\nOEAVdwIM6uJH6YAyNoZeUuSX5A1Ftd7LXQ==\r\n-----END CERTIFICATE-----\r\n",
        #             "key": "-----BEGIN RSA PRIVATE KEY-----\r\nMIIEpQIBAAKCAQEApYcU/bPFF3eRQ8DsQE0opXPvUGF9FU10OF8GWaIhOv023Raf\r\nOl5z1pXolF6Tj6nlQzjJnkgqXzdZZdHoHez0pNSCbjCClsW7wHikgEB2NLZgaDga\r\nd/l8H7j872g3mTd15dD5b5m7/8EusO8OXxE8C9hOhDrsgLyVIYc/QQLWg+5tndSJ\r\n348Z0FwGlYcp8m+x5pjwfWB8l4brU5LT1w5IRF586cE9ZbYowSshhpgIi5H8dsfX\r\nPvx2UsRlKBnTq4O1FQLWWY/W+1HAvjybEdes1PHUg2xy+ci/q32HHuRyanHzb5TW\r\ntG/wv4xJhUo4SWLipPmAuzIauWGfIXpPSZZv9QIDAQABAoIBAFEBMjyV5TX+xZAq\r\nsXMmT2XovozPqK7sIJwVpL3ooeqEUH0RvQqLfpTc99zkC8Kamh+zgrd7CYFfTNiP\r\nSNCcTXz8onfaNY4jZiZi493/rdlOBw/5pLph1WSQ2vcuQUcx5Ph6tBbxXRdkKr1b\r\nv+S2QnRpfsMnMuYtY63syf++q8wT8OMrJVI8d2wZaeLtMAvYLxEEhhH/NJxy/bqC\r\n2LBoYS9ReCw1XZ+Gg3CvMHqtI08p+1shhNMPpohSYEnXY8B3hK777Ie9bAlgxp1k\r\nXjdFZlmG1CRxnbVmQq2jCF9KBeIXMTcu+c1/N4Y9K2ZUThvUizSPwQd01/adjRyd\r\nd8LOCgECgYEA1ZLJtB4+5TDhXf5mY4pYG/40Aq4r709blA6zdvrJV9jRVWVrad67\r\nNFMzbyhDg88GK4ft0QKuVJsMtNL2pXWhqozeNbbhGu22LmtdPdnlmmOfySUPt+jF\r\ndS5YZGmQPTzZ6oCovKq4zRZnLaB/kVaDcFfuLm4cYAyBiQK28ZkUcGUCgYEAxmjx\r\nWjbLb13DqZPQnJKOBAzkM64V6XYVzc5qGNPU7CTntOnSlkAAvfdt4rFcxaTgiIsB\r\nXDambqosOMKGn7+H9m3UVQAWufSZ+ahqishscJNQh8xnkbIG3cY3B/9ybzDPXzdV\r\ndO8D6xq1ODfOo8E8PMfQ+d3M368xqj/iTSYFYFECgYEAzH21v05Obmg1ASh6pMhr\r\nwLHO3tohmwti5gqFb2CEtCYXmSp4hHAM0vbvAnmM24G3qKqH3F4yyTOEIQb1vks5\r\nNfGXOdsXAg+lJiEKsBQYMZE+BvwDZtXral2rqMkioF/JTy1NYwgb1dKjjB5mxqQN\r\nSd4HYlFvvc97n9IHlKA737kCgYEAibf6HzZ9ivW4hJKXcLbBYMpZ9A1YJE7U35/x\r\nQP54gtkzA/5xL92JJlMCsSGPVZkWSXDDJvDAIXx5aYSM0YGurDyb78w5+iVwYzyl\r\nh2OK8bEvarNVCGpcHcAiHqkPE2L77gmIhbwKKjzFoRoLktrkJwRDZ8yvEmyWuqfR\r\nOt+zR6ECgYEAgh3UBwguujmt6NBFGthIyDGFBpmP4esdsIBbQudfkoEm2WvoBKe1\r\nrYI4s1gFHIN4i6/Q3CYaeMobeJ/NrKJRbiSaNTqyapVeBRbiF9H5POdU0nDPXomD\r\nvnJ78ACvsb4VWncmpkofC5/ETLLcxTJYwHQivaGWamK7KlJaA5SHXMM=\r\n-----END RSA PRIVATE KEY-----\r\n",
        #             "pkcs7": "-----BEGIN PKCS7-----\r\nMIIDRAYJKoZIhvcNAQcCoIIDNTCCAzECAQExADALBgkqhkiG9w0BBwGgggMZMIID\r\nFTCCAf2gAwIBAgIJYYMdy7j3myj2MA0GCSqGSIb3DQEBCwUAMCgxJjAkBgNVBAMT\r\nHWpzbS1zYW5kYm94LWRldjEudXMuYXV0aDAuY29tMB4XDTIyMDEwNTIxNTAzNFoX\r\nDTM1MDkxNDIxNTAzNFowKDEmMCQGA1UEAxMdanNtLXNhbmRib3gtZGV2MS51cy5h\r\ndXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC6rM871u1G\r\nRjWdk/UdrD3d9eLVAVDXvwjtslr2qmJ1gRerNcKLwtLoD6fkgD72DmghapS6wn2T\r\nzBqEBBIia6kuS86jZRrsrpPAQBB2MhJbSruU9UCjMdRhXgZYfxaZLj15MYzguCU4\r\nay+dTFd68vZlfei4j+yA5egBrAkKh7Pd0tkNLp55TPQzuVOOuf4kj1bdkaFnFDyu\r\naFM4w5TzHPTmx3FF98OlGPPfTPvafGsWBob1LpWBhMRS29yw1ENCcMgyb58mmIj1\r\ns943+UV1+rCSTSRtaVislj7+7ihRC903ZTk1SwtHotKEXIJVDyzZYB/Q3PkQKDgx\r\nift2h+Ii/DxbAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFCrE\r\nt1U4NJpwTT/1RhfKnS+7My9lMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0BAQsF\r\nAAOCAQEACLxexo+KVCh583HqchgqTT7fA7S8MfvEXCh9yl7eS5NJ0G5KOe7T7/nJ\r\nkXLh8lmx0lGtORLq1gP1Z2FLG5gjp3MQeOPB8qIXexY03c2NsI2IWYhp2FQOnBTz\r\nLI39taxjSAZdNUniEvg+OPBX623NNnPmo9WMENdqD0tuJ+/aKAjgxN8AXJhUdy1i\r\nAA4TjOSlEcBz5l4brf7rcN/3LP+WWsCWHq/R01Of4fA7GHyCG7ZTTMJtG2YI7ngX\r\nA3hLqPrsEofeByfoSwWgtbtPGUj/5uaCuf1QWq0At1EGgPkjZutHeQOkWN2bOEAV\r\ndwIM6uJH6YAyNoZeUuSX5A1Ftd7LXTEA\r\n-----END PKCS7-----\r\n",
        #             "subject": "/CN=jsm-sandbox-dev1.us.auth0.com",
        #         }
        #     ],
        #     "client_id": "RO5HKGnw3v6qWJ4ByHpKdxEl7IxZo1e9",
        #     "callback_url_template": False,
        #     "client_secret": "xC6saJeBRCo7JFmtSv-bX5vYrp0ztnAs4d-2h2l_HOFZWCfUkUyUOMvOjvG1EinU",
        #     "jwt_configuration": {"lifetime_in_seconds": 36000, "secret_encoded": False},
        #     "app_type": "regular_web",
        #     "grant_types": ["authorization_code", "implicit", "refresh_token", "client_credentials"],
        #     "custom_login_page_on": True,
        # }

    def test_should_create_client_app_spa(self):
        # Arrange
        name = "Tests - Temporary App B"
        app_type = AppType.SPA
        # Act
        client_details = management_api.create_client(name, app_type)
        # Assert
        # Assert
        self.created_client_id = client_details["client_id"]
        assert client_details["name"] == name
        assert client_details["app_type"] == app_type.name.lower()
        # I'm leaving this here just as example
        # assert client_details == {
        #     "tenant": "jsm-sandbox-dev1",
        #     "global": False,
        #     "is_token_endpoint_ip_header_trusted": False,
        #     "name": "Tests - Temporary App B",
        #     "cross_origin_auth": False,
        #     "is_first_party": True,
        #     "sso_disabled": False,
        #     "oidc_conformant": False,
        #     "refresh_token": {
        #         "expiration_type": "non-expiring",
        #         "leeway": 0,
        #         "infinite_token_lifetime": True,
        #         "infinite_idle_token_lifetime": True,
        #         "token_lifetime": 2592000,
        #         "idle_token_lifetime": 1296000,
        #         "rotation_type": "non-rotating",
        #     },
        #     "encrypted": True,
        #     "signing_keys": [
        #         {
        #             "cert": "-----BEGIN CERTIFICATE-----\r\nMIIDFTCCAf2gAwIBAgIJYYMdy7j3myj2MA0GCSqGSIb3DQEBCwUAMCgxJjAkBgNV\r\nBAMTHWpzbS1zYW5kYm94LWRldjEudXMuYXV0aDAuY29tMB4XDTIyMDEwNTIxNTAz\r\nNFoXDTM1MDkxNDIxNTAzNFowKDEmMCQGA1UEAxMdanNtLXNhbmRib3gtZGV2MS51\r\ncy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC6rM87\r\n1u1GRjWdk/UdrD3d9eLVAVDXvwjtslr2qmJ1gRerNcKLwtLoD6fkgD72DmghapS6\r\nwn2TzBqEBBIia6kuS86jZRrsrpPAQBB2MhJbSruU9UCjMdRhXgZYfxaZLj15MYzg\r\nuCU4ay+dTFd68vZlfei4j+yA5egBrAkKh7Pd0tkNLp55TPQzuVOOuf4kj1bdkaFn\r\nFDyuaFM4w5TzHPTmx3FF98OlGPPfTPvafGsWBob1LpWBhMRS29yw1ENCcMgyb58m\r\nmIj1s943+UV1+rCSTSRtaVislj7+7ihRC903ZTk1SwtHotKEXIJVDyzZYB/Q3PkQ\r\nKDgxift2h+Ii/DxbAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYE\r\nFCrEt1U4NJpwTT/1RhfKnS+7My9lMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0B\r\nAQsFAAOCAQEACLxexo+KVCh583HqchgqTT7fA7S8MfvEXCh9yl7eS5NJ0G5KOe7T\r\n7/nJkXLh8lmx0lGtORLq1gP1Z2FLG5gjp3MQeOPB8qIXexY03c2NsI2IWYhp2FQO\r\nnBTzLI39taxjSAZdNUniEvg+OPBX623NNnPmo9WMENdqD0tuJ+/aKAjgxN8AXJhU\r\ndy1iAA4TjOSlEcBz5l4brf7rcN/3LP+WWsCWHq/R01Of4fA7GHyCG7ZTTMJtG2YI\r\n7ngXA3hLqPrsEofeByfoSwWgtbtPGUj/5uaCuf1QWq0At1EGgPkjZutHeQOkWN2b\r\nOEAVdwIM6uJH6YAyNoZeUuSX5A1Ftd7LXQ==\r\n-----END CERTIFICATE-----\r\n",
        #             "key": "-----BEGIN RSA PRIVATE KEY-----\r\nMIIEowIBAAKCAQEAnE2RQUK/Tc0Kxy24Us+ZDENiF2WwRLuHAY3rk0NShzYsic9t\r\nXNnyu0QrUUX8S3TgbA4rANlUURJkl7XKjZ0qiGfnUils/YFWS0GKiRqzshLAapja\r\nDzF7nhusSWiwTjJPPUCt63AN2ICFwMMHUPgqUy+vJEkKMBNBew1361p3MEVL8Vr8\r\nWObxUkif/Q23V7LIwhz/4bc0HqZ8p/QwInN7KOrIPICaYU6fuPb49/lGfeYUY8sS\r\n6iIupkVY/VTc1c0nrtKvSGI3S23JIZjRf8ZTico8nWgR605Cgetb57vTynhmIGh5\r\n3DwvPQqg9/s2RzxU7q38+r2wIIzw9RzQFWuoyQIDAQABAoIBADzd0+/W/0pby5Ou\r\n0TWmVBI7d0pnNhI9+J/5VUB+mfe/d+6ekRb0ZJraPAglOc9kjzRk/AgTmcsMX5HY\r\noC0vg+2kkKclLKU3pZQezMUBWfLBbJ7WMSxzd5Elc50OoIGDA+p1coTZmPqzaeKb\r\n0BCO42SLkCeQLeB0zy4NG6LSEtH/vmVA4PZfUCxsq55+nFK5qQHuqHDer8yOmici\r\noO5uUSAQ7i9Gmo3/8j4IfTBQLBAIso/xkFn9yBkiEUBCyPDB0UUIsqwN42djuxI2\r\n+Rb7w8urVS19/G5RMgsr8063qsNUxby95C4I+ThQIfi21fmODnDyQ1Axe6IliPuo\r\nAoLNN0UCgYEAzwXhq//hKOdodzryUy6vfGN3HbnJfw0Vszg+tAme1IluxPBoKnty\r\nQU7OCo+TDfN/tGWvfHBTIB84wq9HMnmo6//FRkmKMCNvkHXmFoPCDEV/vDMHwYYn\r\nAFurPA1kCMQUk5jprtHwQVWi6gHxghktvYTyPkxnC7VxJT+YZUkv3sMCgYEAwUfi\r\n5cQuNlG6xf3mMuzG9GwiCGYRq+2Pech+vsMah+ym6aqE2nXwv9DCWj4YW1iRis7u\r\nUKzDxWH2i5aqxz5fQUhV8ml6MZ1NwI+Cv9HeO7JcAdYv8g+c9T+ZSOckh7J8U8sE\r\nckRarqp5PGT2TpzRiHeE1TIoQsfiGKy1zEKr+YMCgYAxYSXC8PWz2/5+8gB69tfE\r\nw7TV0krNk0FpzjCmoOTRrTZOo0k1WNyX10QuILDi0wHS9a418FTjhI71YPmKgJpa\r\nMFfNvBzJ/qnNu1F2bVcLtkgRi9p9vpHu8+6UFF2X+a0ux3p1yH2WF+cUCgKhFYBj\r\nhCKD2ZV6pXynddPT1PEmIQKBgQCQ0d0nzcvWdXydt3VReOpF3/PMGTZqfTCAzoJx\r\nStzJNb+G23Z5/d7qym+lkFtNrlo3CH+2QQzbC2DhDH5fldNnpdyIKxIctMG6Y41T\r\nTtvWHPklgygfliVD+WhQIKjVaB4R5s8pEyBjOWZnozqOgp/ZQbxsxg02pHA7jsUV\r\nDGuxIwKBgFkFbPEHSByxwUhD7e+oil17+GpOqgQDv3ze67yIrLR4AMp+Ta3yN4XX\r\n6CPPI8MEGukwu3WH+/cPA7wfa085MOR28nUy/Y0lvcsFL5l4dmcTdCWjHqL62gDu\r\nEdX/XB6hZhmgdtvtNsfoozt7BrxstdGLAg6TpbTaQDCyicSi6kcF\r\n-----END RSA PRIVATE KEY-----\r\n",
        #             "pkcs7": "-----BEGIN PKCS7-----\r\nMIIDRAYJKoZIhvcNAQcCoIIDNTCCAzECAQExADALBgkqhkiG9w0BBwGgggMZMIID\r\nFTCCAf2gAwIBAgIJYYMdy7j3myj2MA0GCSqGSIb3DQEBCwUAMCgxJjAkBgNVBAMT\r\nHWpzbS1zYW5kYm94LWRldjEudXMuYXV0aDAuY29tMB4XDTIyMDEwNTIxNTAzNFoX\r\nDTM1MDkxNDIxNTAzNFowKDEmMCQGA1UEAxMdanNtLXNhbmRib3gtZGV2MS51cy5h\r\ndXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC6rM871u1G\r\nRjWdk/UdrD3d9eLVAVDXvwjtslr2qmJ1gRerNcKLwtLoD6fkgD72DmghapS6wn2T\r\nzBqEBBIia6kuS86jZRrsrpPAQBB2MhJbSruU9UCjMdRhXgZYfxaZLj15MYzguCU4\r\nay+dTFd68vZlfei4j+yA5egBrAkKh7Pd0tkNLp55TPQzuVOOuf4kj1bdkaFnFDyu\r\naFM4w5TzHPTmx3FF98OlGPPfTPvafGsWBob1LpWBhMRS29yw1ENCcMgyb58mmIj1\r\ns943+UV1+rCSTSRtaVislj7+7ihRC903ZTk1SwtHotKEXIJVDyzZYB/Q3PkQKDgx\r\nift2h+Ii/DxbAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFCrE\r\nt1U4NJpwTT/1RhfKnS+7My9lMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0BAQsF\r\nAAOCAQEACLxexo+KVCh583HqchgqTT7fA7S8MfvEXCh9yl7eS5NJ0G5KOe7T7/nJ\r\nkXLh8lmx0lGtORLq1gP1Z2FLG5gjp3MQeOPB8qIXexY03c2NsI2IWYhp2FQOnBTz\r\nLI39taxjSAZdNUniEvg+OPBX623NNnPmo9WMENdqD0tuJ+/aKAjgxN8AXJhUdy1i\r\nAA4TjOSlEcBz5l4brf7rcN/3LP+WWsCWHq/R01Of4fA7GHyCG7ZTTMJtG2YI7ngX\r\nA3hLqPrsEofeByfoSwWgtbtPGUj/5uaCuf1QWq0At1EGgPkjZutHeQOkWN2bOEAV\r\ndwIM6uJH6YAyNoZeUuSX5A1Ftd7LXTEA\r\n-----END PKCS7-----\r\n",
        #             "subject": "/CN=jsm-sandbox-dev1.us.auth0.com",
        #         }
        #     ],
        #     "client_id": "ige8DbJsoiX6YrNbQT6BLgwpMYYHSKw7",
        #     "callback_url_template": False,
        #     "client_secret": "9fWynZQFjYibXJe1eUS0fiEgJCzhf3dR5DG61VRvv5lquE2ErHiuw5P6OYzOtTHj",
        #     "jwt_configuration": {"lifetime_in_seconds": 36000, "secret_encoded": False},
        #     "app_type": "spa",
        #     "grant_types": ["authorization_code", "implicit", "refresh_token", "client_credentials"],
        #     "custom_login_page_on": True,
        # }

    def test_should_create_app_and_apply_some_settings(self):
        # Arrange
        name = "Tests - Temporary App C"
        app_type = AppType.REGULAR_WEB
        my_service_address = "app.local:8000"
        allowed_logout_urls = [f"http://{my_service_address}/logout"]
        callbacks = [f"http://{my_service_address}/api/v1/response-oidc"]
        cross_origin_auth = True
        allowed_origins = [f"http://{my_service_address}"]
        web_origins = [f"http://{my_service_address}"]
        grant_types = ["authorization_code"]
        # Act
        client_details = management_api.create_client(
            name, app_type, callbacks, cross_origin_auth, allowed_origins, web_origins, allowed_logout_urls, grant_types
        )
        # Assert
        self.created_client_id = client_details["client_id"]
        assert client_details["name"] == name
        assert client_details["app_type"] == app_type.name.lower()
        assert client_details["callbacks"] == callbacks
        assert client_details["cross_origin_auth"] == cross_origin_auth
        assert client_details["allowed_origins"] == allowed_origins
        assert client_details["web_origins"] == web_origins
        assert client_details["allowed_logout_urls"] == allowed_logout_urls
        assert client_details["grant_types"] == grant_types

    def test_should_retrieve_all_connection(self):
        # Arrange
        fields = ["id", "strategy", "name"]
        fields = None
        # Act
        result = management_api.retrieve_all_connection(fields=fields)
        # Assert
        assert result == [
            {
                "id": "con_kqz7rscXZMuYWqR1",
                "strategy": "facebook",
                "name": "facebook",
                "is_domain_connection": False,
            },
            {
                "id": "con_G4Ai9I9DZv8LIxTd",
                "strategy": "google-oauth2",
                "name": "google-oauth2",
                "is_domain_connection": False,
            },
            {
                "id": "con_XOxbqfMx6XVMBQvu",
                "strategy": "auth0",
                "name": "Username-Password-Authentication",
                "is_domain_connection": False,
            },
            {
                "id": "con_cGZluuxhzsqnZZEe",
                "options": {
                    "name": "email",
                    "totp": {"length": 6, "time_step": 180},
                    "email": {
                        "body": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n    <style type="text/css">.ExternalClass,.ExternalClass div,.ExternalClass font,.ExternalClass p,.ExternalClass span,.ExternalClass td,img{line-height:100%}#outlook a{padding:0}.ExternalClass,.ReadMsgBody{width:100%}a,blockquote,body,li,p,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic;border:0;height:auto;outline:0;text-decoration:none}table{border-collapse:collapse!important}#bodyCell,#bodyTable,body{height:100%!important;margin:0;padding:0;font-family:ProximaNova,sans-serif}#bodyCell{padding:20px}#bodyTable{width:600px}@font-face{font-family:ProximaNova;src:url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-regular-webfont-webfont.eot);src:url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-regular-webfont-webfont.eot?#iefix) format(\'embedded-opentype\'),url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-regular-webfont-webfont.woff) format(\'woff\');font-weight:400;font-style:normal}@font-face{font-family:ProximaNova;src:url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-semibold-webfont-webfont.eot);src:url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-semibold-webfont-webfont.eot?#iefix) format(\'embedded-opentype\'),url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-semibold-webfont-webfont.woff) format(\'woff\');font-weight:600;font-style:normal}@media only screen and (max-width:480px){#bodyTable,body{width:100%!important}a,blockquote,body,li,p,table,td{-webkit-text-size-adjust:none!important}body{min-width:100%!important}#bodyTable{max-width:600px!important}#signIn{max-width:280px!important}}\n</style>\n  </head>\n  <body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0" style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;margin: 0;padding: 0;font-family: &quot;ProximaNova&quot;, sans-serif;height: 100% !important;"><center>\n  <table style="width: 600px;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;mso-table-lspace: 0pt;mso-table-rspace: 0pt;margin: 0;padding: 0;font-family: &quot;ProximaNova&quot;, sans-serif;border-collapse: collapse !important;height: 100% !important;" align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">\n    <tr>\n      <td align="center" valign="top" id="bodyCell" style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;mso-table-lspace: 0pt;mso-table-rspace: 0pt;margin: 0;padding: 20px;font-family: &quot;ProximaNova&quot;, sans-serif;height: 100% !important;">\n      <div class="main">\n        <p style="text-align: center;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%; margin-bottom: 30px;">\n          <img src="https://cdn.auth0.com/styleguide/2.0.9/lib/logos/img/badge.png" width="50" alt="Your logo goes here" style="-ms-interpolation-mode: bicubic;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">\n        </p>\n\n        <!-- Email change content -->\n        {% if operation == \'change_email\' %}\n\n          <p style="font-size: 1.2em;line-height: 1.3;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">Your email address has been updated.</p>\n\n        {% else %}\n\n          <!-- Signup email content -->\n          {% if send == \'link\' or send == \'link_ios\' or send == \'link_android\' %}\n\n            <p style="font-size: 1.2em;line-height: 1.3;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">Click and confirm that you want to sign in to {{ application.name }}. This link will expire in three minutes.</p>\n\n            <div style="text-align:center">\n            <a id="signIn" style="text-transform: uppercase;letter-spacing: 1px;color: #ffffff;text-decoration: none;display: inline-block;min-height: 48px;line-height: 48px;padding-top: 0;padding-right: 26px;padding-bottom: 0;margin: 20px 0;padding-left: 26px;border: 0;outline: 0;background: #eb5424;font-size: 14px;font-style: normal;font-weight: 400;text-align: center;white-space: nowrap;border-radius: 3px;text-overflow: ellipsis;max-width: 280px;overflow: hidden;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;" href="{{ link }}">Sign in to {{ application.name }}</a>\n            </div>\n\n            <p style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">Or sign in using this link:</p>\n            <p style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;"><a style="font-size: 12px; color: #A9B3BC; text-decoration: none;word-break: break-all;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;" href="{{ link }}">{{ link }}</a></p>\n\n            {% elsif send == \'code\' %}\n\n            <p style="font-size: 1.4em; line-height: 1.3;">Your verification code is: <b>{{ code }}</b></p>\n\n          {% endif %}\n\n        {% endif %}\n\n        <p style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">If you are having any issues with your account, please don\'t hesitate to contact us by replying to this mail.</p>\n\n        <br>\n        Thanks!\n        <br>\n\n        <strong>{{ application.name }}</strong>\n\n        <br><br>\n        <hr style="border: 2px solid #EAEEF3; border-bottom: 0; margin: 20px 0;">\n        <p style="text-align: center;color: #A9B3BC;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">\n          If you did not make this request, please contact us by replying to this mail.\n        </p>\n      </div>\n      </td>\n    </tr>\n  </table>\n</center>\n</body>\n</html>',
                        "from": "{{ application.name }} <root@auth0.com>",
                        "syntax": "liquid",
                        "subject": "Welcome to {{ application.name }}",
                    },
                    "disable_signup": False,
                    "brute_force_protection": True,
                },
                "strategy": "email",
                "name": "email",
                "is_domain_connection": False,
                "realms": ["email"],
                "enabled_clients": [],
            },
        ]
        # Just leaving the thing below as an example!
        # assert result == [
        #     {
        #         "id": "con_kqz7rscXZMuYWqR1",
        #         "options": {
        #             "email": True,
        #             "scope": "email,public_profile",
        #             "ads_read": False,
        #             "client_id": "",
        #             "user_link": False,
        #             "user_likes": False,
        #             "user_posts": False,
        #             "read_stream": False,
        #             "user_events": False,
        #             "user_gender": False,
        #             "user_groups": False,
        #             "user_photos": False,
        #             "user_status": False,
        #             "user_videos": False,
        #             "manage_pages": False,
        #             "read_mailbox": False,
        #             "user_friends": False,
        #             "publish_pages": False,
        #             "publish_video": False,
        #             "read_insights": False,
        #             "user_birthday": False,
        #             "user_hometown": False,
        #             "user_location": False,
        #             "ads_management": False,
        #             "public_profile": True,
        #             "user_age_range": False,
        #             "leads_retrieval": False,
        #             "pages_messaging": False,
        #             "pages_show_list": False,
        #             "publish_actions": False,
        #             "pages_manage_cta": False,
        #             "publish_to_groups": False,
        #             "user_tagged_places": False,
        #             "business_management": False,
        #             "read_page_mailboxes": False,
        #             "user_managed_groups": False,
        #             "manage_notifications": False,
        #             "groups_access_member_info": False,
        #             "allow_context_profile_field": False,
        #             "pages_messaging_phone_number": False,
        #             "pages_manage_instant_articles": False,
        #             "pages_messaging_subscriptions": False,
        #             "read_audience_network_insights": False,
        #         },
        #         "strategy": "facebook",
        #         "name": "facebook",
        #         "is_domain_connection": False,
        #         "realms": ["facebook"],
        #         "enabled_clients": [],
        #     },
        #     {
        #         "id": "con_G4Ai9I9DZv8LIxTd",
        #         "options": {"email": True, "scope": ["email", "profile"], "profile": True},
        #         "strategy": "google-oauth2",
        #         "name": "google-oauth2",
        #         "is_domain_connection": False,
        #         "realms": ["google-oauth2"],
        #         "enabled_clients": ["CAR3cmoBtcNUbHYSHKEmPEUEUBSMs0RI", "wkKnt6BQmBtX6Pr2kfJNkMVfm6fh2s5U"],
        #     },
        #     {
        #         "id": "con_XOxbqfMx6XVMBQvu",
        #         "options": {
        #             "mfa": {"active": True, "return_enroll_settings": True},
        #             "passwordPolicy": "good",
        #             "strategy_version": 2,
        #             "brute_force_protection": True,
        #         },
        #         "strategy": "auth0",
        #         "name": "Username-Password-Authentication",
        #         "is_domain_connection": False,
        #         "realms": ["Username-Password-Authentication"],
        #         "enabled_clients": ["CAR3cmoBtcNUbHYSHKEmPEUEUBSMs0RI", "wkKnt6BQmBtX6Pr2kfJNkMVfm6fh2s5U"],
        #     },
        # ]

    @unittest.SkipTest
    def test_should_delete_connection(self):
        # Arrange
        connection_id = "con_cGZluuxhzsqnZZEe"
        # Act
        result = management_api.delete_connection(connection_id)
        # Assert
        assert result == {"deleted_at": "2022-01-09T19:40:22.603Z"}

    @unittest.SkipTest
    def test_should_create_connection_facebook(self):
        # Arrange
        name = "facebook"
        strategy = "facebook"
        # Act
        result = management_api.create_connection(name, strategy)
        # Assert
        assert result == {
            "id": "con_Srme57EQLLnrAdEC",
            "options": {"email": True, "scope": "email,public_profile", "public_profile": True},
            "strategy": "facebook",
            "name": "facebook",
            "is_domain_connection": False,
            "enabled_clients": [],
            "realms": ["facebook"],
        }

    @unittest.SkipTest
    def test_should_create_connection_google(self):
        # Arrange
        name = "google-oauth2"
        strategy = "google-oauth2"
        enabled_clients = ["CAR3cmoBtcNUbHYSHKEmPEUEUBSMs0RI"]
        # Act
        result = management_api.create_connection(name, strategy, enabled_clients)
        # Assert
        assert result == {
            "id": "con_7DDvBmb0szaP036j",
            "options": {"email": True, "scope": ["email", "profile"], "profile": True},
            "strategy": "google-oauth2",
            "name": "google-oauth2",
            "is_domain_connection": False,
            "enabled_clients": ["CAR3cmoBtcNUbHYSHKEmPEUEUBSMs0RI"],
            "realms": ["google-oauth2"],
        }

    @unittest.SkipTest
    def test_retrieve_current_email_provider(self):
        # Act
        # If not e-mail provider has ever been configured, then None will be returned
        result = management_api.current_email_provider()
        # Assert
        assert result == {
            "enabled": False,
            "default_from_address": "Não responda <juntosid-nao-responda@jsmais.com>",
            "credentials": {
                "smtp_host": "smtp.mailgun.org",
                "smtp_port": 587,
                "smtp_user": "juntosid-nao-responda@jsmais.com",
            },
        }

    @unittest.SkipTest
    def test_delete_current_email_provider(self):
        # Act
        result = management_api.delete_email_provider()
        # Assert
        assert result == ""

    @unittest.SkipTest
    def test_should_configure_email_provider(self):
        # Arrange
        arguments = {
            "default_from_address": "Não responda <juntosid-nao-responda@jsmais.com>",
            "smtp_host": "smtp.mailgun.org",
            "smtp_port": 587,
            "smtp_user": "juntosid-nao-responda@jsmais.com",
            "smtp_pass": "YOUR_SMTP_PASSWORD",
        }
        # Act
        result = management_api.configure_email_provider(**arguments)
        # Assert
        assert result == {
            "name": "smtp",
            "enabled": True,
            "default_from_address": "Não responda <juntosid-nao-responda@jsmais.com>",
            "credentials": {
                "smtp_host": "smtp.mailgun.org",
                "smtp_port": 587,
                "smtp_user": "juntosid-nao-responda@jsmais.com",
            },
        }

    @unittest.SkipTest
    def test_should_delete_clients(self):
        # Arrange
        clients = management_api.retrieve_all_clients()
        for client in clients:
            if client["name"].lower() == settings.PRODUCT_A_NAME.lower():
                management_api.delete_client(client["client_id"])
                continue
            if client["name"].lower() == settings.PRODUCT_B_NAME.lower():
                management_api.delete_client(client["client_id"])
                continue
            if client["name"].lower() == settings.PRODUCT_C_NAME.lower():
                management_api.delete_client(client["client_id"])
                continue

    @unittest.SkipTest
    def test_retrieve_all_client_grants(self):
        # Act
        result = management_api.retrieve_all_client_grants()
        # Assert
        assert result == [
            {
                "id": "cgr_99YBl1KhuQ2aI5He",
                "client_id": "CAR3cmoBtcNUbHYSHKEmPEUEUBSMs0RI",
                "audience": "https://jsm-sandbox-dev1.us.auth0.com/api/v2/",
                "scope": [
                    "read:client_grants",
                    "update:client_grants",
                    "read:users",
                    "update:users",
                    "read:clients",
                    "update:clients",
                    "delete:clients",
                    "create:clients",
                    "read:client_keys",
                    "read:connections",
                    "update:connections",
                    "delete:connections",
                    "create:connections",
                    "read:email_provider",
                    "update:email_provider",
                    "delete:email_provider",
                    "create:email_provider",
                ],
            }
        ]

    @unittest.SkipTest
    def test_should_create_client_grant(self):
        # Arrange
        cliend_id = "fsC8VuacDnUu7l2hmg6kkmgPTXrWZEvQ"
        audience = "https://jsm-sandbox-dev1.us.auth0.com/api/v2/"
        scope = ["read:users", "update:users"]
        # Act
        result = management_api.create_client_grant(cliend_id, audience, scope)
        # Assert
        assert result == {
            "id": "cgr_DUlVpNBGUrlGnLyW",
            "client_id": "fsC8VuacDnUu7l2hmg6kkmgPTXrWZEvQ",
            "audience": "https://jsm-sandbox-dev1.us.auth0.com/api/v2/",
            "scope": ["read:users", "update:users"],
        }
