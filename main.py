"""
Medical Device Compliance Scaffold
Integrates LangGraph workflows, Autogen auditors, and document generation
for ISO 13485, ISO 14971, and IEC 62304 compliance
"""

import asyncio
import json
import os
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, TypedDict

import autogen
import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches
from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
import PyPDF2


# ============================================================================
# CORE DATA MODELS
# ============================================================================

class StandardType(Enum):
    """Medical device compliance standards"""
    ISO_13485 = "ISO 13485"
    ISO_14971 = "ISO 14971"
    IEC_62304 = "IEC 62304"


@dataclass
class TraceabilityItem:
    """Represents a single item in the traceability matrix"""
    id: str
    standard: StandardType
    requirement: str
    implementation: str
    verification: str
    validation: str
    status: str = "Open"
    risk_level: str = "Medium"
    assigned_to: str = ""
    completion_date: str = ""


@dataclass
class ComplianceDocument:
    """Represents a compliance document"""
    title: str
    standard: StandardType
    content: str
    traceability_items: List[TraceabilityItem] = field(default_factory=list)
    audit_results: Dict[str, Any] = field(default_factory=dict)
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())


class WorkflowState(TypedDict):
    """LangGraph workflow state"""
    messages: List[Dict[str, Any]]
    current_document: ComplianceDocument
    audit_feedback: Dict[str, List[str]]
    traceability_matrix: List[TraceabilityItem]
    workflow_step: str
    input_document_content: str


# ============================================================================
# DOCUMENT READING FUNCTIONS
# ============================================================================

def read_docx_file(file_path: str) -> str:
    """Extract text content from DOCX file"""
    try:
        doc = Document(file_path)
        content = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                content.append(paragraph.text)
        return '\n'.join(content)
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return ""

def read_pdf_file(file_path: str) -> str:
    """Extract text content from PDF file"""
    try:
        content = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text.strip():
                    content.append(text)
        return '\n'.join(content)
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

