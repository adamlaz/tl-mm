#!/usr/bin/env python3
"""AWS network topology analysis — VPCs, peering, NAT gateways, transit gateways, security groups."""

import boto3
import json
import os
from datetime import datetime, timezone
from botocore.exceptions import ClientError

def safe_call(fn, default=None):
    try:
        return fn()
    except (ClientError, Exception) as e:
        code = getattr(e, 'response', {}).get('Error', {}).get('Code', '')
        if code in ('AccessDeniedException', 'AccessDenied', 'UnauthorizedAccess',
                     'AuthorizationError', 'OptInRequired', 'SubscriptionRequiredException',
                     'UnrecognizedClientException'):
            return {"_error": f"Access denied: {code}"}
        if default is not None:
            return default
        return {"_error": str(e)}

ACCOUNTS = [
    'mm-retail-prod-us',
    'mm-payments-prod-us',
    'mm-cake-development',
    'mm-shared-services',
]

REGION = 'us-east-1'
SAFE_INBOUND_PORTS = {80, 443}


def get_vpc_peering(ec2):
    raw = safe_call(lambda: ec2.describe_vpc_peering_connections()['VpcPeeringConnections'], [])
    if isinstance(raw, dict) and '_error' in raw:
        return raw
    results = []
    for p in raw:
        results.append({
            'id': p['VpcPeeringConnectionId'],
            'status': p.get('Status', {}).get('Code', 'unknown'),
            'requester_vpc': p.get('RequesterVpcInfo', {}).get('VpcId', ''),
            'requester_owner': p.get('RequesterVpcInfo', {}).get('OwnerId', ''),
            'accepter_vpc': p.get('AccepterVpcInfo', {}).get('VpcId', ''),
            'accepter_owner': p.get('AccepterVpcInfo', {}).get('OwnerId', ''),
        })
    return results


def get_nat_gateways(ec2):
    raw = safe_call(lambda: ec2.describe_nat_gateways()['NatGateways'], [])
    if isinstance(raw, dict) and '_error' in raw:
        return raw
    by_state = {}
    for nat in raw:
        st = nat.get('State', 'unknown')
        by_state[st] = by_state.get(st, 0) + 1
    return {'total': len(raw), 'by_state': by_state}


def get_transit_gateway_attachments(ec2):
    raw = safe_call(lambda: ec2.describe_transit_gateway_attachments()['TransitGatewayAttachments'], [])
    if isinstance(raw, dict) and '_error' in raw:
        return raw
    results = []
    for a in raw:
        results.append({
            'id': a['TransitGatewayAttachmentId'],
            'tgw_id': a.get('TransitGatewayId', ''),
            'resource_type': a.get('ResourceType', ''),
            'resource_id': a.get('ResourceId', ''),
            'state': a.get('State', 'unknown'),
        })
    return results


def analyze_security_groups(ec2):
    raw = safe_call(lambda: ec2.describe_security_groups()['SecurityGroups'], [])
    if isinstance(raw, dict) and '_error' in raw:
        return raw

    total = len(raw)
    wide_open = []
    for sg in raw:
        sg_id = sg['GroupId']
        sg_name = sg.get('GroupName', '')
        vpc_id = sg.get('VpcId', '')
        for perm in sg.get('IpPermissions', []):
            from_port = perm.get('FromPort', 0)
            to_port = perm.get('ToPort', 0)
            ip_protocol = perm.get('IpProtocol', '')
            for ip_range in perm.get('IpRanges', []):
                cidr = ip_range.get('CidrIp', '')
                if cidr == '0.0.0.0/0':
                    if ip_protocol == '-1':
                        wide_open.append({
                            'sg_id': sg_id, 'sg_name': sg_name, 'vpc_id': vpc_id,
                            'rule': 'ALL TRAFFIC from 0.0.0.0/0',
                            'protocol': 'all', 'ports': 'all',
                        })
                    elif from_port and to_port:
                        flagged_ports = [
                            p for p in range(from_port, min(to_port + 1, from_port + 100))
                            if p not in SAFE_INBOUND_PORTS
                        ]
                        if flagged_ports:
                            port_desc = f"{from_port}" if from_port == to_port else f"{from_port}-{to_port}"
                            wide_open.append({
                                'sg_id': sg_id, 'sg_name': sg_name, 'vpc_id': vpc_id,
                                'rule': f'0.0.0.0/0 on port(s) {port_desc}',
                                'protocol': ip_protocol, 'ports': port_desc,
                            })
            for ip_range in perm.get('Ipv6Ranges', []):
                cidr = ip_range.get('CidrIpv6', '')
                if cidr == '::/0':
                    if ip_protocol == '-1':
                        wide_open.append({
                            'sg_id': sg_id, 'sg_name': sg_name, 'vpc_id': vpc_id,
                            'rule': 'ALL TRAFFIC from ::/0',
                            'protocol': 'all', 'ports': 'all',
                        })
                    elif from_port and to_port:
                        flagged_ports = [
                            p for p in range(from_port, min(to_port + 1, from_port + 100))
                            if p not in SAFE_INBOUND_PORTS
                        ]
                        if flagged_ports:
                            port_desc = f"{from_port}" if from_port == to_port else f"{from_port}-{to_port}"
                            wide_open.append({
                                'sg_id': sg_id, 'sg_name': sg_name, 'vpc_id': vpc_id,
                                'rule': f'::/0 on port(s) {port_desc}',
                                'protocol': ip_protocol, 'ports': port_desc,
                            })

    return {
        'total_security_groups': total,
        'wide_open_rules': wide_open,
        'wide_open_count': len(wide_open),
    }


