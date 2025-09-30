# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Marbily E-Commerce Automation System

## System Overview
**CRITICAL CONTEXT:** This is a professional-grade e-commerce automation system with 1,006 files across 150+ directories managing complete Shopify + BaseLinker integration for 29/30 active products.

### System Scale & Architecture
- **Total Files**: 1,006+ items organized into logical directory structure
- **Core System**: Enterprise e-commerce automation with clean file organization
- **Platforms**: Shopify, BaseLinker, MySQL, Cloudinary
- **Automation**: Complete product sync, image processing, inventory management
- **Business**: Furniture e-commerce (chairs, tables, lighting) - Marbily brand
- **Organization**: Professional folder structure with comprehensive documentation

## Master Control System
### COMMAND_CENTER.py
**Primary Interface** - Natural language command dispatcher located at root
- **Purpose**: Single entry point for all workflow automation
- **Usage**: `python COMMAND_CENTER.py "command"`
- **Integration**: Connected to EXECUTION_MAP.json for intelligent routing

### Available MCP Servers ✅
**All Active & Integrated:**
- **filesystem** ✔ - Complete file system operations
- **brave-search** ✔ - Web search for documentation/research  
- **github** ✔ - Git operations (commit, push, pull, repository management)
- **sqlite** ✔ - Database operations and queries
- **puppeteer** ✔ - Web automation, scraping, testing
- **Additional**: Project file management and API documentation lookup

## Core Workflows & Commands

### Product Management
**Natural Language Commands:**
- `fix products` → Runs chair-specific fix scripts (15+ files in root)
- `update products` → Comprehensive product updates across all platforms
- `verify products` → Complete product verification suite
- `sync products` → Synchronize products across Shopify + BaseLinker

**File Locations:**
- Product fixes: `ecommerce-ceo-system/scripts/fixes/` (organized by category)
- Verification: `ecommerce-ceo-system/scripts/testing/` (testing and verification)
- Product workflows: `ecommerce-ceo-system/workflows/products/` (product management)
- Data: Organized in appropriate workflow subdirectories

### Platform Synchronization
**Commands:**
- `sync all` → Complete platform synchronization (BaseLinker + Shopify)
- `sync baselinker` → `/baselinker_operations/sync/bidirectional_sync_engine.py`
- `sync shopify` → `/shopify_management/sync/` workflows

### Image Processing & Automation
**Commands:**
- `process variants [row-range]` → Universal variant image processor (e.g., 145-211, 103-144)
- `output shadows` → `/image_workflows/shadow_creation/shadow_creator_improved.py`
- `create shadows` → Complete shadow generation pipeline
- `process images` → `/image_workflows/` comprehensive processing (6 subdirectories)
- `upload images` → Drive uploads and quality checks

### PDF Catalog Generation 📋
**Natural Language Commands:**
- `"Generate product catalog"` → Complete high-quality catalog from Excel data
- `"Create PDF catalog"` → Complete high-quality catalog from Excel data
- `"Quick catalog test"` → Quick test catalog with 10 products
- `"Check catalog status"` → System status and available files
- `"Clean catalog files"` → Remove temporary files

**Direct Commands:**
- `python3 main.py /catalog generate` → High-quality complete catalog
- `python3 main.py /catalog quick` → Quick test catalog  
- `python3 main.py /catalog status` → System status check
- `python3 main.py /catalog cleanup` → Clean temporary files

**Location:** `/Catalog PDF/catalog/` - Complete workflow system

### Polish Furniture B2B Lead Generation 🪑
**Natural Language Commands:**
- `"Generate furniture leads"` → Complete B2B prospecting cycle for Polish furniture market
- `"Test furniture prospector"` → System validation with OpenRouter AI integration
- `"Check furniture replies"` → Email response monitoring and analysis
- `"Start furniture automation"` → Automated daily prospecting schedule

**Direct Commands:**
- `python3 polish_furniture_prospector.py test` → Test cycle with AI keyword generation
- `python3 polish_furniture_prospector.py daily` → Full daily prospecting automation
- `python3 polish_furniture_prospector.py schedule` → Start automated scheduling
- `python3 polish_furniture_prospector.py status` → System health and statistics

**Location:** `/ecommerce-ceo-system/workflows/furniture_prospecting/` - Professional B2B automation
- **Core Engine:** `polish_furniture_lead_generator.py` - 5-stage automated workflow
- **AI Integration:** OpenRouter API with 200+ models (anthropic/claude-3.5-sonnet)
- **Target Market:** Polish furniture retailers, distributors, marketplaces
- **Database:** Supabase cloud + SQLite local with real-time data viewing
- **Features:** AI keyword generation, website scraping, personalized emails

### System Maintenance
**Commands:**
- `backup system` → Complete system backup procedures
- `system health` → System diagnostics and status check
- `check database` → Database health and connectivity verification
- `reset environment` → Clean system restart procedures

