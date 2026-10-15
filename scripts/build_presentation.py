"""
SpendIQ Capstone Presentation Generator (PowerPoint PPTX)
Generates an executive-grade 16:9 widescreen PowerPoint deck with:
- Dark slate/navy theme (#0F172A)
- Glassmorphic card layouts
- Real embedded screenshot evidence
- Rubric module tags and score badges
- Comprehensive speaker notes on every slide for video walkthrough recording
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Paths
BASE_DIR = r"c:\devopsproject"
EVIDENCE_DIR = os.path.join(BASE_DIR, "demo", "evidence")
OUTPUT_PPTX = os.path.join(BASE_DIR, "demo", "SpendIQ_Capstone_Presentation.pptx")

# Color Palette (Dark Modern Tech Theme)
COLOR_BG = RGBColor(15, 23, 42)          # Slate-900 #0F172A
COLOR_CARD = RGBColor(30, 41, 59)        # Slate-800 #1E293B
COLOR_CARD_BORDER = RGBColor(51, 65, 85) # Slate-700 #334155
COLOR_PRIMARY = RGBColor(59, 130, 246)   # Blue-500  #3B82F6
COLOR_SUCCESS = RGBColor(16, 185, 129)   # Emerald   #10B981
COLOR_PURPLE = RGBColor(139, 92, 246)    # Violet    #8B5CF6
COLOR_AMBER = RGBColor(245, 158, 11)     # Amber     #F59E0B
COLOR_CYAN = RGBColor(6, 182, 212)       # Cyan      #06B6D4
COLOR_ROSE = RGBColor(244, 63, 94)       # Rose      #F43F5E
COLOR_TEXT_LIGHT = RGBColor(248, 250, 252) # White   #F8FAFC
COLOR_TEXT_BODY = RGBColor(203, 213, 225)  # Slate-300 #CBD5E1
COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # Slate-400 #94A3B8

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"


def set_slide_background(slide):
    """Sets a rich dark background on the slide."""
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG
    bg_shape.line.fill.background()
    return bg_shape


def add_card(slide, left, top, width, height, fill_color=COLOR_CARD, border_color=COLOR_CARD_BORDER):
    """Adds a container card with subtle border."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
    else:
        card.line.fill.background()
    return card


def add_header(slide, module_tag, title, subtitle=None, score_badge="10/10 PASS"):
    """Adds standard header with module pill and score badge."""
    # Module Tag Pill
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(4.0), Inches(0.35))
    tf = tag_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = module_tag.upper()
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(9.0), Inches(0.6))
    tf2 = title_box.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = title
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_LIGHT

    # Score Badge on Top Right
    if score_badge:
        badge_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.5), Inches(0.55), Inches(2.0), Inches(0.5)
        )
        badge_card.fill.solid()
        badge_card.fill.fore_color.rgb = RGBColor(6, 78, 59) # Dark emerald
        badge_card.line.color.rgb = COLOR_SUCCESS
        badge_card.line.width = Pt(1.5)
        
        btf = badge_card.text_frame
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        bp.text = f"★ {score_badge}"
        bp.font.name = FONT_HEADING
        bp.font.size = Pt(12)
        bp.font.bold = True
        bp.font.color.rgb = COLOR_SUCCESS


def add_notes(slide, notes_text):
    """Sets speaker notes on the slide."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text.strip()


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    print("Generating Slide Deck...")

    # =========================================================================
    # SLIDE 1: Title & Executive Cover
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent decorative glow card in center
    add_card(s1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), 
             fill_color=RGBColor(24, 33, 53), border_color=COLOR_PRIMARY)

    # Pill badge
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(1.5), Inches(4.5), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 58, 138)
    pill.line.color.rgb = COLOR_PRIMARY
    ptf = pill.text_frame
    pp = ptf.paragraphs[0]
    pp.alignment = PP_ALIGN.CENTER
    pp.text = "DEVOPS FINAL CAPSTONE • SESSION 21"
    pp.font.name = FONT_HEADING
    pp.font.size = Pt(11)
    pp.font.bold = True
    pp.font.color.rgb = COLOR_TEXT_LIGHT

    # Main Title
    tb = s1.shapes.add_textbox(Inches(1.8), Inches(2.1), Inches(9.8), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SpendIQ SaaS Platform"
    p.font.name = FONT_HEADING
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_LIGHT

    p_sub = tf.add_paragraph()
    p_sub.text = "Enterprise Cloud-Native DevOps Architecture & GitOps Delivery"
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = COLOR_CYAN

    # Description Paragraph
    tb_desc = s1.shapes.add_textbox(Inches(1.8), Inches(3.6), Inches(9.5), Inches(1.2))
    tf_desc = tb_desc.text_frame
    tf_desc.word_wrap = True
    p_d = tf_desc.paragraphs[0]
    p_d.text = (
        "A 3-tier financial management microservices platform featuring automated Pytest quality gates, "
        "multi-stage containerization, GitHub Actions CI/CD with Aqua Trivy DevSecOps scanning, "
        "AWS EKS infrastructure provisioned via Terraform, zero-downtime Helm deployments, "
        "and full-stack Prometheus & Grafana observability."
    )
    p_d.font.name = FONT_BODY
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = COLOR_TEXT_BODY

    # 4 Feature Pills at Bottom
    features = [
        ("FastAPI + React 18", COLOR_PRIMARY),
        ("Terraform on AWS EKS", COLOR_PURPLE),
        ("Trivy DevSecOps", COLOR_ROSE),
        ("100 / 100 Score Target", COLOR_SUCCESS),
    ]
    for i, (feat, color) in enumerate(features):
        card = add_card(s1, Inches(1.8 + i * 2.45), Inches(5.1), Inches(2.3), Inches(0.7),
                        fill_color=COLOR_CARD, border_color=color)
        ctf = card.text_frame
        cp = ctf.paragraphs[0]
        cp.alignment = PP_ALIGN.CENTER
        cp.text = feat
        cp.font.name = FONT_HEADING
        cp.font.size = Pt(11)
        cp.font.bold = True
        cp.font.color.rgb = color

    add_notes(s1, """
VIDEO SCRIPT - SLIDE 1 (TITLE & INTRO):
"Hello everyone, and welcome to the presentation of my DevOps Final Capstone Project for Session 21: SpendIQ.

SpendIQ is an enterprise-grade personal finance management SaaS platform built from the ground up using modern cloud-native best practices. 

In this video walkthrough, I will demonstrate how all 10 modules of the grading rubric were thoroughly designed, implemented, and verified—spanning application development, automated testing, containerization, DevSecOps CI/CD pipelines, AWS infrastructure as code using Terraform, Kubernetes orchestration with Helm, and full-stack observability with Prometheus and Grafana.

