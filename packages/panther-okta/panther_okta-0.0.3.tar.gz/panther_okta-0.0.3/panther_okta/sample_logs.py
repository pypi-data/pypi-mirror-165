import json

user_session_start = json.dumps(
    {
        "published": "2022-03-22 14:21:53.225",
        "eventType": "user.session.start",
        "version": "0",
        "severity": "INFO",
        "actor": {
            "alternateId": "homer@springfield.gov",
            "displayName": "Homer Simpson",
            "id": "111111",
            "type": "User",
        },
        "client": {
            "device": "Computer",
            "ipAddress": "1.1.1.1",
            "userAgent": {
                "browser": "CHROME",
                "os": "Mac OS X",
                "rawUserAgent": "Mozilla/5.0",
            },
            "zone": "null",
        },
        "p_log_type": "Okta.SystemLog",
    }
)


system_mfa_factor_deactivate = json.dumps(
    {
        "published": "2022-03-22 14:21:53.225",
        "eventType": "system.mfa.factor.deactivate",
        "version": "0",
        "severity": "HIGH",
        "actor": {
            "alternateId": "homer@springfield.gov",
            "displayName": "Homer Simpson",
            "id": "111111",
            "type": "User",
        },
        "client": {
            "device": "Computer",
            "ipAddress": "1.1.1.1",
            "userAgent": {
                "browser": "CHROME",
                "os": "Mac OS X",
                "rawUserAgent": "Mozilla/5.0",
            },
            "zone": "null",
        },
        "p_log_type": "Okta.SystemLog",
    }
)


user_session_impersonation_grant = json.dumps(
    {
        "published": "2022-03-22 14:21:53.225",
        "eventType": "user.session.impersonation.grant",
        "version": "0",
        "severity": "INFO",
        "legacyEventType": "core.user.impersonation.grant.enabled",
        "displayMessage": "Enable impersonation grant",
        "actor": {
            "alternateId": "homer@springfield.gov",
            "displayName": "Homer Simpson",
            "id": "111111",
            "type": "User",
        },
        "client": {
            "device": "Computer",
            "ipAddress": "1.1.1.1",
            "userAgent": {
                "browser": "CHROME",
                "os": "Mac OS X",
                "rawUserAgent": "Mozilla/5.0",
            },
            "zone": "null",
        },
        "p_log_type": "Okta.SystemLog",
    }
)


admin_access_assigned = json.dumps(
    {
        "uuid": "2a992f80-d1ad-4f62-900e-8c68bb72a21b",
        "published": "2020-11-25 21:27:03.496000000",
        "eventType": "user.account.privilege.grant",
        "version": "0",
        "severity": "INFO",
        "legacyEventType": "core.user.admin_privilege.granted",
        "displayMessage": "Grant user privilege",
        "actor": {
            "id": "00uu1uuuuIlllaaaa356",
            "type": "User",
            "alternateId": "jack@acme.io",
            "displayName": "Jack Naglieri",
        },
        "client": {
            "userAgent": {
                "browser": "CHROME",
                "os": "Mac OS X",
                "rawUserAgent": "Mozilla/5.0",
            },
            "geographicalContext": {
                "geolocation": {"lat": 37.7852, "lon": -122.3874},
                "city": "San Francisco",
                "state": "California",
                "country": "United States",
                "postalCode": "94105",
            },
            "zone": "null",
            "ipAddress": "136.24.229.58",
            "device": "Computer",
        },
        "request": {},
        "outcome": {"result": "SUCCESS"},
        "target": [
            {
                "id": "00u6eup97mAJZWYmP357",
                "type": "User",
                "alternateId": "alice@acme.io",
                "displayName": "Alice Green",
            }
        ],
        "transaction": {},
        "debugContext": {
            "debugData": {
                "privilegeGranted": "Organization administrator, Application administrator (all)",
                "requestUri": "/api/internal/administrators/00u6eu8c68bb72a21b57",
                "threatSuspected": "false",
                "url": "/api/internal/administrators/00u6eu8c68bb72a21b57",
                "requestId": "X777JJ9sssQQHHrrrQTyYQAABBE",
            }
        },
        "authenticationContext": {},
        "securityContext": {},
    }
)


