// RemarksApprovalForm - Reusable component for DPR approval steps
// Each approval step includes remarks textfield and approval toggle

const RemarksApprovalForm = () => {
    const [formData, setFormData] = useState({
        approved: false,
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
                    Review & Approval
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

                {/* Approval Toggle */}
                <Box
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        p: 2,
                        borderRadius: 2,
                        bgcolor: formData.approved ? 'action.selected' : 'action.hover',
                        border: '1px solid',
                        borderColor: formData.approved ? 'success.main' : 'divider',
                        transition: 'all 0.2s ease-in-out',
                        mb: 3
                    }}
                >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {formData.approved ? (
                            <CheckCircle color="success" />
                        ) : (
                            <Cancel color="disabled" />
                        )}
                        <Box>
                            <Typography variant="subtitle1" fontWeight="medium">
                                {formData.approved ? 'Approved' : 'Pending Approval'}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                                {formData.approved
                                    ? 'This item has been approved to proceed'
                                    : 'Toggle to approve this submission'}
                            </Typography>
                        </Box>
                    </Box>
                    <Switch
                        checked={formData.approved}
                        onChange={(e) => handleChange('approved', e.target.checked)}
                        color="success"
                        size="medium"
                    />
                </Box>

                {/* Submit Button */}
                <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                    <Button
                        variant="contained"
                        size="large"
                        onClick={handleSubmit}
                        disabled={submitting}
                        startIcon={submitting ? <CircularProgress size={20} color="inherit" /> : <Send />}
                        color={formData.approved ? 'success' : 'primary'}
                        sx={{ py: 1.5, px: 4 }}
                    >
                        {submitting ? 'Submitting...' : 'Submit Decision'}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};
