#!/usr/bin/env python3
"""ECS task definition analysis -- microservice architecture mapping."""

import boto3
import json
import os
from botocore.exceptions import ClientError

def safe_call(fn, default=None):
    try:
        return fn()
    except (ClientError, Exception) as e:
        code = getattr(e, 'response', {}).get('Error', {}).get('Code', '')
        if code in ('AccessDeniedException', 'AccessDenied', 'UnauthorizedAccess', 'AuthorizationError'):
            return {"_error": f"Access denied: {code}"}
        if default is not None:
            return default
        return {"_error": str(e)}

def main():
    os.makedirs('inventory/aws', exist_ok=True)
    ecs_data = json.load(open('inventory/aws/ecs_services.json'))

    results = []
    errors = []
    no_health_check = 0
    total_containers = 0

    for cluster_key, cluster_info in ecs_data.items():
        if not isinstance(cluster_info, dict) or 'error' in cluster_info:
            continue
        profile = cluster_info.get('profile', '')
        region = cluster_info.get('region', 'us-east-1')
        cluster = cluster_info.get('cluster', '')
        services = cluster_info.get('services', [])

        active_services = [s for s in services if s.get('running', 0) > 0 or s.get('desired', 0) > 0]
        if not active_services:
            continue

        try:
            session = boto3.Session(profile_name=profile)
            ecs = session.client('ecs', region_name=region)
        except Exception as e:
            errors.append(f"Session {profile}/{region}: {e}")
            continue

        for svc in active_services:
            svc_name = svc.get('name', '')
            print(f"  {profile}/{cluster}/{svc_name}...", flush=True)

            svc_detail = safe_call(lambda: ecs.describe_services(
                cluster=cluster, services=[svc_name]
            ).get('services', [{}])[0], {})

            if isinstance(svc_detail, dict) and '_error' in svc_detail:
                errors.append(f"DescribeServices {profile}/{cluster}/{svc_name}: {svc_detail['_error']}")
                continue

            td_arn = svc_detail.get('taskDefinition', '') if isinstance(svc_detail, dict) else ''
            if not td_arn:
                continue

            td = safe_call(lambda: ecs.describe_task_definition(
                taskDefinition=td_arn
            ).get('taskDefinition', {}), {})

            if isinstance(td, dict) and '_error' in td:
                errors.append(f"DescribeTaskDef {td_arn}: {td['_error']}")
                continue

            containers = []
            for cd in td.get('containerDefinitions', []):
                has_health = cd.get('healthCheck') is not None
                if not has_health:
                    no_health_check += 1
                total_containers += 1
                containers.append({
                    'name': cd.get('name', ''),
                    'image': cd.get('image', ''),
                    'cpu': cd.get('cpu', 0),
                    'memory': cd.get('memory', 0),
                    'memory_reservation': cd.get('memoryReservation', 0),
                    'essential': cd.get('essential', True),
                    'port_mappings': len(cd.get('portMappings', [])),
                    'has_health_check': has_health,
                    'env_var_count': len(cd.get('environment', [])),
                    'secrets_count': len(cd.get('secrets', [])),
                    'log_driver': cd.get('logConfiguration', {}).get('logDriver', 'none'),
                })

            results.append({
                'profile': profile,
                'region': region,
                'cluster': cluster,
                'service': svc_name,
                'task_definition': td_arn.split('/')[-1] if td_arn else '',
                'launch_type': svc_detail.get('launchType', 'unknown') if isinstance(svc_detail, dict) else 'unknown',
                'desired_count': svc.get('desired', 0),
                'running_count': svc.get('running', 0),
                'container_count': len(containers),
                'containers': containers,
            })

    images = set()
    for r in results:
        for c in r.get('containers', []):
            img = c.get('image', '')
            if img:
                images.add(img.split(':')[0])

    output = {
        'total_services_analyzed': len(results),
        'total_containers': total_containers,
        'containers_without_health_check': no_health_check,
        'unique_images': len(images),
        'errors': errors,
        'services': results,
    }

    with open('inventory/aws/ecs_task_definitions.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nServices analyzed: {len(results)}")
    print(f"Total containers: {total_containers}")
    print(f"Without health check: {no_health_check}")
    print(f"Unique images: {len(images)}")
    print(f"Errors: {len(errors)}")
    print("Done.")

if __name__ == '__main__':
    main()