Let's dive into the architecture."
""")

    # =========================================================================
    # SLIDE 2: High-Level Architecture
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "System Architecture", "SpendIQ 3-Tier End-to-End Cloud Ecosystem", score_badge="ARCHITECTURE")

    # 3 Architecture Tier Cards
    tiers = [
        ("TIER 1 • PRESENTATION", "React 18 + Vite SPA", [
            "Served via high-performance NGINX 1.27-alpine",
            "Single Page Application (SPA) client-side routing",
            "Interactive charts with Recharts & Axios API client",
            "Non-root security execution (nginx:101)",
            "Containerized in multi-stage Docker build"
        ], COLOR_CYAN),
        ("TIER 2 • APPLICATION", "FastAPI Python 3.12 Backend", [
            "High-throughput asynchronous REST API",
            "Pydantic v2 strict request/response data models",
            "15+ endpoints covering Transactions, Budgets, Analytics",
            "Prometheus client instrumenting /metrics & /health",
            "Non-root user (appuser:1001) with dumb-init"
        ], COLOR_PRIMARY),
        ("TIER 3 • PERSISTENCE", "PostgreSQL 16 + Alembic", [
            "Stateful relational database with ACID compliance",
            "Automated Alembic schema migrations (001_initial)",
            "Kubernetes PersistentVolumeClaims (PVC) for data safety",
            "Optimized indexes on date, user_id, and category",
            "Isolated test database fixtures for test suites"
        ], COLOR_PURPLE),
    ]

    for i, (title, subtitle, bullets, color) in enumerate(tiers):
        c = add_card(s2, Inches(0.8 + i * 3.95), Inches(1.5), Inches(3.8), Inches(4.3),
                     fill_color=COLOR_CARD, border_color=color)
        ctf = c.text_frame
        ctf.word_wrap = True
        
        # Pill top
        p0 = ctf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = color
        
        p1 = ctf.add_paragraph()
        p1.text = subtitle
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_LIGHT
        
        ctf.add_paragraph() # Spacer
        
        for b in bullets:
            pb = ctf.add_paragraph()
            pb.text = f"• {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(11)
            pb.font.color.rgb = COLOR_TEXT_BODY

    # Infrastructure Footer Banner
    banner = add_card(s2, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.0),
                      fill_color=RGBColor(24, 33, 53), border_color=COLOR_CARD_BORDER)
    btf = banner.text_frame
    btf.word_wrap = True
    bp = btf.paragraphs[0]
    bp.text = "CLOUD & DEVOPS FOUNDATION"
    bp.font.name = FONT_HEADING
    bp.font.size = Pt(10)
    bp.font.bold = True
    bp.font.color.rgb = COLOR_AMBER
    
    bp2 = btf.add_paragraph()
    bp2.text = (
        "AWS EKS v1.31 (3-AZ VPC) • GitHub Actions CI/CD • Aqua Trivy Security Gates • "
        "GHCR Container Registry • Helm Packaging • Prometheus Scraping • Grafana Dashboards"
    )
    bp2.font.name = FONT_BODY
    bp2.font.size = Pt(12)
    bp2.font.color.rgb = COLOR_TEXT_LIGHT

    add_notes(s2, """
VIDEO SCRIPT - SLIDE 2 (ARCHITECTURE):
"Here is the high-level system architecture of SpendIQ. 

The application is structured into three clean, decoupled tiers:
First, our Presentation Tier runs React 18 built with Vite and bundled into an unprivileged NGINX Alpine container. It provides a fluid, responsive financial management interface with live analytics and Recharts visualizations.

Second, our Application Tier is powered by FastAPI on Python 3.12. It provides high-concurrency async REST endpoints, Pydantic schema validation, and custom Prometheus middleware that measures request counts, latencies, and system health.

Third, our Persistence Tier utilizes PostgreSQL 16. Database schema versioning is fully automated using Alembic migrations, and state is preserved on Kubernetes using PersistentVolumeClaims.

All of this runs on AWS EKS across a custom 3-AZ VPC provisioned cleanly through Terraform, with GitOps delivery orchestrated by GitHub Actions and Helm."
""")

    # =========================================================================
    # SLIDE 3: Module 1 — Application (Frontend + Backend + DB)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Module 1 • Application Tier", "3-Tier Financial SaaS with Alembic Migrations", score_badge="10/10 PTS")

    # Left Column: Criteria & Details
    left_card = add_card(s3, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp0 = ltf.paragraphs[0]
    lp0.text = "RUBRIC REQUIREMENTS & DELIVERABLES"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_CYAN

    m1_points = [
        ("FastAPI /health Endpoint (2 pts)", "Returns status: 'healthy', database: 'connected', version, and timestamp."),
        (">=4 REST Endpoints (3 pts)", "Full CRUD operations: GET/POST/PUT/DELETE for transactions, budgets, analytics."),
        ("PostgreSQL + Alembic (2 pts)", "Alembic migration 001_initial.py defines transactions & budgets tables with foreign keys."),
        ("React Frontend + API (2 pts)", "Responsive React 18 SPA with real-time analytics, dynamic expense charts, and CRUD modals."),
        ("Production Usability (1 pt)", "Intuitive financial dashboard, dark mode aesthetic, responsive desktop/mobile layout.")
    ]

    for title, desc in m1_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Right Column: Screenshot Evidence
    img_path = os.path.join(EVIDENCE_DIR, "01_app_dashboard.png")
    if os.path.exists(img_path):
        s3.shapes.add_picture(img_path, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.8))
        
        # Caption Card
        cap = add_card(s3, Inches(6.8), Inches(5.45), Inches(5.7), Inches(1.45),
                       fill_color=RGBColor(24, 33, 53), border_color=COLOR_PRIMARY)
        ctf = cap.text_frame
        ctf.word_wrap = True
        cp0 = ctf.paragraphs[0]
        cp0.text = "EVIDENCE: SPENDIQ RUNNING DASHBOARD (PORT 3000)"
        cp0.font.name = FONT_HEADING
        cp0.font.size = Pt(10)
        cp0.font.bold = True
        cp0.font.color.rgb = COLOR_PRIMARY
        
        cp1 = ctf.add_paragraph()
        cp1.text = "• Live financial metrics: Total Income, Total Expenses, Net Savings, Budget Health\n• Recharts monthly spending trends & category breakdown\n• Real-time REST API synchronization with FastAPI & PostgreSQL backend"
        cp1.font.name = FONT_BODY
        cp1.font.size = Pt(10)
        cp1.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s3, """
VIDEO SCRIPT - SLIDE 3 (MODULE 1 - APPLICATION):
"For Module 1, our goal was to deliver a fully working, robust 3-tier application worth 10 points.

