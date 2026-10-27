import os
from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CarePilot AI", page_icon="✚", layout="wide")
st.markdown("""<style>
.block-container{padding-top:1.5rem;max-width:1200px}
.hero{background:linear-gradient(115deg,#123e38,#247c69);color:white;padding:2rem;border-radius:20px;margin-bottom:1rem}
.hero h1{color:white;margin:0}.hero p{margin:.4rem 0 0}
.kpi{background:#f1f8f4;border:1px solid #d9e8df;padding:1rem;border-radius:15px;min-height:95px}
.num{font-size:1.6rem;font-weight:800;color:#174a40}.cap{color:#60736f}
.panel{border:1px solid #dce9e4;padding:1rem;border-radius:14px;margin-bottom:.6rem}
</style>""",unsafe_allow_html=True)

FAQ = [
("Prepare for a doctor appointment","Write down your main concern, when it started, medicines and allergies, and questions to ask. Bring relevant reports if available."),
("Track a symptom","Note when it started, frequency, severity, what makes it better or worse, and associated symptoms. Share this with a clinician."),
("Build a healthy routine","Start with realistic habits: consistent sleep, regular movement, balanced meals, hydration, and breaks."),
("Can this app diagnose me?","No. CarePilot is an educational prototype and cannot diagnose conditions or replace a qualified healthcare professional."),
("Medical emergency","Contact your local emergency number or go to the nearest emergency department. Do not rely on this prototype for urgent decisions.")
]
def ask_ai(question, area):
    key=os.getenv("GROQ_API_KEY","")
    try: key=key or st.secrets.get("GROQ_API_KEY","")
    except Exception: pass
    if not key: return None,False
    try:
        from groq import Groq
        client=Groq(api_key=key)
        r=client.chat.completions.create(model="llama-3.3-70b-versatile",temperature=.3,max_tokens=600,messages=[
        {"role":"system","content":"You provide general health information only. Never diagnose or prescribe. Encourage consulting a qualified clinician. For emergencies, advise local emergency services. Tell users not to share identifying information."},
        {"role":"user","content":f"Area: {area}. Question: {question}"}])
        return r.choices[0].message.content,True
    except Exception as e: return f"Live AI could not respond ({type(e).__name__}). Use the built-in guide below.",False

if "appointments" not in st.session_state: st.session_state.appointments=[]
if "habits" not in st.session_state: st.session_state.habits={}
with st.sidebar:
    st.markdown("## ✚ CarePilot AI")
    st.caption("Healthcare companion prototype")
    page=st.radio("Navigate",["Overview","AI Health Guide","Appointment Planner","Wellness Planner","Project & Submission"])
st.markdown('<div class="hero"><h1>CarePilot AI</h1><p>Clearer health questions, appointment preparation, and everyday wellness planning.</p></div>',unsafe_allow_html=True)
st.warning("CarePilot does not diagnose or prescribe. For a medical emergency, contact local emergency services.")

if page=="Overview":
    cols=st.columns(3)
    for col,n,t in zip(cols,["01","02","03"],["AI health-information guide","Appointment preparation demo","Wellness checklist"]):
        with col: st.markdown(f'<div class="kpi"><div class="num">{n}</div><div class="cap">{t}</div></div>',unsafe_allow_html=True)
    st.subheader("Explore the app")
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="panel"><h4>💬 AI Health Guide</h4><p>General information, optional live AI, and offline guidance.</p></div>',unsafe_allow_html=True)
        if st.button("Health guide details"): st.info("Select AI Health Guide in the sidebar.")
    with b:
        st.markdown('<div class="panel"><h4>🗓 Appointment Planner</h4><p>Organise questions and export a CSV planning list.</p></div>',unsafe_allow_html=True)
        if st.button("Planner details"): st.info("Select Appointment Planner in the sidebar.")
    st.write("A practical healthcare prototype with interactive planning workflows and downloadable outputs. Avoid entering personal identifiers or confidential medical information.")

