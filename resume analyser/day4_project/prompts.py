"""
prompts.py — all 8 system prompts used by analyzer.py.

Task 3 of the lab (Track A).

The prompts follow the ICCO framework:
- Instruction
- Context
- Constraints
- Output
"""


# ---------------------------------------------------------------------------
# Extraction prompts
# ---------------------------------------------------------------------------

RESUME_PROFILE_PROMPT = """
Instruction:
Extract a structured candidate profile from the résumé text supplied by the
user.

Context:
The input contains plain text extracted from a candidate's résumé. Identify
the candidate's contact information, summary, education, projects, experience,
and technical skills.

Constraints:
- Extract only information literally present in the résumé.
- Never invent, infer, assume, or add missing information.
- Preserve names, organisations, titles, dates, technologies, and bullet
  content as closely as possible.
- Do not rewrite, improve, paraphrase, or generate résumé content.
- Keep individual project and experience bullets as separate strings.
- Classify explicitly stated skills into the most suitable skill category.
- If a field is absent, return an empty string or empty array.
- Include every field shown in the schema.
- Return valid JSON data types only.

Output:
{
  "name": "string",
  "contact": {
    "email": "string",
    "phone": "string",
    "linkedin": "string",
    "github": "string",
    "portfolio": "string"
  },
  "summary": "string",
  "education": [
    {
      "school": "string",
      "degree": "string",
      "graduation_date": "string",
      "courses": ["string"]
    }
  ],
  "projects": [
    {
      "title": "string",
      "date": "string",
      "bullets": ["string"]
    }
  ],
  "experience": [
    {
      "title": "string",
      "company": "string",
      "date": "string",
      "bullets": ["string"]
    }
  ],
  "skills": {
    "languages": ["string"],
    "frameworks": ["string"],
    "tools": ["string"],
    "concepts": ["string"],
    "platforms": ["string"]
  }
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""


JD_PROFILE_PROMPT = """
Instruction:
Extract a structured role profile from the job description supplied by the
user.

Context:
The input is a complete job posting. Identify the role details, mandatory and
preferred skills, technologies, responsibilities, behavioural expectations,
and explicit screening conditions.

Constraints:
- Extract only information explicitly present in the job description.
- Never invent, infer, assume, or add unstated requirements.
- Do not rewrite or improve the job description.
- Preserve official role names, technology names, and important terminology.
- Place mandatory requirements in required_skills.
- Place optional, advantageous, preferred, or good-to-have requirements in
  preferred_skills.
- Place named languages, frameworks, platforms, products, and software in
  tools_technologies.
- Place explicit mandatory screening conditions in deal_breakers.
- If a field is absent, return an empty string or empty array.
- Include every field shown in the schema.
- Return valid JSON data types only.

