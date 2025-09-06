# Medical_Device_Compliance_Agent
A comprehensive Python-based system for managing medical device compliance across ISO 13485, ISO 14971, and IEC 62304 standards. This system integrates LangGraph workflows, Autogen auditors, and automated document generation to streamline compliance processes.

## Features

- **Multi-Standard Support**: ISO 13485 (QMS), ISO 14971 (Risk Management), IEC 62304 (Medical Device Software)
- **Automated Document Generation**: Creates compliant Word documents with built-in guardrails
- **Traceability Matrix Management**: Tracks requirements across all standards
- **AI-Powered Auditing**: Specialized auditor agents for each standard
- **Document Processing**: Supports DOCX and PDF input files
- **Excel Export**: Generates traceability matrices in Excel format
- **Compliance Reporting**: Automated status reports and analytics

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key (for Autogen agents)

### Dependencies

```bash
pip install asyncio pandas python-docx PyPDF2 python-dotenv autogen-agentchat langgraph openpyxl
```

### Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Quick Start

### Basic Usage

```python
import asyncio
from main import run_compliance_workflow

# Run with default templates
asyncio.run(run_compliance_workflow())

# Run with existing document
asyncio.run(run_compliance_workflow("path/to/document.docx"))
```

### Command Line

```bash
python main.py
```

## Core Components

### Standards Support

- **ISO 13485**: Quality Management Systems for Medical Devices
- **ISO 14971**: Application of Risk Management to Medical Devices  
- **IEC 62304**: Medical Device Software - Software Life Cycle Processes

### Document Processing

The system can process existing documents in multiple formats:

- **DOCX files**: Microsoft Word documents
- **PDF files**: Portable Document Format files
- **Template generation**: Creates compliant templates when no input provided

### Traceability Matrix

Tracks compliance items with:
- Unique identifiers
- Requirements mapping
- Implementation details
- Verification methods
- Validation status
- Risk levels
- Completion tracking

### AI Auditors

Specialized Autogen agents for each standard:
- **ISO13485_Auditor**: QMS compliance review
- **ISO14971_Auditor**: Risk management assessment
- **IEC62304_Auditor**: Software lifecycle validation
- **Compliance_Coordinator**: Cross-standard integration

## Workflow Process

1. **Initialize**: Load traceability matrix and setup workflow
2. **Generate Document**: Create or process compliance documentation
3. **Audit**: AI agents review for standard compliance
4. **Finalize**: Generate Word document and Excel reports

## Output Files

The system generates:
- **Compliance Documents**: Word format with embedded traceability
- **Traceability Matrix**: Excel spreadsheet with full tracking
- **Compliance Reports**: Status analytics and completion metrics

## Document Guardrails

Built-in validation ensures:
- Required sections for each standard
- Minimum content length requirements
- Placeholder content detection
- Template compliance verification

### Required Sections by Standard

**ISO 13485**:
- Purpose and Scope
- QMS Process Description
- Roles and Responsibilities
- Process Controls
- Monitoring and Measurement
- Improvement Actions

**ISO 14971**:
- Risk Management Scope
- Risk Analysis Process
- Risk Evaluation Criteria
- Risk Control Measures
- Risk Management File
- Post-Market Surveillance

**IEC 62304**:
- Software Description
- Safety Classification
- Development Process
- Requirements Specification
- Architecture Design
- Testing and Verification

## API Reference

### Core Classes

```python
class StandardType(Enum):
    ISO_13485 = "ISO 13485"
    ISO_14971 = "ISO 14971" 
    IEC_62304 = "IEC 62304"

@dataclass
class TraceabilityItem:
    id: str
    standard: StandardType
    requirement: str
    implementation: str
    verification: str
    validation: str
    status: str = "Open"
    risk_level: str = "Medium"

@dataclass
class ComplianceDocument:
    title: str
    standard: StandardType
    content: str
    traceability_items: List[TraceabilityItem]
```

### Key Functions

```python
# Document processing
load_document_for_review(file_path: str) -> str
generate_docx_document(doc: ComplianceDocument, output_path: str)

# Traceability management
export_traceability_matrix_to_excel(items: List[TraceabilityItem], output_path: str)
generate_compliance_report(items: List[TraceabilityItem]) -> Dict[str, Any]

# Workflow execution
run_compliance_workflow(input_file_path: str = None)
```

## Configuration

### Auditor Configuration

Modify LLM settings in `create_specialist_auditors()`:

```python
llm_config = {
    "config_list": [{"model": "gpt-4", "api_key": os.getenv("OPENAI_API_KEY")}],
    "temperature": 0.1,
}
```

### Document Templates

Customize templates in `DocumentGuardrails` class for organization-specific requirements.

## Security Considerations

- Path traversal protection for file operations
- Input validation for document processing
- Secure file handling with error management
- API key protection through environment variables

## Example Output

### Compliance Report
```
📊 COMPLIANCE REPORT:
   Total Items: 9
   Completion: 33.3%
   Completed: 3
   Remaining: 6

📋 BY STANDARD:
   ISO 13485: 3 items
   ISO 14971: 3 items
   IEC 62304: 3 items

🎯 BY STATUS:
   Completed: 3 items
   In Progress: 3 items
   Open: 3 items
```

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure OPENAI_API_KEY is set in .env file
2. **File Access Errors**: Check file permissions and paths
3. **Import Errors**: Verify all dependencies are installed
4. **Document Processing**: Ensure input files are not corrupted

### Error Handling

The system includes comprehensive error handling for:
- File I/O operations
- Document parsing
- API communication
- Workflow execution

## Contributing

1. Follow existing code structure and patterns
2. Add appropriate error handling
3. Update documentation for new features
4. Test with all supported standards

## License

This project is designed for medical device compliance management. Ensure proper validation and review before use in regulated environments.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages and logs
3. Verify environment configuration
4. Ensure all dependencies are properly installed