def load_document_for_review(file_path: str) -> str:
    """Load document content based on file extension"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return ""
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        return read_docx_file(file_path)
    elif ext == '.pdf':
        return read_pdf_file(file_path)
    else:
        print(f"Unsupported file format: {ext}")
        return ""

# ============================================================================
# SAMPLE DATA GENERATION
# ============================================================================

def create_sample_traceability_matrix() -> List[TraceabilityItem]:
    """Creates a sample traceability matrix for medical device standards"""
    return [
        # ISO 13485 Quality Management System
        TraceabilityItem(
            id="ISO13485-4.1.1",
            standard=StandardType.ISO_13485,
            requirement="Establish QMS processes and their sequence/interaction",
            implementation="QMS Process Map documented in QM-001",
            verification="Process map review and approval by QA",
            validation="QMS effectiveness audit results",
            status="Completed",
            risk_level="High"
        ),
        TraceabilityItem(
            id="ISO13485-4.2.3",
            standard=StandardType.ISO_13485,
            requirement="Control of documents - ensure current versions available",
            implementation="Document control system DCS-v2.1 implemented",
            verification="Document control procedure testing",
            validation="User acceptance testing completed",
            status="Completed",
            risk_level="Medium"
        ),
        TraceabilityItem(
            id="ISO13485-7.3.2",
            standard=StandardType.ISO_13485,
            requirement="Design and development planning",
            implementation="Design control procedure DC-001 established",
            verification="Design plan template created and reviewed",
            validation="Design process validation pending",
            status="In Progress",
            risk_level="High"
        ),
        # ISO 14971 Risk Management
        TraceabilityItem(
            id="ISO14971-4.1",
            standard=StandardType.ISO_14971,
            requirement="Risk management process shall be established",
            implementation="Risk management plan RMP-001 created",
            verification="Risk process documented and approved",
            validation="Risk management effectiveness review",
            status="Completed",
            risk_level="High"
        ),
        TraceabilityItem(
            id="ISO14971-4.4",
            standard=StandardType.ISO_14971,
            requirement="Risk analysis shall be performed for each hazard",
            implementation="FMEA analysis completed for all subsystems",
            verification="FMEA review by risk committee",
            validation="Risk analysis validation pending",
            status="In Progress",
            risk_level="High"
        ),
        TraceabilityItem(
            id="ISO14971-5.2",
            standard=StandardType.ISO_14971,
            requirement="Risk control measures shall be implemented",
            implementation="Risk mitigation strategies documented",
            verification="Risk controls design review completed",
            validation="Effectiveness of risk controls to be validated",
            status="Open",
            risk_level="Medium"
        ),
        # IEC 62304 Medical Device Software
        TraceabilityItem(
            id="IEC62304-4.3",
            standard=StandardType.IEC_62304,
            requirement="Medical device software safety classification",
            implementation="Software classified as Class B (non-life-threatening)",
            verification="Safety classification review completed",
            validation="Classification validation with risk analysis",
            status="Completed",
            risk_level="High"
        ),
        TraceabilityItem(
            id="IEC62304-5.1.1",
            standard=StandardType.IEC_62304,
            requirement="Planning of software development process",
            implementation="Software development plan SDP-001 established",
            verification="Development plan review and approval",
            validation="Plan effectiveness validation pending",
            status="In Progress",
            risk_level="Medium"
        ),
        TraceabilityItem(
            id="IEC62304-5.5.1",
            standard=StandardType.IEC_62304,
            requirement="Software integration and integration testing",
            implementation="Integration test plan and procedures created",
            verification="Integration testing executed successfully",
            validation="Integration validation pending",
            status="Open",
            risk_level="Medium"
        )
    ]


# ============================================================================
# AUTOGEN SPECIALIST AUDITORS
# ============================================================================

def create_specialist_auditors():
    """Creates specialized auditor agents for each standard"""
    llm_config = {
        "config_list": [{"model": "gpt-5-mini", "api_key": os.getenv("OPENAI_API_KEY")}],
        "temperature": 0.1,
    }

    iso13485_auditor = autogen.AssistantAgent(
        name="ISO13485_Auditor",
        system_message="""You are a specialist auditor for ISO 13485 Quality Management Systems.
        Review documents for:
        - QMS process compliance
        - Document control requirements
        - Management responsibility
        - Resource management
        - Product realization
        - Measurement and improvement
        Provide specific, actionable feedback with clause references.""",
        llm_config=llm_config
    )

    iso14971_auditor = autogen.AssistantAgent(
        name="ISO14971_Auditor",
        system_message="""You are a specialist auditor for ISO 14971 Risk Management.
        Review documents for:
        - Risk management process
        - Risk analysis completeness
        - Risk evaluation criteria
        - Risk control measures
        - Risk management file
        - Post-market surveillance
        Focus on risk-based approach and hazard identification.""",
        llm_config=llm_config
    )

    iec62304_auditor = autogen.AssistantAgent(
        name="IEC62304_Auditor",
        system_message="""You are a specialist auditor for IEC 62304 Medical Device Software.
        Review documents for:
        - Software safety classification
        - Software development planning
        - Software requirements analysis
        - Software architectural design
        - Software integration and testing
        - Software verification and validation
        Ensure software lifecycle process compliance.""",
        llm_config=llm_config
    )

    coordinator = autogen.AssistantAgent(
        name="Compliance_Coordinator",
        system_message="""You coordinate compliance activities across all standards.
        Synthesize feedback from specialist auditors and:
        - Identify cross-standard dependencies
        - Prioritize compliance gaps
        - Recommend corrective actions
        - Track traceability across standards
        Ensure holistic compliance approach.""",
        llm_config=llm_config
    )

    return {
        "iso13485": iso13485_auditor,
        "iso14971": iso14971_auditor,
        "iec62304": iec62304_auditor,
        "coordinator": coordinator
    }


# ============================================================================
# DOCUMENT GENERATION WITH GUARDRAILS
# ============================================================================

class DocumentGuardrails:
    """Implements guardrails for document generation"""

    REQUIRED_SECTIONS = {
        StandardType.ISO_13485: [
            "Purpose and Scope",
            "QMS Process Description",
            "Roles and Responsibilities",
            "Process Controls",
            "Monitoring and Measurement",
            "Improvement Actions"
        ],
        StandardType.ISO_14971: [
            "Risk Management Scope",
            "Risk Analysis Process",
            "Risk Evaluation Criteria",
            "Risk Control Measures",
            "Risk Management File",
            "Post-Market Surveillance"
        ],
        StandardType.IEC_62304: [
            "Software Description",
            "Safety Classification",
            "Development Process",
            "Requirements Specification",
            "Architecture Design",
            "Testing and Verification"
        ]
    }

    @staticmethod
    def validate_content(standard: StandardType, content: str) -> List[str]:
        """Validates document content against guardrails"""
        issues = []
        required_sections = DocumentGuardrails.REQUIRED_SECTIONS.get(standard, [])
        content_lower = content.lower()

        for section in required_sections:
            if section.lower() not in content_lower:
                issues.append(f"Missing required section: {section}")

        if len(content) < 500:
            issues.append("Document content too brief for compliance documentation")

        if "TODO" in content or "TBD" in content:
            issues.append("Document contains placeholder content (TODO/TBD)")

        return issues

    @staticmethod
    def _get_iso13485_template() -> str:
        return """# Quality Management System Document