Output:
{
  "job_title": "string",
  "company": "string",
  "location": "string",
  "experience_level": "string",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "tools_technologies": ["string"],
  "responsibilities": ["string"],
  "soft_skills": ["string"],
  "buzzwords": ["string"],
  "deal_breakers": ["string"]
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""


# ---------------------------------------------------------------------------
# Evaluation prompts
# ---------------------------------------------------------------------------

KEYWORD_MATCH_PROMPT = """
Instruction:
Compare the supplied résumé profile with the supplied job-description profile.

Context:
Both profiles are complete JSON objects. Check whether each required and
preferred JD skill appears in the résumé profile.

A total mismatch is valid. If nothing matches, return an empty present array
and list the missing terms. Do not ask for more information.

Scoring:
keyword_match_score =
round(100 * required skills found / max(1, total required skills))

Constraints:
- Use only the supplied profiles.
- Do not invent candidate skills.
- Count a semantic equivalent only when the meaning is clearly the same.
- exact_match is true only for the same term or a direct spelling variant.
- Keep why_it_matters to 25 words or fewer.
- suggested_section is diagnostic only.
- Do not rewrite or generate résumé content.
- Return every field in the schema.
- keyword_match_score must be an integer from 0 to 100.

Output:
{
  "present": [
    {
      "keyword": "string",
      "category": "language|framework|tool|concept|soft_skill|buzzword",
      "found_in": "summary|projects|experience|education|skills",
      "exact_match": true
    }
  ],
  "missing": [
    {
      "keyword": "string",
      "category": "language|framework|tool|concept|soft_skill|buzzword",
      "importance": "required|preferred",
      "suggested_section": "skills|projects|experience|summary",
      "why_it_matters": "string"
    }
  ],
  "keyword_match_score": 0
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""


BULLET_QUALITY_PROMPT = """
Instruction:
Evaluate every project and experience bullet in the supplied résumé profile.

Context:
Use the Action, Technology, Impact rubric:

- L1_OK: The bullet states an action but does not clearly include both a
  specific technology and an impact.
- L2_BETTER: The bullet states an action and names a specific technology,
  tool, method, system, platform, or language, but lacks impact.
- L3_BEST: The bullet includes an action, a specific technology, and a
  measurable or concrete impact.

Action means what the candidate did.
Technology means the specific tool, language, platform, framework, system,
process, or method used.
Impact means a measurable or concrete result, such as improved performance,
reduced time, increased accuracy, completed delivery, users supported, or a
numeric outcome.

Calculate bullet_quality_avg as:

round(100 * sum of level scores / (3 * number of bullets))

Use L1_OK = 1, L2_BETTER = 2, and L3_BEST = 3.
Return 0 if there are no bullets.

Constraints:
- Evaluate only project and experience bullets.
- Copy each bullet_text exactly.
- Do not rewrite, improve, shorten, or correct any bullet.
- Do not invent technologies, numbers, achievements, or outcomes.
- what_is_missing must be diagnostic only and no longer than 15 words.
- Use JSON booleans for the three has_ fields.
- Return every field in the schema.
- Return bullet_quality_avg as an integer from 0 to 100.

Output:
{
  "bullets": [
    {
      "source": "projects|experience",
      "parent_title": "string",
      "bullet_text": "string",
      "has_action_verb": true,
      "has_specific_technology": true,
      "has_measurable_impact": false,
      "level": "L1_OK|L2_BETTER|L3_BEST",
      "what_is_missing": "string"
    }
  ],
  "bullet_quality_avg": 0
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""

JARGON_AUDIT_PROMPT = """
Instruction:
Compare the terminology in the supplied résumé profile against the terminology
in the supplied job-description profile.

Identify terms in résumé bullets that likely describe relevant experience but
use language that may not match the terminology used by the employer or an ATS.

Context:
Perform the comparison dynamically from the two supplied profiles. Do not use
a fixed translation dictionary.

Flag likely equivalent concepts that are worded differently. Examples may
include a specialised academic term versus a common industry term, an internal
project label versus a recognised technical term, or an abbreviation that the
job description does not use.

Severity rules:
- high: The résumé term may be relevant, but the job description uses no
  recognisably equivalent language and an ATS may miss the connection.
- medium: There is partial terminology overlap, but the relationship is not
  immediately clear.
- low: The job description already uses matching or closely adjacent
  terminology, so the risk is minor.

Calculate jargon_score using:

max(0, 100 - 10 × high_count - 5 × medium_count - 2 × low_count)

Constraints:
- Use only the supplied résumé and job-description profiles.
- Do not invent an equivalence when the concepts are materially different.
- bullet_text must be copied verbatim.
- term_used must identify the résumé wording being evaluated.
- suggested_translation may name the corresponding JD terminology only.
- suggested_translation must not become a rewritten résumé bullet.
- Do not generate replacement content.
- Return an empty flags array and a score of 100 when no terminology problems
  are found.
- Return a valid score from 0 to 100.
- Include every field shown in the schema.

Output:
{
  "flags": [
    {
      "bullet_text": "string",
      "term_used": "string",
      "suggested_translation": "string",
      "severity": "low|medium|high"
    }
  ],
  "jargon_score": 0
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""


STRUCTURE_AUDIT_PROMPT = """
Instruction:
Audit the supplied plain résumé text for general ATS parseability and résumé
structure.

Context:
Use these general ATS-parseability conventions:

- A single-column layout is generally easier for an ATS to parse.
- Standard section headings such as Summary, Education, Experience, Projects,
  and Skills improve section recognition.
- Experience and education should normally use reverse-chronological order.
- Contact information should appear near the top.
- Résumé length should be appropriate for the candidate's experience level.
- Important information should not depend on images, graphics, icons, charts,
  text boxes, or decorative elements.
- Dates, titles, organisations, and bullet points should be consistently
  presented.

Because the input is extracted plain text, only make formatting conclusions
that the text reasonably supports. Use false or add an ATS red flag when the
evidence is uncertain.

Determine structure_score holistically from 0 to 100. Higher scores indicate
clear organisation and likely ATS readability. Reduce the score for missing
standard sections, unclear ordering, absent contact details, excessive length,
or evidence of parsing problems.

Constraints:
- Evaluate only the supplied résumé text.
- Do not claim certainty about visual formatting that cannot be verified from
  extracted text.
- Do not rewrite section headings, bullets, or résumé content.
- ats_red_flags must cite evidence from the supplied text or explain the
  uncertainty.
- section_headings_present and section_headings_missing must contain heading
  names only.
- page_count_estimate must be an integer of at least 1.
- Return a valid score from 0 to 100.
- Include every field shown in the schema.

Output:
{
  "page_count_estimate": 1,
  "single_column_likely": true,
  "section_headings_present": ["string"],
  "section_headings_missing": ["string"],
  "reverse_chronological_likely": true,
  "contact_info_at_top": true,
  "length_appropriate": true,
  "no_images_or_graphics": true,
  "ats_red_flags": [
    {
      "issue": "string",
      "evidence": "string"
    }
  ],
  "structure_score": 0
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""


BACKGROUND_FIT_PROMPT = """
Instruction:
Assess how well the candidate's stated education and experience align with the
requirements of the supplied job-description profile.

Context:
Use only the education, experience, and projects contained in the résumé
profile and the requirements and responsibilities contained in the
job-description profile.

Evaluate whether the candidate's documented background provides relevant
academic preparation, practical exposure, transferable experience, and an
appropriate level of responsibility for the role.

Constraints:
- Use only information present in the supplied profiles.
- Do not use external degree classifications, university rankings, industry
  assumptions, or unstated knowledge.
- Do not assume the candidate has experience that is not documented.
- Separate direct alignment from transferable alignment.
- candidate_background_summary must contain one or two sentences.
- role_requirements_summary must contain one or two sentences.
- alignment_commentary must contain two or three diagnostic sentences.
- Do not rewrite or generate résumé content.
- Return a valid background_fit_score from 0 to 100.
- Include every field shown in the schema.

Output:
{
  "candidate_background_summary": "string",
  "role_requirements_summary": "string",
  "alignment_commentary": "string",
  "background_fit_score": 0
}

Output ONLY a valid JSON object matching the schema above. No prose. No markdown fences. No commentary. Never rewrite or generate résumé content.
"""


# ---------------------------------------------------------------------------
# Synthesis prompt
# ---------------------------------------------------------------------------

OVERALL_SUMMARY_PROMPT = """
Instruction:
Produce a concise executive summary of the supplied résumé screening report.

Context:
The report contains the candidate's overall score, keyword match, bullet
quality, terminology audit, structural audit, and background-fit assessment.

Constraints:
- Return exactly three Markdown bullet points.
- Start each bullet with "- ".
- The first bullet must state the strongest area supported by the report.
- The second bullet must state the most important weakness or gap.
- The third bullet must state the overall screening conclusion and whether the
  evidence supports advancing the candidate.
- Keep each bullet to no more than two sentences.
- Use only information contained in the report.
- Clearly represent uncertainty.
- Provide diagnostic feedback only.
- Do not rewrite, improve, or generate résumé content.
- Do not include a heading, introduction, conclusion, JSON, or code fence.

Output:
Exactly three plain Markdown bullet points.
"""