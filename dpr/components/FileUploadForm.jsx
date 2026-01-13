// FileUploadForm - Component for initial DPR file upload from District Office
// Includes file upload and remarks

const FileUploadForm = () => {
    const [formData, setFormData] = useState({
        dpr_file: null,
        remarks: ''
    });
    const [fileName, setFileName] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [dragOver, setDragOver] = useState(false);
    const fileInputRef = useRef(null);

    const handleChange = (field, value) => {
        setFormData(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleFileSelect = (event) => {
        const file = event.target.files?.[0];
        if (file) {
            setFileName(file.name);
            handleChange('dpr_file', file);
        }
    };

    const handleDrop = (event) => {
        event.preventDefault();
        setDragOver(false);
        const file = event.dataTransfer.files?.[0];
        if (file) {
            setFileName(file.name);
            handleChange('dpr_file', file);
        }
    };

    const handleDragOver = (event) => {
        event.preventDefault();
        setDragOver(true);
    };

    const handleDragLeave = () => {
        setDragOver(false);
    };

    const handleSubmit = () => {
        if (submitting) return;
        if (!formData.dpr_file) {
            alert('Please upload a DPR document');
            return;
        }
        setSubmitting(true);
        submitWorkflowForm(formData);
    };

    return (
        <Container maxWidth="sm" sx={{ py: 3 }}>
            <Paper
                elevation={0}
                sx={{
                    p: 3,
                    border: '1px solid',
                    borderColor: 'divider',
                    borderRadius: 2
                }}
            >
                <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
                    Upload DPR Document
                </Typography>

                {/* File Upload Area */}
                <Box
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onClick={() => fileInputRef.current?.click()}
                    sx={{
                        border: '2px dashed',
                        borderColor: dragOver ? 'primary.main' : fileName ? 'success.main' : 'divider',
                        borderRadius: 2,
                        p: 4,
                        textAlign: 'center',
                        cursor: 'pointer',
                        bgcolor: dragOver ? 'action.hover' : fileName ? 'action.selected' : 'background.default',
                        transition: 'all 0.2s ease-in-out',
                        mb: 3,
                        '&:hover': {
                            borderColor: 'primary.main',
                            bgcolor: 'action.hover'
                        }
                    }}
                >
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf,.doc,.docx,.xls,.xlsx"
                        onChange={handleFileSelect}
                        style={{ display: 'none' }}
                    />
                    {fileName ? (
                        <Box>
                            <CheckCircle color="success" sx={{ fontSize: 48, mb: 1 }} />
                            <Typography variant="subtitle1" color="success.main" fontWeight="medium">
                                {fileName}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                                Click to change file
                            </Typography>
                        </Box>
                    ) : (
                        <Box>
                            <CloudUpload color="action" sx={{ fontSize: 48, mb: 1 }} />
                            <Typography variant="subtitle1" color="text.secondary">
                                Drag & drop your DPR file here
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                                or click to browse (PDF, DOC, XLS)
                            </Typography>
                        </Box>
                    )}
                </Box>

                {/* Remarks Field */}
                <TextField
                    label="Remarks / Description"
                    placeholder="Brief description of the DPR, project details, or any notes..."
                    value={formData.remarks}
                    onChange={(e) => handleChange('remarks', e.target.value)}
                    multiline
                    minRows={3}
                    maxRows={6}
                    fullWidth
                    variant="outlined"
                    sx={{ mb: 3 }}
                />

                {/* Submit Button */}
                <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                    <Button
                        variant="contained"
                        size="large"
                        onClick={handleSubmit}
                        disabled={submitting || !formData.dpr_file}
                        startIcon={submitting ? <CircularProgress size={20} color="inherit" /> : <Send />}
                        sx={{ py: 1.5, px: 4 }}
                    >
                        {submitting ? 'Uploading...' : 'Submit DPR'}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};
