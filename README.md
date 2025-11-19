# GIA BPMN Workflow Standard v2.0 (Condensed)

**Target**: AI Agents, Developers | **Platform**: GIA Workflow Engine | **Tech**: BPMN 2.0, Python 3.x, React + MUI

## Quick Reference

- **File Naming**: `id="task_name"` → `scripts/task_name.py` (EXACT MATCH, case-sensitive)
- **Variables**: Direct access `result = email` (NO prefixes: `workflow.email` ❌)
- **Conditions**: Python `and/or/not` (NOT `&&/||/!` ❌)
- **User Tasks**: `<formData>` REQUIRED, custom React component OPTIONAL
- **Service Task**: Returns `response` by default; use `<resultVariable name="custom_name" />` for named outputs
- **Call Activity**: Use `calledElement` + `dataInput`/`dataOutput` for variable mapping
- **Messages**: Define `<message>` elements, link with `messageRef` in send/receive tasks
- **IDs**: `[a-zA-Z0-9_]` only (underscores for multi-word: `enter_data`)
- **Logging**: `_debug*`, `_info*`, `_warning*`, `_error*` prefixes
- **React**: No imports, no exports, use `submitWorkflowForm(data)`

## Core Principles

1. **Pure BPMN 2.0**: No vendor extensions (Camunda, Activiti)
2. **Exact File Matching**: File names = task IDs exactly
3. **Global Variables**: Access workflow vars directly without prefixes
4. **XML Compliance**: Alphanumeric + underscores only in IDs

## Task Types

### 1. Script Task (Python)

**BPMN**:
```xml
<scriptTask id="validate" name="Validate Data" scriptFormat="python">
  <script>scripts/validate.py</script>
</scriptTask>
```

**Python Template** (`scripts/validate.py`):
```python
"""Description | Inputs: email, amount | Outputs: email_valid, amount_valid"""
import re

def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email)) if email else False

# Direct variable access (no prefixes)
email_valid = is_valid_email(email)
amount_valid = float(amount) > 0 if amount else False

# Logging (optional ONLY if necessary)
_debug_input = f"email={email}, amount={amount}"
_info_result = f"Valid: email={email_valid}, amount={amount_valid}"
_warning_email = "Invalid email" if not email_valid else None
_error_critical = "Both invalid" if not (email_valid or amount_valid) else None
```

**Logging Prefixes**:
- `_debug_*`: Diagnostic info (inputs, config, performance)
- `_info_*`: Status messages (progress, summaries)
- `_warning_*`: Non-critical issues (low confidence, rate limits)
- `_error_*`: Critical errors (API failures, validation errors)

---

### 2. User Task (Forms)

**BPMN** (Auto-generated - RECOMMENDED):
```xml
<userTask id="enter_data" name="Enter Data">
  <extensionElements>
    <formData xmlns="http://example.org/form">
      <formField id="email" label="Email" type="String" required="true"/>
      <formField id="amount" label="Amount" type="Number" required="true"/>
      <formField id="agree" label="Agree?" type="Boolean" required="false"/>
      <formField id="deadline" label="Deadline" type="DateTime" required="false"/>
      <formField id="files" label="Documents" type="Files" required="false"/>
      <formField id="audio_data" label="Record Audio" type="Audio" required="false"/>
      <formField id="media_data" label="Record Media" type="Media" required="false"/>
    </formData>
    <!-- Platform auto-generates form UI from formData - NO component needed! -->
  </extensionElements>
</userTask>
```

**Field Types**: `String`, `Number`, `Boolean`, `DateTime`, `Files`, `Audio`, `Media`

