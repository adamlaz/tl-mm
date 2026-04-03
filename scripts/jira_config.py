"""Jira project classification and JQL helpers for segmented analysis."""

ENGINEERING = [
    'AH', 'AHSKREST', 'AL', 'APOLLO', 'BO', 'CAS', 'CE', 'CLD', 'CLN', 'CLOUD',
    'CM', 'CORE', 'CQP', 'DEV', 'DO', 'DP', 'DR', 'DRAC', 'DSO', 'EI', 'FUL',
    'HULK', 'IAL', 'KEN', 'KR', 'L2', 'LAA', 'LEO', 'LIBRA', 'MAUI', 'MIRA',
    'MP', 'NEO', 'NOVA', 'OP', 'OR', 'PHOEN', 'PI', 'PLTFRM', 'PLTRTL', 'POL',
    'POS', 'PR', 'REST', 'SE', 'SIR', 'SM', 'TAUR', 'TD', 'TEM', 'TESTBO',
    'TESTREST', 'THOR', 'TMP', 'TPR', 'TRD', 'TSTRSN', 'TTD', 'VEGA', 'WOL',
    # Ambiguous but clearly engineering
    'AAK', 'AI', 'OS', 'PAY', 'PLAT', 'UP', 'UPK', 'RE',
]

CUSTOMER_SUCCESS = [
    'ACT', 'BB', 'BBOOK', 'CHECK', 'CONNECT', 'CONVO', 'DASH', 'EA',
    'ELCE', 'EN', 'FAS', 'FASCPY', 'GUESS', 'KWG', 'KWGCPY', 'MPOS',
    'PCATALOG', 'RL', 'RRS', 'SGNT', 'SNUS', 'TAL', 'TALCPY', 'TCSD',
    'TEA', 'TFSR', 'TSC', 'TSCTEST', 'UR', 'WEMA', 'WIN', 'WM',
]

OPERATIONS = [
    'AR', 'AUD', 'BT', 'BTP', 'CAKE', 'CHRC', 'CP', 'CX', 'ELC', 'GRC',
    'ITP', 'JC', 'KDS', 'LPC', 'M60', 'MCP', 'PD', 'PP', 'PS', 'PSTT',
    'PTES', 'RES', 'RM', 'RP', 'ST', 'TAR', 'TOP', 'TOS',
]

INACTIVE = [
    'CK', 'CL', 'GO', 'MDM', 'RPT', 'SSP', 'TCD', 'TS', 'TSR',
    'TSTF', 'TSTFNEW', 'TT', 'TUP',
]

_CLASSIFICATION_MAP = {}
for k in ENGINEERING: _CLASSIFICATION_MAP[k] = 'engineering'
for k in CUSTOMER_SUCCESS: _CLASSIFICATION_MAP[k] = 'customer_success'
for k in OPERATIONS: _CLASSIFICATION_MAP[k] = 'operations'
for k in INACTIVE: _CLASSIFICATION_MAP[k] = 'inactive'


def classify_project(key):
    return _CLASSIFICATION_MAP.get(key, 'unclassified')


def _project_in_jql(keys):
    quoted = [f'"{k}"' for k in keys]
    return f'project in ({",".join(quoted)})'


def engineering_jql():
    return _project_in_jql(ENGINEERING)


def customer_success_jql():
    return _project_in_jql(CUSTOMER_SUCCESS)


def operations_jql():
    return _project_in_jql(OPERATIONS)


def all_active_jql():
    return _project_in_jql(ENGINEERING + CUSTOMER_SUCCESS + OPERATIONS)


SEGMENTS = {
    'overall': None,
    'engineering': engineering_jql,
    'customer_success': customer_success_jql,
    'operations': operations_jql,
}


def classify_assignee(projects, issue_counts):
    """Infer role from project mix and issue type distribution."""
    if not projects:
        return 'unknown'

    eng_count = sum(1 for p in projects if classify_project(p) == 'engineering')
    cs_count = sum(1 for p in projects if classify_project(p) == 'customer_success')
    ops_count = sum(1 for p in projects if classify_project(p) == 'operations')
    total_proj = len(projects)

    total_issues = issue_counts.get('total', 0)
    epics = issue_counts.get('epics', 0)
    other = issue_counts.get('other', 0)
    bugs = issue_counts.get('bugs', 0)
    stories = issue_counts.get('stories', 0)

    if total_proj >= 10 and eng_count > 0 and (cs_count > 0 or ops_count > 0):
        return 'cross_functional'

    if cs_count > eng_count and cs_count > ops_count:
        return 'customer_success'

    if ops_count > eng_count and ops_count > cs_count:
        return 'operations'

    if total_issues > 0 and (epics + other) / total_issues > 0.5:
        if eng_count >= ops_count:
            return 'engineering_lead'
        return 'product_or_pm'

    if eng_count >= cs_count and eng_count >= ops_count:
        return 'engineering_ic'

    return 'unclassified'
