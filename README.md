# Medical_Device_Compliance_Agent
A comprehensive Python-based system for managing medical device compliance across ISO 13485, ISO 14971, and IEC 62304 standards. This system integrates LangGraph workflows, Autogen auditors, and automated document generation to streamline compliance processes.

## Overview

This repository contains a comprehensive medical device compliance system designed with auditor best practices in mind. The system integrates automated workflows, multi-standard auditing, and traceability management for ISO 13485, ISO 14971, and IEC 62304 compliance.

## Auditor-Focused Features

### Multi-Standard Compliance Auditing
- **ISO 13485**: Quality Management System auditing with focus on QMS processes, document control, and management responsibility
- **ISO 14971**: Risk Management auditing covering risk processes, hazard analysis, and control measures
- **IEC 62304**: Software lifecycle auditing for safety classification, development planning, and verification

### Automated Audit Workflows
- Token-optimized LLM-based auditing system
- Batch processing for efficient document review
- Standardized audit feedback with specific clause references
- Comprehensive traceability matrix generation

### Document Processing & Validation
- Support for multiple formats: DOCX, PDF, TXT
- Automated content extraction and validation
- Minimum document length requirements (500 characters)
- File size limits (50MB max) for processing efficiency

## Auditor Practice Standards

### Traceability Management
The system maintains comprehensive traceability items with:
- **Unique Identifiers**: Standard-specific ID format (e.g., ISO13485-4.1.1)
- **Requirement Mapping**: Direct linkage to standard clauses
- **Implementation Evidence**: Documented implementation details
- **Verification Status**: Tracked verification activities
- **Validation Records**: Validation evidence and results
- **Risk Assessment**: Associated risk levels (Low, Medium, High, Critical)

### Compliance Status Tracking
- **Open**: Items requiring attention
- **In Progress**: Active work items
- **Completed**: Fully implemented and verified
- **Blocked**: Items with dependencies or issues

### Risk-Based Auditing
Risk levels guide audit priorities:
- **Critical**: Immediate attention required
- **High**: Priority review items
- **Medium**: Standard review cycle
- **Low**: Routine monitoring

## Audit Process Workflow

### 1. Document Initialization
```
Input Document → Content Extraction → Validation → Processing
```

### 2. Multi-Standard Analysis
```
Document Content → ISO 13485 Audit → ISO 14971 Audit → IEC 62304 Audit
```

### 3. Traceability Generation
```
Audit Results → Traceability Matrix → Status Tracking → Risk Assessment
```

### 4. Report Generation
```
Audit Findings → Compliance Document → Excel Matrix → Final Report
```

## Key Auditor Benefits

### Efficiency Optimization
- **Token Usage Management**: Optimized LLM calls to reduce costs
- **Batch Processing**: Multiple documents processed simultaneously
- **Content Caching**: Reduced redundant processing
- **Template Standardization**: Consistent document structures

### Comprehensive Coverage
- **Cross-Standard Integration**: Unified view across all applicable standards
- **Gap Analysis**: Automated identification of compliance gaps
- **Evidence Tracking**: Complete audit trail maintenance
- **Continuous Monitoring**: Ongoing compliance status updates

### Quality Assurance
- **Standardized Templates**: Pre-built compliance document templates
- **Validation Rules**: Automated content validation
- **Review Workflows**: Structured review and approval processes
- **Version Control**: Document change tracking and management

## Usage for Auditors

### Quick Start
1. **Environment Setup**: Configure API keys in `.env` file
2. **Document Upload**: Place documents in supported formats
3. **Run Audit**: Execute `python main.py` for automated processing
4. **Review Results**: Check generated compliance documents and matrices

### Output Files
- **Compliance Documents**: `{standard}_compliance_document.docx`
- **Traceability Matrix**: `traceability_matrix_{timestamp}.xlsx`
- **Audit Reports**: Comprehensive findings with recommendations

### Audit Review Points
- Document control procedures and version management
- Process mapping completeness and accuracy
- Risk analysis coverage and control measures
- Software safety classification and lifecycle compliance
- Management review effectiveness and CAPA integration

## Technical Architecture

### Core Components
- **OptimizedAuditorSystem**: Multi-agent auditing with specialized auditors per standard
- **ComplianceWorkflow**: LangGraph-based workflow orchestration
- **DocumentProcessor**: Multi-format document handling
- **TraceabilityManager**: Matrix generation and status tracking

### Data Models
- **TraceabilityItem**: Individual compliance items with full lifecycle tracking
- **ComplianceDocument**: Document containers with audit results
- **WorkflowState**: Comprehensive state management for audit processes

## Best Practices for Auditors

### Document Review
- Verify document control procedures are current and effective
- Check traceability between requirements and implementation
- Validate risk management integration across all processes
- Ensure software lifecycle compliance for medical device software

### Evidence Collection
- Maintain comprehensive audit trails
- Document all findings with specific standard references
- Track remediation activities and verification
- Monitor ongoing compliance through regular reviews

### Reporting Standards
- Use standardized templates for consistency
- Include specific clause references in findings
- Provide clear remediation recommendations
- Track completion status and effectiveness verification

## Configuration

### Environment Variables
```
OPENAI_API_KEY=your_api_key_here
MAX_TOKENS_PER_REQUEST=4000
DEFAULT_TEMPERATURE=0.1
```

### Supported Standards
- ISO 13485:2016 (Quality Management Systems)
- ISO 14971:2019 (Risk Management)
- IEC 62304:2006+A1:2015 (Software Lifecycle)

## Dependencies

See `requirements.txt` for complete dependency list including:
- `autogen` - Multi-agent auditing system
- `langgraph` - Workflow orchestration
- `python-docx` - Document processing
- `PyPDF2` - PDF content extraction
- `pandas` - Data analysis and matrix generation

## Support

For auditor-specific questions or compliance guidance, refer to the comprehensive templates and examples included in the system. The automated workflows provide standardized approaches aligned with regulatory expectations and industry best practices.
