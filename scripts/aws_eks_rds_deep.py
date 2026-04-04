#!/usr/bin/env python3
"""Deep dive on EKS clusters, RDS instances, and ElastiCache clusters across AWS accounts."""

import boto3
import json
import os
from collections import defaultdict
from botocore.exceptions import ClientError


def safe_call(fn, default=None):
    try:
        return fn()
    except (ClientError, Exception) as e:
        code = getattr(e, 'response', {}).get('Error', {}).get('Code', '')
        if code in ('AccessDeniedException', 'AccessDenied', 'UnauthorizedAccess',
                     'AuthorizationError', 'OptInRequired', 'SubscriptionRequiredException'):
            return {"_error": f"Access denied: {code}"}
        if default is not None:
            return default
        return {"_error": str(e)}


PROFILES = [
    'mm-retail-prod-us', 'mm-payments-prod-us', 'mm-cake-development',
    'mm-cake-r-and-d', 'mm-shared-services', 'mm-retail-prod-eu',
    'mm-retail-prod-apac', 'mm-retail-prod-us-dr',
]
REGIONS = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']

access_errors = []


def collect_eks(profile, region):
    session = boto3.Session(profile_name=profile)
    eks = session.client('eks', region_name=region)

    cluster_names = safe_call(lambda: eks.list_clusters()['clusters'], [])
    if isinstance(cluster_names, dict) and '_error' in cluster_names:
        if 'Access denied' in cluster_names.get('_error', ''):
            access_errors.append(f"EKS/{profile}/{region}: {cluster_names['_error']}")
        return []

    results = []
    for name in cluster_names:
        detail = safe_call(lambda n=name: eks.describe_cluster(name=n)['cluster'])
        if isinstance(detail, dict) and '_error' in detail:
            results.append({'name': name, '_error': detail['_error'], 'profile': profile, 'region': region})
            continue

        nodegroups = safe_call(lambda n=name: eks.list_nodegroups(clusterName=n)['nodegroups'], [])
        ng_details = []
        if isinstance(nodegroups, list):
            for ng in nodegroups:
                ngd = safe_call(lambda n=name, g=ng: eks.describe_nodegroup(clusterName=n, nodegroupName=g)['nodegroup'])
                if isinstance(ngd, dict) and '_error' not in ngd:
                    scaling = ngd.get('scalingConfig', {})
                    ng_details.append({
                        'name': ngd.get('nodegroupName', ng),
                        'instance_types': ngd.get('instanceTypes', []),
                        'desired_size': scaling.get('desiredSize'),
                        'min_size': scaling.get('minSize'),
                        'max_size': scaling.get('maxSize'),
                        'ami_type': ngd.get('amiType', ''),
                        'capacity_type': ngd.get('capacityType', ''),
                        'status': ngd.get('status', ''),
                    })

        addons = safe_call(lambda n=name: eks.list_addons(clusterName=n)['addons'], [])
        addon_details = []
        if isinstance(addons, list):
            for addon_name in addons:
                ad = safe_call(lambda n=name, a=addon_name: eks.describe_addon(clusterName=n, addonName=a)['addon'])
                if isinstance(ad, dict) and '_error' not in ad:
                    addon_details.append({
                        'name': ad.get('addonName', addon_name),
                        'version': ad.get('addonVersion', ''),
                        'status': ad.get('status', ''),
                    })

        logging_cfg = detail.get('logging', {})
        enabled_log_types = []
        for lc in logging_cfg.get('clusterLogging', []):
            if lc.get('enabled'):
                enabled_log_types.extend(lc.get('types', []))

        vpc_cfg = detail.get('resourcesVpcConfig', {})

        results.append({
            'name': name,
            'profile': profile,
            'region': region,
            'k8s_version': detail.get('version', ''),
            'platform_version': detail.get('platformVersion', ''),
            'status': detail.get('status', ''),
            'endpoint_public': vpc_cfg.get('endpointPublicAccess', None),
            'endpoint_private': vpc_cfg.get('endpointPrivateAccess', None),
            'enabled_log_types': enabled_log_types,
            'node_groups': ng_details,
            'addons': addon_details,
            'created_at': detail.get('createdAt', ''),
        })
    return results


def collect_rds(profile, region):
    session = boto3.Session(profile_name=profile)
    rds = session.client('rds', region_name=region)

    instances = safe_call(lambda: rds.describe_db_instances()['DBInstances'], [])
    if isinstance(instances, dict) and '_error' in instances:
        if 'Access denied' in instances.get('_error', ''):
            access_errors.append(f"RDS/{profile}/{region}: {instances['_error']}")
        return []

    results = []
    for db in instances:
        param_groups = [pg['DBParameterGroupName'] for pg in db.get('DBParameterGroups', [])]
        option_groups = [og['OptionGroupName'] for og in db.get('OptionGroupMemberships', [])]

        results.append({
            'db_identifier': db.get('DBInstanceIdentifier', ''),
            'profile': profile,
            'region': region,
            'engine': db.get('Engine', ''),
            'engine_version': db.get('EngineVersion', ''),
            'instance_class': db.get('DBInstanceClass', ''),
            'storage_type': db.get('StorageType', ''),
            'allocated_storage_gb': db.get('AllocatedStorage', 0),
            'multi_az': db.get('MultiAZ', False),
            'storage_encrypted': db.get('StorageEncrypted', False),
            'backup_retention_days': db.get('BackupRetentionPeriod', 0),
            'parameter_groups': param_groups,
            'option_groups': option_groups,
            'performance_insights_enabled': db.get('PerformanceInsightsEnabled', False),
            'read_replica_source': db.get('ReadReplicaSourceDBInstanceIdentifier', ''),
            'publicly_accessible': db.get('PubliclyAccessible', False),
            'status': db.get('DBInstanceStatus', ''),
            'endpoint': db.get('Endpoint', {}).get('Address', ''),
        })
    return results