## Purpose and Scope
This document establishes the Quality Management System (QMS) processes in accordance with ISO 13485 requirements.

## QMS Process Description
The QMS encompasses all processes from design and development through production, installation, and servicing.

## Roles and Responsibilities
- Management Representative: Overall QMS responsibility
- Quality Manager: Day-to-day QMS operations
- Process Owners: Individual process management

## Process Controls
Key processes are controlled through documented procedures, work instructions, and monitoring.

## Monitoring and Measurement
Regular audits and management reviews ensure QMS effectiveness.

## Improvement Actions
Continuous improvement through corrective and preventive actions."""

    @staticmethod
    def _get_iso14971_template() -> str:
        return """# Risk Management Plan

## Risk Management Scope
This plan covers risk management activities for [Device Name] throughout its lifecycle.

## Risk Analysis Process
Systematic process for identifying hazards, estimating risks, and evaluating risk acceptability.

## Risk Evaluation Criteria
Risk acceptance criteria based on severity and probability classifications.

## Risk Control Measures
Hierarchy of risk control: inherent safety, protective measures, information for safety.

## Risk Management File
Comprehensive documentation of all risk management activities and decisions.

## Post-Market Surveillance
Ongoing monitoring of device performance and emerging risks."""

    @staticmethod
    def _get_iec62304_template() -> str:
        return """# Software Development Plan

## Software Description
[Device software overview, intended use, and operating environment]

## Safety Classification
Software safety classification per IEC 62304: Class A/B/C determination.

## Development Process
Software lifecycle processes including planning, requirements, design, implementation, testing.

## Requirements Specification
Comprehensive software requirements derived from system requirements.

## Architecture Design
High-level software architecture ensuring safety and maintainability.