elif page=="AI Health Guide":
    st.subheader("AI Health Guide")
    st.write("Ask a general question. Do not include personal identifiers.")
    q=st.text_area("Your question",placeholder="Example: How can I prepare for a routine doctor appointment?",height=100)
    area=st.selectbox("Information area",["General health information","Appointment preparation","Healthy habits","Understanding symptoms"])
    if st.button("Generate guidance",type="primary"):
        if len(q.strip())<5: st.error("Please enter a more specific question.")
        else:
            answer,live=ask_ai(q,area)
            if answer:
                st.markdown("### Guidance");st.write(answer)
                st.caption("Live language-model response; verify important information with a clinician." if live else "Live AI unavailable; showing a fallback notice.")
            else:
                st.info("Live AI is not configured. Built-in general guides are available below. See README.md for optional AI setup.")
                for title,body in FAQ:
                    with st.expander(title): st.write(body)
    st.divider();st.subheader("Quick answers")
    for title,body in FAQ:
        with st.expander(title): st.write(body)

elif page=="Appointment Planner":
    st.subheader("Appointment Planner")
    st.write("Local planning demo only; this does not book a real clinic appointment.")
    with st.form("appt",clear_on_submit=True):
        typ=st.selectbox("Appointment type",["General Practitioner","Dentist","Mental wellbeing","Specialist","Follow-up","Other"])
        dt=st.date_input("Preferred date",value=date.today())
        qs=st.text_area("Questions to discuss",placeholder="Avoid personal identifiers")
        ok=st.form_submit_button("Add to planner",type="primary")
        if ok:
            if not qs.strip(): st.error("Add at least one question or topic.")
            else:
                st.session_state.appointments.append({"Type":typ,"Preferred date":str(dt),"Questions":qs.strip()})
                st.success("Added to this session's planner.")
    if st.session_state.appointments:
        df=pd.DataFrame(st.session_state.appointments)
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.download_button("Download planner CSV",df.to_csv(index=False).encode(),"carepilot_planner.csv","text/csv")
        if st.button("Clear planner"): st.session_state.appointments=[];st.rerun()
    else: st.caption("Your planned items will appear here.")
    st.caption("Entries exist only during this app session; no database or booking integration is connected.")

elif page=="Wellness Planner":
    st.subheader("Wellness Planner")
    st.write("Choose realistic general habits for today.")
    opts=["Take movement breaks","Drink water regularly","Plan balanced meals","Keep a consistent sleep time","Spend time outdoors if practical","Take a mindful breathing break"]
    for item in opts: st.session_state.habits[item]=st.checkbox(item,value=st.session_state.habits.get(item,False),key="habit_"+item)
    done=sum(bool(st.session_state.habits.get(x)) for x in opts)
    st.progress(done/len(opts));st.write(f"**{done} of {len(opts)} habits checked**")
    txt="CarePilot wellness checklist\n\n"+"\n".join(f"[{'x' if st.session_state.habits.get(x) else ' '}] {x}" for x in opts)
    st.download_button("Download today's checklist",txt,"carepilot_wellness.txt","text/plain")
    st.caption("This is not personalised medical advice. Follow your clinician's guidance.")

else:
    st.subheader("Project & Submission")
    st.write("Healthcare-domain functional web application / innovation prototype.")
    for title,desc in [
    ("Healthcare/technology domain","Healthcare information and appointment preparation"),
    ("Meaningful AI use","AI-assisted development; optional live language-model response with Groq key"),
    ("Practical outcome","Interactive guide, planner, checklist, CSV and text downloads"),
    ("Prompt documentation","See prompts.md and update it with prompts actually used"),
    ("Minimum 2-minute video","Use VIDEO_DEMO_SCRIPT.md as a guide"),
    ("Accessible project link","Publish to GitHub or public Drive and verify access")]:
        st.markdown(f'<div class="panel"><b>{title}</b><br>{desc}</div>',unsafe_allow_html=True)
    st.checkbox("I tested each page and download")
    st.checkbox("I recorded a demo video of at least 2 minutes")
    st.checkbox("My project link is accessible")
    st.checkbox("Prompt documentation reflects my actual prompts")
    st.warning("Do not claim live AI is enabled unless you configured and tested the API key.")
