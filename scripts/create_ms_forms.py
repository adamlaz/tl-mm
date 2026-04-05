#!/usr/bin/env python3
"""
Create Microsoft Forms surveys using the undocumented Forms API.
Auth via browser cookies (grab from F12 dev tools).

Usage:
    python scripts/create_ms_forms.py test              # Verify auth works
    python scripts/create_ms_forms.py inspect            # Dump existing DevEx form questions
    python scripts/create_ms_forms.py create             # Create all 4 surveys
    python scripts/create_ms_forms.py create dora        # Create just one survey

Setup:
    1. Open Forms in browser, open F12 dev tools > Network tab
    2. Make a change in any form to trigger a request to formapi
    3. Copy the 'cookie' header value into .forms-cookie
    4. Copy the '__requestverificationtoken' header value into .forms-token
"""

import requests
import json
import random
import sys
import time
import uuid
from pathlib import Path

TENANT_ID = "0edabf89-5e13-42c3-abd6-f687e9fe0f3a"
USER_ID = "39c1e1ec-60e1-43ac-a793-fb4d0b470e14"
BASE_URL = "https://forms.cloud.microsoft/formapi/api"
DEVEX_FORM_ID = "ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRUNVdXNk1IQUxTUTlKRkNIQjVSUDQzS1VCTi4u"

ROOT = Path(__file__).parent.parent


def load_auth():
    cookie_file = ROOT / ".forms-cookie"
    token_file = ROOT / ".forms-token"
    missing = []
    if not cookie_file.exists():
        missing.append(".forms-cookie")
    if not token_file.exists():
        missing.append(".forms-token")
    if missing:
        print(f"Missing auth files: {', '.join(missing)}")
        print("See script header for setup instructions.")
        sys.exit(1)
    return {
        "cookie": cookie_file.read_text().strip(),
        "token": token_file.read_text().strip(),
    }


class FormsAPI:
    def __init__(self, auth):
        self.s = requests.Session()
        self.session_id = str(uuid.uuid4())
        self.s.headers.update({
            "accept": "application/json",
            "content-type": "application/json",
            "cookie": auth["cookie"],
            "origin": "https://forms.cloud.microsoft",
            "referer": "https://forms.cloud.microsoft/Pages/DesignPageV2.aspx",
            "__requestverificationtoken": auth["token"],
            "x-ms-form-request-ring": "business",
            "x-ms-form-request-source": "ms-formweb",
            "x-usersessionid": self.session_id,
            "odata-version": "4.0",
            "odata-maxversion": "4.0",
        })

    def _url(self, path):
        return f"{BASE_URL}/{TENANT_ID}/users/{USER_ID}/{path}"

    def _qid(self):
        return "r" + "".join(f"{random.randint(0,15):x}" for _ in range(32))

    def _req(self, method, path, body=None):
        self.s.headers["x-correlationid"] = str(uuid.uuid4())
        url = self._url(path)
        if body:
            r = self.s.request(method, url, json=body)
        else:
            r = self.s.request(method, url)
        return r

    def get_form(self, form_id):
        return self._req("GET", f"forms('{form_id}')")

    def get_questions(self, form_id):
        return self._req("GET", f"forms('{form_id}')/questions")

    def create_form(self, title, description=""):
        body = {"title": title}
        if description:
            body["description"] = description
        return self._req("POST", "forms", body)

    def add_question(self, form_id, *, q_type, title, order, required=True,
                     question_info=None, allow_multiple=False, subtitle=""):
        qi = json.dumps(question_info) if question_info else ""
        body = {
            "questionInfo": qi,
            "type": q_type,
            "title": title,
            "id": self._qid(),
            "order": order,
            "isQuiz": False,
            "required": required,
        }
        if allow_multiple:
            body["allowMultipleValues"] = True
        if subtitle:
            body["subtitle"] = subtitle
        r = self._req("POST", f"forms('{form_id}')/questions", body)
        time.sleep(0.4)
        return r


# --- Question info builders ---

def rating_5(left="Strongly Disagree", right="Strongly Agree"):
    return {
        "Length": 5, "RatingShape": "Number",
        "LeftDescription": left, "RightDescription": right,
        "MinRating": 1, "ShuffleOptions": False,
        "ShowRatingLabel": False, "IsMathQuiz": False,
    }