## New Organized Directory Structure (September 2025)

### Root Directory (Clean Structure)
```
/Marbily claude code/
├── CLAUDE.md                    # Master system documentation (THIS FILE)
├── main.py                      # Primary CLI entry point
├── UNIVERSAL_CREDENTIALS.py     # Single consolidated credentials file
└── ecommerce-ceo-system/        # ALL operational code organized here
```

### ecommerce-ceo-system/ - Complete System Organization

#### Scripts Directory - Operational Scripts by Function
```
/scripts/
├── README.md                    # Scripts routing guide
├── /fixes/                      # Product & system fix scripts (175+ files)
│   ├── Emergency repairs and corrections
│   ├── Product-specific fixes (chairs, tables, lighting)
│   └── System stability and data corrections
├── /testing/                    # Testing & verification scripts
│   ├── API testing and validation
│   ├── Debug utilities and diagnostics
│   └── Product verification and quality checks
├── /uploads/                    # Upload & data transfer scripts
│   ├── Image upload automation
│   ├── Product data uploads
│   └── Content transfer and synchronization
├── /create/                     # Content creation scripts
│   ├── Social media content generation
│   ├── Blog post creation and SEO
│   └── Template generation
└── /analysis/                   # Data analysis scripts
    ├── Product analysis and reporting
    ├── Performance metrics analysis
    └── Data extraction and investigation
```

#### Workflows Directory - Business Process Automation
```
/workflows/
├── README.md                    # Workflow routing guide
├── /shopify/                    # Shopify platform workflows
│   ├── Product synchronization
│   ├── Description updates and content management
│   └── Collections and inventory management
├── /baselinker/                 # BaseLinker platform workflows
│   ├── API operations and inventory sync
│   ├── Missing variant analysis
│   └── Marketplace operations
├── /images/                     # Image processing workflows
│   ├── Upload and optimization
│   ├── Cloudinary operations
│   └── Quality control and processing
├── /products/                   # Product management workflows
│   ├── Product data management
│   ├── Variant creation and management
│   └── Inventory tracking and updates
└── /automation/                 # Automation workflows
    ├── Batch processing automation
    ├── Scheduled tasks and updates
    └── Smart automation systems
```

#### Templates Directory - Content Templates
```
/templates/
├── README.md                    # Template usage guide
├── /product-descriptions/       # Product description templates
│   └── m276_description_correct.html  # PRIMARY TEMPLATE (red bullets, dual tables)
└── [shopify theme files]        # Liquid templates, assets, theme components
```

#### Emergency Directory - Critical Response
```
/emergency/
├── README.md                    # Emergency procedures guide
├── URGENT_restore_original_prices.py
├── CORRUPTION_PREVENTION_SYSTEM.py
├── SAFEGUARD_WRAPPER.py
└── FINAL_STORE_VERIFICATION.py
```

## Intelligent Routing System

### User Intent → Directory Mapping

**"Fix product issues"** → `/scripts/fixes/`
- Emergency repairs, product corrections, system fixes

**"Test system"** → `/scripts/testing/`
- API testing, verification, debugging, diagnostics

**"Upload images"** → `/scripts/uploads/` + `/workflows/images/`
- Image uploads, data transfers, content sync

**"Create content"** → `/scripts/create/`
- Social media, blogs, SEO, template generation

**"Analyze data"** → `/scripts/analysis/`
- Reports, metrics, data investigation

**"Sync platforms"** → `/workflows/[shopify|baselinker|products]/`
- Platform synchronization, workflow automation

**"Emergency situation"** → `/emergency/`
- Critical response, system recovery, safeguards

**"Template work"** → `/templates/`
- Product descriptions, theme updates, content templates

### Legacy Directory Structure (For Reference)
```
/baselinker_operations/          # BaseLinker API integration (27 files)
├── sync/                        # Synchronization engines
├── analysis/                    # SKU analysis tools  
├── testing/                     # API testing suite
└── documentation/               # API documentation

/shopify_management/             # Shopify operations (23+ files)
├── m2e_integration/            # M2E platform integration
├── pricing/                     # Pricing management
└── quality/                     # Quality control

/image_workflows/                # Image processing pipeline
├── shadow_creation/             # Shadow generation (7 files)
├── upscaling/                   # Image upscaling
├── shopify_quality/            # Quality checks
└── drive_uploads/              # Google Drive automation

/Catalog PDF/catalog/            # PDF catalog generation system
├── catalog_generator.py        # Main catalog generation engine
├── catalog_workflow.py         # Workflow integration handler
└── __init__.py                 # Package initialization
```