def collect_elasticache(profile, region):
    session = boto3.Session(profile_name=profile)
    ec = session.client('elasticache', region_name=region)

    clusters = safe_call(lambda: ec.describe_cache_clusters(ShowCacheNodeInfo=True)['CacheClusters'], [])
    if isinstance(clusters, dict) and '_error' in clusters:
        if 'Access denied' in clusters.get('_error', ''):
            access_errors.append(f"ElastiCache/{profile}/{region}: {clusters['_error']}")
        return []

    repl_groups_raw = safe_call(lambda: ec.describe_replication_groups()['ReplicationGroups'], [])
    repl_map = {}
    if isinstance(repl_groups_raw, list):
        for rg in repl_groups_raw:
            repl_map[rg.get('ReplicationGroupId', '')] = {
                'description': rg.get('Description', ''),
                'status': rg.get('Status', ''),
                'cluster_enabled': rg.get('ClusterEnabled', False),
                'num_node_groups': len(rg.get('NodeGroups', [])),
                'at_rest_encryption': rg.get('AtRestEncryptionEnabled', False),
                'transit_encryption': rg.get('TransitEncryptionEnabled', False),
                'automatic_failover': rg.get('AutomaticFailover', ''),
            }

    results = []
    for c in clusters:
        repl_id = c.get('ReplicationGroupId', '')
        results.append({
            'cluster_id': c.get('CacheClusterId', ''),
            'profile': profile,
            'region': region,
            'engine': c.get('Engine', ''),
            'engine_version': c.get('EngineVersion', ''),
            'node_type': c.get('CacheNodeType', ''),
            'num_cache_nodes': c.get('NumCacheNodes', 0),
            'status': c.get('CacheClusterStatus', ''),
            'replication_group_id': repl_id,
            'replication_group': repl_map.get(repl_id, {}),
            'parameter_group': c.get('CacheParameterGroup', {}).get('CacheParameterGroupName', ''),
            'at_rest_encryption': c.get('AtRestEncryptionEnabled', False),
            'transit_encryption': c.get('TransitEncryptionEnabled', False),
        })
    return results


if __name__ == '__main__':
    os.makedirs('inventory/aws', exist_ok=True)

    all_eks = []
    all_rds = []
    all_elasticache = []

    for profile in PROFILES:
        for region in REGIONS:
            tag = f"{profile}/{region}"

            print(f"[EKS] {tag} ...", flush=True)
            eks_results = collect_eks(profile, region)
            if eks_results:
                print(f"       -> {len(eks_results)} cluster(s)", flush=True)
            all_eks.extend(eks_results)

            print(f"[RDS] {tag} ...", flush=True)
            rds_results = collect_rds(profile, region)
            if rds_results:
                print(f"       -> {len(rds_results)} instance(s)", flush=True)
            all_rds.extend(rds_results)

            print(f"[ElastiCache] {tag} ...", flush=True)
            ec_results = collect_elasticache(profile, region)
            if ec_results:
                print(f"       -> {len(ec_results)} cluster(s)", flush=True)
            all_elasticache.extend(ec_results)

    with open('inventory/aws/eks_clusters.json', 'w') as f:
        json.dump(all_eks, f, indent=2, default=str)
    with open('inventory/aws/rds_instances.json', 'w') as f:
        json.dump(all_rds, f, indent=2, default=str)
    with open('inventory/aws/elasticache_clusters.json', 'w') as f:
        json.dump(all_elasticache, f, indent=2, default=str)

    print("\n" + "=" * 60, flush=True)
    print(f"EKS clusters:       {len(all_eks)}", flush=True)
    eks_versions = defaultdict(int)
    for c in all_eks:
        v = c.get('k8s_version', 'unknown')
        eks_versions[v] += 1
    for v, cnt in sorted(eks_versions.items()):
        print(f"  k8s {v}: {cnt}", flush=True)

    print(f"\nRDS instances:       {len(all_rds)}", flush=True)
    engine_counts = defaultdict(int)
    for db in all_rds:
        engine_counts[db.get('engine', 'unknown')] += 1
    for eng, cnt in sorted(engine_counts.items(), key=lambda x: -x[1]):
        print(f"  {eng}: {cnt}", flush=True)

    print(f"\nElastiCache clusters: {len(all_elasticache)}", flush=True)
    ec_engines = defaultdict(int)
    for c in all_elasticache:
        ec_engines[c.get('engine', 'unknown')] += 1
    for eng, cnt in sorted(ec_engines.items(), key=lambda x: -x[1]):
        print(f"  {eng}: {cnt}", flush=True)

    if access_errors:
        print(f"\nAccess errors ({len(access_errors)}):", flush=True)
        for e in access_errors:
            print(f"  {e}", flush=True)
    else:
        print("\nNo access errors.", flush=True)

    print("\nDone. Files written:", flush=True)
    print("  inventory/aws/eks_clusters.json", flush=True)
    print("  inventory/aws/rds_instances.json", flush=True)
    print("  inventory/aws/elasticache_clusters.json", flush=True)
