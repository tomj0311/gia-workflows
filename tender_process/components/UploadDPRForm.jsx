const UploadDPRForm = ({ initialData = {} }) => {
  const [fileName, setFileName] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        setError('Only PDF files are allowed.');
        setFileName('');
        return;
      }
      setFileName(file.name);
      setError('');
    }
  };

  const handleSubmit = () => {
    if (!fileName) {
      setError('Please select a PDF file to upload.');
      return;
    }
    
    // Simulating file upload returning a path
    const data = {
      dpr_file_name: fileName,
      dpr_file_path: `/uploads/${fileName}` 
    };
    
    submitWorkflowForm(data);
  };

  return (
    <Box sx={{ p: 3, maxWidth: 600 }}>
      <Typography variant="h5" gutterBottom>
        Upload DPR File
      </Typography>
      
      <Box sx={{ my: 3 }}>
        <input
          accept="application/pdf"
          id="dpr-upload-file"
          type="file"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <label htmlFor="dpr-upload-file">
          <Button variant="outlined" component="span" fullWidth>
            {fileName ? fileName : "Select PDF File"}
          </Button>
        </label>
      </Box>

      {error && (
        <Typography color="error" variant="body2" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      <Button 
        variant="contained" 
        color="primary" 
        fullWidth 
        onClick={handleSubmit}
        disabled={!!error || !fileName}
      >
        Submit DPR
      </Button>
    </Box>
  );
};