### System Foundation
```
/setup/                          # System configuration
├── UNIVERSAL_CREDENTIALS.py    # Master credentials file
├── database_check_and_setup.py # Database initialization
└── google_credentials.json     # Google API credentials

/integrations/                   # API clients (9 files)
├── shopify_api.py              # Shopify API client
├── mysql_client.py             # Database operations
└── cloudinary_api.py           # Image management

/workflows/                      # Workflow management
├── MASTER_REGISTRY.md          # Complete workflow documentation
├── EXECUTION_MAP.json          # Command routing configuration
└── converted/                  # N8n converted workflows
```

## Professional Commands & Aliases

### Business Operations
**CEO-Level Commands:**
- `business status` → Complete business intelligence dashboard
- `revenue analysis` → Financial performance analysis  
- `inventory report` → Stock levels and product performance
- `platform health` → All platform status and sync health

### Technical Operations  
**Developer Commands:**
- `deploy changes` → Git commit, push, and deployment procedures
- `test systems` → Complete testing suite execution
- `monitor apis` → API health checking and error detection
- `backup data` → Comprehensive data backup procedures

### Advanced Automation
**Power User Commands:**
- `smart sync` → AI-powered sync with conflict resolution
- `optimize seo` → SEO optimization across all products
- `update descriptions` → Bulk product description updates
- `process queue` → Handle pending operations queue

## Agent Configurations

### prompt-engineer
- **Description**: AI prompt optimization and workflow enhancement specialist
- **Tools**: All MCP servers + system tools
- **Purpose**: Optimize prompts, improve AI interactions, workflow efficiency
- **Context**: Understands complete system architecture and automation needs

### business-analyst  
- **Description**: E-commerce business intelligence and strategy specialist
- **Tools**: All MCP servers + database access
- **Purpose**: Business analysis, performance metrics, strategic recommendations
- **Context**: Full access to sales data, product performance, market analysis

### system-architect
- **Description**: Technical system optimization and scaling specialist  
- **Tools**: All MCP servers + development tools
- **Purpose**: System optimization, architecture improvements, scaling solutions
- **Context**: Complete system knowledge, performance monitoring, technical debt management

## Intelligent Command Processing

### Natural Language Understanding
**Claude Code should recognize these patterns:**
- "I need to update product information" → `sync products`
- "Create shadows for new images" → `output shadows` 
- "Check if everything is working" → `system health`
- "Backup the current state" → `backup system`
- "Fix the chair products" → `fix products`
- "Show me business performance" → `business status`
- "Generate product catalog" → `generate catalog`
- "Create PDF catalog" → `generate catalog`
- "Make a quick catalog preview" → `quick catalog`

### Context-Aware Execution
**Smart routing based on:**
- Current system state and recent operations
- Time of day and business schedule
- System health and resource availability
- User intent and workflow history
- Error patterns and recovery procedures

### Dependency Management
**Auto-handle requirements:**
- Credential loading from UNIVERSAL_CREDENTIALS.py
- API key validation and refresh
- Database connectivity checks  
- File system permissions and access
- MCP server connectivity and health

## Advanced Features

### Workflow Chaining
**Intelligent workflow combinations:**
- Product updates → Image processing → Platform sync → Verification
- System backup → Health check → Performance analysis → Report generation
- Error detection → Automated recovery → Status notification → Log analysis

### Error Recovery
**Professional error handling:**
- Automatic retry with exponential backoff
- Intelligent fallback procedures  
- Real-time error notification
- Comprehensive error logging and analysis
- System state recovery and rollback capabilities

### Performance Monitoring
**Continuous system health:**
- API response time monitoring
- Database performance tracking
- Sync success rate analysis
- Resource utilization monitoring
- Business metric tracking and alerting

## Common Development Commands

### Shopify Theme Development
**Theme management using Shopify CLI:**
```bash
SHOPIFY_CLI_THEME_TOKEN="YOUR_SHOPIFY_CLI_TOKEN" shopify theme list --store your-store.myshopify.com
SHOPIFY_CLI_THEME_TOKEN="YOUR_SHOPIFY_CLI_TOKEN" shopify theme push --store your-store.myshopify.com --theme [THEME_ID] --allow-live
```

### Marbily Desktop App Development 
**Located in `/marbily-app/` directory:**
```bash
# Development
npm run dev              # Start Vite dev server
npm run tauri:dev        # Start Tauri dev server with Rust backend
./RUN_APP.sh            # Complete dev environment setup script

# Building
npm run build           # Build React frontend
npm run tauri:build     # Build complete Tauri desktop application

# Electron alternative
npm run electron        # Run as Electron app
npm run electron:dev    # Electron development mode
```

