// ChecklistForm - specific form for checklist validation
// Includes multiline textfield for checklist notes

const ChecklistForm = () => {
    const [formData, setFormData] = useState({
        checklist_notes: ''
    });
    const [submitting, setSubmitting] = useState(false);

    const handleChange = (field, value) => {
        setFormData(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleSubmit = () => {
        if (submitting) return;
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
                    Checklist Validation
                </Typography>

                {/* Checklist Notes Field */}
                <TextField
                    label="Checklist Information"
                    placeholder="Enter checklist details here..."
                    value={formData.checklist_notes}
                    onChange={(e) => handleChange('checklist_notes', e.target.value)}
                    multiline
                    minRows={6}
                    maxRows={12}
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
                        disabled={submitting}
                        startIcon={submitting ? <CircularProgress size={20} color="inherit" /> : <Send />}
                        color="primary"
                        sx={{ py: 1.5, px: 4 }}
                    >
                        {submitting ? 'Submitting...' : 'Submit Checklist'}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};