**Custom Component** (OPTIONAL - only if custom UX needed, `components/enter_data.jsx`):
```javascript
const EnterData = ({ initialData = {} }) => {
  const [data, setData] = useState({
    email: initialData.email || '',
    amount: initialData.amount || 0
  });
  
  const [errors, setErrors] = useState({});
  
  const handleSubmit = () => {
    const newErrors = {};
    
    // Validate fields before submission (MANDATORY)
    if (!data.email) {
      newErrors.email = 'Email is required';
    } else if (!data.email.includes('@')) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    if (!data.amount || data.amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
    }
    
    // Return early if validation fails
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    // Submit only after validation passes
    submitWorkflowForm(data);
  };
  
  return (
    <Box sx={{ maxWidth: 500, p: 3 }}>
      <TextField fullWidth label="Email" value={data.email}
        onChange={(e) => {
          setData({...data, email: e.target.value});
          setErrors({...errors, email: ''});
        }}
        error={!!errors.email}
        helperText={errors.email}
        required />
      <TextField fullWidth label="Amount" type="number" value={data.amount}
        onChange={(e) => {
          setData({...data, amount: e.target.value});
          setErrors({...errors, amount: ''});
        }}
        error={!!errors.amount}
        helperText={errors.amount}
        required />
      <Button onClick={handleSubmit} variant="contained" fullWidth sx={{ mt: 2 }}>
        Submit
      </Button>
    </Box>
  );
};
// NO import statements! NO export statements!
// Pre-loaded: useState, Box, TextField, Button, Typography, etc.
// MANDATORY: Validate all fields before calling submitWorkflowForm(data)
```

---

### 3. Service Task (Function Invocation)

**Use for invoking Python functions/modules. For calling other workflows/subprocesses, use Call Activity (see below).**

**Basic Example**:
```xml
<serviceTask id="analyze" name="Analyze Data">
  <extensionElements xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <serviceConfiguration xmlns="http://example.org/service">
      <function>
        <moduleName>Whisper</moduleName>
        <functionName>transcribe_uploaded_audio</functionName>
        <parameters>
          <parameter name="file_path" value=""/>
        </parameters>
      </function>
    </serviceConfiguration>
  </extensionElements>
</serviceTask>
```

**With Custom Result Variable** (RECOMMENDED for reusability):
```xml
<serviceTask id="transcribe_audio" name="Transcribe Audio">
  <extensionElements xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <serviceConfiguration xmlns="http://example.org/service">
      <function>
        <moduleName>Whisper</moduleName>
        <functionName>transcribe_uploaded_audio</functionName>
        <parameters>
          <parameter name="file_path" value=""/>
        </parameters>
      </function>
    </serviceConfiguration>
    <resultVariable name="transcription_result" />
  </extensionElements>
</serviceTask>
```

**Key Points**:
- **moduleName**: The Python module to invoke (e.g., `Whisper`, `DataProcessor`)
- **functionName**: The specific function within the module (e.g., `transcribe_uploaded_audio`)
- **parameters**: Input parameters with names and values (can reference workflow variables)
- **resultVariable**: (OPTIONAL) Custom variable name to store the output instead of default `response`
- The function has access to workflow variables passed through parameters
- This task type is for function invocations, not for general subprocess calls

**Output Handling**:
- **Default**: Service tasks return a `response` object containing the function's output
- **Custom Variable**: Use `<resultVariable name="custom_name" />` to store output in a named variable (e.g., `transcription_result`, `analysis_output`)
- The output can be either plain text or JSON format
- Subsequent tasks access the output via the variable name (default `response` or custom name)
- Example with default: Access as `response` in next task
- Example with custom: If `<resultVariable name="transcription_result" />`, access as `transcription_result` in next task
- For text responses, the variable contains the text string directly
- For JSON responses, the variable contains the JSON object
- **Benefits of custom result variables**:
  - Multiple service tasks can have distinct output variables
  - Clearer variable names improve workflow readability
  - Prevents overwriting when chaining multiple service tasks
  - Other tasks can reference specific outputs by meaningful names

---

### 4. Call Activity (Subprocess/Reusable Workflow)

**Use for calling another workflow or subprocess. Supports input/output variable mapping.**

```xml
<callActivity id="call_validate_payment" name="Validate Payment" 
              calledElement="SubProcess_ValidatePayment">
  <extensionElements>
    <!-- Input: Send variables to subprocess -->
    <dataInput>
      <assignment>
        <from>payment</from>
        <to>payment</to>
      </assignment>
    </dataInput>
    
    <!-- Output: Get results back from subprocess -->
    <dataOutput>
      <assignment>
        <from>validation_result</from>
        <to>payment_status</to>
      </assignment>
      <assignment>
        <from>processing_fee</from>
        <to>fee</to>
      </assignment>
    </dataOutput>
  </extensionElements>
</callActivity>
```