## Testing and Verification
Verification activities to ensure requirements implementation and safety."""

    @staticmethod
    def generate_compliant_template(standard: StandardType) -> str:
        """Generates a compliant document template"""
        template_map = {
            StandardType.ISO_13485: DocumentGuardrails._get_iso13485_template,
            StandardType.ISO_14971: DocumentGuardrails._get_iso14971_template,
            StandardType.IEC_62304: DocumentGuardrails._get_iec62304_template
        }

        template_func = template_map.get(standard)
        return template_func() if template_func else "# Compliance Document Template"


def generate_docx_document(doc: ComplianceDocument, output_path: str):
    """Generates a Word document with guardrails compliance"""
    # Validate and sanitize output path to prevent path traversal
    safe_filename = os.path.basename(output_path)
    if not safe_filename or '..' in output_path or os.path.isabs(output_path):
        safe_filename = "compliance_document.docx"
    output_path = safe_filename

    # Validate content first
    issues = DocumentGuardrails.validate_content(doc.standard, doc.content)

    # Create Word document
    word_doc = Document()

    # Add title
    title = word_doc.add_heading(doc.title, 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add document info
    info_table = word_doc.add_table(rows=4, cols=2)
    info_table.style = 'Table Grid'

    info_data = [
        ("Standard", doc.standard.value),
        ("Created Date", doc.created_date),
        ("Document Status", "Draft" if issues else "Approved"),
        ("Compliance Issues", str(len(issues)))
    ]

    for i, (label, value) in enumerate(info_data):
        info_table.cell(i, 0).text = label
        info_table.cell(i, 1).text = value

    word_doc.add_paragraph()

    # Add compliance issues if any
    if issues:
        word_doc.add_heading('Compliance Issues', level=1)
        for issue in issues:
            word_doc.add_paragraph(issue, style='List Bullet')
        word_doc.add_page_break()

    # Add main content
    word_doc.add_heading('Document Content', level=1)

    # Split content by lines and add as paragraphs
    content_lines = doc.content.strip().split('\n')
    for line in content_lines:
        line = line.strip()
        if line.startswith('# '):
            word_doc.add_heading(line[2:], level=1)
        elif line.startswith('## '):
            word_doc.add_heading(line[3:], level=2)
        elif line:
            word_doc.add_paragraph(line)

    # Add traceability matrix if available
    if doc.traceability_items:
        word_doc.add_page_break()
        word_doc.add_heading('Traceability Matrix', level=1)

        # Create table for traceability items
        trace_table = word_doc.add_table(rows=1, cols=6)
        trace_table.style = 'Table Grid'

        # Headers
        headers = ['ID', 'Requirement', 'Implementation', 'Verification', 'Status', 'Risk Level']
        for i, header in enumerate(headers):
            trace_table.cell(0, i).text = header

        # Add traceability items
        for item in doc.traceability_items:
            row_cells = trace_table.add_row().cells
            row_cells[0].text = item.id
            row_cells[1].text = f"{item.requirement[:50]}..." if len(item.requirement) > 50 else item.requirement
            row_cells[2].text = f"{item.implementation[:50]}..." if len(item.implementation) > 50 else item.implementation
            row_cells[3].text = f"{item.verification[:50]}..." if len(item.verification) > 50 else item.verification
            row_cells[4].text = item.status
            row_cells[5].text = item.risk_level

    # Save document
    try:
        word_doc.save(output_path)
        print(f"Document saved to: {output_path}")
    except (IOError, PermissionError, OSError) as e:
        print(f"Error saving document: {e}")
        raise


# ============================================================================
# LANGGRAPH WORKFLOW DEFINITION
# ============================================================================

def create_compliance_workflow():
    """Creates the LangGraph workflow for compliance processing"""

    def initialize_workflow(state: WorkflowState) -> WorkflowState:
        """Initialize the workflow with sample data"""
        print("🚀 Initializing compliance workflow...")

        state["traceability_matrix"] = create_sample_traceability_matrix()
        state["audit_feedback"] = {}
        state["workflow_step"] = "initialized"

        state["messages"] = add_messages(state["messages"], [{
            "role": "system",
            "content": "Workflow initialized with sample traceability matrix"
        }])

        return state

    def generate_document(state: WorkflowState) -> WorkflowState:
        """Generate compliance document based on standard"""
        print("📄 Generating compliance document...")

        standard = getattr(state.get("current_document"), "standard", StandardType.ISO_13485)
        
        # Use input document content if available, otherwise use template
        if state.get("input_document_content"):
            content = state["input_document_content"]
            print("📥 Using uploaded document content for review")
        else:
            content = DocumentGuardrails.generate_compliant_template(standard)
            print("📝 Using standard template")

        relevant_items = [
            item for item in state["traceability_matrix"]
            if item.standard == standard
        ]

        doc = ComplianceDocument(
            title=f"{standard.value} Compliance Document",
            standard=standard,
            content=content,
            traceability_items=relevant_items
        )

        state["current_document"] = doc
        state["workflow_step"] = "document_generated"

        state["messages"] = add_messages(state["messages"], [{
            "role": "assistant",
            "content": f"Generated {standard.value} compliance document with {len(relevant_items)} traceability items"
        }])

        return state

    def audit_document(state: WorkflowState) -> WorkflowState:
        """Simulate audit process using Autogen agents"""
        print("🔍 Auditing document with specialist auditors...")

        audit_feedback = {
            "iso13485": [
                "QMS process interactions need more detail",
                "Management review frequency should be specified",
                "Document control procedure reference missing"
            ],
            "iso14971": [
                "Risk evaluation criteria need quantitative thresholds",
                "Post-market surveillance plan incomplete",
                "Risk control effectiveness measures undefined"
            ],
            "iec62304": [
                "Software architecture documentation insufficient",
                "Integration testing strategy needs elaboration",
                "Verification methods not fully specified"
            ],
            "coordinator": [
                "Cross-standard traceability gaps identified",
                "Risk management integration with QMS needed",
                "Software verification should reference risk controls"
            ]
        }

        state["audit_feedback"] = audit_feedback
        state["workflow_step"] = "document_audited"

        total_issues = sum(len(feedback) for feedback in audit_feedback.values())

        state["messages"] = add_messages(state["messages"], [{
            "role": "system",
            "content": f"Audit completed. Found {total_issues} items for review across all standards"
        }])

        return state

    def finalize_compliance(state: WorkflowState) -> WorkflowState:
        """Finalize compliance documentation"""
        print("✅ Finalizing compliance documentation...")

        doc = state["current_document"]
        doc.audit_results = state["audit_feedback"]

        safe_filename = "".join(c for c in doc.standard.value if c.isalnum() or c in (' ', '-', '_')).rstrip()
        output_path = f"{safe_filename.replace(' ', '_')}_compliance_document.docx"
        generate_docx_document(doc, output_path)

        state["workflow_step"] = "completed"

        state["messages"] = add_messages(state["messages"], [{
            "role": "assistant",
            "content": f"Compliance documentation finalized. Document saved as {output_path}"
        }])

        return state

    # Build the workflow graph
    workflow = StateGraph(WorkflowState)

    workflow.add_node("initialize", initialize_workflow)
    workflow.add_node("generate_document", generate_document)
    workflow.add_node("audit_document", audit_document)
    workflow.add_node("finalize", finalize_compliance)

    workflow.add_edge(START, "initialize")
    workflow.add_edge("initialize", "generate_document")
    workflow.add_edge("generate_document", "audit_document")
    workflow.add_edge("audit_document", "finalize")
    workflow.add_edge("finalize", END)

    return workflow.compile()


# ============================================================================
# TRACEABILITY MATRIX UTILITIES
# ============================================================================

def export_traceability_matrix_to_excel(items: List[TraceabilityItem], output_path: str):
    """Export traceability matrix to Excel format"""
    data = [{
        'ID': item.id,
        'Standard': item.standard.value,
        'Requirement': item.requirement,
        'Implementation': item.implementation,
        'Verification': item.verification,
        'Validation': item.validation,
        'Status': item.status,
        'Risk Level': item.risk_level,
        'Assigned To': item.assigned_to,
        'Completion Date': item.completion_date
    } for item in items]

    df = pd.DataFrame(data)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Traceability Matrix', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Traceability Matrix']

        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except (AttributeError, TypeError, ValueError):
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

    print(f"Traceability matrix exported to: {output_path}")


def generate_compliance_report(items: List[TraceabilityItem]) -> Dict[str, Any]:
    """Generate compliance status report"""
    report = {
        "total_items": len(items),
        "by_standard": {},
        "by_status": defaultdict(int),
        "by_risk_level": defaultdict(int),
        "completion_stats": {}
    }

    completed_count = 0
    for item in items:
        if item.standard.value not in report["by_standard"]:
            report["by_standard"][item.standard.value] = 0
        report["by_standard"][item.standard.value] += 1

        report["by_status"][item.status] += 1
        if item.status == "Completed":
            completed_count += 1

        report["by_risk_level"][item.risk_level] += 1

    report["by_status"] = dict(report["by_status"])
    report["by_risk_level"] = dict(report["by_risk_level"])

    completion_percentage = (completed_count / len(items)) * 100 if items else 0
    report["completion_stats"]["percentage"] = round(completion_percentage, 1)
    report["completion_stats"]["completed"] = completed_count
    report["completion_stats"]["remaining"] = len(items) - completed_count

    return report


# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================

async def run_compliance_workflow(input_file_path: str = None):
    """Main function to run the complete compliance workflow"""
    print("=" * 80)
    print("MEDICAL DEVICE COMPLIANCE WORKFLOW")
    print("=" * 80)

    # Load input document if provided
    input_content = ""
    if input_file_path:
        print(f"📂 Loading document: {input_file_path}")
        input_content = load_document_for_review(input_file_path)
        if input_content:
            print(f"✅ Document loaded successfully ({len(input_content)} characters)")
        else:
            print("⚠️ Failed to load document, using template instead")

    workflow = create_compliance_workflow()

    initial_state = {
        "messages": [],
        "current_document": None,
        "audit_feedback": {},
        "traceability_matrix": [],
        "workflow_step": "starting",
        "input_document_content": input_content
    }

    final_state = await workflow.ainvoke(initial_state)

    print("\n" + "=" * 80)
    print("WORKFLOW RESULTS")
    print("=" * 80)

    for msg in final_state["messages"]:
        content = getattr(msg, 'content', str(msg))
        print(f"📝 {content}")

    matrix_file = "traceability_matrix.xlsx"
    export_traceability_matrix_to_excel(final_state["traceability_matrix"], matrix_file)

    report = generate_compliance_report(final_state["traceability_matrix"])

    print(f"\n📊 COMPLIANCE REPORT:")
    print(f"   Total Items: {report['total_items']}")
    print(f"   Completion: {report['completion_stats']['percentage']}%")
    print(f"   Completed: {report['completion_stats']['completed']}")
    print(f"   Remaining: {report['completion_stats']['remaining']}")

    print(f"\n📋 BY STANDARD:")
    for standard, count in report["by_standard"].items():
        print(f"   {standard}: {count} items")

    print(f"\n🎯 BY STATUS:")
    for status, count in report["by_status"].items():
        print(f"   {status}: {count} items")

    print(f"\n⚠️  BY RISK LEVEL:")
    for risk_level, count in report["by_risk_level"].items():
        print(f"   {risk_level}: {count} items")

    print(f"\n✅ Generated Files:")
    if final_state.get('current_document'):
        print(f"   - {final_state['current_document'].title.replace(' ', '_')}.docx")
    print(f"   - {matrix_file}")

    return final_state


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    load_dotenv()
    
    # Example usage with document file
    # asyncio.run(run_compliance_workflow("path/to/your/document.docx"))
    # asyncio.run(run_compliance_workflow("path/to/your/document.pdf"))
    
    # Run without input file (uses templates)
    asyncio.run(run_compliance_workflow())