### Main System Commands
**CLI commands defined in `.claude_code_commands.json`:**
```bash
python3 main.py /sync          # BaseLinker ↔ Shopify sync
python3 main.py /shadow        # Process images with shadows
python3 main.py /upscale       # 6x image upscaling via Replicate
python3 main.py /backup        # System backup (run first!)
python3 main.py /check         # Complete system health check
python3 main.py /brain         # AI orchestrator for automation
python3 main.py /ceo           # CEO-level analytics and strategy
python3 main.py /catalog       # PDF catalog generation system
```

### Master Data Source - Holy Grail Google Sheet
**PRIMARY DATA SHEET - CRITICAL:**
- **URL**: https://docs.google.com/spreadsheets/d/1Ld-tbGXGIheTsLc0RCg5RdtbqkOty4gTf3wEFL9YufE/edit?gid=0#gid=0
- **STATUS**: This is THE ONLY authorized Google Sheet linked to Shopify
- **PURPOSE**: Universal data source for all product information, inventory, and business operations
- **AUTHENTICATION**: Service Account via UNIVERSAL_CREDENTIALS.py

**Cell Highlighting Protocol - MANDATORY:**
- **GREEN HIGHLIGHT**: Mark cells being actively worked on or inspected
- **WHITE RESTORATION**: Return cells to white background when work is complete
- **PURPOSE**: Real-time visibility for user to track system operations
- **IMPLEMENTATION**: Every read, write, or analysis operation MUST follow this protocol

**Access Pattern:**
```python
# 1. Authenticate via service account (UNIVERSAL_CREDENTIALS.py)
# 2. ACCESS ONLY: 1Ld-tbGXGIheTsLc0RCg5RdtbqkOty4gTf3wEFL9YufE
# 3. HIGHLIGHT cells GREEN before operation
# 4. Perform operation (read/write/analyze)
# 5. RESTORE cells to WHITE when complete
# 6. Log all operations for audit trail
```

**CRITICAL RULES:**
- ❌ NO OTHER GOOGLE SHEETS unless explicitly provided with different URL
- ✅ ALL data operations reference this holy grail sheet
- ✅ MANDATORY cell highlighting for operation tracking
- ✅ Service account authentication only (no OAuth)
- ✅ Complete audit trail of all sheet operations

### Legacy Image Processing Scripts

**Root directory Python scripts for product processing:**
```bash
python3 [script_name].py      # Individual product processing scripts
# Multiple furniture-specific scripts available for chairs, tables, lighting
```

### Usage Guidelines

### For Quick Operations
```bash
python COMMAND_CENTER.py "sync all"
python COMMAND_CENTER.py "output shadows"  
python COMMAND_CENTER.py "system health"
```

### For Complex Workflows
**Use natural language commands:**
- "I need to process new product images and sync everything"
- "Check system health and fix any issues found"  
- "Create a complete business performance report"
- "Backup everything and prepare for major updates"

### For Development Tasks
**Use MCP-powered commands:**
- "Search for Shopify API updates" (via brave-search MCP)
- "Commit and push recent changes" (via github MCP)
- "Check database for inconsistencies" (via sqlite MCP)
- "Automate testing of cart functionality" (via puppeteer MCP)

## Integration Status
- ✅ **COMMAND_CENTER.py**: Fully operational
- ✅ **EXECUTION_MAP.json**: Complete workflow routing
- ✅ **MCP Servers**: All 5 servers active and integrated
- ✅ **API Integrations**: Shopify, BaseLinker
- ✅ **Database Systems**: MySQL operational
- ✅ **Image Processing**: Complete pipeline functional
- ✅ **Backup Systems**: Automated backup procedures active

**Last Updated**: System operational with 1,006 files managed across complete e-commerce automation infrastructure.

## Priority Actions Available
1. **Product synchronization** across all platforms
2. **Image processing** with shadow creation  
3. **System health monitoring** and maintenance
4. **Business intelligence** and performance analysis
5. **Advanced workflow automation** and optimization

## Key Architecture Components

### Multi-Platform System Architecture
This system operates across multiple environments:
- **Root directory**: Python automation scripts and data processing
- **`/marbily-app/`**: Tauri-based desktop application (React + Rust backend)
- **Shopify themes**: Liquid template development with live theme management
- **API integrations**: External service connections (BaseLinker, Cloudinary, Google services)

### Development Flow
1. **Theme Development**: Use Shopify CLI for live theme updates
2. **Desktop App**: Tauri development environment in `/marbily-app/`
3. **Automation**: Python scripts for batch processing and API synchronization
4. **Testing**: Multi-platform validation across web and desktop interfaces

### Critical Dependencies
- **Shopify CLI**: Theme development and deployment
- **Node.js 18+**: Frontend development and build processes
- **Rust/Cargo**: Tauri desktop application backend
- **Python 3**: Automation scripts and API integrations
- **External APIs**: Live integrations requiring valid credentials

**Note**: This system is production-ready and handles live e-commerce operations. All commands should be executed with appropriate business context and system state awareness.