system_api_token_create = json.dumps(
    {
        "uuid": "2a992f80-d1ad-4f62-900e-8c68bb72a21b",
        "published": "2021-01-08 21:28:34.875",
        "eventType": "system.api_token.create",
        "version": "0",
        "severity": "INFO",
        "legacyEventType": "api.token.create",
        "displayMessage": "Create API token",
        "actor": {
            "alternateId": "user@example.com",
            "displayName": "Test User",
            "id": "00u3q14ei6KUOm4Xi2p4",
            "type": "User",
        },
        "outcome": {"result": "SUCCESS"},
        "request": {},
        "debugContext": {},
        "target": [
            {
                "id": "00Tpki36zlWjhjQ1u2p4",
                "type": "Token",
                "alternateId": "unknown",
                "displayName": "test_key",
                "details": None,
            }
        ],
    }
)


system_api_token_revoke = json.dumps(
    {
        "uuid": "2a992f80-d1ad-4f62-900e-8c68bb72a21b",
        "published": "2021-01-08 21:28:34.875",
        "eventType": "system.api_token.revoke",
        "version": "0",
        "severity": "INFO",
        "legacyEventType": "api.token.revoke",
        "displayMessage": "Revoke API token",
        "actor": {
            "alternateId": "user@example.com",
            "displayName": "Test User",
            "id": "00u3q14ei6KUOm4Xi2p4",
            "type": "User",
        },
        "outcome": {"result": "SUCCESS"},
        "request": {},
        "debugContext": {},
        "target": [
            {
                "id": "00Tpki36zlWjhjQ1u2p4",
                "type": "Token",
                "alternateId": "unknown",
                "displayName": "test_key",
                "details": None,
            }
        ],
    }
)


user_session_start_failed = json.dumps(
    {
        "uuid": "2a992f80-d1ad-4f62-900e-8c68bb72a21b",
        "published": "2020-11-25 21:27:03.496000000",
        "eventType": "user.session.start",
        "version": "0",
        "severity": "INFO",
        "displayMessage": "User login to Okta",
        "actor": {
            "id": "00uu1uuuuIlllaaaa356",
            "type": "User",
            "alternateId": "jack@acme.io",
            "displayName": "Jack Naglieri",
        },
        "client": {
            "userAgent": {
                "browser": "CHROME",
                "os": "Mac OS X",
                "rawUserAgent": "Mozilla/5.0",
            },
            "geographicalContext": {
                "geolocation": {"lat": 37.7852, "lon": -122.3874},
                "city": "San Francisco",
                "state": "California",
                "country": "United States",
                "postalCode": "94105",
            },
            "zone": "null",
            "ipAddress": "136.24.229.58",
            "device": "Computer",
        },
        "request": {},
        "outcome": {"result": "FAILURE", "reason": "VERIFICATION_ERROR"},
    }
)


failed_login = json.dumps(
    {
        "actor": {
            "alternateId": "admin",
            "displayName": "unknown",
            "id": "unknown",
            "type": "User",
        },
        "authenticationContext": {
            "authenticationStep": 0,
            "externalSessionId": "unknown",
        },
        "client": {
            "device": "Computer",
            "geographicalContext": {
                "city": "Dois Irmaos",
                "country": "Brazil",
                "geolocation": {"lat": -29.6116, "lon": -51.0933},
                "postalCode": "93950",
                "state": "Rio Grande do Sul",
            },
            "ipAddress": "redacted",
            "userAgent": {
                "browser": "CHROME",
                "os": "Linux",
                "rawUserAgent": "Mozilla/5.0",
            },
            "zone": "null",
        },
        "debugContext": {
            "debugData": {
                "loginResult": "VERIFICATION_ERROR",
                "requestId": "redacted",
                "requestUri": "redacted",
                "threatSuspected": "false",
                "url": "redacted",
            }
        },
        "displayMessage": "User login to Okta",
        "eventType": "user.session.start",
        "legacyEventType": "core.user_auth.login_failed",
        "outcome": {"reason": "VERIFICATION_ERROR", "result": "FAILURE"},
        "p_any_domain_names": ["rnvtelecom.com.br"],
        "p_any_ip_addresses": ["redacted"],
        "p_event_time": "redacted",
        "p_log_type": "Okta.SystemLog",
        "p_parse_time": "redacted",
        "p_row_id": "redacted",
        "p_source_id": "redacted",
        "p_source_label": "Okta",
        "published": "redacted",
        "request": {
            "ipChain": [
                {
                    "geographicalContext": {
                        "city": "Dois Irmaos",
                        "country": "Brazil",
                        "geolocation": {"lat": -29.6116, "lon": -51.0933},
                        "postalCode": "93950",
                        "state": "Rio Grande do Sul",
                    },
                    "ip": "redacted",
                    "version": "V4",
                }
            ]
        },
        "securityContext": {
            "asNumber": 263297,
            "asOrg": "renovare telecom",
            "domain": "rnvtelecom.com.br",
            "isProxy": False,
            "isp": "renovare telecom",
        },
        "severity": "INFO",
        "transaction": {"detail": {}, "id": "redacted", "type": "WEB"},
        "uuid": "redacted",
        "version": "0",
    }
)


