import re

import boto3

from collectors import PersonRecord

PROFILES_WITH_HUMAN_USERS = [
    "mm-cake-development",
    "mm-retail-prod-us",
    "mm-retail-prod-eu",
    "mm-retail-prod-apac",
    "mm-customer-analytics",
    "mm-mm-archive",
    "mm-security",
]

SERVICE_KEYWORDS = re.compile(
    r"(?i)(pipeline|bitbucket|deploy|monitoring|api[-_]?service|"
    r"service[-_]?account|lambda|ecr|analytics[-_]?svc|s3|prometheus|"
    r"gitlab|doc[-_]?gen|terraform|ci-|cd-|bot|automation|system)",
)


def _humanize_username(username: str) -> str:
    name = re.sub(r"[-_.]", " ", username)
    return name.title()


def _is_service_account(username: str) -> bool:
    return bool(SERVICE_KEYWORDS.search(username))


def _list_iam_users(profile: str) -> list[dict]:
    session = boto3.Session(profile_name=profile)
    iam = session.client("iam")
    users = []
    paginator = iam.get_paginator("list_users")
    for page in paginator.paginate():
        for user in page["Users"]:
            users.append({
                "username": user["UserName"],
                "created_date": user["CreateDate"].isoformat(),
                "arn": user["Arn"],
            })
    return users


def collect() -> list[PersonRecord]:
    records = []
    seen = set()

    for profile in PROFILES_WITH_HUMAN_USERS:
        try:
            users = _list_iam_users(profile)
            print(f"  {profile}: {len(users)} IAM users found")
        except Exception as e:
            print(f"  {profile}: FAILED - {e}")
            continue

        for user in users:
            username = user["username"]
            is_svc = _is_service_account(username)

            if is_svc:
                continue

            dedup_key = (username, profile)
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            records.append(PersonRecord(
                source="aws_iam",
                canonical_name=_humanize_username(username),
                account_id=username,
                metadata={
                    "aws_profile": profile,
                    "created_date": user["created_date"],
                    "is_service_account": False,
                },
            ))

    print(f"Collected {len(records)} AWS IAM person records (human accounts)")
    return records


if __name__ == "__main__":
    collect()
