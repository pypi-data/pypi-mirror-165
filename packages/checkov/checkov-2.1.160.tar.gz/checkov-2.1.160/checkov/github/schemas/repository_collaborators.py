from checkov.common.vcs.vcs_schema import VCSSchema


class RepositoryCollaboratorsSchema(VCSSchema):
    def __init__(self):
        schema = {
            "type": "array",
            "items": {
                "title": "Collaborator",
                "description": "Collaborator",
                "type": "object",
                "properties": {
                    "login": {
                        "type": "string",
                        "examples": [
                            "octocat"
                        ]
                    },
                    "id": {
                        "type": "integer",
                        "examples": [
                            1
                        ]
                    },
                    "email": {
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "name": {
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "node_id": {
                        "type": "string",
                        "examples": [
                            "MDQ6VXNlcjE="
                        ]
                    },
                    "avatar_url": {
                        "type": "string",
                        "format": "uri",
                        "examples": [
                            "https://github.com/images/error/octocat_happy.gif"
                        ]
                    },
                    "gravatar_id": {
                        "type": [
                            "string",
                            "null"
                        ],
                        "examples": [
                            "41d064eb2195891e12d0413f63227ea7"
                        ]
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": [
                            "https://api.github.com/users/octocat"
                        ]
                    },
                    "html_url": {
                        "type": "string",
                        "format": "uri",
                        "examples": [
                            "https://github.com/octocat"
                        ]
                    },
                    "followers_url": {
                        "type": "string",
                        "format": "uri",
                        "examples": [
                            "https://api.github.com/users/octocat/followers"
                        ]
                    },
                    "following_url": {
                        "type": "string",
                        "examples": [
                            "https://api.github.com/users/octocat/following{/other_user}"
                        ]
                    },
                    "gists_url": {
                        "type": "string",
                        "examples": [
                            "https://api.github.com/users/octocat/gists{/gist_id}"
                        ]
                    },
                    "starred_url": {
                        "type": "string",
                        "examples": [
                            "https://api.github.com/users/octocat/starred{/owner}{/repo}"
                        ]
                    },
                    "subscriptions_url": {
                        "type": "string",
                        "format": "uri",
                        "examples": [
                            "https://api.github.com/users/octocat/subscriptions"
                        ]
                    },
                    "organizations_url": {
                        "type": "string",
                        "format": "uri",
                        "examples": [
                            "https://api.github.com/users/octocat/orgs"
                        ]
                    },
                    "repos_url": {
                        "type": "string",
                        "format": "uri",
                        "examples": [
                            "https://api.github.com/users/octocat/repos"
                        ]
                    },
                    "events_url": {
                        "type": "string",
                        "examples": [
                            "https://api.github.com/users/octocat/events{/privacy}"
                        ]
                    },
                    "received_events_url": {
                        "type": "string",
                        "format": "uri",
                        "examples": [
                            "https://api.github.com/users/octocat/received_events"
                        ]
                    },
                    "type": {
                        "type": "string",
                        "examples": [
                            "User"
                        ]
                    },
                    "site_admin": {
                        "type": "boolean"
                    },
                    "permissions": {
                        "type": "object",
                        "properties": {
                            "pull": {
                                "type": "boolean"
                            },
                            "triage": {
                                "type": "boolean"
                            },
                            "push": {
                                "type": "boolean"
                            },
                            "maintain": {
                                "type": "boolean"
                            },
                            "admin": {
                                "type": "boolean"
                            }
                        },
                        "required": [
                            "pull",
                            "push",
                            "admin"
                        ]
                    },
                    "role_name": {
                        "type": "string",
                        "examples": [
                            "admin"
                        ]
                    }
                },
                "required": [
                    "avatar_url",
                    "events_url",
                    "followers_url",
                    "following_url",
                    "gists_url",
                    "gravatar_id",
                    "html_url",
                    "id",
                    "node_id",
                    "login",
                    "organizations_url",
                    "received_events_url",
                    "repos_url",
                    "site_admin",
                    "starred_url",
                    "subscriptions_url",
                    "type",
                    "url",
                    "role_name"
                ]
            }
        }
        super().__init__(schema=schema)


schema = RepositoryCollaboratorsSchema()