incomplete_geolocation_info = json.dumps(
    {
        "actor": {
            "alternateId": "admin",
            "displayName": "unknown",
            "id": "unknown",
            "type": "User",
        },
        "authenticationContext": {
            "authenticationStep": 0,
            "externalSessionId": "unknown",
        },
        "client": {
            "device": "Computer",
            "geographicalContext": {
                "country": "Brazil",
                "geolocation": {"lat": -29.6116, "lon": -51.0933},
                "postalCode": "93950",
                "state": "Rio Grande do Sul",
            },
            "ipAddress": "redacted",
            "userAgent": {
                "browser": "CHROME",
                "os": "Linux",
                "rawUserAgent": "Mozilla/5.0",
            },
            "zone": "null",
        },
        "debugContext": {
            "debugData": {
                "loginResult": "VERIFICATION_ERROR",
                "requestId": "redacted",
                "requestUri": "redacted",
                "threatSuspected": "false",
                "url": "redacted",
            }
        },
        "displayMessage": "User login to Okta",
        "eventType": "user.session.start",
        "legacyEventType": "core.user_auth.login_failed",
        "outcome": {
            "result": "SUCCESS",
        },
        "p_any_domain_names": ["rnvtelecom.com.br"],
        "p_any_ip_addresses": ["redacted"],
        "p_event_time": "redacted",
        "p_log_type": "Okta.SystemLog",
        "p_parse_time": "redacted",
        "p_row_id": "redacted",
        "p_source_id": "redacted",
        "p_source_label": "Okta",
        "published": "redacted",
        "request": {
            "ipChain": [
                {
                    "geographicalContext": {
                        "country": "Brazil",
                        "geolocation": {"lat": -29.6116, "lon": -51.0933},
                        "postalCode": "93950",
                        "state": "Rio Grande do Sul",
                    },
                    "ip": "redacted",
                    "version": "V4",
                }
            ]
        },
        "securityContext": {
            "asNumber": 263297,
            "asOrg": "renovare telecom",
            "domain": "rnvtelecom.com.br",
            "isProxy": False,
            "isp": "renovare telecom",
        },
        "severity": "INFO",
        "transaction": {"detail": {}, "id": "redacted", "type": "WEB"},
        "uuid": "redacted",
        "version": "0",
    }
)


