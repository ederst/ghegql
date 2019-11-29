import github3
import argparse

parser = argparse.ArgumentParser(description="Do some GraphQL.")
parser.add_argument("url", help="URL of a GitHub Enterprise instance")
parser.add_argument("-q", "--query", help="GraphQL query, use @ for referencing a file")
parser.add_argument("-t", "--token", help="Login token, use @ for referencing a file")
args = parser.parse_args()

github_base_url = args.url
github_api_base_url = f"{github_base_url}/api"

if args.token[0] == "@":
    with open(args.token[1:], mode="r") as file:
        github_login_token = file.read().replace("\n", "")
else:
    github_login_token = args.token

if args.query[0] == "@":
    with open(args.query[1:], mode="r") as file:
        graphql_query = file.read()
else:
    graphql_query = args.query

github_session = github3.session.GitHubSession(default_read_timeout=300)
github_connection = github3.GitHubEnterprise(github_base_url, session=github_session, verify=True)
github_connection.login(token=github_login_token)

github_graphql_url = github_connection.session.build_url("graphql", base_url=github_api_base_url)

response = github_connection.session.post(github_graphql_url, json={"query": graphql_query})

# print and make compatible with jq
print(str(response.json()).replace("'", "\""))
