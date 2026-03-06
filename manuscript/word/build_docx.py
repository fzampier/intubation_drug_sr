#!/usr/bin/env python3
"""Build a properly formatted DOCX for the intubation SR/NMA manuscript."""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import re

doc = Document()

# --- Default style setup ---
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.paragraph_format.line_spacing = 2.0
style.paragraph_format.space_after = Pt(0)
style.paragraph_format.space_before = Pt(0)

# Heading styles
for level in range(1, 4):
    hs = doc.styles[f'Heading {level}']
    hs.font.name = 'Times New Roman'
    hs.font.color.rgb = RGBColor(0, 0, 0)
    hs.font.bold = True
    hs.paragraph_format.line_spacing = 2.0
    hs.paragraph_format.space_before = Pt(12)
    hs.paragraph_format.space_after = Pt(6)
    if level == 1:
        hs.font.size = Pt(14)
    elif level == 2:
        hs.font.size = Pt(12)
    else:
        hs.font.size = Pt(12)
        hs.font.italic = True

def add_para(text, bold=False, italic=False, alignment=None, space_after=None, font_size=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = 'Times New Roman'
    run.font.size = Pt(font_size or 12)
    if alignment:
        p.alignment = alignment
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p

def add_mixed_para(parts, alignment=None, space_after=None):
    """Add paragraph with mixed formatting. parts = [(text, bold, italic, superscript), ...]"""
    p = doc.add_paragraph()
    for part in parts:
        text = part[0]
        bold = part[1] if len(part) > 1 else False
        italic = part[2] if len(part) > 2 else False
        superscript = part[3] if len(part) > 3 else False
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        if superscript:
            run.font.superscript = True
    if alignment:
        p.alignment = alignment
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p

def set_cell_shading(cell, color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_text(cell, text, bold=False, italic=False, size=9, alignment=WD_ALIGN_PARAGRAPH.CENTER):
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    p.alignment = alignment
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)

def set_cell_mixed(cell, parts, size=9, alignment=WD_ALIGN_PARAGRAPH.CENTER):
    cell.text = ""
    p = cell.paragraphs[0]
    for part in parts:
        text = part[0]
        bold = part[1] if len(part) > 1 else False
        italic = part[2] if len(part) > 2 else False
        superscript = part[3] if len(part) > 3 else False
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        if superscript:
            run.font.superscript = True
    p.alignment = alignment
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)

# ============================================================================
# TITLE PAGE
# ============================================================================
section = doc.sections[0]
section.top_margin = Inches(1)
section.bottom_margin = Inches(1)
section.left_margin = Inches(1)
section.right_margin = Inches(1)

# Spacer
for _ in range(3):
    add_para("", space_after=0)

add_para("Induction agents for emergency tracheal intubation in critically ill adults: a systematic review and network meta-analysis",
         bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, font_size=16, space_after=18)