**Key Points**:
- **calledElement**: ID of the subprocess/workflow to call
- **dataInput**: Map parent workflow variables → subprocess variables
- **dataOutput**: Map subprocess results → parent workflow variables
- **from/to**: `<from>` is source variable, `<to>` is destination variable
- Input `<from>` refers to parent scope, `<to>` refers to subprocess scope
- Output `<from>` refers to subprocess scope, `<to>` refers to parent scope

**Complete Example with Subprocess**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             id="call_activity_example">
  
  <!-- Main Process -->
  <process id="main_process" name="Main Process">
    <startEvent id="start"/>
    
    <scriptTask id="prepare_payment" name="Prepare Payment" scriptFormat="python">
      <script>scripts/prepare_payment.py</script>
    </scriptTask>
    
    <!-- Call the validation subprocess -->
    <callActivity id="call_validate_payment" name="Validate Payment"
                  calledElement="SubProcess_ValidatePayment">
      <extensionElements>
        <dataInput>
          <assignment>
            <from>payment</from>
            <to>payment</to>
          </assignment>
        </dataInput>
        <dataOutput>
          <assignment>
            <from>validation_result</from>
            <to>payment_status</to>
          </assignment>
          <assignment>
            <from>processing_fee</from>
            <to>fee</to>
          </assignment>
        </dataOutput>
      </extensionElements>
    </callActivity>
    
    <exclusiveGateway id="check_status" name="Valid?"/>
    
    <endEvent id="end_success"/>
    <endEvent id="end_failure"/>
    
    <sequenceFlow sourceRef="start" targetRef="prepare_payment"/>
    <sequenceFlow sourceRef="prepare_payment" targetRef="call_validate_payment"/>
    <sequenceFlow sourceRef="call_validate_payment" targetRef="check_status"/>
    <sequenceFlow sourceRef="check_status" targetRef="end_success">
      <conditionExpression xsi:type="tFormalExpression">
        payment_status == "valid"
      </conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="check_status" targetRef="end_failure">
      <conditionExpression xsi:type="tFormalExpression">
        payment_status != "valid"
      </conditionExpression>
    </sequenceFlow>
  </process>
  
  <!-- Subprocess Definition -->
  <process id="SubProcess_ValidatePayment" name="Validate Payment Subprocess">
    <startEvent id="sub_start"/>
    
    <scriptTask id="validate_payment" name="Validate Payment" scriptFormat="python">
      <script>scripts/validate_payment.py</script>
    </scriptTask>
    
    <scriptTask id="calculate_fee" name="Calculate Fee" scriptFormat="python">
      <script>scripts/calculate_fee.py</script>
    </scriptTask>
    
    <endEvent id="sub_end"/>
    
    <sequenceFlow sourceRef="sub_start" targetRef="validate_payment"/>
    <sequenceFlow sourceRef="validate_payment" targetRef="calculate_fee"/>
    <sequenceFlow sourceRef="calculate_fee" targetRef="sub_end"/>
  </process>
</definitions>
```

---

### 5. Send Task & Receive Task (Message Flows)

**Send Task** (sends a message to another process or external system):
```xml
<sendTask id="send_purchase_request" name="Send Purchase Request"
          messageRef="Msg_PurchaseRequest">
  <extensionElements>
    <!-- Payload sent to the receiver -->
    <messagePayload xmlns="http://example.org/message">
      {
        "orderId": "{orderId}",
        "items": {items},
        "totalAmount": {amount}
      }
    </messagePayload>
  </extensionElements>
</sendTask>
```

**Receive Task** (waits for a message from another process or external system):
```xml
<receiveTask id="receive_purchase_request" name="Receive Purchase Request"
             messageRef="Msg_PurchaseRequest"/>