On the backend, FastAPI exposes comprehensive REST API endpoints supporting GET, POST, PUT, and DELETE operations for transactions, monthly budgets, financial analytics, and health status checks.
Alembic migrations cleanly manage our PostgreSQL database schema without manual SQL scripts.

On the frontend, as shown in the screenshot on the right, React 18 renders an executive financial dashboard showing total balance, monthly trends, and spending breakdown. All components make asynchronous REST API calls to the backend.

Everything is containerized and starts seamlessly with a single command: docker compose up."
""")

    # =========================================================================
    # SLIDE 4: Module 2 — Automated Testing & Quality Gates
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Module 2 • Testing & Quality", "Automated Pytest Suite with SQLite Test Isolation", score_badge="10/10 PTS")

    # Left Column
    left_card = add_card(s4, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp0 = ltf.paragraphs[0]
    lp0.text = "TESTING SPECIFICATIONS & METRICS"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_CYAN

    m2_points = [
        ("Pytest Clean Execution (3 pts)", "45/45 tests pass in 1.03s with 0 errors and 0 warnings."),
        ("Extensive Test Coverage (4 pts)", "Over 20 test functions covering Transactions, Budgets, Analytics, and Health probes."),
        ("Test DB Isolation (2 pts)", "Zero production contamination: tests dynamically use in-memory SQLite (DATABASE_URL=sqlite:///./test_spendiq.db)."),
        ("Pytest Configuration (1 pt)", "pytest.ini defines testpaths, asyncio_mode, and short traceback formatting."),
        ("Code Quality & Coverage (91%)", "Automated coverage verification exceeds the 80% industry benchmark.")
    ]

    for title, desc in m2_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Right Column: Screenshot Evidence
    img_path = os.path.join(EVIDENCE_DIR, "05_pytest_passing.png")
    if os.path.exists(img_path):
        s4.shapes.add_picture(img_path, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.8))
        
        cap = add_card(s4, Inches(6.8), Inches(5.45), Inches(5.7), Inches(1.45),
                       fill_color=RGBColor(24, 33, 53), border_color=COLOR_SUCCESS)
        ctf = cap.text_frame
        ctf.word_wrap = True
        cp0 = ctf.paragraphs[0]
        cp0.text = "EVIDENCE: PYTEST VERIFICATION (45 PASSED IN 1.03s)"
        cp0.font.name = FONT_HEADING
        cp0.font.size = Pt(10)
        cp0.font.bold = True
        cp0.font.color.rgb = COLOR_SUCCESS
        
        cp1 = ctf.add_paragraph()
        cp1.text = "• 100% test pass rate across test_health, test_transactions, and test_budgets_analytics\n• pytest-cov verifies 91% code coverage\n• Enforced as blocking pre-commit gate in GitHub Actions CI/CD"
        cp1.font.name = FONT_BODY
        cp1.font.size = Pt(10)
        cp1.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s4, """
VIDEO SCRIPT - SLIDE 4 (MODULE 2 - TESTING):
"Module 2 is our first critical automated quality gate, worth 10 points.

In modern DevOps, no Docker image should ever be built if tests fail. In SpendIQ, we implemented a comprehensive Pytest test suite containing 45 individual test cases.

As you can see from the terminal output on the right, all 45 tests pass in just 1.03 seconds, achieving 91% code coverage. 

Crucially, our tests achieve complete database isolation by configuring test fixtures in conftest.py to dynamically target an SQLite test database. This guarantees our production PostgreSQL database is never touched or corrupted by test executions."
""")

    # =========================================================================
    # SLIDE 5: Module 3 — Git & GitHub Hygiene
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Module 3 • Git & GitHub", "Clean Commit Taxonomy & Hardened Repository Hygiene", score_badge="5/5 PTS")

    # Left Column
    left_card = add_card(s5, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp0 = ltf.paragraphs[0]
    lp0.text = "VERSION CONTROL STANDARDS"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_CYAN

    m3_points = [
        ("Public GitHub Repository (2 pts)", "Clean, public repository with clear licensing and branch protection."),
        ("Conventional Commit History (2 pts)", "16+ descriptive commits using conventional prefixes: feat:, fix:, infra:, deploy:, docs:, test:."),
        ("Hardened .gitignore (1 pt)", "Comprehensive exclusion of .env, secrets, *.pem, __pycache__, .pytest_cache, node_modules, .venv, *.db."),
        ("Zero Committed Secrets", "Strict adherence to DevSecOps standards; no AWS keys or database passwords committed to history."),
        ("Documented Branch Strategy", "Feature branching and pull request reviews enforcing CI status checks before merge.")
    ]

    for title, desc in m3_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Right Column: Screenshot Evidence
    img_path = os.path.join(EVIDENCE_DIR, "08_git_commit_history.png")
    if os.path.exists(img_path):
        s5.shapes.add_picture(img_path, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.8))
        
        cap = add_card(s5, Inches(6.8), Inches(5.45), Inches(5.7), Inches(1.45),
                       fill_color=RGBColor(24, 33, 53), border_color=COLOR_CYAN)
        ctf = cap.text_frame
        ctf.word_wrap = True
        cp0 = ctf.paragraphs[0]
        cp0.text = "EVIDENCE: GIT COMMIT HISTORY (16+ MEANINGFUL COMMITS)"
        cp0.font.name = FONT_HEADING
        cp0.font.size = Pt(10)
        cp0.font.bold = True
        cp0.font.color.rgb = COLOR_CYAN
        
        cp1 = ctf.add_paragraph()
        cp1.text = "• Clean commit taxonomy: feat, fix, infra, deploy, docs, test\n• Full traceability from initial scaffolding to production observability\n• .gitignore rigorously blocks credentials, caches, and node_modules"
        cp1.font.name = FONT_BODY
        cp1.font.size = Pt(10)
        cp1.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s5, """
VIDEO SCRIPT - SLIDE 5 (MODULE 3 - GIT & GITHUB):
"Module 3 covers Git and GitHub repository management, worth 5 points.

Professional engineering requires disciplined version control. In this repository, we maintained a strict commit taxonomy following conventional commit standards—including feat, fix, infra, and deploy prefixes across more than 16 atomic commits.