# Authors
authors_parts = [
    ("Fernando G. Zampieri, MD, PhD", False),
    ("1,2,5", False, False, True),
    ("; Raysa C. Schmidt, MD", False),
    ("2,5", False, False, True),
    ("; Bruno A.M.P. Besen, MD, PhD", False),
    ("2,5", False, False, True),
    ("; Fernando J.D.S. Ramos, MD, PhD", False),
    ("2,5", False, False, True),
    ("; François Lamontagne, MD, MSc", False),
    ("3", False, False, True),
    ("; Neill K.J. Adhikari, MDCM, MSc", False),
    ("4", False, False, True),
    ("; Flávio G.R. Freitas, MD, PhD", False),
    ("2,5", False, False, True),
    ("; Flávia R. Machado, MD, PhD", False),
    ("2,5", False, False, True),
]
add_mixed_para(authors_parts, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
add_para("for the PROMINE Investigators", italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)

# Affiliations
affiliations = [
    "1. Department of Critical Care Medicine, University of Alberta, Edmonton, Canada",
    "2. Intensive Care Department, Hospital São Paulo, Escola Paulista de Medicina, Universidade Federal de São Paulo, São Paulo, SP, Brazil",
    "3. Department of Medicine, Université de Sherbrooke, Sherbrooke, Canada",
    "4. Department of Critical Care Medicine, Sunnybrook Health Sciences Centre, University of Toronto, Toronto, Canada",
    "5. Brazilian Research in Intensive Care Network (BRICNet)",
]
for aff in affiliations:
    add_para(aff, font_size=10, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)

add_para("", space_after=12)

# Corresponding author
add_para("Corresponding author:", bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_para("Fernando G. Zampieri", alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_para("CSB 2-124, 8440 112 St NW, Edmonton, AB, T6G 2B7, Canada", alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_para("fzampier@ualberta.ca", alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

add_para("Word count: Abstract: 249 / Manuscript: 3,067", bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_para("PROSPERO: CRD420251251225", bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)

# Page break
doc.add_page_break()

# ============================================================================
# ABSTRACT
# ============================================================================
doc.add_heading('Abstract', level=1)

p = doc.add_paragraph()
r = p.add_run('Background: ')
r.bold = True
r.font.name = 'Times New Roman'
r = p.add_run('Etomidate, ketamine, and propofol are all used as induction agents for emergency tracheal intubation in critically ill adults but it remains uncertain which agent should be preferable.')
r.font.name = 'Times New Roman'

p = doc.add_paragraph()
r = p.add_run('Methods: ')
r.bold = True
r.font.name = 'Times New Roman'
r = p.add_run('We searched MEDLINE and Embase (inception to December 2025) for randomized controlled trials comparing etomidate, ketamine, propofol, or ketamine\u2013propofol combination (ketofol) for emergency or rapid sequence intubation in critically ill adults. We performed random-effects network meta-analysis using the frequentist framework. The primary outcome was short-term mortality (28\u201330 day, or ICU/in-hospital mortality when unavailable). Secondary outcomes included cardiovascular collapse, post-induction hypotension, vasopressor use, first-pass intubation success, and peri-intubation cardiac arrest. Certainty of evidence was assessed using the CINeMA framework.')
r.font.name = 'Times New Roman'

p = doc.add_paragraph()
r = p.add_run('Results: ')
r.bold = True
r.font.name = 'Times New Roman'
r = p.add_run('Nine trials (4,672 patients, four treatments) were included. Ketamine and etomidate probably result in similar mortality (OR 0.96, 95% CI 0.80\u20131.16; I\u00B2 = 30%; moderate certainty). Evidence for other mortality comparisons was very uncertain: ketamine vs propofol (OR 1.53, 0.80\u20132.93; 1 trial; low certainty) and etomidate vs propofol (OR 0.63, 0.32\u20131.24; indirect only; very low certainty). Compared with etomidate, ketamine probably increases cardiovascular collapse (OR 1.44, 1.20\u20131.71; moderate certainty) and may increase post-induction hypotension (OR 1.34, 1.07\u20131.68; low certainty) and peri-intubation vasopressor use (OR 1.45, 1.21\u20131.74; low certainty). There was probably little or no difference in first-pass intubation success or cardiac arrest.')
r.font.name = 'Times New Roman'

p = doc.add_paragraph()
r = p.add_run('Conclusions: ')
r.bold = True
r.font.name = 'Times New Roman'
r = p.add_run('Etomidate and ketamine probably result in similar mortality, but confidence intervals are compatible with clinically important differences in either direction\u2014ketamine probably causes more peri-intubation hemodynamic instability. Beyond one trial, no randomized evidence exists for propofol in emergency intubation of critically ill adults.')
r.font.name = 'Times New Roman'

p = doc.add_paragraph()
r = p.add_run('Keywords: ')
r.bold = True
r.font.name = 'Times New Roman'
r = p.add_run('intubation; rapid sequence induction; etomidate; ketamine; propofol; network meta-analysis; critically ill')
r.font.name = 'Times New Roman'

doc.add_page_break()

# ============================================================================
# INTRODUCTION
# ============================================================================
doc.add_heading('Introduction', level=1)

add_para('Emergency tracheal intubation in critically ill patients is a high-risk procedure. In the INTUBE study, an international cohort of nearly 3,000 patients, major adverse peri-intubation events occurred in 45% of cases, including cardiovascular instability in 43% and cardiac arrest in 3% [1]. Peri-intubation cardiac arrest is independently associated with increased mortality, with hemodynamic instability at induction identified as a key risk factor [2]. The choice of induction agent is one of the few modifiable factors that may influence peri-intubation hemodynamics.')

add_para('The choice of induction agent varies globally. In the INTUBE cohort spanning 29 countries, propofol was the most frequently used induction agent for emergency intubation, whereas etomidate, ketamine, and midazolam were each used less often [1]. Practice differs in North America, where etomidate accounts for approximately 90% of rapid sequence intubations in emergency departments, with ketamine use growing but still below 15% [3,4]. Etomidate provides reliable hemodynamic stability but inhibits 11\u03B2-hydroxylase, causing transient adrenal suppression even after a single dose\u2014a concern particularly in septic patients [5]. Ketamine exerts sympathomimetic effects through endogenous catecholamine release, but may cause myocardial depression in catecholamine-depleted patients [6]. Propofol causes dose-dependent vasodilation that limits its use in hemodynamically unstable patients, yet it remains the most widely used induction agent for emergency intubation worldwide. Ketamine\u2013propofol combinations (ketofol) have been proposed to balance these pharmacodynamic profiles.')

add_para('Several pairwise meta-analyses have compared etomidate and ketamine for emergency intubation [7\u201310], generally finding no statistically significant difference in mortality; a Bayesian meta-analysis, however, found a moderate probability that ketamine may reduce mortality [11]. These analyses were limited to the etomidate\u2013ketamine comparison and could not incorporate evidence from trials involving propofol or ketofol. Two recent trials have substantially changed the evidence landscape: the RSI trial [12] (2,359 patients), the largest randomized comparison of etomidate and ketamine to date; and the PROMINE trial [13], the first randomized trial comparing propofol with ketamine for emergency intubation in critically ill patients, thereby enabling a network meta-analysis beyond the etomidate\u2013ketamine dyad.')

add_para('We therefore conducted a systematic review and network meta-analysis comparing etomidate, ketamine, propofol, and ketofol for emergency tracheal intubation in critically ill adults, with short-term mortality as the primary outcome.')

# ============================================================================
# METHODS
# ============================================================================
doc.add_heading('Methods', level=1)

add_para('This systematic review and network meta-analysis was registered on PROSPERO (CRD420251251225) and is reported in accordance with the PRISMA-NMA extension [14].')

doc.add_heading('Eligibility criteria', level=2)

add_para('We included parallel-group randomized controlled trials comparing etomidate, ketamine (including esketamine or S-ketamine), propofol, or ketamine\u2013propofol combination (ketofol) as induction agents for emergency or rapid sequence intubation in critically ill or acutely ill adults (\u226516 years). Studies were eligible regardless of clinical setting (emergency department, intensive care unit, prehospital, or acute hospital ward). Co-interventions (opioids, neuromuscular blocking agents, preoxygenation strategies) were permitted if applied similarly across treatment arms.')

add_para('We excluded observational studies, crossover trials, simulation or volunteer studies, conference abstracts without sufficient data for risk of bias assessment and effect estimation, studies of elective or operating-room intubations, procedural sedation without intubation, studies focused on post-intubation sedation rather than induction, pediatric studies in which adult data could not be isolated, elective surgical populations without acute critical illness, and studies where the randomized intervention was not the hypnotic induction agent. Only English-language publications were included; one eligible study published in Turkish (Cinar 2011 [15]) was retained because sufficient information was available from its English-language abstract and AI-assisted translation (Claude, Anthropic).')

doc.add_heading('Information sources and search strategy', level=2)

add_para('We searched MEDLINE (via PubMed) and Embase (via Ovid) from inception to December 2025. Forward citation searching of included trials was performed to identify additional relevant studies. Trial registries (ClinicalTrials.gov, WHO ICTRP) were consulted for contextual information. The complete search strategies are provided in the Supplement.')

doc.add_heading('Study selection and data extraction', level=2)

add_para('Search results were imported into a systematic review platform (Rayyan, Rayyan Systems Inc., Cambridge, MA) for deduplication and screening. Two reviewers independently screened titles and abstracts; disagreements at this stage were resolved by consensus. This was followed by full-text assessment of potentially eligible reports against the predefined criteria. Disagreements were resolved through discussion. Reasons for exclusion at the full-text stage were recorded. Data were extracted independently by two reviewers using a standardized form and verified against source publications. Extracted information included study characteristics (authors, year, country, setting, single vs multicenter, funding), population (sample size, age, sex, severity scores, baseline hemodynamics, vasopressor use), interventions (agent, dose, co-induction agents, neuromuscular blocker type and dose), and arm-level outcome data with definitions and time windows.')

doc.add_heading('Risk of bias assessment', level=2)

add_para('Risk of bias was assessed using the Cochrane Risk of Bias 2 (RoB 2) tool [16] across five domains: randomization process, deviations from intended interventions, missing outcome data, measurement of the outcome, and selection of the reported result. Each study was rated as low risk, some concerns, or high risk of bias.')

doc.add_heading('Outcomes', level=2)

add_para('The primary outcome was short-term mortality, defined as 28\u201330 day mortality where reported, or ICU or in-hospital mortality when 28\u201330 day data were unavailable. Secondary outcomes included: cardiovascular collapse (composite of hypotension, vasopressor initiation or escalation, and/or cardiac arrest, as defined by individual studies); post-induction hypotension (blood pressure below study-defined thresholds within 0\u201315 minutes); new or escalated vasopressor use (analyzed at peri-intubation and 24-hour time points separately); first-pass intubation success; and peri-intubation cardiac arrest. All binary outcomes were analyzed as odds ratios (OR) with 95% confidence intervals (CI).')

doc.add_heading('Statistical analysis', level=2)

p = doc.add_paragraph()
r = p.add_run('Arm-level binary data were converted to study-level contrasts (log OR and standard error) using the ')
r.font.name = 'Times New Roman'
r = p.add_run('pairwise()')
r.font.name = 'Times New Roman'
r.italic = True
r = p.add_run(' function from the ')
r.font.name = 'Times New Roman'
r = p.add_run('meta')
r.font.name = 'Times New Roman'
r.italic = True
r = p.add_run(' package (version 8.2-1) [17]. Random-effects network meta-analysis was performed using the frequentist approach implemented in the ')
r.font.name = 'Times New Roman'
r = p.add_run('netmeta')
r.font.name = 'Times New Roman'
r.italic = True
r = p.add_run(' package (version 3.3-1) [18] in R (version 4.5.2). Etomidate was designated as the reference treatment. Esketamine and S-ketamine were grouped under the ketamine node.')
r.font.name = 'Times New Roman'

add_para('Between-study heterogeneity was quantified using I\u00B2 and \u03C4\u00B2. Global inconsistency was evaluated using the design-by-treatment interaction test, and local inconsistency was assessed through node-splitting. Treatment rankings were summarized using P-scores [19].')

add_para('Pairwise meta-analysis of etomidate versus ketamine was performed using the Paule\u2013Mandel estimator for \u03C4\u00B2 with 95% prediction intervals.')

doc.add_heading('Subgroup and sensitivity analyses', level=2)

add_para('Pre-specified subgroup analyses for the primary outcome included stratification by clinical setting (emergency department, ICU, or mixed\u2014studies enrolling across both ED and ICU settings were classified as mixed because patients could not be disaggregated by location) and overall risk of bias. A planned subgroup analysis by baseline vasopressor use was not feasible because only three of nine studies reported this information. Similarly, degree of RSI protocolization, a predefined effect modifier, could not be formally evaluated because the distinction between strict and pragmatic protocols was not sufficiently categorical across studies. Other clinically important subgroups\u2014such as patients with heart failure or by primary diagnosis\u2014could not be examined because individual-study data were not available at this level.')

add_para('Sensitivity analyses excluded: (a) studies where the ketamine arm included a midazolam adjunct (Cinar 2011 [15], Punt 2014 [20]); and (b) analyses collapsing or removing ketofol as a separate treatment node.')

doc.add_heading('Certainty of evidence', level=2)

add_para('Certainty of evidence for key comparisons was assessed using the CINeMA framework (Confidence in Network Meta-Analysis) [21], evaluating six domains: within-study bias, reporting bias, indirectness, imprecision, heterogeneity, and incoherence. Ratings were classified as high, moderate, low, or very low certainty. Because the etomidate\u2013ketamine comparison was informed entirely by direct evidence (7 trials), certainty for this comparison was assessed without indirect contributions. The etomidate\u2013propofol comparison relied entirely on indirect evidence through the ketamine node.')

doc.add_heading('Use of large language models', level=2)

add_para('This review made extensive use of large language models (LLMs) for transparency and reproducibility. The search strategy was designed with assistance from Gemini 3.0 Pro (Google). Screening was performed using Rayyan.ai, and selected full-text articles were retrieved by the first and last authors. Data extraction was performed by Claude Opus 4.6 (Anthropic) from source PDFs, followed by manual verification by F.J.D.S.R. and the first author. Risk of bias assessments were drafted by the LLM and reviewed by F.R.M. CINeMA certainty-of-evidence assessments were performed by F.G.Z. and reviewed by F.R.M. Statistical analysis code (R) was written with assistance from Claude Opus 4.6. All LLM outputs were critically reviewed and verified by the investigators; extracted data were cross-checked against source PDFs for all included studies.')

# ============================================================================
# RESULTS
# ============================================================================
doc.add_heading('Results', level=1)

doc.add_heading('Study selection', level=2)

add_para('The search identified 1,087 records after deduplication. After title/abstract screening and full-text review, 9 trials met the inclusion criteria (Figure 1). One additional trial (Agarwal 2025 [22]) initially met the eligibility criteria but was excluded after independent review identified that its published summary statistics\u2014including means, standard deviations, medians, and interquartile ranges across all baseline variables\u2014were identical to those of Srivilaithon 2023 [23], a previously included study conducted in a different country with a different sample size, consistent with data fabrication.')

doc.add_heading('Study characteristics', level=2)

add_para('The 9 included trials [24,15,20,25,26,27,23,12,13] enrolled 4,672 patients across four treatment nodes: etomidate (8 trials), ketamine (8 trials), propofol (1 trial), and ketofol (1 trial). Studies were conducted in ICU (5 trials), emergency department (2 trials), and mixed settings (2 trials), across six countries. Sample sizes ranged from 22 to 2,359 patients. The characteristics of included studies are presented in Table 1.')

doc.add_heading('Risk of bias', level=2)

add_para('Eight studies were rated as having \u201Csome concerns\u201D and one (Punt 2014 [20]) as \u201Chigh risk\u201D of bias (Figure 2). No trial blinded the clinician performing intubation except Cinar 2011 [15] (identical syringes prepared by an uninvolved clinician). Five trials blinded outcome assessors, ICU staff, or adjudicators [24,27,23,25,13]. Mortality, as an objective outcome, was considered less susceptible to bias from lack of blinding.')

doc.add_heading('Primary outcome: short-term mortality', level=2)

add_para('Nine trials contributed to the mortality network meta-analysis (Figure 3A). Network heterogeneity was low (I\u00B2 = 30%, \u03C4\u00B2 = 0.017). Formal assessment of global inconsistency was not possible because only one comparison (etomidate vs ketamine) was informed by multiple studies; node-splitting similarly could not be performed as no comparison had both direct and indirect evidence.')

add_para('Ketamine and etomidate probably result in similar short-term mortality (NMA estimate: OR 0.96, 95% CI 0.80\u20131.16; 7 direct studies, 4,345 patients; moderate certainty) (Figure 3B, Table 2). In the direct pairwise meta-analysis using the Paule\u2013Mandel estimator, the pooled OR was 1.02 (95% CI 0.77\u20131.36; 95% prediction interval 0.47\u20132.21), consistent with the NMA result; the small numerical difference reflects the different \u03C4\u00B2 estimators and the network structure. The comparison of ketamine vs propofol was based on a single trial and showed that ketamine may increase mortality compared with propofol, although the evidence is very uncertain (OR 1.53, 95% CI 0.80\u20132.93; low certainty). The indirect estimate for etomidate vs propofol was very uncertain (OR 0.63, 95% CI 0.32\u20131.24; very low certainty). Ketamine and ketofol may result in similar mortality (OR 0.84, 95% CI 0.41\u20131.72; 1 trial; low certainty). P-scores for mortality ranked propofol first (0.84), followed by ketofol (0.54), ketamine (0.38), and etomidate (0.24); however, these rankings should be interpreted with extreme caution given the low to very low certainty of evidence for all comparisons except etomidate\u2013ketamine.')

add_para('All results are summarized in Table 2.')

doc.add_heading('Secondary outcomes', level=2)

add_para('Compared with etomidate, ketamine probably increases cardiovascular collapse (OR 1.44, 95% CI 1.20\u20131.71; moderate certainty) and may increase post-induction hypotension (OR 1.34, 95% CI 1.07\u20131.68; low certainty) and peri-intubation vasopressor use (OR 1.45, 95% CI 1.21\u20131.74; low certainty). Vasopressor use at 24 hours showed substantial heterogeneity (I\u00B2 = 96%) and was not reliably estimable. No study reported vasopressor use at a 1-hour time point, precluding analysis at that protocol-specified interval.')

add_para('There is probably little or no difference in first-pass intubation success (OR 0.95, 95% CI 0.77\u20131.16; moderate certainty). Ketamine may result in little or no difference in peri-intubation cardiac arrest (OR 1.13, 95% CI 0.70\u20131.82; low certainty).')

doc.add_heading('Subgroup and sensitivity analyses', level=2)

add_para('The effect of etomidate versus ketamine on mortality was consistent across clinical settings (ED, ICU, mixed; test for subgroup differences p = 0.83) and across risk-of-bias categories (p = 0.88). Excluding studies with midazolam adjuncts did not materially change the results. Collapsing ketofol into the ketamine node (OR 0.95, 0.80\u20131.12) or removing the ketofol node entirely (OR 0.96, 0.80\u20131.16) yielded similar estimates. A post-hoc sensitivity analysis excluding the largest trial (Casey 2025, which contributed ~50% of all patients) showed that cardiovascular collapse (OR 1.59, 1.12\u20132.24) and peri-intubation vasopressor use (OR 1.50, 1.06\u20132.15) remained significantly higher with ketamine, whereas the hypotension finding was attenuated (OR 1.01, 0.59\u20131.73). For vasopressor use at 24 hours, excluding Casey resolved the heterogeneity (I\u00B2 dropped from 96%), with the single remaining study (a sepsis-only population) showing higher 24-hour vasopressor use with etomidate. Cardiac arrest was unchanged (OR 1.09, 0.60\u20131.95). eFigures in the Supplement.')

doc.add_heading('Certainty of evidence', level=2)

add_para('Certainty was moderate for the etomidate\u2013ketamine mortality comparison (downgraded for imprecision: the confidence interval does not exclude a clinically important absolute difference of 2\u20133%) and for cardiovascular collapse and first-pass success. Certainty was low or very low for all other comparisons and outcomes, primarily due to imprecision, indirectness (especially for comparisons involving propofol, which relied on a single trial or indirect evidence), and heterogeneous outcome definitions (Table 2).')

# ============================================================================
# DISCUSSION
# ============================================================================
doc.add_heading('Discussion', level=1)

add_para('In this systematic review and network meta-analysis of 9 randomized trials enrolling 4,672 critically ill adults, etomidate and ketamine probably result in similar short-term mortality, but confidence intervals do not exclude clinically important differences. Ketamine probably causes more peri-intubation cardiovascular instability than etomidate. Evidence for propofol and ketofol was limited to single trials.')

add_para('Our mortality findings are consistent with all five recent pairwise meta-analyses comparing etomidate and ketamine [7\u201310]. This analysis adds propofol and ketofol to the comparison for the first time. Notably, a large observational study from the Brazilian Airway Registry (BARCO) reported higher 28-day mortality with etomidate than with ketamine (60.5% vs 54.4%) [28]. The discordance between that observational finding and the randomized evidence synthesized here likely reflects residual confounding\u2014etomidate may be preferentially selected for patients perceived to be at higher hemodynamic risk\u2014though the possibility of a real but modest effect that randomized trials have been underpowered to detect individually cannot be excluded.')

add_para('Ketamine was associated with higher odds of cardiovascular collapse, post-induction hypotension, and peri-intubation vasopressor use compared with etomidate. This may seem paradoxical given ketamine\u2019s sympathomimetic properties, but critically ill patients are often catecholamine-depleted, blunting the indirect sympathetic stimulation on which ketamine\u2019s hemodynamic stability depends. In this setting, ketamine\u2019s direct myocardial depressant effect may predominate [6]. The protocol specified vasopressor analysis at up to 30 minutes, 1 hour, and 24 hours; at the 24-hour time point, substantial heterogeneity (I\u00B2 = 96%) precluded reliable estimation, highlighting the lack of standardized hemodynamic outcome definitions in this field.')

add_para('Two recent trials deserve specific discussion. The RSI trial [12] enrolled 2,359 patients\u2014nearly half of all patients in this review\u2014across 14 sites in the United States and was the first with mortality as the primary endpoint (28-day mortality 28.1% ketamine vs 29.1% etomidate). It also provided the most detailed hemodynamic data: cardiovascular collapse occurred in 22.1% of ketamine vs 17.0% of etomidate patients, largely driven by vasopressor escalation. These patterns are consistent with the pooled estimates in our network meta-analysis. Sensitivity analysis excluding the RSI trial showed that the cardiovascular collapse and peri-intubation vasopressor findings persisted, whereas the hypotension finding was attenuated. Whether dose differences across trials\u2014some permitted ketamine 1\u20132 mg/kg while others used a fixed 2 mg/kg\u2014contributed to the heterogeneity in hemodynamic effects warrants further investigation. PROMINE [13] is the only randomized trial comparing propofol with ketamine in critically ill adults. The trial enrolled 175 ICU patients in Brazil; results provided by the investigators showed that esketamine was associated with higher blood pressure in the periintubation period although numeric mortality was higher with ketamine than propofol (60% vs 50%, OR 1.53, 95% CI 0.80\u20132.93). Because PROMINE is the sole trial connecting propofol to the network, all propofol comparisons depend on it. The indirect estimate for etomidate versus propofol (OR 0.63, 95% CI 0.32\u20131.24; very low certainty) suggests large statistical imprecision remains for the comparison between propofol and etomidate. Similarly, the direct ketamine\u2013propofol comparison from PROMINE alone is too imprecise to draw definitive conclusions: the confidence interval is compatible with propofol reducing mortality by 20% or increasing it nearly threefold. What these estimates do show is that propofol is not obviously worse than etomidate or ketamine for mortality, which should motivate larger trials. Notably, a secondary analysis of the INTUBE cohort found that propofol was associated with peri-intubation cardiovascular instability (OR 1.28, 95% CI 1.05\u20131.57) but not with life-threatening cardiovascular collapse, suggesting that propofol-related hemodynamic effects may be transient and amenable to management [29]. No trial has directly compared propofol with etomidate. The single ketofol trial (KEEP PACE [25]) used reduced doses of both components with fentanyl co-administration, limiting its generalizability.')

add_para('Drug selection for emergency intubation is a modifiable factor that may be associated with important differences in outcomes for critically ill patients. The best available evidence compares ketamine with etomidate: mortality is probably similar but confidence intervals do not exclude clinically important differences, and ketamine probably causes more peri-intubation hemodynamic instability. For propofol, PROMINE is the first and only randomized trial in this setting; its results are hypothesis-generating but insufficient to guide practice. No trial has compared propofol with etomidate. Further trials\u2014particularly testing propofol against etomidate and ketamine\u2014are needed. Standardized definitions for hemodynamic outcomes, particularly vasopressor use, are also needed to allow meaningful comparison across future studies.')

add_para('This review has several limitations. First, most included trials were open-label, which may introduce performance bias for subjectively assessed outcomes such as hypotension. However, mortality\u2014our primary outcome\u2014is objective and less susceptible to ascertainment bias. Second, the treatment network is sparse: propofol and ketofol each connect to the network through a single trial, and the etomidate\u2013propofol comparison is entirely indirect. Formal consistency testing was not informative because no comparison had both direct and indirect evidence. Third, definitions of hemodynamic outcomes varied considerably across studies, particularly for hypotension thresholds and vasopressor time windows, contributing to clinical heterogeneity. Indeed, vasopressor use at 24 hours showed an I\u00B2 of 96%, precluding reliable estimation. Fourth, a planned subgroup analysis by baseline vasopressor use was not feasible because only three studies reported this variable, despite its likely role as an effect modifier. Fifth, we included two studies (Cinar 2011 [15], Punt 2014 [20]) in which the ketamine arm received a midazolam adjunct; sensitivity analyses excluding these trials yielded consistent results. Punt 2014 used a cluster-crossover design (alternating treatment periods); we used the study-reported estimates, which may not fully account for the cluster structure. Finally, our search was restricted to English-language publications, although one Turkish-language study was included based on its English abstract and AI-assisted translation.')

# ============================================================================
# CONCLUSIONS
# ============================================================================
doc.add_heading('Conclusions', level=1)

add_para('Etomidate and ketamine probably result in similar short-term mortality, but confidence intervals do not exclude clinically important differences in either direction, and ketamine is probably associated with more peri-intubation hemodynamic instability. Evidence for propofol is limited to a single trial. Large uncertainty remains regarding the optimal drug for emergency intubation of critically ill patients. Further trials\u2014particularly testing propofol against etomidate and ketamine\u2014are needed.')

doc.add_page_break()

# ============================================================================
# REFERENCES
# ============================================================================
doc.add_heading('References', level=1)

references = [
    "Russotto V, Myatra SN, Laffey JG, et al. Intubation practices and adverse peri-intubation events in critically ill patients from 29 countries. JAMA. 2021;325(12):1164\u20131172.",
    "De Jong A, Rolle A, Molinari N, et al. Cardiac arrest and mortality related to intubation procedure in critically ill adult patients: a multicenter cohort study. Crit Care Med. 2018;46(4):532\u2013539.",
    "Brown CA 3rd, Bair AE, Pallin DJ, Walls RM; NEAR III Investigators. Techniques, success, and adverse events of emergency department adult intubations. Ann Emerg Med. 2015;65(4):363\u2013370.e1.",
    "April MD, Arana A, Schauer SG, et al. Ketamine versus etomidate and peri-intubation hypotension: a National Emergency Airway Registry study. Acad Emerg Med. 2020;27(11):1106\u20131115.",
    "Albert SG, Ariyan S, Rather A. The effect of etomidate on adrenal function in critical illness: a systematic review. Intensive Care Med. 2011;37(6):901\u2013910.",
    "Waxman K, Shoemaker WC, Lippmann M. Cardiovascular effects of anesthetic induction with ketamine. Anesth Analg. 1980;59(5):355\u2013358.",
    "Kotani Y, Piersanti G, Maiucci G, et al. Etomidate as an induction agent for endotracheal intubation in critically ill patients: a meta-analysis of randomized trials. J Crit Care. 2023;77:154317.",
    "Greer A, Hewitt M, Khazaneh PT, et al. Ketamine versus etomidate for rapid sequence intubation: a systematic review and meta-analysis of randomized trials. Crit Care Med. 2025;53(2):e374\u2013e383.",
    "Daghmouri MA, Chaouch MA, Noomen M, et al. Etomidate versus ketamine for in-hospital rapid sequence intubation: a systematic review and meta-analysis. Eur J Emerg Med. 2025;32(3):160\u2013170.",
    "de Morais LB, Radel-Neto GR, Dos Santos Valsecchi VA, et al. Readdressing rapid sequence induction and intubation using ketamine or etomidate: a systematic review and meta-analysis of randomized clinical trials. Medicine. 2025;104(19):e42207.",
    "Koroki T, Kotani Y, Yaguchi T, et al. Ketamine versus etomidate as an induction agent for tracheal intubation in critically ill adults: a Bayesian meta-analysis. Crit Care. 2024;28(1):48.",
    "Casey JD, Seitz KP, Driver BE, et al. Ketamine or etomidate for tracheal intubation of critically ill adults. N Engl J Med. 2025. doi:10.1056/NEJMoa2511420.",
    "Schmidt RC, Zampieri FG, Ramos FJDS, et al. Propofol versus esketamine for rapid sequence intubation of critically ill patients (PROMINE): a randomized clinical trial. Intensive Care Med. 2025 (accepted).",
    "Hutton B, Salanti G, Caldwell DM, et al. The PRISMA extension statement for reporting of systematic reviews incorporating network meta-analyses of health care interventions: checklist and explanations. Ann Intern Med. 2015;162(11):777\u2013784.",
    "Cinar O, Pirat A, Zeyneloglu P, et al. Hemodynamic and metabolic responses to ketamine and etomidate sedations during endotracheal intubation in critically ill patients. Turk Yogun Bakim Dernegi Derg. 2011;9:77\u201384.",
    "Sterne JAC, Savovi\u0107 J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ. 2019;366:l4898.",
    "Balduzzi S, R\u00FCcker G, Schwarzer G. How to perform a meta-analysis with R: a practical tutorial. Evid Based Ment Health. 2019;22(4):153\u2013160.",
    "R\u00FCcker G, Krahn U, K\u00F6nig J, Efthimiou O, Papakonstantinou T, Schwarzer G. netmeta: Network meta-analysis using frequentist methods. R package version 3.3-1, 2024.",
    "R\u00FCcker G, Schwarzer G. Ranking treatments in frequentist network meta-analysis works without resampling methods. BMC Med Res Methodol. 2015;15:58.",
    "Punt CD, Dormans TPJ, Oosterhuis WP, et al. Etomidate and S-ketamine for the intubation of patients on the intensive care unit: a prospective, open-label study. Neth J Crit Care. 2014;18(2):4\u20137.",
    "Nikolakopoulou A, Higgins JPT, Papakonstantinou T, et al. CINeMA: An approach for assessing confidence in the results of a network meta-analysis. PLoS Med. 2020;17(4):e1003082.",
    "Agarwal D, Goyal C. Comparative outcomes of etomidate versus ketamine for emergency intubation in septic patients: a randomized controlled trial. SSR Inst Int J Life Sci. 2025;11(5):8348\u20138355.",
    "Srivilaithon W, Bumrungphanithaworn A, Daorattanachai K, et al. Clinical outcomes after a single induction dose of etomidate versus ketamine for emergency department sepsis intubation: a randomized controlled trial. Sci Rep. 2023;13(1):6362.",
    "Jabre P, Combes X, Lapostolle F, et al; for the KETASED Collaborative Study Group. Etomidate versus ketamine for rapid sequence intubation in acutely ill patients: a multicentre randomised controlled trial. Lancet. 2009;374(9686):293\u2013300.",
    "Smischney NJ, Nicholson WT, Brown DR, et al. Ketamine/propofol admixture vs etomidate for intubation in the critically ill: KEEP PACE randomized clinical trial. J Trauma Acute Care Surg. 2019;87(4):883\u2013891.",
    "Matchett G, Gasanova I, Riccio CA, et al. Etomidate versus ketamine for emergency endotracheal intubation: a randomized clinical trial. Intensive Care Med. 2022;48(1):78\u201391.",
    "Knack SKS, Prekker ME, Moore JC, et al. The effect of ketamine versus etomidate for rapid sequence intubation on maximum Sequential Organ Failure Assessment score: a randomized clinical trial. J Emerg Med. 2023;65(5):e371\u2013e382.",
    "Maia IWA, Decker SRR, Oliveira e Silva L, et al; for the Brazilian Airway Registry Cooperation (BARCO) group. Ketamine, etomidate, and mortality in emergency department intubations. JAMA Netw Open. 2025;8(12):e2548060.",
    "Russotto V, Tassistro E, Myatra SN, et al; for the INTUBE Study Investigators. Peri-intubation cardiovascular collapse in patients who are critically ill: insights from the INTUBE study. Am J Respir Crit Care Med. 2022;206(4):449\u2013458.",
]

for i, ref in enumerate(references, 1):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    r = p.add_run(f"{i}. {ref}")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)

doc.add_page_break()

# ============================================================================
# TABLE 1: Study Characteristics
# ============================================================================
# Switch to landscape
new_section = doc.add_section(WD_ORIENT.LANDSCAPE)
new_section.orientation = WD_ORIENT.LANDSCAPE
new_section.page_width = Inches(11)
new_section.page_height = Inches(8.5)
new_section.top_margin = Inches(0.7)
new_section.bottom_margin = Inches(0.7)
new_section.left_margin = Inches(0.7)
new_section.right_margin = Inches(0.7)

add_para("Table 1. Characteristics of Included Studies", bold=True, space_after=6, font_size=11)

table1 = doc.add_table(rows=10, cols=8)
table1.style = 'Table Grid'
table1.alignment = WD_TABLE_ALIGNMENT.CENTER

# Headers
headers = ["Study", "N", "Population", "Comparison", "Induction dose", "NMBA\u2016", "Primary outcome (original)", "Key secondary outcomes"]
for i, h in enumerate(headers):
    set_cell_text(table1.rows[0].cells[i], h, bold=True, size=8)
    set_cell_shading(table1.rows[0].cells[i], "D9E2F3")

# Data rows
data = [
    ["Jabre 2009 (KETASED)", "469", "Prehospital/ED, multicenter (77), France", "E vs K", "E 0.3 vs K 2 mg/kg", "Sux 1 mg/kg", "Maximum SOFA (days 1\u20133)", "28-d mortality; cortisol levels"],
    ["Cinar 2011*", "22", "ICU, single-center, Turkey", "E vs K", "E 0.3 vs K 2 mg/kg + midaz 0.03 mg/kg", "None", "Heart rate, MAP", "Cortisol levels; SOFA day 9"],
    ["Punt 2014*", "301", "ICU, single-center, Netherlands", "E vs SK", "E 0.2\u20130.3 vs SK 0.5 mg/kg + midaz 2.5 mg", "Roc", "28-d mortality", "Cortisol levels; ICU LOS"],
    ["Smischney 2019 (KEEP PACE)", "152", "ICU, single-center, USA", "E vs Ketofol", "E 0.15 vs KP 0.5 + 0.5 mg/kg\u2020", "Sux (57%) / Roc (36%)", "MAP change at 5 min", "New vasopressor use; cortisol levels"],
    ["Matchett 2022 (EvK)", "791", "ICU, single-center, USA", "E vs K", "E 0.2\u20130.3 vs K 1\u20132 mg/kg", "Roc (81%) / Sux (18%)", "Day 7 survival", "28-d mortality"],
    ["Knack 2023", "143", "ED, single-center, USA", "E vs K", "E 0.3 vs K 2 mg/kg", "Sux (92%)", "Maximum SOFA\u2021", "30-d mortality; hypotension"],
    ["Srivilaithon 2023", "260", "ED (sepsis), single-center, Thailand", "E vs K", "E 0.2\u20130.3 vs K 1\u20132 mg/kg", "Sux 1.5 mg/kg\u00A7", "28-d survival", "Hypotension; vasopressor use 24 h"],
    ["Casey 2025 (RSI)", "2,359", "ED + ICU, multicenter (14), USA", "E vs K", "E 0.2\u20130.3 vs K 1\u20132 mg/kg", "Roc (69%) / Sux (31%)", "28-d in-hospital mortality", "CV collapse"],
    ["Schmidt 2025 (PROMINE)", "175", "ICU, multicenter (2), Brazil", "P vs ESK", "P 1.5 vs ESK 2 mg/kg", "Roc 1.2 mg/kg (98%)", "Lowest MAP within 10 min", "Hospital mortality; CV collapse"],
]

for r_idx, row_data in enumerate(data):
    for c_idx, val in enumerate(row_data):
        align = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
        set_cell_text(table1.rows[r_idx + 1].cells[c_idx], val, size=8, alignment=align)

# Set column widths
widths = [Cm(3.5), Cm(1.2), Cm(4.0), Cm(2.2), Cm(3.8), Cm(3.2), Cm(3.8), Cm(3.8)]
for row in table1.rows:
    for i, w in enumerate(widths):
        row.cells[i].width = w

# Footnotes
footnotes = (
    "N = patients analyzed; E = etomidate; K = ketamine; SK = S-ketamine; ESK = esketamine; "
    "P = propofol; KP = ketamine\u2013propofol admixture; Sux = succinylcholine; Roc = rocuronium; "
    "ED = emergency department; ICU = intensive care unit; NMBA = neuromuscular blocking agent; "
    "CV = cardiovascular; LOS = length of stay; MAP = mean arterial pressure; SOFA = Sequential Organ Failure Assessment.\n"
    "*Ketamine arm included midazolam adjunct \u2014 flagged for sensitivity analysis.\n"
    "\u2020Both drugs at reduced doses; fentanyl 50 \u00B5g co-administered.\n"
    "\u2021Primary outcome changed mid-trial from mortality to maximum SOFA.\n"
    "\u00A7NMBA use differed significantly between groups.\n"
    "\u2016NMBA reporting varies across studies: some report intended treatment, others actual administration."
)
add_para(footnotes, font_size=8, space_after=0)

doc.add_page_break()

# ============================================================================
# TABLE 2: NMA Results
# ============================================================================
add_para("Table 2. Summary of Network Meta-Analysis Results: Primary and Secondary Outcomes", bold=True, space_after=6, font_size=11)

table2 = doc.add_table(rows=13, cols=6)
table2.style = 'Table Grid'
table2.alignment = WD_TABLE_ALIGNMENT.CENTER

# Headers
headers2 = ["Outcome / Comparison", "Studies, k (N)", "Evidence", "OR (95% CI)", "I\u00B2", "Certainty\u1D48"]
for i, h in enumerate(headers2):
    set_cell_text(table2.rows[0].cells[i], h, bold=True, size=9)
    set_cell_shading(table2.rows[0].cells[i], "D9E2F3")

# Mortality section header
set_cell_text(table2.rows[1].cells[0], "Short-term mortality (primary outcome)", bold=True, italic=True, size=9, alignment=WD_ALIGN_PARAGRAPH.LEFT)
for c in range(1, 6):
    set_cell_text(table2.rows[1].cells[c], "", size=9)
# Merge mortality header row
table2.rows[1].cells[0].merge(table2.rows[1].cells[5])
set_cell_text(table2.rows[1].cells[0], "Short-term mortality (primary outcome)", bold=True, italic=True, size=9, alignment=WD_ALIGN_PARAGRAPH.LEFT)

mort_data = [
    ["   Ketamine vs Etomidate", "7 (4,345)", "Direct", "0.96 (0.80\u20131.16)", "30%", "Moderate"],
    ["   Ketofol vs Etomidate", "1 (152)", "Direct", "0.84 (0.41\u20131.72)", "", "Low"],
    ["   Propofol vs Etomidate", "0 (\u2014)", "Indirect", "0.63 (0.32\u20131.24)", "", "Very low"],
    ["   Ketamine vs Propofol", "1 (175)", "Direct", "1.53 (0.80\u20132.93)", "", "Low"],
]

for r_idx, row_data in enumerate(mort_data):
    for c_idx, val in enumerate(row_data):
        align = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
        set_cell_text(table2.rows[r_idx + 2].cells[c_idx], val, size=9, alignment=align)

# Secondary outcomes header
set_cell_text(table2.rows[6].cells[0], "Secondary outcomes \u2014 Ketamine vs Etomidateᵇ", bold=True, italic=True, size=9, alignment=WD_ALIGN_PARAGRAPH.LEFT)
table2.rows[6].cells[0].merge(table2.rows[6].cells[5])
set_cell_text(table2.rows[6].cells[0], "Secondary outcomes \u2014 Ketamine vs Etomidateᵇ", bold=True, italic=True, size=9, alignment=WD_ALIGN_PARAGRAPH.LEFT)

sec_data = [
    ["   Cardiovascular collapse", "3 [2] (3,331)", "NMA", "1.44 (1.20\u20131.71)", "0%", "Moderate"],
    ["   Post-induction hypotension", "4 [3] (2,871)", "NMA", "1.34 (1.07\u20131.68)", "0%", "Low"],
    ["   Vasopressor, peri-intubation", "5 [3] (3,413)", "NMA", "1.45 (1.21\u20131.74)", "0%", "Low"],
    ["   Vasopressor, 24 hoursᵃ", "2 [2] (2,421)", "PW", "0.58 (0.14\u20132.33)", "96%", "Very low"],
    ["   First-pass intubation success", "5 [4] (3,718)", "NMA", "0.95 (0.77\u20131.16)", "0%", "Moderate"],
    ["   Peri-intubation cardiac arrest", "7 [5] (4,142)", "NMA", "1.13 (0.70\u20131.82)", "0%", "Low"],
]

for r_idx, row_data in enumerate(sec_data):
    for c_idx, val in enumerate(row_data):
        align = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
        set_cell_text(table2.rows[r_idx + 7].cells[c_idx], val, size=9, alignment=align)

# Set column widths for table 2
widths2 = [Cm(6.0), Cm(3.5), Cm(2.2), Cm(4.5), Cm(1.8), Cm(3.0)]
for row in table2.rows:
    for i, w in enumerate(widths2):
        row.cells[i].width = w

# Footnotes for table 2
fn2 = (
    "OR = odds ratio; CI = confidence interval; NMA = network meta-analysis; PW = pairwise meta-analysis. "
    "For mortality, I\u00B2 refers to network-level heterogeneity; for secondary outcomes, I\u00B2 is comparison-specific. "
    "For mortality comparisons, OR < 1 favors the first-named treatment (lower mortality). "
    "For secondary outcomes, OR > 1 indicates a higher event rate with ketamine vs etomidate. "
    "Certainty of evidence assessed using the CINeMA framework.\n"
    "\u1D43Substantial heterogeneity; individual study ORs were 0.87 (Casey 2025) and 0.28 (Srivilaithon 2023). Result should be interpreted with caution.\n"
    "\u1D47Studies, k [direct]: total studies contributing to the NMA [direct ketamine vs etomidate comparisons]. Remaining studies contribute indirect evidence through the propofol or ketofol nodes.\n"
    "\u1D9CSecondary outcomes for propofol comparisons are available in the Supplement (eFigures).\n"
    "\u1D48Reasons for downgrading certainty: K vs E mortality: imprecision; Ketofol vs E: imprecision, indirectness; "
    "P vs E: bias, indirectness, imprecision; K vs P: imprecision, indirectness; CV collapse: bias; hypotension: bias, indirectness; "
    "vasopressor (peri): bias, indirectness; vasopressor (24h): bias, heterogeneity, imprecision; first-pass: bias; "
    "cardiac arrest: bias, imprecision. See eTables in Supplement for detailed CINeMA assessments."
)
add_para(fn2, font_size=8, space_after=0)

# Switch back to portrait for figure legends
new_section2 = doc.add_section(WD_ORIENT.PORTRAIT)
new_section2.orientation = WD_ORIENT.PORTRAIT
new_section2.page_width = Inches(8.5)
new_section2.page_height = Inches(11)
new_section2.top_margin = Inches(1)
new_section2.bottom_margin = Inches(1)
new_section2.left_margin = Inches(1)
new_section2.right_margin = Inches(1)

# ============================================================================
# FIGURE LEGENDS
# ============================================================================
doc.add_heading('Figure Legends', level=1)

p = doc.add_paragraph()
r = p.add_run('Figure 1. PRISMA flow diagram. ')
r.bold = True
r.font.name = 'Times New Roman'
r = p.add_run('Study identification, screening, and inclusion process. MEDLINE and Embase were searched from inception to December 2025. Nine randomized controlled trials met the inclusion criteria.')
r.font.name = 'Times New Roman'

add_para("", space_after=12)

p = doc.add_paragraph()
r = p.add_run('Figure 2. Risk of bias assessment (Cochrane RoB 2 tool). ')
r.bold = True
r.font.name = 'Times New Roman'
r = p.add_run('(A) Traffic-light plot showing domain-level judgements for each study. D1 = randomization process; D2 = deviations from intended interventions; D3 = missing outcome data; D4 = measurement of the outcome; D5 = selection of the reported result. (B) Summary plot showing the distribution of risk-of-bias judgements across all studies. Eight studies were rated as \u201Csome concerns\u201D and one (Punt 2014) as \u201Chigh risk,\u201D driven by the cluster-randomized design and midazolam adjunct in the ketamine arm.')
r.font.name = 'Times New Roman'

add_para("", space_after=12)

p = doc.add_paragraph()
r = p.add_run('Figure 3. Network geometry and pairwise meta-analysis of etomidate vs ketamine for short-term mortality. ')
r.bold = True
r.font.name = 'Times New Roman'
r = p.add_run('(A) Network geometry for the mortality analysis. Node size is proportional to the total number of patients randomized to each treatment. Edge thickness is proportional to the number of studies for each direct comparison. The etomidate\u2013ketamine comparison dominates the network (7 of 9 studies). (B) Forest plot showing the pairwise random-effects meta-analysis for etomidate vs ketamine (7 studies, 4,345 patients). Squares represent individual study estimates (size proportional to weight); the diamond represents the pooled estimate. The pooled OR was 1.02 (95% CI 0.77\u20131.36; 95% prediction interval 0.47\u20132.21; I\u00B2 = 30%), consistent with no difference in mortality between agents.')
r.font.name = 'Times New Roman'

# ============================================================================
# SAVE
# ============================================================================
output_path = "/Users/fernandogodinhozampieri/Desktop/intubation_sr/manuscript/output/manuscript.docx"
doc.save(output_path)
print(f"Saved to {output_path}")