```

**Message Definition** (define messages at the top level):
```xml
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             id="message_workflow">
  
  <!-- Message Definitions -->
  <message id="Msg_PurchaseRequest" name="Purchase Request Message"/>
  <message id="Msg_Acknowledgement" name="Acknowledgement Message"/>
  
  <process id="buyer_process" name="Buyer Process">
    <startEvent id="start"/>
    
    <!-- Send purchase request -->
    <sendTask id="send_purchase_request" name="Send Purchase Request"
              messageRef="Msg_PurchaseRequest">
      <extensionElements>
        <messagePayload xmlns="http://example.org/message">
          {
            "orderId": "{orderId}",
            "items": {items},
            "totalAmount": {amount}
          }
        </messagePayload>
      </extensionElements>
    </sendTask>
    
    <!-- Wait for acknowledgement -->
    <receiveTask id="receive_acknowledgement" name="Receive Acknowledgement"
                 messageRef="Msg_PurchaseRequest"/>
    
    <endEvent id="end"/>
    
    <sequenceFlow sourceRef="start" targetRef="send_purchase_request"/>
    <sequenceFlow sourceRef="send_purchase_request" targetRef="receive_acknowledgement"/>
    <sequenceFlow sourceRef="receive_acknowledgement" targetRef="end"/>
  </process>
  
  <process id="supplier_process" name="Supplier Process">
    <startEvent id="start_supplier"/>
    
    <!-- Wait for purchase request -->
    <receiveTask id="receive_purchase_request" name="Receive Purchase Request"
                 messageRef="Msg_PurchaseRequest"/>
    
    <!-- Process the request -->
    <scriptTask id="process_order" name="Process Order" scriptFormat="python">
      <script>scripts/process_order.py</script>
    </scriptTask>
    
    <!-- Send acknowledgement back -->
    <sendTask id="send_acknowledgement" name="Send Acknowledgement"
              messageRef="Msg_Acknowledgement">
      <extensionElements>
        <messagePayload xmlns="http://example.org/message">
          {
            "orderId": "{orderId}",
            "status": "acknowledged",
            "estimatedDelivery": "{delivery_date}"
          }
        </messagePayload>
      </extensionElements>
    </sendTask>
    
    <endEvent id="end_supplier"/>
    
    <sequenceFlow sourceRef="start_supplier" targetRef="receive_purchase_request"/>
    <sequenceFlow sourceRef="receive_purchase_request" targetRef="process_order"/>
    <sequenceFlow sourceRef="process_order" targetRef="send_acknowledgement"/>
    <sequenceFlow sourceRef="send_acknowledgement" targetRef="end_supplier"/>
  </process>
</definitions>
```

**Key Points**:
- **messageRef**: Links send/receive tasks to message definitions
- **messagePayload**: JSON payload with workflow variables (use `{variable}` syntax)
- **Receive Task**: Blocks execution until message is received
- **Send Task**: Sends message and continues immediately
- Messages enable communication between different processes or external systems

---

### 6. Gateway (Decisions)

**Exclusive Gateway** (choose one path):
```xml
<exclusiveGateway id="check_valid" name="Valid?"/>

<sequenceFlow sourceRef="check_valid" targetRef="process_task">
  <conditionExpression xsi:type="tFormalExpression">
    email_valid == True and amount &gt; 100
  </conditionExpression>
</sequenceFlow>

<sequenceFlow sourceRef="check_valid" targetRef="error_task">
  <conditionExpression xsi:type="tFormalExpression">
    not (email_valid == True and amount &gt; 100)
  </conditionExpression>