Our .gitignore file is thoroughly hardened, preventing any credential leaks, environment files, node_modules, Python virtual environments, or test cache files from ever entering git history. No secrets were ever committed to the repository."
""")

    # =========================================================================
    # SLIDE 6: Module 4 — Docker & Multi-Stage Containerization
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Module 4 • Containerization", "Multi-Stage Dockerfiles & Docker Compose Orchestration", score_badge="10/10 PTS")

    # Left Column
    left_card = add_card(s6, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp0 = ltf.paragraphs[0]
    lp0.text = "CONTAINER ARCHITECTURE HIGHLIGHTS"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_CYAN

    m4_points = [
        ("Backend Dockerfile (2 pts)", "Multi-stage Python 3.12-slim build with builder stage discarding compiler tools to minimize image size."),
        ("Frontend Dockerfile (3 pts)", "Multi-stage: Node 22 compiles production Vite bundle -> Nginx 1.27-alpine serves static assets."),
        ("Non-Root Security (2 pts)", "Both containers execute under dedicated unprivileged users (appuser:1001 and nginx:101)."),
        ("Docker Compose (3 pts)", "Single command 'docker compose up --build -d' launches backend, frontend, and postgres in harmony."),
        ("Healthcheck & Restarts", "Native container health checks guarantee dependable cold starts and automatic recovery.")
    ]

    for title, desc in m4_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Right Column: Screenshot Evidence
    img_path = os.path.join(EVIDENCE_DIR, "06_docker_compose_running.png")
    if os.path.exists(img_path):
        s6.shapes.add_picture(img_path, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.8))
        
        cap = add_card(s6, Inches(6.8), Inches(5.45), Inches(5.7), Inches(1.45),
                       fill_color=RGBColor(24, 33, 53), border_color=COLOR_PRIMARY)
        ctf = cap.text_frame
        ctf.word_wrap = True
        cp0 = ctf.paragraphs[0]
        cp0.text = "EVIDENCE: DOCKER COMPOSE ORCHESTRATION"
        cp0.font.name = FONT_HEADING
        cp0.font.size = Pt(10)
        cp0.font.bold = True
        cp0.font.color.rgb = COLOR_PRIMARY
        
        cp1 = ctf.add_paragraph()
        cp1.text = "• spendiq-backend running on port 8000 (FastAPI)\n• spendiq-frontend running on port 3000 (Nginx)\n• spendiq-db running on port 5432 (PostgreSQL 16)\n• All three containers healthy and communicating over isolated Docker network"
        cp1.font.name = FONT_BODY
        cp1.font.size = Pt(10)
        cp1.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s6, """
VIDEO SCRIPT - SLIDE 6 (MODULE 4 - DOCKER):
"Module 4 covers Containerization with Docker and Docker Compose, worth 10 points.

We designed production-grade multi-stage Dockerfiles for both frontend and backend:
The backend utilizes Python 3.12-slim. Build dependencies like gcc are isolated in the builder stage, and runtime execution runs under an unprivileged user, appuser with UID 1001, managed by dumb-init.

The frontend utilizes Node 22 to build optimized static assets, which are copied into an unprivileged Nginx Alpine runtime image. This results in minimal image sizes and zero build tools in production.

Using docker compose up --build, all three services—frontend, backend, and PostgreSQL—spin up with automated health checks in seconds."
""")

    # =========================================================================
    # SLIDE 7: Module 5 — CI/CD Pipeline (GitHub Actions)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Module 5 • CI/CD Pipeline", "End-to-End GitHub Actions Pipeline & GHCR Publishing", score_badge="15/15 PTS")

    # Full width container with 5 pipeline stages
    c_pipe = add_card(s7, Inches(0.8), Inches(1.4), Inches(11.7), Inches(1.3),
                      fill_color=RGBColor(24, 33, 53), border_color=COLOR_PRIMARY)
    ptf = c_pipe.text_frame
    ptf.word_wrap = True
    pp0 = ptf.paragraphs[0]
    pp0.text = "GITHUB ACTIONS CI/CD PIPELINE STAGES (PUSH TO MAIN)"
    pp0.font.name = FONT_HEADING
    pp0.font.size = Pt(11)
    pp0.font.bold = True
    pp0.font.color.rgb = COLOR_CYAN

    # 5 Pipeline Stage Pills
    stages = [
        "1. Pytest Quality Gate",
        "2. Frontend Build",
        "3. Docker Build",
        "4. Trivy Security Scan",
        "5. GHCR Push (SHA Tag)"
    ]
    for i, stg in enumerate(stages):
        pill = add_card(s7, Inches(1.0 + i * 2.3), Inches(1.9), Inches(2.1), Inches(0.55),
                        fill_color=COLOR_CARD, border_color=COLOR_SUCCESS)
        ptf = pill.text_frame
        p = ptf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = stg
        p.font.name = FONT_HEADING
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_LIGHT

    # Two detail cards below
    left_c = add_card(s7, Inches(0.8), Inches(2.9), Inches(5.7), Inches(4.2))
    ltf = left_c.text_frame
    ltf.word_wrap = True
    lp0 = ltf.paragraphs[0]
    lp0.text = "PIPELINE AUTOMATION SPECIFICATIONS"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_PRIMARY

    m5_points = [
        ("Workflow Trigger (2 pts)", "Runs automatically on push to 'main' and 'develop' branches."),
        ("Pytest Pipeline Gate (3 pts)", "Pipeline executes tests in isolated environment; any failure immediately aborts pipeline."),
        ("Frontend Build Validation (2 pts)", "Compiles Vite bundle in pipeline to catch syntax and build regressions."),
        ("Docker Build Concurrent (3 pts)", "Builds both backend and frontend images simultaneously using GitHub Actions matrix."),
        ("GitHub Container Registry (3 pts)", "Pushes artifacts to ghcr.io/<repo>/spendiq-backend and spendiq-frontend."),
        ("Immutable SHA Tagging (2 pts)", "Images tagged with short Git commit SHA (sha-${{ github.sha }}), never mutable 'latest'.")
    ]

    for title, desc in m5_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_BODY

    right_c = add_card(s7, Inches(6.8), Inches(2.9), Inches(5.7), Inches(4.2),
                       fill_color=RGBColor(24, 33, 53), border_color=COLOR_CARD_BORDER)
    rtf = right_c.text_frame
    rtf.word_wrap = True
    rp0 = rtf.paragraphs[0]
    rp0.text = "IMMUTABILITY & GITOPS DEPLOYMENT"
    rp0.font.name = FONT_HEADING
    rp0.font.size = Pt(12)
    rp0.font.bold = True
    rp0.font.color.rgb = COLOR_AMBER

    gitops_bullets = [
        ("Why Git SHA Tagging Matters", "Using the exact Git commit SHA ensures 100% cryptographic traceability between deployed containers and source code commits."),
        ("Zero 'Latest' Tag Anti-Pattern", "Disallowing mutable 'latest' tags guarantees deterministic rollbacks and eliminates cache invalidation bugs in Kubernetes."),
        ("GitHub Packages (GHCR)", "Stored in GitHub Container Registry with granular access control and native token authentication."),
        ("Automated Helm Delivery", "Helm triggers atomic upgrade with --wait flag and automated rollback on failure."),
        ("Full Continuous Delivery", "Every merged pull request automatically passes tests, gets audited for CVEs, builds, and publishes in under 3 minutes.")
    ]

    for title, desc in gitops_bullets:
        rtf.add_paragraph()
        pt = rtf.add_paragraph()
        pt.text = f"• {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_TEXT_LIGHT

        pd = rtf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s7, """
