// WebsiteInputForm - Input form for website URL

const WebsiteInputForm = () => {
    const [formData, setFormData] = useState({
        website_url: ''
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
                <Typography variant="h6" gutterBottom color="primary">
                    Website Scraper Input
                </Typography>
                
                <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        fullWidth
                        label="Website URL"
                        placeholder="https://example.com"
                        value={formData.website_url}
                        onChange={(e) => handleChange('website_url', e.target.value)}
                        variant="outlined"
                        helperText="Enter the full URL including https://"
                    />
                    
                    <Button
                        variant="contained"
                        onClick={handleSubmit}
                        disabled={submitting || !formData.website_url}
                        fullWidth
                        size="large"
                    >
                        {submitting ? 'Starting Scraping...' : 'Start Scraping'}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};
