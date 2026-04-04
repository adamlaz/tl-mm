#!/usr/bin/env python3
"""Bitbucket dependency/package analysis for top active repos."""

import requests
import json
import os
import time

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)

DEP_FILES = ['package.json', 'pom.xml', 'build.gradle', 'requirements.txt', 'go.mod', 'Gemfile']

NOTABLE_DEPS = {
    'react': 'React', 'next': 'Next.js', 'express': 'Express', 'typescript': 'TypeScript',
    'vue': 'Vue', 'angular': 'Angular', '@angular/core': 'Angular', 'jest': 'Jest',
    'mocha': 'Mocha', 'webpack': 'Webpack', 'vite': 'Vite', 'nestjs': 'NestJS',
    '@nestjs/core': 'NestJS', 'fastify': 'Fastify', 'aws-sdk': 'AWS SDK v2',
    '@aws-sdk/client-s3': 'AWS SDK v3', 'mongoose': 'Mongoose', 'sequelize': 'Sequelize',
    'prisma': 'Prisma', '@prisma/client': 'Prisma', 'typeorm': 'TypeORM',
}

def fetch_file(workspace, repo, filename):
    url = f"{BB_API}/repositories/{workspace}/{repo}/src/HEAD/{filename}"
    resp = requests.get(url, auth=AUTH)
    if resp.status_code == 404:
        return None
    if resp.status_code == 429:
        time.sleep(5)
        resp = requests.get(url, auth=AUTH)
    if resp.status_code != 200:
        return None
    return resp.text

def analyze_package_json(content):
    try:
        pkg = json.loads(content)
    except Exception:
        return None
    deps = pkg.get('dependencies', {})
    dev_deps = pkg.get('devDependencies', {})
    notable = {}
    for dep_name, version in {**deps, **dev_deps}.items():
        if dep_name in NOTABLE_DEPS:
            notable[NOTABLE_DEPS[dep_name]] = version
    return {
        'type': 'nodejs',
        'name': pkg.get('name', ''),
        'version': pkg.get('version', ''),
        'dependency_count': len(deps),
        'dev_dependency_count': len(dev_deps),
        'total_deps': len(deps) + len(dev_deps),
        'notable_frameworks': notable,
        'has_typescript': 'typescript' in dev_deps or 'typescript' in deps,
        'node_engine': pkg.get('engines', {}).get('node', ''),
    }

def analyze_requirements_txt(content):
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith('#')]
    packages = {}
    for line in lines:
        for sep in ['==', '>=', '<=', '~=', '!=']:
            if sep in line:
                name, ver = line.split(sep, 1)
                packages[name.strip()] = ver.strip()
                break
        else:
            packages[line] = ''
    return {'type': 'python', 'package_count': len(packages), 'packages': dict(list(packages.items())[:20])}

def analyze_pom_xml(content):
    import re
    java_ver = re.search(r'<java.version>(\d+)</java.version>', content)
    spring_ver = re.search(r'<spring-boot.version>([^<]+)</spring-boot.version>', content)
    group_id = re.search(r'<groupId>([^<]+)</groupId>', content)
    artifact_id = re.search(r'<artifactId>([^<]+)</artifactId>', content)
    deps = re.findall(r'<dependency>', content)
    return {
        'type': 'java_maven',
        'group_id': group_id.group(1) if group_id else '',
        'artifact_id': artifact_id.group(1) if artifact_id else '',
        'java_version': java_ver.group(1) if java_ver else '',
        'spring_boot_version': spring_ver.group(1) if spring_ver else '',
        'dependency_count': len(deps),
    }

def main():
    os.makedirs('inventory/bitbucket', exist_ok=True)
    metrics = json.load(open('inventory/bitbucket/metrics.json'))
    repos = [(m.get('workspace', m.get('_workspace', '')), m.get('repo', m.get('slug', ''))) for m in metrics[:30]]

    results = []
    stack_counts = {'nodejs': 0, 'python': 0, 'java_maven': 0, 'java_gradle': 0, 'go': 0, 'ruby': 0, 'unknown': 0}
    framework_counts = {}

    for i, (ws, repo) in enumerate(repos):
        print(f"[{i+1}/{len(repos)}] {ws}/{repo}...", flush=True)
        entry = {'workspace': ws, 'repo': repo, 'dep_files': {}}

        for filename in DEP_FILES:
            content = fetch_file(ws, repo, filename)
            time.sleep(0.3)
            if content is None:
                continue

            if filename == 'package.json':
                analysis = analyze_package_json(content)
                if analysis:
                    entry['dep_files']['package.json'] = analysis
                    stack_counts['nodejs'] += 1
                    for fw, ver in analysis.get('notable_frameworks', {}).items():
                        framework_counts[fw] = framework_counts.get(fw, 0) + 1
            elif filename == 'requirements.txt':
                analysis = analyze_requirements_txt(content)
                if analysis:
                    entry['dep_files']['requirements.txt'] = analysis
                    stack_counts['python'] += 1
            elif filename == 'pom.xml':
                analysis = analyze_pom_xml(content)
                if analysis:
                    entry['dep_files']['pom.xml'] = analysis
                    stack_counts['java_maven'] += 1
            elif filename == 'build.gradle':
                entry['dep_files']['build.gradle'] = {'type': 'java_gradle', 'found': True}
                stack_counts['java_gradle'] += 1
            elif filename == 'go.mod':
                entry['dep_files']['go.mod'] = {'type': 'go', 'found': True}
                stack_counts['go'] += 1
            elif filename == 'Gemfile':
                entry['dep_files']['Gemfile'] = {'type': 'ruby', 'found': True}
                stack_counts['ruby'] += 1

        if not entry['dep_files']:
            stack_counts['unknown'] += 1

        results.append(entry)

    output = {
        'repos_analyzed': len(results),
        'stack_distribution': stack_counts,
        'framework_frequency': dict(sorted(framework_counts.items(), key=lambda x: -x[1])),
        'per_repo': results,
    }

    with open('inventory/bitbucket/dependency_analysis.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nStack distribution: {stack_counts}")
    print(f"Framework frequency: {framework_counts}")
    print("Done.")

if __name__ == '__main__':
    main()