first_login = json.dumps(
    {
        "actor": {
            "alternateId": "buser@example.com",
            "displayName": "Bobert User",
            "id": "111",
            "type": "User",
        },
        "authenticationContext": {"authenticationStep": 0, "externalSessionId": "111"},
        "client": {
            "device": "Computer",
            "geographicalContext": {
                "city": "Baltimore",
                "country": "United States",
                "geolocation": {"lat": 39.2891, "lon": -76.5583},
                "postalCode": "21224",
                "state": "Maryland",
            },
            "ipAddress": "192.168.0.9",
            "userAgent": {
                "browser": "CHROME",
                "os": "Windows 10",
                "rawUserAgent": "Mozilla/5.0",
            },
            "zone": "null",
        },
        "debugContext": {
            "debugData": {
                "requestId": "11111",
                "requestUri": "/api/v1/authn/factors/password/verify",
                "threatSuspected": "false",
                "url": "/api/v1/authn/factors/password/verify?rememberDevice=false",
            }
        },
        "displayMessage": "User login to Okta",
        "eventType": "user.session.start",
        "legacyEventType": "core.user_auth.login_success",
        "outcome": {"result": "SUCCESS"},
        "p_any_domain_names": ["comcast.net"],
        "p_any_ip_addresses": ["192.168.0.9"],
        "p_event_time": "2020-01-01 00:00:00.000000000",
        "p_log_type": "Okta.SystemLog",
        "p_parse_time": "2020-01-01 00:00:01.000000000",
        "p_row_id": "111222",
        "published": "2020-01-01 00:00:00.000000000",
        "request": {
            "ipChain": [
                {
                    "geographicalContext": {
                        "city": "Baltimore",
                        "country": "United States",
                        "geolocation": {"lat": 39.2891, "lon": -76.5583},
                        "postalCode": "21224",
                        "state": "Maryland",
                    },
                    "ip": "192.168.0.9",
                    "version": "V4",
                }
            ]
        },
        "securityContext": {
            "asNumber": 1234,
            "asOrg": "comcast",
            "domain": "comcast.net",
            "isProxy": False,
            "isp": "comcast cable communications  llc",
        },
        "severity": "INFO",
        "transaction": {"detail": {}, "id": "AbC", "type": "WEB"},
        "uuid": "1234-abc-1234",
        "version": "0",
    }
)


second_login = json.dumps(
    {
        "actor": {
            "alternateId": "buser@example.com",
            "displayName": "Bobert User",
            "id": "111",
            "type": "User",
        },
        "authenticationContext": {"authenticationStep": 0, "externalSessionId": "111"},
        "client": {
            "device": "Computer",
            "geographicalContext": {
                "city": "Bethesda",
                "country": "United States",
                "geolocation": {"lat": 38.9846, "lon": -77.0947},
                "postalCode": "20810",
                "state": "Maryland",
            },
            "ipAddress": "192.168.0.9",
            "userAgent": {
                "browser": "CHROME",
                "os": "Windows 10",
                "rawUserAgent": "Mozilla/5.0",
            },
            "zone": "null",
        },
        "debugContext": {
            "debugData": {
                "requestId": "11111",
                "requestUri": "/api/v1/authn/factors/password/verify",
                "threatSuspected": "false",
                "url": "/api/v1/authn/factors/password/verify?rememberDevice=false",
            }
        },
        "displayMessage": "User login to Okta",
        "eventType": "user.session.start",
        "legacyEventType": "core.user_auth.login_success",
        "outcome": {"result": "SUCCESS"},
        "p_any_domain_names": ["comcast.net"],
        "p_any_ip_addresses": ["192.168.0.9"],
        "p_event_time": "2020-01-02 00:00:00.000000000",
        "p_log_type": "Okta.SystemLog",
        "p_parse_time": "2020-01-02 00:00:01.000000000",
        "p_row_id": "111222",
        "published": "2020-01-02 00:00:00.000000000",
        "request": {
            "ipChain": [
                {
                    "geographicalContext": {
                        "city": "Bethesda",
                        "country": "United States",
                        "geolocation": {"lat": 38.9846, "lon": -77.0947},
                        "postalCode": "20810",
                        "state": "Maryland",
                    },
                    "ip": "192.168.0.9",
                    "version": "V4",
                }
            ]
        },
        "securityContext": {
            "asNumber": 1234,
            "asOrg": "comcast",
            "domain": "comcast.net",
            "isProxy": False,
            "isp": "comcast cable communications  llc",
        },
        "severity": "INFO",
        "transaction": {"detail": {}, "id": "AbC", "type": "WEB"},
        "uuid": "1234-abc-1234",
        "version": "0",
    }
)