</sequenceFlow>
```

**Parallel Gateway** (execute all paths):
```xml
<parallelGateway id="split"/>  <!-- Start parallel -->
<parallelGateway id="join"/>   <!-- Wait for all -->
```

**XML Escaping**: `<` → `&lt;`, `>` → `&gt;`, `&` → `&amp;`

---

## Complete Workflow Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             id="example_workflow">
  <process id="validation_process" name="Data Validation">
    <startEvent id="start"/>
    
    <userTask id="enter_data" name="Enter Data">
      <formData xmlns="http://example.org/form">
        <formField id="email" label="Email" type="String" required="true"/>
        <formField id="amount" label="Amount" type="Number" required="true"/>
      </formData>
    </userTask>
    
    <scriptTask id="validate" name="Validate" scriptFormat="python">
      <script>scripts/validate.py</script>
    </scriptTask>
    
    <exclusiveGateway id="check_valid" name="Valid?"/>
    
    <serviceTask id="process" name="Process Data">
      <extensionElements xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">
        <serviceConfiguration xmlns="http://example.org/service">
          <function>
            <moduleName>DataProcessor</moduleName>
            <functionName>process_validated_data</functionName>
            <parameters>
              <parameter name="email" value=""/>
              <parameter name="amount" value=""/>
            </parameters>
          </function>
        </serviceConfiguration>
        <resultVariable name="processing_result" />
      </extensionElements>
    </serviceTask>
    
    <endEvent id="end_success"/>
    <endEvent id="end_failure"/>
    
    <sequenceFlow sourceRef="start" targetRef="enter_data"/>
    <sequenceFlow sourceRef="enter_data" targetRef="validate"/>
    <sequenceFlow sourceRef="validate" targetRef="check_valid"/>
    <sequenceFlow sourceRef="check_valid" targetRef="process">
      <conditionExpression xsi:type="tFormalExpression">
        email_valid == True and amount_valid == True
      </conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="check_valid" targetRef="end_failure">
      <conditionExpression xsi:type="tFormalExpression">
        not (email_valid == True and amount_valid == True)
      </conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="process" targetRef="end_success"/>
  </process>
</definitions>
```

**Files needed**:
- `workflow.bpmn` (above)
- `scripts/validate.py` (see Script Task section)
- NO React components needed (auto-generated from formData)

**Note**: The service task uses `<resultVariable name="processing_result" />` to store output in `processing_result` instead of default `response`.

---

## Common Errors & Solutions

| Error | Wrong ❌ | Right ✅ |
|-------|---------|---------|
| **File naming** | `validation.py` | `validate.py` (match ID exactly) |
| **Multi-word IDs** | `enter-data`, `enterData` | `enter_data` |
| **Variables** | `workflow.email`, `context['email']` | `email` |
| **Conditions** | `amount > 100 && valid` | `amount > 100 and valid` |
| **React imports** | `import { Box } from '@mui/material'` | (no imports - pre-loaded) |
| **React exports** | `export default MyForm` | (no exports) |
| **Form submit** | `props.onSubmit(data)` | `submitWorkflowForm(data)` (AFTER validation) |
| **Missing validation** | Submit directly on button click | Validate fields → check errors → then call `submitWorkflowForm(data)` |
| **Missing formData** | `<userTask>` with no `<formData>` | Always include `<formData>` |
| **Service Task structure** | Old agent-based format | Use function-based: `<moduleName>`, `<functionName>`, `<parameters>` |
| **Service result variable** | Use `<resultVariable name="task_specific_result" />` for each |
| **Service vs Call** | `<serviceTask>` for subprocess | Use `<callActivity>` for subprocesses |
| **Call Activity mapping** | No `dataInput`/`dataOutput` | Always map variables with assignments |
| **Message flows** | `<receiveTask>` with no `messageRef` | Always define message and link with `messageRef` |
| **XML chars** | `amount < 100` in XML | `amount &lt; 100` |

---

## Layout Rules

**Node Positioning** (prevents overlaps):
- **X**: 100, 250, 400, 550, 700, 850, 1000, 1150, 1300 (150px spacing)
- **Y**: 100, 220, 340, 460 (120px spacing)
- **Max 5-7 nodes per row** (Keep diagrams compact and readable)
- **Visual Appeal**: Ensure arrows are straight where possible and nodes are aligned to the grid. Avoid crossing lines.

```
Row 1 (Y=100): [Start] → [Task1] → [Task2] → [Gateway] → [Task3] → [End]
              X=100     X=250     X=400      X=550      X=700     X=850
```

---

## Workflow Creation Checklist