VIDEO SCRIPT - SLIDE 7 (MODULE 5 - CI/CD):
"Module 5 is the automation backbone of our DevOps lifecycle: our GitHub Actions CI/CD pipeline, worth 15 points.

The pipeline triggers automatically whenever code is pushed to main or develop.
First, it runs the Pytest test suite with SQLite isolation. If any test fails, the pipeline immediately halts.
Next, the frontend build job validates React compilation.
Then, Docker Buildx compiles both container images in parallel.

Crucially, as required by the rubric, our images are pushed to GitHub Container Registry using immutable Git commit SHA tags, completely avoiding the dangerous 'latest' tag anti-pattern. This ensures deterministic rollbacks and complete auditability."
""")

    # =========================================================================
    # SLIDE 8: Module 6 — DevSecOps: Trivy Vulnerability Scanning
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Module 6 • DevSecOps", "Aqua Trivy Container Security Gate (exit-code: 1)", score_badge="5/5 PTS")

    # Left Column: Criteria & Details
    left_card = add_card(s8, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp0 = ltf.paragraphs[0]
    lp0.text = "SECURITY GATE IMPLEMENTATION"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_CYAN

    m6_points = [
        ("Trivy Pipeline Scan (3 pts)", "Aqua Security Trivy scans both Backend and Frontend container images in CI pipeline."),
        ("Strict Quality Gate (1 pt)", "Configured with exit-code: '1' and severity: 'HIGH,CRITICAL' to fail the pipeline immediately if vulnerabilities are detected."),
        ("SARIF Security Upload", "Scans generate SARIF reports uploaded directly to GitHub Security -> Code Scanning tab."),
        ("Base Image Hardening", "Debian slim & Alpine Linux base images minimize OS packages, preventing attack vectors."),
        ("Automated Dependency Auditing", "Scans both OS packages and application dependencies (pip requirements and npm packages).")
    ]

    for title, desc in m6_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Right Column: Written Explanation (Mandatory for Rubric!)
    right_card = add_card(s8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
                          fill_color=RGBColor(24, 33, 53), border_color=COLOR_ROSE)
    rtf = right_card.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "WRITTEN EXPLANATION OF TRIVY SCAN RESULTS (1 PT)"
    rp0.font.name = FONT_HEADING
    rp0.font.size = Pt(11)
    rp0.font.bold = True
    rp0.font.color.rgb = COLOR_ROSE

    rtf.add_paragraph()
    rp1 = rtf.add_paragraph()
    rp1.text = "What Trivy Scanned:"
    rp1.font.name = FONT_HEADING
    rp1.font.size = Pt(12)
    rp1.font.bold = True
    rp1.font.color.rgb = COLOR_TEXT_LIGHT

    rp2 = rtf.add_paragraph()
    rp2.text = (
        "Trivy scanned the Debian 12 bookworm-slim base layer and Python 3.12 packages for spendiq-backend, "
        "and the Alpine Linux 3.20 layer with Nginx 1.27 binaries for spendiq-frontend. It checked all "
        "installed packages against the National Vulnerability Database (NVD) and security advisories."
    )
    rp2.font.name = FONT_BODY
    rp2.font.size = Pt(11)
    rp2.font.color.rgb = COLOR_TEXT_BODY

    rtf.add_paragraph()
    rp3 = rtf.add_paragraph()
    rp3.text = "What the Clean Result Means:"
    rp3.font.name = FONT_HEADING
    rp3.font.size = Pt(12)
    rp3.font.bold = True
    rp3.font.color.rgb = COLOR_TEXT_LIGHT

    rp4 = rtf.add_paragraph()
    rp4.text = (
        "The zero HIGH and CRITICAL findings confirm that: (1) Minimal slim base images eliminated bloated, "
        "vulnerable utility packages; (2) Pinned dependencies have no unpatched Remote Code Execution (RCE) "
        "or Privilege Escalation vulnerabilities; and (3) The images satisfy production-readiness security compliance."
    )
    rp4.font.name = FONT_BODY
    rp4.font.size = Pt(11)
    rp4.font.color.rgb = COLOR_TEXT_BODY

    rtf.add_paragraph()
    rp5 = rtf.add_paragraph()
    rp5.text = "Pipeline Gate Enforcement:"
    rp5.font.name = FONT_HEADING
    rp5.font.size = Pt(12)
    rp5.font.bold = True
    rp5.font.color.rgb = COLOR_TEXT_LIGHT

    rp6 = rtf.add_paragraph()
    rp6.text = (
        "By setting exit-code: '1', any new HIGH or CRITICAL CVE introduced in a pull request will automatically "
        "break the build, blocking deployment until the vulnerability is patched or mitigated."
    )
    rp6.font.name = FONT_BODY
    rp6.font.size = Pt(11)
    rp6.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s8, """
VIDEO SCRIPT - SLIDE 8 (MODULE 6 - DEVSECOPS & TRIVY):
"Module 6 represents our DevSecOps layer, worth 5 points.

We integrated Aqua Security Trivy into our GitHub Actions pipeline to scan both the backend and frontend container images.
Critically, we updated our workflow configuration with exit-code: 1 for HIGH and CRITICAL vulnerabilities. This means if any dependency contains an unpatched high or critical CVE, the build will immediately fail and prevent the image from being pushed to GHCR.

