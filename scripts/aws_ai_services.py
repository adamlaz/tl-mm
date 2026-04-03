#!/usr/bin/env python3
"""AWS AI service usage detail -- SageMaker, Bedrock, AI-related Lambda/S3."""

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
        return {"_error": str(e)} if default is None else default


def check_sagemaker(profile, region='us-east-1'):
    session = boto3.Session(profile_name=profile)
    sm = session.client('sagemaker', region_name=region)

    notebooks = safe_call(lambda: [{
        'name': nb['NotebookInstanceName'],
        'status': nb['NotebookInstanceStatus'],
        'instance_type': nb['InstanceType'],
        'created': nb['CreationTime'].isoformat(),
    } for nb in sm.list_notebook_instances()['NotebookInstances']], [])

    endpoints = safe_call(lambda: [{
        'name': ep['EndpointName'],
        'status': ep['EndpointStatus'],
        'created': ep['CreationTime'].isoformat(),
    } for ep in sm.list_endpoints()['Endpoints']], [])

    domains = safe_call(lambda: [{
        'id': d['DomainId'],
        'name': d['DomainName'],
        'status': d['Status'],
    } for d in sm.list_domains()['Domains']], [])

    return {'notebooks': notebooks, 'endpoints': endpoints, 'domains': domains}


def check_bedrock(profile, region='us-east-1'):
    session = boto3.Session(profile_name=profile)
    try:
        br = session.client('bedrock', region_name=region)
        models = safe_call(lambda: [{
            'id': m['modelId'],
            'provider': m.get('providerName', ''),
        } for m in br.list_foundation_models().get('modelSummaries', [])[:10]], [])

        br_rt = session.client('bedrock-runtime', region_name=region)
        return {'available_models_sample': models, 'bedrock_accessible': True}
    except Exception as e:
        return {'bedrock_accessible': False, '_error': str(e)}


def get_ai_lambda_details(profile, region='us-east-1'):
    session = boto3.Session(profile_name=profile)
    lam = session.client('lambda', region_name=region)
    ai_keywords = ['ai', 'ml', 'sagemaker', 'bedrock', 'model', 'predict', 'detoxify', 'agent']
    all_fns = safe_call(lambda: lam.list_functions()['Functions'], [])
    if isinstance(all_fns, dict) and '_error' in all_fns:
        return all_fns
    ai_fns = []
    for fn in all_fns:
        name = fn['FunctionName'].lower()
        if any(kw in name for kw in ai_keywords):
            ai_fns.append({
                'name': fn['FunctionName'],
                'runtime': fn.get('Runtime', 'N/A'),
                'description': fn.get('Description', ''),
                'memory': fn.get('MemorySize', 0),
                'last_modified': fn.get('LastModified', ''),
            })
    return ai_fns


if __name__ == '__main__':
    os.makedirs('inventory/aws', exist_ok=True)
    result = {}

    profiles_to_check = ['mm-cake-development', 'mm-cake-r-and-d', 'mm-madmobile-mgmt']

    for profile in profiles_to_check:
        print(f"=== {profile} ===", flush=True)
        result[profile] = {}

        print(f"  SageMaker...", flush=True)
        result[profile]['sagemaker'] = check_sagemaker(profile)

        print(f"  Bedrock...", flush=True)
        result[profile]['bedrock'] = check_bedrock(profile)

        print(f"  AI-related Lambdas...", flush=True)
        result[profile]['ai_lambdas'] = get_ai_lambda_details(profile)

    # Catalog AI-related S3 buckets from existing inventory
    resources = json.load(open('inventory/aws/resources_flat.json'))
    ai_buckets = [r for r in resources if r['type'] == 'S3' and
                  any(kw in r['name'].lower() for kw in ['sagemaker', 'ai', 'ml', 'model', 'bedrock', 'neo'])]
    result['ai_s3_buckets'] = [{'profile': b['profile'], 'name': b['name']} for b in ai_buckets]
    print(f"\n  AI-related S3 buckets: {len(ai_buckets)}", flush=True)

    with open('inventory/aws/ai_services.json', 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print("\nDone.", flush=True)