def choice_info(options, allow_other=False):
    return {
        "Choices": [{"Description": o, "IsGenerated": False} for o in options],
        "ChoiceType": 0, "AllowOtherAnswer": allow_other,
        "OptionDisplayStyle": "ListAll",
        "ChoiceRestrictionType": "None", "ShowRatingLabel": False,
    }


def text_info(multiline=False):
    return {"Multiline": multiline, "ShowRatingLabel": False}


# --- Survey definitions ---

def get_surveys():
    return {
        "dora": {
            "title": "DORA Quick Check \u2014 Mad Mobile Engineering Assessment",
            "description": (
                "Software delivery performance against Google\u2019s DORA research benchmarks. "
                "~3 minutes. One per team/squad. Responses are anonymous."
            ),
            "questions": [
                {"title": "How often does your team deploy code to production?",
                 "subtitle": "Deployment Frequency \u2014 pick the answer that best describes your team over the last 3 months.",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["On-demand (multiple deploys per day)",
                     "Between once per day and once per week",
                     "Between once per week and once per month",
                     "Between once per month and once every 6 months",
                     "Fewer than once every 6 months"])},
                {"title": "How long does it typically take for a commit to reach production?",
                 "subtitle": "Lead Time for Changes",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Less than one hour",
                     "Between one hour and one day", "Between one day and one week",
                     "Between one week and one month", "Between one month and six months",
                     "More than six months"])},
                {"title": "What percentage of deployments to production result in a degraded service or require remediation (hotfix, rollback, patch)?",
                 "subtitle": "Change Failure Rate",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["0\u20135%", "6\u201315%", "16\u201330%",
                     "31\u201345%", "46\u201360%", "61%+"])},
                {"title": "When a service incident or defect occurs in production, how long does it typically take to restore service?",
                 "subtitle": "Failed Deployment Recovery Time",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Less than one hour",
                     "Between one hour and one day", "Between one day and one week",
                     "Between one week and one month", "More than one month"])},
                {"title": "To what extent do you meet or exceed your reliability targets (SLAs/SLOs)?",
                 "subtitle": "Reliability",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["We consistently meet or exceed them",
                     "We meet them most of the time", "We meet them about half the time",
                     "We rarely meet them", "We don\u2019t have formal reliability targets"])},
                {"title": "Team Name / Product Area",
                 "type": "Question.TextField", "required": True,
                 "question_info": text_info(False)},
                {"title": "How many engineers are on your team?",
                 "type": "Question.TextField", "required": True,
                 "question_info": text_info(False)},
                {"title": "What percentage of your team\u2019s time goes to maintenance/legacy work vs. new feature development?",
                 "subtitle": "e.g., Maintenance: 60% | New Features: 40%",
                 "type": "Question.TextField", "required": True,
                 "question_info": text_info(False)},
                {"title": "Is there anything that would significantly improve your team\u2019s delivery performance that leadership should know about?",
                 "type": "Question.TextField", "required": False,
                 "question_info": text_info(True)},
            ],
        },
        "westrum": {
            "title": "Westrum Organizational Culture Survey \u2014 Mad Mobile",
            "description": (
                "Measures organizational culture type \u2014 Pathological, Bureaucratic, or Generative. "
                "~2 minutes. Scale: 1=Strongly Disagree to 5=Strongly Agree. Responses are anonymous."
            ),
            "questions": [
                {"title": "Information is actively sought out.",
                 "subtitle": "People in this organization proactively look for information to do their jobs well, rather than waiting for it to come to them.",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                {"title": "Messengers are not punished.",
                 "subtitle": "When someone delivers bad news or reports a problem, they are thanked and supported \u2014 not blamed, sidelined, or ignored.",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                {"title": "Responsibilities are shared.",
                 "subtitle": "When problems arise, teams collaborate across boundaries to solve them rather than pointing fingers.",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                {"title": "Cross-functional collaboration is encouraged.",
                 "subtitle": "Working with people outside your immediate team is easy, supported, and normal \u2014 not bureaucratic or politically charged.",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                {"title": "Failure leads to inquiry, not punishment.",
                 "subtitle": "When something goes wrong, the response focuses on understanding what happened and preventing recurrence \u2014 not finding someone to blame.",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                {"title": "New ideas are welcomed.",
                 "subtitle": "People feel comfortable proposing new approaches, technologies, or process changes without fear of being shot down or ignored.",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                {"title": "What is one thing about how information flows at Mad Mobile that you would change if you could?",
                 "type": "Question.TextField", "required": False,
                 "question_info": text_info(True)},
            ],
        },
        "pragmatic": {
            "title": "Pragmatic Engineer Test \u2014 Mad Mobile",
            "description": (
                "Engineering culture maturity \u2014 12 yes/no questions by Gergely Orosz. "
                "~2 minutes. Answer based on how your team actually operates today. Responses are anonymous."
            ),
            "questions": [
                {"title": "Can you do a build and deployment in one step?",
                 "subtitle": "i.e., a single command or button click triggers the full CI/CD pipeline from commit to production",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Do you deploy to production at least once per week?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Do you have automated tests that give you confidence in your deployments?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Do you fix bugs before writing new features?",
                 "subtitle": "i.e., when a significant bug is found, does it take priority over feature work?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Do you have up-to-date architecture and system documentation?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Do you do code reviews before merging?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Do you have on-call rotations with clear escalation paths?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Do engineers have quiet working conditions?",
                 "subtitle": "i.e., ability to get 2+ hours of uninterrupted focus time most days",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Can new engineers push code to production in their first week?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Do you do blameless post-mortems after incidents?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Are engineers involved in product decisions?",
                 "subtitle": "i.e., engineers participate in scoping, architecture decisions, and prioritization \u2014 not just executing tickets",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Do you have a career ladder with clear levels and expectations?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["Yes", "No"])},
                {"title": "Team / Product Area",
                 "type": "Question.TextField", "required": True,
                 "question_info": text_info(False)},
                {"title": "Your Role",
                 "type": "Question.TextField", "required": True,
                 "question_info": text_info(False)},
                {"title": "Is there a question above where you answered \u2018No\u2019 that frustrates you the most? Which one and why?",
                 "type": "Question.TextField", "required": False,
                 "question_info": text_info(True)},
            ],
        },
        "ai_tooling": {
            "title": "AI Adoption & Tooling Survey \u2014 Mad Mobile",
            "description": (
                "AI tool adoption, effectiveness, tooling landscape, and AI readiness. "
                "~5 minutes. All engineering, product, design, QE. Responses are anonymous."
            ),
            "questions": [
                {"title": "Which AI tools do you use at least weekly?",
                 "subtitle": "Select all that apply",
                 "type": "Question.Choice", "required": True, "allow_multiple": True,
                 "question_info": choice_info([
                     "Cursor (AI-assisted coding)",
                     "Claude (Anthropic) \u2014 directly or via Cursor",
                     "ChatGPT / OpenAI",
                     "Lovable (AI prototyping / UI generation)",
                     "n8n AI workflows (Smart Prompts, ETL, etc.)",
                     "Amazon Bedrock / SageMaker",
                     "GitHub Copilot", "Gemini (Google)",
                     "Bland.AI (customer support)",
                     "Revenue.io (sales intelligence)",
                     "AI features built into existing tools (Jira, Confluence, etc.)",
                     "Amazon Q Developer / CodeWhisperer",
                     "Custom internal AI tools or scripts",
                     "None \u2014 I don\u2019t currently use AI tools",
                 ], allow_other=True)},
                {"title": "What do you primarily use AI tools for?",
                 "subtitle": "Select all that apply",
                 "type": "Question.Choice", "required": True, "allow_multiple": True,
                 "question_info": choice_info([
                     "Writing or generating code",
                     "Code review and debugging",
                     "Writing tests",
                     "Writing documentation",
                     "Writing user stories or requirements",
                     "Analyzing logs or production issues (RCA)",
                     "Data analysis or querying",
                     "Internal communication (drafting messages, summarizing)",
                     "Learning new technologies or codebases",
                     "I don\u2019t currently use AI tools",
                 ], allow_other=True)},
                # Q3-Q6: Likert with N/A option (use Choice since Rating doesn't support N/A)
                {"title": "AI tools meaningfully improve my daily productivity.",
                 "subtitle": "1=Strongly Disagree, 5=Strongly Agree",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["1 \u2014 Strongly Disagree", "2 \u2014 Disagree",
                     "3 \u2014 Neutral", "4 \u2014 Agree", "5 \u2014 Strongly Agree",
                     "N/A \u2014 I don\u2019t use AI tools"])},
                {"title": "I have the training and support I need to use AI tools effectively.",
                 "subtitle": "1=Strongly Disagree, 5=Strongly Agree",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["1 \u2014 Strongly Disagree", "2 \u2014 Disagree",
                     "3 \u2014 Neutral", "4 \u2014 Agree", "5 \u2014 Strongly Agree", "N/A"])},
                {"title": "My team has clear guidelines on when and how to use AI tools (e.g., code review standards, security, IP).",
                 "subtitle": "1=Strongly Disagree, 5=Strongly Agree",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["1 \u2014 Strongly Disagree", "2 \u2014 Disagree",
                     "3 \u2014 Neutral", "4 \u2014 Agree", "5 \u2014 Strongly Agree", "N/A"])},
                {"title": "I trust the output from AI tools enough to use it without heavy manual review.",
                 "subtitle": "1=Strongly Disagree, 5=Strongly Agree",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info(["1 \u2014 Strongly Disagree", "2 \u2014 Disagree",
                     "3 \u2014 Neutral", "4 \u2014 Agree", "5 \u2014 Strongly Agree", "N/A"])},
                # Q7: No N/A, use Rating
                {"title": "Mad Mobile\u2019s AI strategy for our products (CAKE, Concierge, Neo) is clear to me.",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                # Q8: Tooling landscape multi-select
                {"title": "Which of these tools do you use at least weekly?",
                 "subtitle": "Beyond AI \u2014 the full set of tools you rely on. Select all that apply.",
                 "type": "Question.Choice", "required": True, "allow_multiple": True,
                 "question_info": choice_info([
                     "Jira", "Confluence", "Bitbucket", "VS Code", "IntelliJ IDEA",
                     "Postman / Insomnia", "Docker", "Jenkins", "Grafana", "Datadog",
                     "Slack", "Microsoft Teams", "Figma", "SonarQube", "Snyk",
                     "SpiraTest / QCenter", "Salesforce", "Five9",
                 ], allow_other=True)},
                {"title": "What are the 1\u20133 tools most essential to your daily work?",
                 "type": "Question.TextField", "required": True,
                 "question_info": text_info(False)},
                {"title": "Are there tools your team pays for or has access to that you rarely or never use? If so, which ones?",
                 "type": "Question.TextField", "required": False,
                 "question_info": text_info(True)},
                {"title": "Are there tools or capabilities you wish you had but don\u2019t? What would make your work significantly easier?",
                 "type": "Question.TextField", "required": False,
                 "question_info": text_info(True)},
                # Q11a-d: Rating 1-5
                {"title": "I have too many tools to manage \u2014 there is overlap and redundancy in what we use.",
                 "subtitle": "1=Strongly Disagree, 5=Strongly Agree",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                {"title": "Our tools are well-integrated \u2014 data flows between systems without manual effort.",
                 "subtitle": "1=Strongly Disagree, 5=Strongly Agree",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                {"title": "When a new tool is introduced, I receive adequate onboarding and documentation.",
                 "subtitle": "1=Strongly Disagree, 5=Strongly Agree",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                {"title": "I know who to ask when I have problems with a tool or need access to a new one.",
                 "subtitle": "1=Strongly Disagree, 5=Strongly Agree",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5()},
                # Q12: Confidence rating
                {"title": "How confident are you that Mad Mobile can deliver competitive AI-powered features to customers in the next 12 months?",
                 "type": "Question.Rating", "required": True,
                 "question_info": rating_5("Not at all confident", "Very confident")},
                # Q13: Biggest barrier
                {"title": "What is the biggest barrier to Mad Mobile delivering on its AI product vision?",
                 "subtitle": "Select one",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info([
                     "We don\u2019t have the right infrastructure",
                     "We don\u2019t have the right skills/talent",
                     "Our existing tech debt prevents us from moving fast enough",
                     "The AI strategy isn\u2019t clearly defined",
                     "We\u2019re spread too thin across too many products",
                     "I don\u2019t think there\u2019s a significant barrier",
                 ], allow_other=True)},
                # Context questions
                {"title": "Team / Product Area",
                 "type": "Question.TextField", "required": True,
                 "question_info": text_info(False)},
                {"title": "Role",
                 "subtitle": "Select one",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info([
                     "Software Engineer (Frontend)", "Software Engineer (Backend)",
                     "Software Engineer (Full Stack)", "QE / Quality Engineer",
                     "DevOps / SRE / Infrastructure", "Product Manager",
                     "Product Designer", "Engineering Manager / Lead",
                 ], allow_other=True)},
                {"title": "How long have you been at Mad Mobile?",
                 "type": "Question.Choice", "required": True,
                 "question_info": choice_info([
                     "Less than 6 months", "6 months \u2013 1 year",
                     "1 \u2013 2 years", "2 \u2013 4 years", "4+ years",
                 ])},
            ],
        },
    }


# --- Commands ---

def cmd_test(api):
    print("Testing auth by reading existing DevEx form...")
    r = api.get_form(DEVEX_FORM_ID)
    if r.ok:
        data = r.json()
        print(f"  OK! Form title: {data.get('title', '?')}")
        print(f"  Status: {data.get('status', '?')}")
        print(f"  Created: {data.get('createdDate', '?')}")
        return True
    else:
        print(f"  FAILED: {r.status_code}")
        print(f"  Response: {r.text[:500]}")
        if r.status_code == 401:
            print("\n  Token likely expired. Grab fresh cookies from F12 dev tools.")
        return False


def cmd_inspect(api):
    print(f"Inspecting DevEx form questions...")
    r = api.get_questions(DEVEX_FORM_ID)
    if r.ok:
        data = r.json()
        questions = data.get("value", data) if isinstance(data, dict) else data
        if isinstance(questions, list):
            for i, q in enumerate(questions):
                print(f"\n--- Question {i+1} ---")
                print(json.dumps(q, indent=2))
        else:
            print(json.dumps(data, indent=2))
    else:
        print(f"FAILED: {r.status_code} - {r.text[:500]}")


def cmd_create(api, survey_name="all"):
    surveys = get_surveys()

    if survey_name != "all":
        if survey_name not in surveys:
            print(f"Unknown survey: {survey_name}")
            print(f"Available: {', '.join(surveys.keys())}")
            sys.exit(1)
        surveys = {survey_name: surveys[survey_name]}

    created_forms = []

    for key, survey in surveys.items():
        print(f"\n{'='*60}")
        print(f"Creating: {survey['title']}")
        print(f"{'='*60}")

        r = api.create_form(survey["title"], survey.get("description", ""))
        if not r.ok:
            print(f"  FAILED to create form: {r.status_code}")
            print(f"  Response: {r.text[:500]}")
            print(f"  Skipping {key}...")
            continue

        form_data = r.json()
        form_id = form_data.get("id", "")
        print(f"  Form created! ID: {form_id}")

        errors = []
        for i, q in enumerate(survey["questions"]):
            order = (i + 1) * 1000000 + 500
            r = api.add_question(
                form_id,
                q_type=q["type"],
                title=q["title"],
                order=order,
                required=q.get("required", True),
                question_info=q.get("question_info"),
                allow_multiple=q.get("allow_multiple", False),
                subtitle=q.get("subtitle", ""),
            )
            status = "OK" if r.ok else f"FAIL({r.status_code})"
            q_short = q["title"][:60] + ("..." if len(q["title"]) > 60 else "")
            print(f"  [{i+1}/{len(survey['questions'])}] {status} - {q_short}")
            if not r.ok:
                errors.append((i+1, q["title"], r.status_code, r.text[:200]))

        edit_url = f"https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id={form_id}"
        created_forms.append({"key": key, "title": survey["title"],
                              "form_id": form_id, "url": edit_url, "errors": errors})

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for f in created_forms:
        status = "with errors" if f["errors"] else "OK"
        print(f"\n  {f['key']}: {status}")
        print(f"  Edit: {f['url']}")
        if f["errors"]:
            for num, title, code, msg in f["errors"]:
                print(f"    ERROR Q{num}: [{code}] {title[:50]}... - {msg[:100]}")

    return created_forms


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("test", "inspect", "create"):
        print("Usage: python scripts/create_ms_forms.py {test|inspect|create} [survey_name]")
        print("  test     - verify auth works")
        print("  inspect  - dump existing DevEx form questions")
        print("  create   - create surveys (all, or: dora, westrum, pragmatic, ai_tooling)")
        sys.exit(1)

    auth = load_auth()
    api = FormsAPI(auth)
    action = sys.argv[1]

    if action == "test":
        ok = cmd_test(api)
        if ok:
            print("\nAuth works! Run 'inspect' to see question format, or 'create' to build surveys.")
    elif action == "inspect":
        cmd_inspect(api)
    elif action == "create":
        survey = sys.argv[2] if len(sys.argv) > 2 else "all"
        cmd_create(api, survey)