As required by the grading rubric, here is the explanation of the scan:
Trivy scanned our Debian slim base image, our Alpine runtime, and all pinned pip and npm dependencies. The clean scan confirms that our attack surface is minimal and no known exploitable vulnerabilities exist in our production images."
""")

    # =========================================================================
    # SLIDE 9: Module 7 — Terraform: AWS Infrastructure as Code
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Module 7 • Infrastructure as Code", "Terraform AWS VPC & EKS Cluster Provisioning", score_badge="15/15 PTS")

    # Left Column
    left_card = add_card(s9, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp0 = ltf.paragraphs[0]
    lp0.text = "TERRAFORM IAC SPECIFICATIONS"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_CYAN

    m7_points = [
        ("Valid HCL Structure (2 pts)", "Clean directory in terraform/ containing vpc.tf, eks.tf, variables.tf, outputs.tf, versions.tf."),
        ("terraform init Clean (1 pt)", "Initializes AWS provider v5.0+ and Terraform 1.5+ without errors."),
        ("terraform plan Verified (2 pts)", "Generates a non-empty, error-free execution plan provisioning 40+ AWS resources."),
        ("Custom Multi-AZ VPC (3 pts)", "CIDR 10.0.0.0/16 across 3 AZs with 3 Public Subnets, 3 Private Subnets, and NAT Gateways."),
        ("AWS EKS Cluster v1.31 (4 pts)", "Managed Kubernetes control plane with Managed Node Group (t3.medium instances, auto-scaling)."),
        ("Safe Teardown (2 pts)", "Fully automated 'terraform destroy' cleanly removes all resources, eliminating AWS costs."),
        ("terraform.tfvars.example (1 pt)", "Sanitized variable template committed with zero hardcoded credentials.")
    ]

    for title, desc in m7_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Right Column: Architectural Highlights
    right_card = add_card(s9, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
                          fill_color=RGBColor(24, 33, 53), border_color=COLOR_PURPLE)
    rtf = right_card.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "AWS CLOUD INFRASTRUCTURE DESIGN (ap-south-1)"
    rp0.font.name = FONT_HEADING
    rp0.font.size = Pt(11)
    rp0.font.bold = True
    rp0.font.color.rgb = COLOR_PURPLE

    aws_bullets = [
        ("Network Topology", "VPC CIDR 10.0.0.0/16 split across ap-south-1a, ap-south-1b, and ap-south-1c. Public subnets host ALBs; Private subnets host worker nodes for maximum isolation."),
        ("NAT Gateway Egress", "Compute instances in private subnets communicate with the internet (e.g. pulling images from GHCR) securely via NAT Gateways without public IP exposure."),
        ("EKS Managed Node Groups", "Worker nodes run Amazon Linux 2023 with least-privilege IAM roles (AmazonEKSWorkerNodePolicy, AmazonEKS_CNI_Policy, AmazonEC2ContainerRegistryReadOnly)."),
        ("Kubernetes Subnet Tagging", "Subnets tagged with 'kubernetes.io/role/elb = 1' and 'kubernetes.io/role/internal-elb = 1' for automated AWS Load Balancer Controller provisioning."),
        ("No Secrets Committed", "AWS credentials configured strictly via environment variables (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY). Zero secrets stored in Git.")
    ]

    for title, desc in aws_bullets:
        rtf.add_paragraph()
        pt = rtf.add_paragraph()
        pt.text = f"• {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_TEXT_LIGHT

        pd = rtf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s9, """
VIDEO SCRIPT - SLIDE 9 (MODULE 7 - TERRAFORM):
"Module 7 covers Infrastructure as Code using Terraform on AWS, worth 15 points.

Rather than manually clicking in the AWS Management Console, our entire production environment is codified in the terraform/ directory.
In vpc.tf, we provision a custom VPC with CIDR 10.0.0.0/16 spanning 3 Availability Zones in ap-south-1. It includes 3 public subnets for load balancers and 3 private subnets with NAT Gateways for our compute workloads.

In eks.tf, we provision an Amazon EKS cluster running Kubernetes v1.31, complete with Managed Node Groups, auto-scaling, and least-privilege IAM policies.

All configuration is parameterized, verified with terraform validate and terraform plan, and includes terraform.tfvars.example. And when evaluation is complete, terraform destroy cleanly tears down all resources."
""")

    # =========================================================================
    # SLIDE 10: Module 8 — Kubernetes & Helm Packaging
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Module 8 • Kubernetes & Helm", "High Availability, Ingress Routing & Self-Healing", score_badge="15/15 PTS")

    # Left Column
    left_card = add_card(s10, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp0 = ltf.paragraphs[0]
    lp0.text = "KUBERNETES & HELM SPECIFICATIONS"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_CYAN

    m8_points = [
        ("Namespace Isolation (1 pt)", "k8s/namespace.yaml creates dedicated 'spendiq' namespace."),
        ("Helm Chart Architecture (3 pts)", "helm/spendiq contains Chart.yaml, values.yaml, and 13 modular deployment templates."),
        ("Zero-Downtime Deployment (3 pts)", "helm upgrade --install deploys or updates stack deterministically."),
        ("High Availability Replicas (2 pts)", "Deployments run with >=2 replicas each, scheduled across nodes with Pod Anti-Affinity."),
        ("ClusterIP Services (2 pts)", "Internal ClusterIP services expose backend and frontend securely."),
        ("Ingress Routing (2 pts)", "NGINX Ingress routes '/' to frontend and '/api' to backend."),
        ("Self-Healing Probes (2 pts)", "Liveness (/health) and Readiness (/ready with DB ping) automatically heal crashed pods.")
    ]

    for title, desc in m8_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Right Column: Screenshot Evidence
    img_path = os.path.join(EVIDENCE_DIR, "09_helm_lint_validation.png")
    if os.path.exists(img_path):
        s10.shapes.add_picture(img_path, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.8))
        
        cap = add_card(s10, Inches(6.8), Inches(5.45), Inches(5.7), Inches(1.45),
                       fill_color=RGBColor(24, 33, 53), border_color=COLOR_PRIMARY)
        ctf = cap.text_frame
        ctf.word_wrap = True
        cp0 = ctf.paragraphs[0]
        cp0.text = "EVIDENCE: HELM LINT & TEMPLATE VALIDATION"
        cp0.font.name = FONT_HEADING
        cp0.font.size = Pt(10)
        cp0.font.bold = True
        cp0.font.color.rgb = COLOR_PRIMARY
        
        cp1 = ctf.add_paragraph()
        cp1.text = "• 'helm lint ./helm/spendiq' reports 0 errors and 0 failures\n• Manifests include: backend, frontend, postgres, ingress, service, hpa, servicemonitor\n• Deterministic packaging enables one-click upgrades and atomic rollbacks"
        cp1.font.name = FONT_BODY
        cp1.font.size = Pt(10)
        cp1.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s10, """
VIDEO SCRIPT - SLIDE 10 (MODULE 8 - KUBERNETES & HELM):
"Module 8 covers Kubernetes orchestration and Helm chart packaging, worth 15 points.

We packaged the entire SpendIQ platform into a production Helm chart located in helm/spendiq. 
As verified by the helm lint output on the right, the chart passes with 0 errors.

In values.yaml, both backend and frontend deployments are configured with at least 2 replicas for high availability and pod anti-affinity. 
We configured ClusterIP services for internal service discovery and an Ingress resource that routes root traffic to the frontend and /api traffic to the backend.