third_login = json.dumps(
    {
        "actor": {
            "alternateId": "buser@example.com",
            "displayName": "Bobert User",
            "id": "111",
            "type": "User",
        },
        "authenticationContext": {"authenticationStep": 0, "externalSessionId": "111"},
        "client": {
            "device": "Computer",
            "geographicalContext": {
                "city": "Baltimore",
                "country": "United States",
                "geolocation": {"lat": 39.2891, "lon": -76.5583},
                "postalCode": "21224",
                "state": "Maryland",
            },
            "ipAddress": "192.168.0.9",
            "userAgent": {
                "browser": "CHROME",
                "os": "Windows 10",
                "rawUserAgent": "Mozilla/5.0",
            },
            "zone": "null",
        },
        "debugContext": {
            "debugData": {
                "requestId": "11111",
                "requestUri": "/api/v1/authn/factors/password/verify",
                "threatSuspected": "false",
                "url": "/api/v1/authn/factors/password/verify?rememberDevice=false",
            }
        },
        "displayMessage": "User login to Okta",
        "eventType": "user.session.start",
        "legacyEventType": "core.user_auth.login_success",
        "outcome": {"result": "SUCCESS"},
        "p_any_domain_names": ["comcast.net"],
        "p_any_ip_addresses": ["192.168.0.9"],
        "p_event_time": "2020-01-02 00:01:00.000000000",
        "p_log_type": "Okta.SystemLog",
        "p_parse_time": "2020-01-02 00:01:01.000000000",
        "p_row_id": "111222",
        "published": "2020-01-02 00:00:01.000000000",
        "request": {
            "ipChain": [
                {
                    "geographicalContext": {
                        "city": "Baltimore",
                        "country": "United States",
                        "geolocation": {"lat": 39.2891, "lon": -76.5583},
                        "postalCode": "21224",
                        "state": "Maryland",
                    },
                    "ip": "192.168.0.9",
                    "version": "V4",
                }
            ]
        },
        "securityContext": {
            "asNumber": 1234,
            "asOrg": "comcast",
            "domain": "comcast.net",
            "isProxy": False,
            "isp": "comcast cable communications  llc",
        },
        "severity": "INFO",
        "transaction": {"detail": {}, "id": "AbC", "type": "WEB"},
        "uuid": "1234-abc-1234",
        "version": "0",
    }
)


support_password_reset = json.dumps(
    {
        "uuid": "12343",
        "published": "2021-11-29 18:56:40.014",
        "eventType": "user.account.reset_password",
        "version": "0",
        "severity": "INFO",
        "legacyEventType": "core.user.config.user_status.password_reset",
        "displayMessage": "Fired when the user's Okta password is reset",
        "actor": {
            "alternateId": "system@okta.com",
            "displayName": "system@okta.com",
            "id": "1111111",
            "type": "User",
        },
        "client": {
            "device": "Computer",
            "ipAddress": "1.1.1.1",
            "userAgent": {
                "browser": "CHROME",
                "os": "Mac OS X",
            },
            "zone": "null",
        },
        "outcome": {"result": "SUCCESS"},
        "target": [
            {
                "alternateId": "homer@springfield.gov",
                "displayName": "Homer Simpson",
                "id": "1111111",
                "type": "User",
            }
        ],
        "transaction": {"detail": {}, "id": "unknown", "type": "WEB"},
        "p_log_type": "Okta.SystemLog",
    }
)


admin_password_reset = json.dumps(
    {
        "uuid": "2aaaaaaaaaabbbbbbbbbbbbddddddddddd",
        "eventType": "user.account.reset_password",
        "version": "0",
        "severity": "INFO",
        "legacyEventType": "core.user.config.user_status.password_reset",
        "displayMessage": "Fired when the user's Okta password is reset",
        "actor": {
            "alternateId": "marge@springfield.gov",
            "displayName": "Marge Simpson",
            "id": "1111",
            "type": "User",
        },
        "client": {
            "device": "Computer",
            "geographicalContext": {
                "city": "Springfield",
                "country": "United States",
                "postalCode": "80014",
                "state": "Debated",
            },
            "ipAddress": "1.1.1.1",
            "userAgent": {
                "browser": "CHROME",
                "os": "Mac OS X",
                "rawUserAgent": "Mozilla/5.0",
            },
            "zone": "null",
        },
        "outcome": {"result": "SUCCESS"},
        "target": [
            {
                "alternateId": "homer@springfield.gov",
                "displayName": "Homer Simpson",
                "id": "1.1.1.1",
                "type": "User",
            }
        ],
        "transaction": {"detail": {}, "id": "1111", "type": "WEB"},
        "p_log_type": "Okta.SystemLog",
    }
)
