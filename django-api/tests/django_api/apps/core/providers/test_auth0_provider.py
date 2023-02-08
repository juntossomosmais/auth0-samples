import unittest

from datetime import date

from apps.core.providers.auth0_provider import resource_owner

from django_api.apps.core.providers.auth0_provider import management_api


class ManagementAPITests(unittest.TestCase):
    @unittest.SkipTest
    def test_should_retrieve_user_details(self):
        # Arrange
        user_id = "email|61f685d478d57a7db2054875"
        # Act
        user_details = management_api.retrieve_user_details(user_id)
        # Assert
        assert user_details == {
            "created_at": "2022-01-30T12:34:41.611Z",
            "email": "willian.lima.antunes@gmail.com",
            "email_verified": True,
            "identities": [
                {"user_id": "61f685d478d57a7db2054875", "provider": "email", "connection": "email", "isSocial": False}
            ],
            "name": "willian.lima.antunes@gmail.com",
            "nickname": "willian.lima.antunes",
            "picture": "https://s.gravatar.com/avatar/38ecfbc56718536ca51fcaae7d7da9b3?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fwi.png",
            "updated_at": "2022-01-30T12:34:41.611Z",
            "user_id": "email|61f685d478d57a7db2054875",
            "last_ip": "2804:14d:1a87:c8de:254e:64d6:7a01:59ff",
            "last_login": "2022-01-30T12:34:41.609Z",
            "logins_count": 1,
        }

    @unittest.SkipTest
    def test_should_create_email_passwordless(self):
        # Arrange
        email = "willian.lima.antunes@gmail.com"
        # Act
        result = management_api.create_user_email_one_time_password(email)
        # Assert
        assert result == {
            "created_at": "2022-01-30T13:08:17.944Z",
            "email": "willian.lima.antunes@gmail.com",
            "email_verified": True,
            "identities": [
                {"connection": "email", "user_id": "61f68dc178d57a7db2810c52", "provider": "email", "isSocial": False}
            ],
            "name": "willian.lima.antunes@gmail.com",
            "nickname": "willian.lima.antunes",
            "picture": "https://s.gravatar.com/avatar/38ecfbc56718536ca51fcaae7d7da9b3?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fwi.png",
            "updated_at": "2022-01-30T13:08:17.944Z",
            "user_id": "email|61f68dc178d57a7db2810c52",
        }

    @unittest.SkipTest
    def test_should_create_email_passwordless_followed_by_its_account_linking(self):
        # Arrange
        primary_account_id = "auth0|61e466c0ae29b30076468b30"
        email = "willian.lima.antunes@gmail.com"
        # Act
        result = management_api.create_user_email_one_time_password(email)
        user_id = result["user_id"]
        provider = result["identities"][0]["provider"]
        result = management_api.link_accounts_through_secondary_accounts_details(primary_account_id, provider, user_id)
        # Assert
        assert result == [
            {
                "profileData": {
                    "email": "willian.lima.antunes@gmail.com",
                    "email_verified": True,
                    "username": "44060267031",
                },
                "user_id": "61e466c0ae29b30076468b30",
                "provider": "auth0",
                "connection": "Username-Password-Authentication",
                "isSocial": False,
            },
            {
                "profileData": {
                    "name": "Willian Antunes",
                    "email": "willian.lima.antunes@gmail.com",
                    "given_name": "Willian",
                    "family_name": "Antunes",
                    "picture": "https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=10218925956491642&height=50&width=50&ext=1646139045&hash=AeQVlkNVU7OaFTkHEsQ",
                    "picture_large": "https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=10218925956491642&width=999999&ext=1646139045&hash=AeS2O4NwKvYkiB6IKhY",
                    "name_format": "{first} {last}",
                    "short_name": "Willian",
                    "installed": True,
                    "install_type": "UNKNOWN",
                    "video_upload_limits": {"length": 14460, "size": 28633115306},
                    "email_verified": True,
                },
                "user_id": "10218925956491642",
                "provider": "facebook",
                "connection": "facebook",
                "isSocial": True,
            },
            {
                "profileData": {"email": "willian.lima.antunes@gmail.com", "email_verified": True},
                "connection": "email",
                "user_id": "61f6903f78d57a7db2aaedd5",
                "provider": "email",
                "isSocial": False,
            },
        ]

    @unittest.SkipTest
    def test_should_update_user_profile_scenario_1(self):
        # Arrange
        user_id = "auth0|61e466c0ae29b30076468b30"
        full_name = "Curt Smith"
        given_name = "Curt"
        family_name = "Smith"
        user_metadata = {
            "city": "São Paulo",
            "state": "SP",
            "birthday": date(1989, 6, 23).isoformat(),
            "gender": "masculine",
        }
        # Act
        result = management_api.update_user(user_id, full_name, family_name, given_name, user_metadata)
        # Assert
        assert result == {
            "created_at": "2022-01-30T12:49:47.557Z",
            "email": "willian.lima.antunes@gmail.com",
            "email_verified": True,
            "identities": [
                {
                    "user_id": "61e466c0ae29b30076468b30",
                    "provider": "auth0",
                    "connection": "Username-Password-Authentication",
                    "isSocial": False,
                }
            ],
            "name": "Curt Smith",
            "nickname": "willian.lima.antunes",
            "picture": "https://s.gravatar.com/avatar/38ecfbc56718536ca51fcaae7d7da9b3?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fwi.png",
            "updated_at": "2022-01-30T14:31:18.773Z",
            "user_id": "auth0|61e466c0ae29b30076468b30",
            "username": "44060267031",
            "family_name": "Smith",
            "given_name": "Curt",
            "user_metadata": {"birthday": "1989-06-23", "city": "São Paulo", "gender": "masculine", "state": "SP"},
            "last_ip": "2804:14d:1a87:c8de:254e:64d6:7a01:59ff",
            "last_login": "2022-01-30T13:20:50.313Z",
            "logins_count": 4,
        }

    @unittest.SkipTest
    def test_should_update_user_profile_scenario_2(self):
        # Arrange
        user_id = "auth0|61e466c0ae29b30076468b30"
        full_name = "Curt Smith"
        given_name = None
        family_name = None
        user_metadata = None
        app_metadata = {
            "Product C": {
                "owner": True,
            },
        }
        # Act
        result = management_api.update_user(user_id, full_name, family_name, given_name, user_metadata, app_metadata)
        # Assert
        assert result == {
            "created_at": "2022-01-30T12:49:47.557Z",
            "email": "willian.lima.antunes@gmail.com",
            "email_verified": True,
            "identities": [
                {
                    "user_id": "61e466c0ae29b30076468b30",
                    "provider": "auth0",
                    "connection": "Username-Password-Authentication",
                    "isSocial": False,
                }
            ],
            "name": "Curt Smith",
            "nickname": "willian.lima.antunes",
            "picture": "https://s.gravatar.com/avatar/38ecfbc56718536ca51fcaae7d7da9b3?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fwi.png",
            "updated_at": "2022-01-30T14:38:36.891Z",
            "user_id": "auth0|61e466c0ae29b30076468b30",
            "username": "44060267031",
            "family_name": "Smith",
            "given_name": "Curt",
            "user_metadata": {"birthday": "1989-06-23", "city": "São Paulo", "gender": "masculine", "state": "SP"},
            "app_metadata": {"Product C": {"owner": True}},
            "last_ip": "2804:14d:1a87:c8de:254e:64d6:7a01:59ff",
            "last_login": "2022-01-30T13:20:50.313Z",
            "logins_count": 4,
        }

    @unittest.SkipTest
    def test_should_retrieve_user(self):
        # Arrange
        user_id = "auth0|61e466c0ae29b30076468b30"
        # Act
        result = management_api.retrieve_user(user_id)
        # Assert
        assert result == {
            "created_at": "2022-01-30T12:49:47.557Z",
            "email": "willian.lima.antunes@gmail.com",
            "email_verified": True,
            "identities": [
                {
                    "user_id": "61e466c0ae29b30076468b30",
                    "provider": "auth0",
                    "connection": "Username-Password-Authentication",
                    "isSocial": False,
                }
            ],
            "name": "Jafar Iago",
            "nickname": "willian.lima.antunes",
            "picture": "https://s.gravatar.com/avatar/38ecfbc56718536ca51fcaae7d7da9b3?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fwi.png",
            "updated_at": "2022-01-30T22:07:52.331Z",
            "user_id": "auth0|61e466c0ae29b30076468b30",
            "username": "44060267031",
            "family_name": "Smith",
            "given_name": "Curt",
            "user_metadata": {"birthday": "1985-06-23", "city": "São Paulo", "gender": "masculine", "state": "SP"},
            "app_metadata": {"Product C": {"owner": True}},
            "last_ip": "2804:14d:1a87:c8de:d982:7d20:62f6:cea3",
            "last_login": "2022-01-30T19:44:12.175Z",
            "logins_count": 6,
        }


