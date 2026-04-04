#!/usr/bin/env python3
"""Cross-system bus factor / knowledge concentration analysis."""

import json
import os
from collections import defaultdict

def main():
    os.makedirs('inventory/cross_system', exist_ok=True)

    review_net = {}
    try:
        review_net = json.load(open('inventory/bitbucket/review_network.json'))
    except Exception as e:
        print(f"Review network: {e}")

    reviewer_conc = {}
    try:
        reviewer_conc = json.load(open('inventory/bitbucket/reviewer_concentration.json'))
    except Exception as e:
        print(f"Reviewer concentration: {e}")

    assignee_data = {}
    try:
        assignee_data = json.load(open('inventory/jira/assignee_concentration.json'))
    except Exception as e:
        print(f"Assignee concentration: {e}")

    user_map = {}
    try:
        user_map = json.load(open('inventory/users/unified_user_map.json'))
    except Exception as e:
        print(f"User map: {e}")

    heavy_reviewers = []
    nodes = review_net.get('nodes', [])
    for node in nodes:
        if node.get('reviews_given', 0) > 100:
            heavy_reviewers.append({
                'name': node['name'],
                'reviews_given': node['reviews_given'],
                'reviews_received': node.get('reviews_received', 0),
                'prs_authored': node.get('prs_authored', 0),
                'repos': node.get('repos', []),
            })
    heavy_reviewers.sort(key=lambda x: -x['reviews_given'])

    reviewer_bottleneck_repos = []
    per_repo = reviewer_conc.get('per_repo', [])
    for repo in per_repo:
        top_revs = repo.get('top_reviewers', [])
        if top_revs and top_revs[0].get('pct', 0) > 50:
            reviewer_bottleneck_repos.append({
                'repo': f"{repo.get('workspace','')}/{repo.get('repo','')}",
                'top_reviewer': top_revs[0].get('name', ''),
                'pct': top_revs[0].get('pct', 0),
                'total_prs': repo.get('total_prs', 0),
            })

    overloaded_assignees = []
    assignees = assignee_data.get('assignees', assignee_data.get('top_assignees', []))
    if isinstance(assignees, list):
        for a in assignees:
            total = a.get('total', a.get('open_issues', 0))
            if total > 50:
                overloaded_assignees.append({
                    'name': a.get('name', a.get('assignee', '')),
                    'open_issues': total,
                })

    reviewer_names = {r['name'].lower() for r in heavy_reviewers}
    assignee_names = {a['name'].lower() for a in overloaded_assignees}
    overlap = reviewer_names & assignee_names

    key_person_risks = []
    for name in overlap:
        reviewer = next((r for r in heavy_reviewers if r['name'].lower() == name), {})
        assignee = next((a for a in overloaded_assignees if a['name'].lower() == name), {})
        key_person_risks.append({
            'name': reviewer.get('name', assignee.get('name', name)),
            'reviews_given': reviewer.get('reviews_given', 0),
            'open_issues': assignee.get('open_issues', 0),
            'risk_factors': ['heavy_reviewer', 'overloaded_assignee'],
            'risk_score': reviewer.get('reviews_given', 0) + assignee.get('open_issues', 0) * 3,
        })
    key_person_risks.sort(key=lambda x: -x['risk_score'])

    output = {
        'heavy_reviewers_100plus': heavy_reviewers,
        'reviewer_bottleneck_repos': reviewer_bottleneck_repos,
        'overloaded_assignees_50plus': overloaded_assignees,
        'key_person_risks': key_person_risks,
        'summary': {
            'heavy_reviewers': len(heavy_reviewers),
            'bottleneck_repos': len(reviewer_bottleneck_repos),
            'overloaded_assignees': len(overloaded_assignees),
            'dual_risk_individuals': len(key_person_risks),
        }
    }

    with open('inventory/cross_system/bus_factor.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Heavy reviewers (>100): {len(heavy_reviewers)}")
    print(f"Bottleneck repos (>50% single reviewer): {len(reviewer_bottleneck_repos)}")
    print(f"Overloaded assignees (>50 issues): {len(overloaded_assignees)}")
    print(f"Dual-risk individuals: {len(key_person_risks)}")
    if key_person_risks:
        print(f"Top risk: {key_person_risks[0]['name']} (score {key_person_risks[0]['risk_score']})")
    print("Done.")

if __name__ == '__main__':
    main()