**BPMN XML**:
- [ ] Unique IDs (alphanumeric + underscores only)
- [ ] At least one `<startEvent>` and `<endEvent>`
- [ ] Proper namespaces: `xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"`
- [ ] All `<sequenceFlow>` have `sourceRef` and `targetRef`
- [ ] XML special chars escaped (`<` → `&lt;`, etc.)
- [ ] No overlapping positions (use grid: X=100,250,400... Y=100,220,340...)

**Script Tasks**:
- [ ] File name = task ID exactly (`id="validate"` → `scripts/validate.py`)
- [ ] Docstring with inputs/outputs
- [ ] Direct variable access (no prefixes)
- [ ] Logging variables (`_debug*`, `_info*`, `_warning*`, `_error*`)
- [ ] Valid Python syntax

**User Tasks**:
- [ ] `<formData>` element with all fields (REQUIRED)
- [ ] Field types: String, Number, Boolean, DateTime, Files, Audio, Audio/Video
- [ ] Required/optional flags set correctly
- [ ] Custom component ONLY if custom UX needed (OPTIONAL)
- [ ] If custom component: No imports, no exports, use `submitWorkflowForm(data)`

**Gateways**:
- [ ] Python operators (`and`, `or`, `not`)
- [ ] XML chars escaped in conditions
- [ ] Mutually exclusive conditions (XOR) or all paths (parallel)

**Validation**:
- [ ] All files in correct locations (`scripts/`, `components/`)
- [ ] Python syntax valid
- [ ] React component syntax valid (if used)
- [ ] No overlapping node positions
- [ ] Variable flow traced through workflow

---

## Common Workflow Patterns

### 1. Form → Validate → Process
```
[Start] → [User Input] → [Validate Script] → [Gateway]
                                               ├→ [Valid] → [Process] → [Success]
                                               └→ [Invalid] → [Error] → [Failure]
```

### 2. Parallel Processing
```
[Start] → [Split Gateway]
           ├→ [Task A]
           ├→ [Task B]
           └→ [Task C]
         → [Join Gateway] → [Combine] → [End]
```

### 3. Loop with Condition
```
[Start] → [Init] → [Process] → [Gateway: More?]
                     ↑           ├→ [Yes] ─┘
                                 └→ [No] → [End]
```

### 4. Error Handling with Retry
```
[Start] → [Try] → [Success?]
           ↑       ├→ [Yes] → [End Success]
           |       └→ [No] → [Retry?]
           └────────────────── [Yes] ─┘
                               [No] → [Handle Error] → [End Failure]
```

### 5. Message Flow Between Processes
```
Process A:
[Start] → [Send Message] → [Wait for Response] → [Process Response] → [End]

Process B:
[Start] → [Receive Message] → [Process Request] → [Send Response] → [End]
```

### 6. Reusable Subprocess with Call Activity
```
Main Process:
[Start] → [Prepare Data] → [Call: Validation Subprocess] → [Process Results] → [End]
                             ↓ (pass variables)        ↑ (return results)
                        
Validation Subprocess:
[Start] → [Validate] → [Calculate] → [Return Results] → [End]
```

---

## AI Agent Instructions Summary

**When creating workflows**:
1. **Analyze**: Identify tasks, decisions, data flow, error handling
2. **Design**: Plan BPMN elements, layout (5-7 nodes/row), conditions. Focus on visual appeal.
3. **Create BPMN**: Unique IDs, proper namespaces, positioned on grid. Ensure no overlaps.
4. **Create Files**: 
   - Python scripts for script tasks (match ID exactly)
   - `<formData>` for ALL user tasks (REQUIRED)
   - Custom React components ONLY if needed (OPTIONAL)
5. **Validate**: Check syntax, file names, positions, variable flow

**Priorities**:
- Clean layout (no overlaps, 5-7 nodes/row)
- Visually appealing diagrams (aligned nodes, straight lines)
- Exact file name matching
- formData always included
- Auto-generated forms preferred over custom components
- Clear error handling
- Documented inputs/outputs

---

**End of Condensed Guide** | Full version: See original README.md for detailed examples and troubleshooting
