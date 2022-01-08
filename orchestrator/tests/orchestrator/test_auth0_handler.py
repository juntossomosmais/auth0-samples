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

    # @unittest.SkipTest
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
