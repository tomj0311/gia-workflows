// RemarksForm - Reusable component for DPR review steps
// Includes only remarks textfield, no approval toggle

const RemarksForm = () => {
    const [formData, setFormData] = useState({
        remarks: ''
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
                    Review
                </Typography>

                {/* Remarks Field */}
                <TextField
                    label="Remarks / Comments"
                    placeholder="Enter your remarks, observations, or feedback..."
                    value={formData.remarks}
                    onChange={(e) => handleChange('remarks', e.target.value)}
                    multiline
                    minRows={4}
                    maxRows={8}
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
                        {submitting ? 'Submitting...' : 'Submit Review'}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};
