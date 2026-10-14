import json
import re
from datetime import datetime
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Claims Intake & Triage Assistant", page_icon="🛡️", layout="wide")

REQUIRED_FIELDS = ["claimant_name", "policy_number", "incident_date", "incident_time", "location", "description", "vehicle_or_asset_id"]
DOC_PATTERNS = {
    "FIR / police report": r"\b(fir|police report|incident report)\b",
    "Photos / video": r"\b(photo|photos|photograph|photographs|picture|pictures|video|footage)\b",
    "Third-party insurance details": r"\b(other driver.?s insurance|third.party insurance|third party insurance|insurance details)\b",
    "Repair estimate": r"\b(repair estimate|estimate from (a )?garage|garage estimate|quotation for repair)\b",
    "Medical report / bills": r"\b(medical report|medical bill|hospital bill|medical records)\b",
    "Driving licence": r"\b(driving licence|driver.?s license|driving license)\b",
    "Registration certificate": r"\b(registration certificate|\brc\b)\b",
    "Claim form": r"\bclaim form\b",
    "Policy document": r"\bpolicy document|policy copy\b",
}
DATE_RE = re.compile(r"\b(\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b", re.I)

def parse_date(s):
    s=s.strip()
    for fmt in ("%Y-%m-%d","%d/%m/%Y","%d-%m-%Y","%m/%d/%Y","%d %b %Y","%d %B %Y","%d Sept %Y","%d Sep %Y"):
        try: return datetime.strptime(s,fmt).date().isoformat()
        except ValueError: pass
    return s

def extract(text):
    """Conservative baseline: only extracts facts from explicit phrases; no external AI call."""
    original=text.strip()
    low=original.lower()
    sources=[]
    # Multi-source lines should use Source: detail format.
    for line in original.splitlines():
        m=re.match(r"\s*(claim form|email|customer description|incident report|agent note)\s*:\s*(.*)",line,re.I)
        if m:
            sources.append({"source":m.group(1).strip().title(),"text":m.group(2).strip()})
    if not sources:
        sources=[{"source":"Claimant-provided description","text":original}]
    combined="\n".join(s["text"] for s in sources)
    lowc=combined.lower()

    claim_type="Unknown / needs review"
    if re.search(r"\b(car|vehicle|motor|bumper|collision|crash|truck|bike|motorcycle)\b",lowc):
        claim_type="Motor - Accident"
    elif re.search(r"\b(health|hospital|medical|illness|surgery|doctor)\b",lowc):
        claim_type="Health"
    elif re.search(r"\b(home|house|property|fire|roof|burglary)\b",lowc):
        claim_type="Property"
    elif re.search(r"\b(travel|flight|baggage|trip)\b",lowc):
        claim_type="Travel"

    incident_type="Not stated"
    incident_patterns=[
        (r"rear.?end collision|hit from behind|rear ended","Rear-end collision"),
        (r"\b(side.?swipe|sideswiped)\b","Side-swipe collision"),
        (r"\b(theft|stolen|burglary)\b","Theft / burglary"),
        (r"\b(fire|caught fire)\b","Fire"),
        (r"\b(flood|water damage)\b","Flood / water damage"),
        (r"\b(fell|slipped|fall)\b","Slip / fall"),
        (r"\b(illness|diagnosed|sick)\b","Illness / medical event"),
    ]
    for pat,label in incident_patterns:
        if re.search(pat,lowc): incident_type=label; break

    dates=[]
    for src in sources:
        for match in DATE_RE.findall(src["text"]):
            dates.append({"source":src["source"],"raw":match,"normalized":parse_date(match)})
    unique_dates=list(dict.fromkeys(d["normalized"] for d in dates))
    conflicts=[]
    if len(unique_dates)>1:
        conflicts.append({"field":"incident_date","values":dates,"message":"Different dates appear in the supplied sources. Do not choose one without clarification."})

    time_match=re.search(r"\b(?:at\s+)?(\d{1,2}(?::\d{2})?\s?(?:am|pm))\b",combined,re.I)
    location_match=re.search(r"\b(?:at|near|in|on)\s+([A-Z][A-Za-z0-9 ,'-]{2,45}?)(?=[,.]|\s+(?:yesterday|today|on|at|and|where)|$)",combined)
    policy_match=re.search(r"\b(?:policy number|policy no\.?|policy #)\s*[:#-]?\s*([A-Z0-9-]{4,})",combined,re.I)
    claimant_match=re.search(r"\b(?:claimant name|my name is|name)\s*[:\-]?\s*([A-Z][A-Za-z'-]+(?:\s+[A-Z][A-Za-z'-]+){0,3})",combined,re.I)
    vehicle_match=re.search(r"\b(?:registration number|vehicle number|number plate|registration no\.?)\s*[:#-]?\s*([A-Z]{2}\s?\d{1,2}\s?[A-Z]{0,3}\s?\d{1,4})",combined,re.I)
    docs=[name for name,pat in DOC_PATTERNS.items() if re.search(pat,lowc)]
    damage=[]
    for phrase in ["rear bumper","boot","bonnet","windscreen","windshield","left door","right door","headlight","tail light","front bumper","engine"]:
        if phrase in lowc: damage.append(phrase.title())

    fields={
        "claimant_name": claimant_match.group(1).strip() if claimant_match else None,
        "policy_number": policy_match.group(1).strip() if policy_match else None,
        "incident_date": unique_dates[0] if len(unique_dates)==1 else None,
        "incident_time": time_match.group(1).strip() if time_match else None,
        "location": location_match.group(1).strip() if location_match else None,
        "description": original or None,
        "vehicle_or_asset_id": vehicle_match.group(1).strip() if vehicle_match else None,
    }
    # If conflicting dates exist, incident_date remains null and conflict is explicit.
    missing=[f for f in REQUIRED_FIELDS if not fields.get(f)]
    if conflicts:
        missing.append("incident_date (conflicting values; clarification required)")
    if conflicts:
        triage="Contradictory information - manual review"
    elif any(f in missing for f in ["policy_number","incident_date","description"]):
        triage="Additional information required"
    elif claim_type=="Unknown / needs review":
        triage="Manual review"
    elif len(missing)>=3:
        triage="Additional information required"
    else:
        triage="Initial review"

    next_steps=[]
    if not fields["policy_number"]: next_steps.append("Request the policy number and verify active coverage.")
    if not fields["incident_date"]: next_steps.append("Confirm the incident date; resolve conflicting dates before proceeding.")
    if not fields["incident_time"]: next_steps.append("Ask for the incident time, if known.")
    if not fields["location"]: next_steps.append("Request the incident location.")
    if not fields["vehicle_or_asset_id"] and claim_type=="Motor - Accident": next_steps.append("Request the vehicle registration number.")
    if "Repair estimate" not in docs and claim_type=="Motor - Accident": next_steps.append("Request a repair estimate or inspection report.")
    if claim_type=="Motor - Accident" and "Photos / video" not in docs: next_steps.append("Request photographs of the damage, if available.")
    if conflicts: next_steps.append("Contact the claimant to reconcile the conflicting source information and record the confirmed value.")
    if not next_steps: next_steps.append("Verify the supplied information and documents, then route for adjuster review.")
    # Explicitly label recommendations as system-generated.
    return {
        "claim_type": claim_type,
        "incident_type": incident_type,
        "incident_details": {"dates_found":dates,"damage_or_loss_items":damage,"location":fields["location"],"time":fields["incident_time"]},
        "documents_available":docs,
        "extracted_fields":fields,
        "missing_information":missing,
        "conflicts":conflicts,
        "triage_category":triage,
        "next_steps_recommended_by_system":next_steps,
        "evidence_boundary":{
            "claimant_provided_facts":"The extracted fields, source text, and detected document mentions are based only on the text supplied. Document mentions are not proof that a document was reviewed.",
            "system_inferences":[f"Claim type classified as: {claim_type}",f"Incident type classified as: {incident_type}"],
            "limitations":"This is a demonstration baseline, not an insurer decision or coverage determination. Human review is required."
        }
    }