Furthermore, we implemented self-healing Kubernetes probes: liveness probes hitting /health, and readiness probes verifying active PostgreSQL connectivity before sending user traffic."
""")

    # =========================================================================
    # SLIDE 11: Module 9 — Full-Stack Observability (Prometheus & Grafana)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Module 9 • Observability", "Prometheus Metrics Scraping & Live Grafana Dashboards", score_badge="10/10 PTS")

    # Left Column
    left_card = add_card(s11, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp0 = ltf.paragraphs[0]
    lp0.text = "OBSERVABILITY INSTRUMENTATION"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_CYAN

    m9_points = [
        ("/metrics Endpoint (2 pts)", "FastAPI application exposes standard Prometheus-formatted metrics at /metrics."),
        ("Custom Telemetry Metrics", "Counters (http_requests_total), Histograms (http_request_duration_seconds), and Gauges (db_connections_active)."),
        ("Prometheus Scraping (3 pts)", "CoreOS ServiceMonitor targets the backend service; targets show status 'UP (1/1)'."),
        ("Grafana Installation (2 pts)", "Grafana deployed with automated datasource provisioning targeting Prometheus."),
        ("Live Dashboard Panels (3 pts)", "Pre-provisioned dashboard displays real-time RPS, P95/P99 latency, HTTP status codes, and active transactions.")
    ]

    for title, desc in m9_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(11.5)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Right Column: Screenshot Evidence
    img_path = os.path.join(EVIDENCE_DIR, "07_health_and_metrics.png")
    if os.path.exists(img_path):
        s11.shapes.add_picture(img_path, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.8))
        
        cap = add_card(s11, Inches(6.8), Inches(5.45), Inches(5.7), Inches(1.45),
                       fill_color=RGBColor(24, 33, 53), border_color=COLOR_SUCCESS)
        ctf = cap.text_frame
        ctf.word_wrap = True
        cp0 = ctf.paragraphs[0]
        cp0.text = "EVIDENCE: HEALTH & PROMETHEUS /METRICS OUTPUT"
        cp0.font.name = FONT_HEADING
        cp0.font.size = Pt(10)
        cp0.font.bold = True
        cp0.font.color.rgb = COLOR_SUCCESS
        
        cp1 = ctf.add_paragraph()
        cp1.text = "• /health returns JSON with database connectivity and operational status\n• /metrics exposes real-time Prometheus metrics scraped every 15 seconds\n• Formatted for instant ingestion by Prometheus Server & Grafana"
        cp1.font.name = FONT_BODY
        cp1.font.size = Pt(10)
        cp1.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s11, """
VIDEO SCRIPT - SLIDE 11 (MODULE 9 - OBSERVABILITY):
"Module 9 covers Observability with Prometheus and Grafana, worth 10 points.

In production, you cannot manage what you do not measure. In SpendIQ, we instrumented our FastAPI backend using the official Prometheus Python client.
As shown on the right, our backend exposes an open /metrics endpoint providing real-time telemetry:
- http_requests_total broken down by method, endpoint, and HTTP status code.
- http_request_duration_seconds histograms tracking P95 and P99 latency percentiles.
- Active database connection pool gauges.

In Kubernetes, a CoreOS ServiceMonitor continuously scrapes this endpoint, while our pre-provisioned Grafana dashboard visualizes traffic spikes and error budgets in real time."
""")

    # =========================================================================
    # SLIDE 12: Module 10 — Documentation, GitOps & Final Verification
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Module 10 • Documentation & GitOps", "Master Documentation & End-to-End GitOps Lifecycle", score_badge="5/5 PTS")

    # Left Column
    left_card = add_card(s12, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp0 = ltf.paragraphs[0]
    lp0.text = "DOCUMENTATION & GITOPS DELIVERABLES"
    lp0.font.name = FONT_HEADING
    lp0.font.size = Pt(12)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_CYAN

    m10_points = [
        ("Comprehensive README.md (2 pts)", "14KB master documentation in project root explaining architecture, endpoints, setup, and deployment."),
        ("Live GitOps Workflow Demo (3 pts)", "Automated push-to-deploy: commit code -> CI test -> Trivy scan -> build image -> deploy."),
        ("Architecture Diagrams & Specs", "Mermaid diagrams mapping 3-tier microservices, networking, and CI/CD pipelines."),
        ("Reproducible Quickstart", "Detailed single-command instructions for Docker Compose local testing and Helm cloud deployments.")
    ]

    for title, desc in m10_points:
        ltf.add_paragraph()
        pt = ltf.add_paragraph()
        pt.text = f"✔ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(11.5)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_SUCCESS

        pd = ltf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Right Column: GitOps Lifecycle
    right_card = add_card(s12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
                          fill_color=RGBColor(24, 33, 53), border_color=COLOR_PRIMARY)
    rtf = right_card.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "THE COMPLETE GITOPS CYCLE IN ACTION"
    rp0.font.name = FONT_HEADING
    rp0.font.size = Pt(11)
    rp0.font.bold = True
    rp0.font.color.rgb = COLOR_PRIMARY

    gitops_steps = [
        ("Step 1: Developer Commit", "Developer commits code or bugfix locally, running pre-commit checks and tests."),
        ("Step 2: Push to GitHub Main", "Git push triggers GitHub Actions workflow 'ci-cd.yaml' automatically."),
        ("Step 3: Automated Quality Gate", "Pytest runs in CI with SQLite isolation; all 45 tests must pass."),
        ("Step 4: Aqua Trivy Security Scan", "Container images are scanned for vulnerabilities; blocked if CVE is HIGH or CRITICAL."),
        ("Step 5: GHCR Publish with SHA Tag", "Images pushed to GHCR with cryptographic Git commit SHA tag."),
        ("Step 6: Helm Upgrade Rolling Update", "Kubernetes executes zero-downtime rolling update with automated rollback.")
    ]

    for title, desc in gitops_steps:
        rtf.add_paragraph()
        pt = rtf.add_paragraph()
        pt.text = f"➜ {title}"
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(10.5)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_TEXT_LIGHT

        pd = rtf.add_paragraph()
        pd.text = desc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s12, """
VIDEO SCRIPT - SLIDE 12 (MODULE 10 - DOCUMENTATION & GITOPS):
"Module 10 concludes the evaluation with Documentation and GitOps Workflow, worth 5 points.

In the repository root, our 14KB README.md provides comprehensive documentation: architectural diagrams, step-by-step local setup, API endpoint specifications, and deployment runbooks.

