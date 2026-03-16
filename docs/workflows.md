# Docling Factory Workflows

This document provides detailed workflow diagrams for the Docling Factory application.

## Table of Contents

- [Application Startup Flow](#application-startup-flow)
- [Individual File Processing Flow](#individual-file-processing-flow)
- [Batch Processing Flow](#batch-processing-flow)
- [Document Parsing Flow](#document-parsing-flow)
- [Output Management Flow](#output-management-flow)
- [Error Handling Flow](#error-handling-flow)

## Application Startup Flow

```mermaid
flowchart TD
    START([Start Application]) --> CHECK_DIRS{Check Directories}
    CHECK_DIRS -->|Missing| CREATE_DIRS[Create input/ and output/ directories]
    CHECK_DIRS -->|Exist| INIT_GRADIO[Initialize Gradio Interface]
    CREATE_DIRS --> INIT_GRADIO
    
    INIT_GRADIO --> LOAD_UI[Load UI Components]
    LOAD_UI --> SETUP_TABS[Setup Tabs:<br/>- Individual Upload<br/>- Batch Processing<br/>- Output Management]
    
    SETUP_TABS --> START_SERVER[Start Web Server<br/>Port: 7860]
    START_SERVER --> READY([Application Ready])
    
    style START fill:#e1f5ff
    style READY fill:#c8e6c9
    style CREATE_DIRS fill:#fff9c4
```

## Individual File Processing Flow

```mermaid
flowchart TD
    START([User Uploads File]) --> SELECT_FORMATS[User Selects Output Formats:<br/>☑ Markdown<br/>☑ HTML<br/>☑ JSON]
    
    SELECT_FORMATS --> CHECK_GPU{GPU Enabled?}
    
    CHECK_GPU -->|Yes| INIT_GPU[Initialize Parser<br/>with GPU]
    CHECK_GPU -->|No| INIT_CPU[Initialize Parser<br/>with CPU]
    
    INIT_GPU --> VALIDATE
    INIT_CPU --> VALIDATE
    
    VALIDATE{Validate File} -->|Invalid| ERROR1[Display Error:<br/>Unsupported Format]
    VALIDATE -->|Valid| PROGRESS_START[Display: Starting...]
    
    PROGRESS_START --> PARSE[Parse Document<br/>using Docling + Docling-Parse]
    
    PARSE --> PROGRESS_EXTRACT[Display: Extracting content...]
    PROGRESS_EXTRACT --> EXTRACT[Extract Content:<br/>- Text<br/>- Tables<br/>- Images<br/>- Metadata]
    
    EXTRACT --> PROGRESS_FORMAT[Display: Generating formats...]
    PROGRESS_FORMAT --> GENERATE{Generate Selected Formats}
    
    GENERATE -->|Markdown| MARKDOWN[Create Markdown File<br/>filename_timestamp.md]
    GENERATE -->|HTML| HTML[Create HTML File<br/>filename_timestamp.html]
    GENERATE -->|JSON| JSON[Create JSON File<br/>filename_timestamp.json]
    
    MARKDOWN --> SAVE[Save to output/ directory]
    HTML --> SAVE
    JSON --> SAVE
    
    SAVE --> PROGRESS_COMPLETE[Display: Complete!]
    PROGRESS_COMPLETE --> DISPLAY[Display Results in Tabs:<br/>- Markdown Tab<br/>- HTML Tab<br/>- JSON Tab]
    
    ERROR1 --> END([End])
    DISPLAY --> END
    
    style START fill:#e1f5ff
    style SELECT_FORMATS fill:#fff9c4
    style PARSE fill:#f3e5f5
    style PROGRESS_START fill:#e1bee7
    style PROGRESS_EXTRACT fill:#e1bee7
    style PROGRESS_FORMAT fill:#e1bee7
    style PROGRESS_COMPLETE fill:#e1bee7
    style DISPLAY fill:#c8e6c9
    style ERROR1 fill:#ffcdd2
```

## Batch Processing Flow

```mermaid
flowchart TD
    START([User Clicks Process Batch]) --> SELECT_FORMATS[User Selects Output Formats:<br/>☑ Markdown<br/>☑ HTML<br/>☑ JSON]
    
    SELECT_FORMATS --> CHECK_GPU{GPU Enabled?}
    
    CHECK_GPU -->|Yes| INIT_GPU[Initialize Parser<br/>with GPU]
    CHECK_GPU -->|No| INIT_CPU[Initialize Parser<br/>with CPU]
    
    INIT_GPU --> CHECK_INPUT
    INIT_CPU --> CHECK_INPUT
    
    CHECK_INPUT{Check input/<br/>directory} -->|Empty| ERROR1[Display Warning:<br/>No files found]
    CHECK_INPUT -->|Has Files| SCAN[Scan for Documents]
    
    SCAN --> FILTER[Filter by Extensions:<br/>.pdf, .docx, .pptx, etc.]
    
    FILTER --> INIT_PROGRESS[Initialize Progress:<br/>Total files counted]
    INIT_PROGRESS --> LOOP_START{More Files?}
    
    LOOP_START -->|Yes| PROCESS_FILE[Process Next File]
    PROCESS_FILE --> PROGRESS_UPDATE[Display: Processing file X/Y...]
    
    PROGRESS_UPDATE --> PARSE[Parse Document<br/>with Docling + Docling-Parse]
    
    PARSE -->|Success| GENERATE_FORMATS[Generate Selected Formats:<br/>MD, HTML, JSON]
    PARSE -->|Error| RECORD_ERROR[Record Error]
    
    GENERATE_FORMATS --> RECORD_SUCCESS[Record Success]
    
    RECORD_SUCCESS --> UPDATE_PROGRESS[Update Progress Bar:<br/>X/Y files complete]
    RECORD_ERROR --> UPDATE_PROGRESS
    
    UPDATE_PROGRESS --> LOOP_START
    
    LOOP_START -->|No| GENERATE_SUMMARY[Generate Summary:<br/>- Total Files<br/>- Successful<br/>- Failed<br/>- File List with Formats]
    
    GENERATE_SUMMARY --> DISPLAY[Display Summary]
    
    ERROR1 --> END([End])
    DISPLAY --> END
    
    style START fill:#e1f5ff
    style SELECT_FORMATS fill:#fff9c4
    style PARSE fill:#f3e5f5
    style PROGRESS_UPDATE fill:#e1bee7
    style UPDATE_PROGRESS fill:#e1bee7
    style DISPLAY fill:#c8e6c9
    style ERROR1 fill:#ffcdd2
```

## Document Parsing Flow

```mermaid
flowchart TD
    START([Parse Document]) --> CALLBACK1[Progress Callback:<br/>Starting...]
    
    CALLBACK1 --> LOAD[Load Document File]
    
    LOAD --> DETECT{Detect Format}
    
    DETECT -->|PDF| PDF_PIPELINE[PDF Pipeline:<br/>- Docling-Parse<br/>- OCR<br/>- Table Detection<br/>- Layout Analysis]
    DETECT -->|DOCX| DOCX_PIPELINE[DOCX Pipeline:<br/>- Extract Text<br/>- Extract Tables<br/>- Extract Images]
    DETECT -->|Other| GENERIC_PIPELINE[Generic Pipeline:<br/>- Text Extraction]
    
    PDF_PIPELINE --> CONVERT
    DOCX_PIPELINE --> CONVERT
    GENERIC_PIPELINE --> CONVERT
    
    CONVERT[Convert to<br/>Docling Document] --> CALLBACK2[Progress Callback:<br/>Extracting content...]
    
    CALLBACK2 --> EXTRACT_TEXT[Extract Text Content]
    
    EXTRACT_TEXT --> EXTRACT_TABLES[Extract Tables]
    EXTRACT_TABLES --> EXTRACT_META[Extract Metadata:<br/>- Page Count<br/>- Author<br/>- Creation Date]
    
    EXTRACT_META --> CALLBACK3[Progress Callback:<br/>Generating formats...]
    
    CALLBACK3 --> CHECK_FORMATS{Check Selected Formats}
    
    CHECK_FORMATS -->|Markdown| FORMAT_MD[Format as Markdown]
    CHECK_FORMATS -->|HTML| FORMAT_HTML[Format as HTML<br/>via export_to_html]
    CHECK_FORMATS -->|JSON| FORMAT_JSON[Format as JSON]
    
    FORMAT_MD --> TIMESTAMP[Add Timestamp]
    FORMAT_HTML --> TIMESTAMP
    FORMAT_JSON --> TIMESTAMP
    
    TIMESTAMP --> SAVE[Save to output/]
    
    SAVE --> CALLBACK4[Progress Callback:<br/>Complete!]
    
    CALLBACK4 --> RETURN[Return Result Object:<br/>with format paths]
    RETURN --> END([End])
    
    style START fill:#e1f5ff
    style CONVERT fill:#f3e5f5
    style CALLBACK1 fill:#e1bee7
    style CALLBACK2 fill:#e1bee7
    style CALLBACK3 fill:#e1bee7
    style CALLBACK4 fill:#e1bee7
    style SAVE fill:#c8e6c9
```

## Output Management Flow

```mermaid
flowchart TD
    START([Output Management]) --> ACTION{User Action}
    
    ACTION -->|Refresh| LIST[List Output Files]
    ACTION -->|Clear| CLEAR_FLOW
    
    LIST --> SCAN[Scan output/ directory]
    SCAN --> SORT[Sort by Modified Time<br/>Newest First]
    SORT --> DISPLAY_LIST[Display File List:<br/>- Name<br/>- Size<br/>- Date]
    DISPLAY_LIST --> END1([End])
    
    CLEAR_FLOW{Clear All or<br/>By Age?}
    CLEAR_FLOW -->|All| CONFIRM1{Confirm?}
    CLEAR_FLOW -->|By Age| GET_DAYS[Get Days Threshold]
    
    CONFIRM1 -->|No| CANCEL1[Cancel Operation]
    CONFIRM1 -->|Yes| DELETE_ALL[Delete All Files]
    
    GET_DAYS --> FILTER[Filter Files<br/>Older Than Threshold]
    FILTER --> CONFIRM2{Confirm?}
    
    CONFIRM2 -->|No| CANCEL2[Cancel Operation]
    CONFIRM2 -->|Yes| DELETE_OLD[Delete Old Files]
    
    DELETE_ALL --> SUCCESS1[Display Success Message]
    DELETE_OLD --> SUCCESS2[Display Success Message]
    
    CANCEL1 --> END2([End])
    CANCEL2 --> END2
    SUCCESS1 --> END2
    SUCCESS2 --> END2
    
    style START fill:#e1f5ff
    style DELETE_ALL fill:#ffcdd2
    style DELETE_OLD fill:#ffcdd2
    style SUCCESS1 fill:#c8e6c9
    style SUCCESS2 fill:#c8e6c9
```

## Error Handling Flow

```mermaid
flowchart TD
    START([Error Occurs]) --> CLASSIFY{Error Type}
    
    CLASSIFY -->|File Not Found| FILE_ERROR[Log Error:<br/>File Not Found]
    CLASSIFY -->|Parse Error| PARSE_ERROR[Log Error:<br/>Parsing Failed]
    CLASSIFY -->|GPU Error| GPU_ERROR[Log Error:<br/>GPU Issue]
    CLASSIFY -->|IO Error| IO_ERROR[Log Error:<br/>IO Operation Failed]
    CLASSIFY -->|Other| GENERIC_ERROR[Log Error:<br/>Unknown Error]
    
    FILE_ERROR --> CHECK_CRITICAL{Critical?}
    PARSE_ERROR --> CHECK_CRITICAL
    GPU_ERROR --> FALLBACK{Can Fallback<br/>to CPU?}
    IO_ERROR --> CHECK_CRITICAL
    GENERIC_ERROR --> CHECK_CRITICAL
    
    FALLBACK -->|Yes| RETRY_CPU[Retry with CPU]
    FALLBACK -->|No| CHECK_CRITICAL
    
    RETRY_CPU -->|Success| SUCCESS[Continue Processing]
    RETRY_CPU -->|Failed| CHECK_CRITICAL
    
    CHECK_CRITICAL -->|Yes| STOP[Stop Processing]
    CHECK_CRITICAL -->|No| CONTINUE[Continue with<br/>Next File]
    
    STOP --> NOTIFY_USER[Display Error<br/>to User]
    CONTINUE --> RECORD[Record Error<br/>in Results]
    SUCCESS --> RECORD_SUCCESS[Record Success]
    
    NOTIFY_USER --> END([End])
    RECORD --> END
    RECORD_SUCCESS --> END
    
    style START fill:#ffcdd2
    style STOP fill:#ffcdd2
    style SUCCESS fill:#c8e6c9
    style RECORD_SUCCESS fill:#c8e6c9
```

## Data Flow Diagram

```mermaid
flowchart LR
    subgraph Input
        USER[User]
        FILES[Document Files]
        FORMATS[Format Selection:<br/>MD/HTML/JSON]
    end
    
    subgraph Processing
        UI[Gradio UI<br/>with Progress Display]
        PARSER[DoclingParser<br/>with Callbacks]
        DOCLING[Docling Library]
        PARSE[Docling-Parse]
    end
    
    subgraph Output
        MD[Markdown Files]
        HTML[HTML Files]
        JSON[JSON Files]
        LOGS[Log Files]
    end
    
    USER -->|Upload/Configure| UI
    USER -->|Select Formats| FORMATS
    FORMATS -->|Format List| PARSER
    FILES -->|Read| PARSER
    UI -->|Commands| PARSER
    PARSER -->|Progress Updates| UI
    PARSER -->|Convert| DOCLING
    DOCLING -->|Enhanced Parsing| PARSE
    PARSE -->|Parsed Data| DOCLING
    DOCLING -->|Document Object| PARSER
    PARSER -->|Write| MD
    PARSER -->|Write| HTML
    PARSER -->|Write| JSON
    PARSER -->|Write| LOGS
    MD -->|Display in Tab| UI
    HTML -->|Display in Tab| UI
    JSON -->|Display in Tab| UI
    UI -->|Results| USER
    
    style USER fill:#e1f5ff
    style FORMATS fill:#fff9c4
    style UI fill:#fff3e0
    style PARSER fill:#fff3e0
    style DOCLING fill:#f3e5f5
    style PARSE fill:#f3e5f5
    style MD fill:#c8e6c9
    style HTML fill:#c8e6c9
    style JSON fill:#c8e6c9
```

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle: Application Started
    
    Idle --> Initializing: User Action
    Initializing --> Ready: Parser Initialized
    
    Ready --> Processing: Start Parse
    Processing --> Extracting: Document Loaded
    Extracting --> Formatting: Content Extracted
    Formatting --> Saving: Formats Generated
    Saving --> Complete: Files Saved
    
    Complete --> Ready: Continue
    Complete --> [*]: Exit
    
    Processing --> Error: Parse Failed
    Extracting --> Error: Extraction Failed
    Formatting --> Error: Format Failed
    Saving --> Error: Save Failed
    
    Error --> Ready: Retry
    Error --> [*]: Exit
    
    note right of Processing
        Can use CPU or GPU
    end note
    
    note right of Complete
        Outputs saved with timestamp
    end note
```

## Sequence Diagram: Individual File Upload

```mermaid
sequenceDiagram
    actor User
    participant UI as Gradio UI
    participant App as app.py
    participant Parser as DoclingParser
    participant Docling as Docling Library
    participant Parse as Docling-Parse
    participant FS as File System
    
    User->>UI: Select Formats (MD/HTML/JSON)
    User->>UI: Upload File
    UI->>App: file_upload_event(file, formats)
    App->>Parser: parse_document(file_path, formats, callback)
    
    Parser->>UI: callback("Starting...", 0, 3)
    UI-->>User: Display progress
    
    Parser->>FS: Check file exists
    FS-->>Parser: File found
    
    Parser->>Docling: convert(file_path)
    Docling->>Parse: Enhanced parsing
    Parse-->>Docling: Parsed structure
    Docling->>Docling: OCR & Analysis
    Docling-->>Parser: Document object
    
    Parser->>UI: callback("Extracting content...", 1, 3)
    UI-->>User: Update progress
    
    Parser->>Parser: Extract markdown (if selected)
    Parser->>Parser: Extract HTML (if selected)
    Parser->>Parser: Extract JSON (if selected)
    
    Parser->>UI: callback("Generating formats...", 2, 3)
    UI-->>User: Update progress
    
    Parser->>FS: Save markdown file (if selected)
    Parser->>FS: Save HTML file (if selected)
    Parser->>FS: Save JSON file (if selected)
    
    FS-->>Parser: Files saved
    
    Parser->>UI: callback("Complete!", 3, 3)
    Parser-->>App: Result object with format paths
    
    App->>UI: Display markdown tab (if selected)
    App->>UI: Display HTML tab (if selected)
    App->>UI: Display JSON tab (if selected)
    
    UI-->>User: Show results in tabs
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        BROWSER[Web Browser]
    end
    
    subgraph "Application Server"
        GRADIO[Gradio Server<br/>Port: 7860]
        APP[Application Logic<br/>app.py]
        PARSER[Parser Module<br/>docling_parser.py]
    end
    
    subgraph "Processing Layer"
        CPU[CPU Processing]
        GPU[GPU Processing<br/>Optional]
    end
    
    subgraph "Storage Layer"
        INPUT[input/<br/>Directory]
        OUTPUT[output/<br/>Directory]
        LOGS[logs/<br/>Directory]
    end
    
    BROWSER <-->|HTTP| GRADIO
    GRADIO <--> APP
    APP <--> PARSER
    PARSER <--> CPU
    PARSER <-.->|Optional| GPU
    PARSER <--> INPUT
    PARSER <--> OUTPUT
    PARSER <--> LOGS
    
    style BROWSER fill:#e1f5ff
    style GRADIO fill:#fff3e0
    style APP fill:#fff3e0
    style PARSER fill:#fff3e0
    style GPU fill:#f3e5f5,stroke-dasharray: 5 5
```

## Notes

- All workflows include comprehensive error handling
- GPU processing is optional and falls back to CPU if unavailable
- Timestamps ensure no output file overwrites
- **Real-time progress tracking** is available for both individual and batch operations
- **Multiple output formats** (Markdown, HTML, JSON) can be selected via checkboxes
- **Docling-Parse integration** provides enhanced document structure recognition
- Progress callbacks provide user feedback at each processing stage
- All operations are logged for debugging and audit purposes
- Output format selection is persistent across sessions
- Tabbed interface allows easy comparison between different output formats