st.title("🛡️ AI Claims Intake & Triage Assistant")
st.caption("Synthetic-data demo • Conservative extraction • Missing-data and contradiction checks")
with st.sidebar:
    st.header("How to use")
    st.write("Paste a claim description or use the sample. For contradiction testing, include source-labelled lines such as `Claim form: Accident date = 12 Sept 2026` and `Email: Accident date = 13 Sept 2026`.")
    st.warning("Do not enter real customer or policyholder personal data.")
sample = """My car was hit from behind yesterday while I was waiting at a signal. The rear bumper and boot are damaged. I have already filed an FIR. I have photos of the damage and the other driver's insurance details."""
if "claim_text" not in st.session_state:
    st.session_state["claim_text"] = sample
text_input=st.text_area("Claim description / source notes", key="claim_text", height=180, placeholder="Paste synthetic claim text here...")
col1,col2=st.columns([1,1])
with col1:
    run=st.button("Analyze claim", type="primary", use_container_width=True)
with col2:
    clear=st.button("Load contradictory-date example", use_container_width=True)
if clear:
    st.session_state["claim_text"]="Claim form: Accident date = 12 Sept 2026. Vehicle hit from behind; rear bumper damaged. Policy number: POL-2048.\nEmail: Accident date = 13 Sept 2026. Photos available; FIR filed."
    st.rerun()
if run:
    result=extract(text_input)
    st.subheader("Triage result")
    st.metric("Initial triage category", result["triage_category"])
    a,b,c=st.columns(3)
    a.metric("Claim type",result["claim_type"])
    b.metric("Incident",result["incident_type"])
    c.metric("Documents mentioned",len(result["documents_available"]))
    st.subheader("Structured claim summary")
    st.json(result, expanded=True)
    st.subheader("Next steps")
    for i,step in enumerate(result["next_steps_recommended_by_system"],1): st.write(f"{i}. {step}")
    st.subheader("Missing information")
    if result["missing_information"]:
        for item in result["missing_information"]: st.write("• "+item)
    else: st.success("No required fields are missing under this baseline schema.")
    if result["conflicts"]:
        st.error("Contradiction detected. Human clarification is required.")
    st.download_button("Download structured JSON", data=json.dumps(result,indent=2), file_name="claim_output.json", mime="application/json")
else:
    st.info("Click Analyze claim to generate the structured record.")
st.divider()
st.caption("Safety: synthetic data only. The tool supports intake triage; it does not decide liability, fraud, or coverage.")