class AuthenticationAPITests(unittest.TestCase):
    @unittest.SkipTest
    def test_resource_owner_when_password_is_wrong(self):
        # Arrange
        email = "willian.lima.antunes@gmail.com"
        password = "WrongPassword"
        # Act
        response = resource_owner(email, password)
        # Assert
        assert response is None

    @unittest.SkipTest
    def test_resource_owner_when_password_is_right(self):
        # Arrange
        email = "willian.lima.antunes@gmail.com"
        password = "YouRVeryCurious"
        # Act
        response = resource_owner(email, password)
        # Assert
        assert response == {
            "access_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9hbnR1bmVzLnVzLmF1dGgwLmNvbS8ifQ..EPGj9cKIFuNN-7Xi.uhgNKOmCHYjV7lzPb2BF8muGKQ-3EXARsftztmI5X1ZDlPP6rexgGMHkBhbROmvKniWY2R0ORuQ9wNRaCZLw1iiNO4AkzqDci4o621NIULJLRUJ6vsQdUZ2_POjSL-Io7gxzdznyeJeEcA739EaaSv6oA3-E-t0isJvKBABne-awLOST1xSygDPUTnhHiv45EEbkIcXCAFM-J88T5yk1XqXJIxO4s0dXniT50DXCBtDiBiLS94Fe-TsXJYH6zpVOxNx20S32y8cy_f0KgW9VWxmjFwQcACBJjS-2scyYuW8cTfyrU5KRJHROhmExnH1Kazlr9N1tBa3KW5noDuPqyH4T8_rrkbA.zrdIEtJFC5FYKGRKeJzrGg",
            "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZhWVp3X0NFSTBJUnotU2FHOWJoaSJ9.eyJuaWNrbmFtZSI6IndpbGxpYW4ubGltYS5hbnR1bmVzIiwibmFtZSI6IndpbGxpYW4ubGltYS5hbnR1bmVzQGdtYWlsLmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci8zOGVjZmJjNTY3MTg1MzZjYTUxZmNhYWU3ZDdkYTliMz9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRndpLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDIzLTAyLTA4VDE4OjAxOjM4LjY0NloiLCJlbWFpbCI6IndpbGxpYW4ubGltYS5hbnR1bmVzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL2FudHVuZXMudXMuYXV0aDAuY29tLyIsImF1ZCI6IjRVdzE3ZU92NEE1NHM1dHJlNHl1bDR4ellaQnhVWXBHIiwiaWF0IjoxNjc1ODc5Mjk4LCJleHAiOjE2NzU5MTUyOTgsInN1YiI6ImF1dGgwfDYzYTBlNTY3ODU2YjhmMmRlZTFhODdmYiJ9.JkrOxJ9l8Iq9J193futituoClX_xdyxJTu_UEiXHk36gcMoSjxvPw5Klja56Yof8tu-TvskpMhk3YG63bAlPvhG3txJezyNT_WB2t13sLDbVhCdf41tYGdQpf4jzC-AF5dt9JvW_1zK4w5aKBlmAO3eDjaKYAvKw-uPY8Mn7Itx_vsPQRWQjLC7xiUI0mNmZ7D6zS_aJkoTMarIaFCMcBN8WlHKw2-m_3XOwNs256VBh3XO0VEL3XTmFPBehw9oV9VUBlzQWVm_Lk2x4x0OYh95yZu9P-y24LFXZ7Gy4XBiUh3Pcw_THKXT7mKOeuJ6hzPSjIxtjApO5rdvtwPMDzg",
            "scope": "openid profile email address phone",
            "expires_in": 86400,
            "token_type": "Bearer",
        }