def scan_account(profile):
    print(f"\n  [{profile}]", flush=True)
    session = boto3.Session(profile_name=profile)
    ec2 = session.client('ec2', region_name=REGION)
    data = {'profile': profile}
    blocked = []

    print(f"    VPC Peering ...", end='', flush=True)
    peering = get_vpc_peering(ec2)
    data['vpc_peering'] = peering
    if isinstance(peering, dict) and '_error' in peering:
        blocked.append(f"VPC Peering: {peering['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        print(f" {len(peering)} connections", flush=True)

    print(f"    NAT Gateways ...", end='', flush=True)
    nats = get_nat_gateways(ec2)
    data['nat_gateways'] = nats
    if isinstance(nats, dict) and '_error' in nats:
        blocked.append(f"NAT GW: {nats['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        print(f" {nats.get('total', 0)} total ({nats.get('by_state', {})})", flush=True)

    print(f"    Transit Gateway ...", end='', flush=True)
    tgw = get_transit_gateway_attachments(ec2)
    data['transit_gateway_attachments'] = tgw
    if isinstance(tgw, dict) and '_error' in tgw:
        blocked.append(f"TGW: {tgw['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        print(f" {len(tgw)} attachments", flush=True)

    print(f"    Security Groups ...", end='', flush=True)
    sgs = analyze_security_groups(ec2)
    data['security_groups'] = sgs
    if isinstance(sgs, dict) and '_error' in sgs:
        blocked.append(f"SGs: {sgs['_error']}")
        print(f" BLOCKED", flush=True)
    else:
        print(f" {sgs['total_security_groups']} total, {sgs['wide_open_count']} wide-open rules flagged", flush=True)

    data['blocked_apis'] = blocked
    return data


if __name__ == '__main__':
    os.makedirs('inventory/aws', exist_ok=True)

    print("=== AWS Network Topology Analysis ===", flush=True)
    print(f"  Accounts: {len(ACCOUNTS)}", flush=True)
    print(f"  Region: {REGION}", flush=True)
    print(f"  Started: {datetime.now(timezone.utc).isoformat()}", flush=True)

    results = {}
    for profile in ACCOUNTS:
        results[profile] = scan_account(profile)

    output = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'region': REGION,
        'accounts_scanned': len(ACCOUNTS),
        'accounts': results,
    }

    outpath = 'inventory/aws/network_topology.json'
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  Wrote {outpath}", flush=True)

    print("\n=== Summary ===", flush=True)
    total_peering = 0
    total_nats = 0
    total_tgw = 0
    total_sgs = 0
    total_flags = 0
    for profile, data in results.items():
        blocked = data.get('blocked_apis', [])
        print(f"\n  {profile}:", flush=True)
        if blocked:
            print(f"    Blocked: {', '.join(blocked)}", flush=True)

        peer = data.get('vpc_peering', [])
        if isinstance(peer, list):
            total_peering += len(peer)
            active = [p for p in peer if p.get('status') == 'active']
            print(f"    VPC Peering: {len(peer)} total, {len(active)} active", flush=True)

        nats = data.get('nat_gateways', {})
        if isinstance(nats, dict) and '_error' not in nats:
            total_nats += nats.get('total', 0)
            print(f"    NAT Gateways: {nats.get('total', 0)} ({nats.get('by_state', {})})", flush=True)

        tgw = data.get('transit_gateway_attachments', [])
        if isinstance(tgw, list):
            total_tgw += len(tgw)
            print(f"    Transit GW: {len(tgw)} attachments", flush=True)

        sgs = data.get('security_groups', {})
        if isinstance(sgs, dict) and '_error' not in sgs:
            total_sgs += sgs.get('total_security_groups', 0)
            total_flags += sgs.get('wide_open_count', 0)
            print(f"    Security Groups: {sgs['total_security_groups']} total, {sgs['wide_open_count']} flagged", flush=True)
            for wo in sgs.get('wide_open_rules', [])[:5]:
                print(f"      ⚠ {wo['sg_id']} ({wo['sg_name']}): {wo['rule']}", flush=True)

    print(f"\n  Totals: {total_peering} peering, {total_nats} NATs, {total_tgw} TGW, "
          f"{total_sgs} SGs, {total_flags} flagged rules", flush=True)
    print("\nDone.", flush=True)