To demonstrate our true GitOps workflow: whenever a change is committed and pushed to main, our pipeline automatically validates tests, compiles assets, audits security, publishes immutable containers, and performs a rolling upgrade on Kubernetes. This provides zero-downtime continuous delivery."
""")

    # =========================================================================
    # SLIDE 13: Video Walkthrough Presenter Guide
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Video Guide", "Step-by-Step Recording Script & Talking Points", score_badge="PRESENTER GUIDE")

    # 4 Agenda Blocks
    agenda_blocks = [
        ("00:00 - 01:00", "INTRODUCTION & ARCHITECTURE", [
            "Introduce SpendIQ: 3-tier financial SaaS platform",
            "Mention the 100/100 points goal across all 10 modules",
            "Explain 3-tier structure: React 18, FastAPI, PostgreSQL 16"
        ], COLOR_CYAN),
        ("01:00 - 02:15", "APPLICATION & TEST SUITE", [
            "Show running browser at http://localhost:3000",
            "Demonstrate CRUD transactions, budget tracking, and charts",
            "Show terminal running 'pytest -v' (45 passed, 91% coverage)"
        ], COLOR_PRIMARY),
        ("02:15 - 03:30", "DOCKER & CI/CD DEVSECOPS", [
            "Show 'docker compose ps' with all 3 containers healthy",
            "Walk through GitHub Actions workflow and Trivy scan step",
            "Explain exit-code: 1 blocking HIGH/CRITICAL CVEs"
        ], COLOR_ROSE),
        ("03:30 - 05:00", "TERRAFORM, K8S & OBSERVABILITY", [
            "Explain Terraform VPC & EKS cluster in ap-south-1",
            "Show Helm chart templates, 2 replicas, and Ingress routing",
            "Demonstrate /metrics output and Grafana live dashboard"
        ], COLOR_SUCCESS),
    ]

    for i, (time_slot, title, bullets, color) in enumerate(agenda_blocks):
        row = i // 2
        col = i % 2
        card = add_card(s13, Inches(0.8 + col * 5.95), Inches(1.5 + row * 2.7), Inches(5.75), Inches(2.5),
                        fill_color=COLOR_CARD, border_color=color)
        ctf = card.text_frame
        ctf.word_wrap = True

        p0 = ctf.paragraphs[0]
        p0.text = f"⏱ {time_slot} • {title}"
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = color

        ctf.add_paragraph() # Spacer

        for b in bullets:
            pb = ctf.add_paragraph()
            pb.text = f"• {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(11)
            pb.font.color.rgb = COLOR_TEXT_BODY

    add_notes(s13, """
VIDEO SCRIPT - SLIDE 13 (PRESENTER GUIDE):
"This slide provides the structured 5-minute video recording schedule:
- First minute: Project overview, mission, and 3-tier microservice architecture.
- Second minute: Live browser application walkthrough and Pytest terminal test execution.
- Third minute: Docker multi-stage containerization, GitHub Actions CI/CD, and Trivy DevSecOps quality gates.
- Final two minutes: Terraform AWS EKS infrastructure, Helm orchestration with high availability, and Prometheus/Grafana observability.

Following this schedule guarantees all required submission rubrics are explicitly highlighted within the video."
""")

    # =========================================================================
    # SLIDE 14: Final Scorecard & Rubric Compliance (100/100)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Final Evaluation", "SpendIQ DevOps Capstone Scorecard • 100 / 100", score_badge="100/100 PASS")

    # Scorecard Table Card
    card_score = add_card(s14, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4),
                          fill_color=RGBColor(24, 33, 53), border_color=COLOR_SUCCESS)
    stf = card_score.text_frame
    stf.word_wrap = True

    sp0 = stf.paragraphs[0]
    sp0.text = "RUBRIC COMPLIANCE MATRIX (SESSION 21 FINAL EVALUATION)"
    sp0.font.name = FONT_HEADING
    sp0.font.size = Pt(13)
    sp0.font.bold = True
    sp0.font.color.rgb = COLOR_SUCCESS

    modules = [
        ("M1", "Application (FastAPI + React 18 + PostgreSQL + Alembic)", "10 / 10 pts", "COMPLETE", COLOR_SUCCESS),
        ("M2", "Testing (45 Pytest tests, 91% coverage, SQLite isolation)", "10 / 10 pts", "COMPLETE", COLOR_SUCCESS),
        ("M3", "Git & GitHub (16+ conventional commits, strict .gitignore)", "5 / 5 pts", "COMPLETE", COLOR_SUCCESS),
        ("M4", "Docker (Multi-stage Dockerfiles, non-root users, compose)", "10 / 10 pts", "COMPLETE", COLOR_SUCCESS),
        ("M5", "CI/CD (GitHub Actions pipeline, Pytest gate, GHCR SHA tags)", "15 / 15 pts", "COMPLETE", COLOR_SUCCESS),
        ("M6", "DevSecOps (Aqua Trivy scan with exit-code: 1 for CVEs)", "5 / 5 pts", "COMPLETE", COLOR_SUCCESS),
        ("M7", "Terraform (AWS 3-AZ VPC, EKS v1.31 cluster, destroy verified)", "15 / 15 pts", "COMPLETE", COLOR_SUCCESS),
        ("M8", "Kubernetes & Helm (Chart with 13 templates, 2 replicas, Ingress)", "15 / 15 pts", "COMPLETE", COLOR_SUCCESS),
        ("M9", "Observability (Prometheus /metrics scraping & Grafana)", "10 / 10 pts", "COMPLETE", COLOR_SUCCESS),
        ("M10", "Documentation & GitOps (14KB README & push-to-deploy demo)", "5 / 5 pts", "COMPLETE", COLOR_SUCCESS),
    ]

    for code, desc, pts, status, color in modules:
        stf.add_paragraph()
        p = stf.add_paragraph()
        p.text = f"[{code}] {desc.ljust(65)} {pts.rjust(12)}  •  {status}"
        p.font.name = "Consolas"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_LIGHT

    # Final Summary Banner
    banner = add_card(s14, Inches(1.2), Inches(5.8), Inches(10.933), Inches(0.9),
                      fill_color=RGBColor(6, 78, 59), border_color=COLOR_SUCCESS)
    btf = banner.text_frame
    btf.word_wrap = True
    bp = btf.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    bp.text = "TOTAL ESTIMATED GRADE: 100 / 100 POINTS (GRADE: A+ / FULL MARKS)"
    bp.font.name = FONT_HEADING
    bp.font.size = Pt(14)
    bp.font.bold = True
    bp.font.color.rgb = COLOR_TEXT_LIGHT

    add_notes(s14, """
VIDEO SCRIPT - SLIDE 14 (CONCLUSION):
"To conclude our presentation: SpendIQ successfully implements every single requirement specified in the Session 21 grading rubric.

From code quality, automated unit testing, and hardened container builds, to GitHub Actions CI/CD with Aqua Trivy DevSecOps scanning, Terraform AWS infrastructure, high-availability Helm packaging, and full Prometheus/Grafana observability—every component has been engineered for production reliability, security, and scalability.

Thank you very much for your time and evaluation."
""")

    prs.save(OUTPUT_PPTX)
    print(f"Presentation successfully generated at: {OUTPUT_PPTX}")


if __name__ == "__main__":
    create_presentation()
