import { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { AuthContext } from '../App';
import { companyAPI, uploadAPI } from '../services/api';
import {
    Upload as UploadIcon, FileSpreadsheet, CheckCircle, XCircle,
    AlertTriangle, Eye, Building2, Plus, FileText
} from 'lucide-react';

function Upload() {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const [companies, setCompanies] = useState([]);
    const [selectedCompany, setSelectedCompany] = useState('');
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [uploadResult, setUploadResult] = useState(null);
    const [pendingValidations, setPendingValidations] = useState([]);
    const [showNewCompany, setShowNewCompany] = useState(false);
    const [newCompany, setNewCompany] = useState({ name: '', industry: 'Services' });
    const [dragActive, setDragActive] = useState(false);

    useEffect(() => {
        loadCompanies();
    }, []);

    useEffect(() => {
        if (selectedCompany) {
            loadPendingValidations(selectedCompany);
        }
    }, [selectedCompany]);

    const loadCompanies = async () => {
        try {
            const response = await companyAPI.getAll();
            setCompanies(response.data);
            if (response.data.length > 0) {
                setSelectedCompany(response.data[0].id);
            }
        } catch (error) {
            console.error('Failed to load companies:', error);
        }
    };

    const loadPendingValidations = async (companyId) => {
        try {
            const response = await uploadAPI.getPending(companyId);
            setPendingValidations(response.data);
        } catch (error) {
            console.error('Failed to load pending validations:', error);
        }
    };

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleFile = (selectedFile) => {
        const ext = selectedFile.name.split('.').pop().toLowerCase();
        if (!['csv', 'xlsx', 'xls', 'pdf'].includes(ext)) {
            alert('Please upload a CSV, XLSX, or PDF file');
            return;
        }
        setFile(selectedFile);
        setUploadResult(null);
    };

    const handleUpload = async () => {
        if (!file || !selectedCompany) return;

        setUploading(true);
        try {
            const response = await uploadAPI.uploadFile(selectedCompany, file);
            setUploadResult(response.data);
            setFile(null);
            loadPendingValidations(selectedCompany);
        } catch (error) {
            alert(error.response?.data?.detail || 'Upload failed');
        } finally {
            setUploading(false);
        }
    };

    const handleValidation = async (id, isApproved) => {
        try {
            await uploadAPI.validate({ financial_data_id: id, is_approved: isApproved });
            loadPendingValidations(selectedCompany);
            if (isApproved) {
                navigate(`/analysis/${selectedCompany}`);
            }
        } catch (error) {
            console.error('Validation failed:', error);
        }
    };

    const handleCreateCompany = async (e) => {
        e.preventDefault();
        try {
            const response = await companyAPI.create(newCompany);
            setCompanies([...companies, response.data]);
            setSelectedCompany(response.data.id);
            setShowNewCompany(false);
            setNewCompany({ name: '', industry: 'Services' });
        } catch (error) {
            console.error('Failed to create company:', error);
        }
    };

    return (
        <div className="upload-page">
            <h1>{t('upload.title')}</h1>

            {/* Company Selector */}
            <div className="company-selector">
                <div className="form-group">
                    <label className="form-label">{t('upload.company')}</label>
                    <div className="flex gap-md">
                        <select
                            className="form-select"
                            value={selectedCompany}
                            onChange={(e) => setSelectedCompany(e.target.value)}
                            style={{ flex: 1 }}
                        >
                            {companies.length === 0 && <option value="">No companies</option>}
                            {companies.map((company) => (
                                <option key={company.id} value={company.id}>
                                    {company.name} ({company.industry})
                                </option>
                            ))}
                        </select>
                        <button className="btn btn-secondary" onClick={() => setShowNewCompany(true)}>
                            <Plus size={18} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Upload Zone */}
            <div
                className={`upload-zone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                {file ? (
                    <div className="file-preview">
                        {file.name.toLowerCase().endsWith('.pdf') ? (
                            <FileText size={48} className="file-icon" />
                        ) : (
                            <FileSpreadsheet size={48} className="file-icon" />
                        )}
                        <p className="file-name">{file.name}</p>
                        <p className="file-size">{(file.size / 1024).toFixed(1)} KB</p>
                        <div className="file-actions">
                            <button className="btn btn-secondary" onClick={() => setFile(null)}>
                                Change File
                            </button>
                            <button
                                className="btn btn-primary"
                                onClick={handleUpload}
                                disabled={uploading || !selectedCompany}
                            >
                                {uploading ? t('upload.uploading') : 'Upload & Analyze'}
                            </button>
                        </div>
                    </div>
                ) : (
                    <>
                        <UploadIcon size={48} className="upload-icon" />
                        <p className="upload-text">{t('upload.dragDrop')}</p>
                        <p className="upload-or">{t('upload.or')}</p>
                        <label className="btn btn-primary">
                            {t('upload.browse')}
                            <input
                                type="file"
                                accept=".csv,.xlsx,.xls,.pdf"
                                onChange={(e) => e.target.files[0] && handleFile(e.target.files[0])}
                                hidden
                            />
                        </label>
                        <p className="upload-hint">Supported formats: CSV, XLSX, PDF</p>
                    </>
                )}
            </div>

            {/* Upload Result */}
            {uploadResult && (
                <div className="upload-result animate-fadeIn">
                    <div className="result-header">
                        <CheckCircle size={24} className="success-icon" />
                        <h3>{t('upload.success')}</h3>
                    </div>
                    <p className="result-message">{uploadResult.message}</p>
                    <div className="result-preview">
                        <h4>Detected Data:</h4>
                        <ul>
                            {uploadResult.preview_data?.detected_categories?.map((cat, idx) => (
                                <li key={idx}>{cat}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}

            {/* Pending Validations */}
            {pendingValidations.length > 0 && (
                <div className="pending-validations">
                    <h2>
                        <AlertTriangle size={20} />
                        Pending Validations
                    </h2>
                    {pendingValidations.map((item) => (
                        <div key={item.id} className="validation-card">
                            <div className="validation-header">
                                <FileSpreadsheet size={20} />
                                <span className="file-name">{item.file_name}</span>
                                <span className="upload-date">
                                    {new Date(item.upload_date).toLocaleDateString()}
                                </span>
                            </div>

                            {item.preview_data?.preview && (
                                <div className="data-preview">
                                    <table>
                                        <thead>
                                            <tr>
                                                {item.preview_data.columns?.slice(0, 5).map((col, idx) => (
                                                    <th key={idx}>{col}</th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {item.preview_data.preview?.slice(0, 3).map((row, idx) => (
                                                <tr key={idx}>
                                                    {Object.values(row).slice(0, 5).map((val, vidx) => (
                                                        <td key={vidx}>{String(val).substring(0, 20)}</td>
                                                    ))}
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}

                            <div className="validation-actions">
                                <button
                                    className="btn btn-danger"
                                    onClick={() => handleValidation(item.id, false)}
                                >
                                    <XCircle size={16} />
                                    Reject
                                </button>
                                <button
                                    className="btn btn-success"
                                    onClick={() => handleValidation(item.id, true)}
                                >
                                    <CheckCircle size={16} />
                                    {t('upload.validate')}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* New Company Modal */}
            {showNewCompany && (
                <div className="modal-overlay" onClick={() => setShowNewCompany(false)}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <h2>{t('upload.newCompany')}</h2>
                        <form onSubmit={handleCreateCompany}>
                            <div className="form-group">
                                <label className="form-label">Company Name</label>
                                <input
                                    type="text"
                                    className="form-input"
                                    value={newCompany.name}
                                    onChange={(e) => setNewCompany({ ...newCompany, name: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">Industry</label>
                                <select
                                    className="form-select"
                                    value={newCompany.industry}
                                    onChange={(e) => setNewCompany({ ...newCompany, industry: e.target.value })}
                                >
                                    {['Manufacturing', 'Retail', 'Agriculture', 'Services', 'Logistics', 'E-commerce'].map((ind) => (
                                        <option key={ind} value={ind}>{ind}</option>
                                    ))}
                                </select>
                            </div>
                            <div className="modal-actions">
                                <button type="button" className="btn btn-secondary" onClick={() => setShowNewCompany(false)}>
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn-primary">Create</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <style>{`
        .upload-page h1 {
          font-size: var(--font-size-2xl);
          font-weight: 700;
          margin-bottom: var(--spacing-xl);
        }

        .company-selector {
          margin-bottom: var(--spacing-xl);
          max-width: 500px;
        }

        .upload-zone {
          background: var(--bg-card);
          border: 2px dashed var(--border);
          border-radius: var(--radius-xl);
          padding: var(--spacing-2xl);
          text-align: center;
          transition: all var(--transition-normal);
          cursor: pointer;
        }

        .upload-zone.active {
          border-color: var(--primary);
          background: rgba(99, 102, 241, 0.1);
        }

        .upload-zone.has-file {
          border-style: solid;
          border-color: var(--primary);
        }

        .upload-icon {
          color: var(--text-muted);
          margin-bottom: var(--spacing-md);
        }

        .upload-text {
          font-size: var(--font-size-lg);
          color: var(--text-primary);
          margin-bottom: var(--spacing-xs);
        }

        .upload-or {
          color: var(--text-muted);
          margin-bottom: var(--spacing-md);
        }

        .upload-hint {
          color: var(--text-muted);
          font-size: var(--font-size-sm);
          margin-top: var(--spacing-md);
        }

        .file-preview {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: var(--spacing-sm);
        }

        .file-icon {
          color: var(--primary);
        }

        .file-name {
          font-weight: 600;
          color: var(--text-primary);
        }

        .file-size {
          font-size: var(--font-size-sm);
          color: var(--text-muted);
        }

        .file-actions {
          display: flex;
          gap: var(--spacing-md);
          margin-top: var(--spacing-md);
        }

        .upload-result {
          margin-top: var(--spacing-xl);
          padding: var(--spacing-lg);
          background: rgba(16, 185, 129, 0.1);
          border: 1px solid rgba(16, 185, 129, 0.3);
          border-radius: var(--radius-lg);
        }

        .result-header {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          margin-bottom: var(--spacing-md);
        }

        .success-icon {
          color: var(--success);
        }

        .pending-validations {
          margin-top: var(--spacing-2xl);
        }

        .pending-validations h2 {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          margin-bottom: var(--spacing-lg);
          color: var(--warning);
        }

        .validation-card {
          background: var(--bg-card);
          border: 1px solid var(--border);
          border-radius: var(--radius-lg);
          padding: var(--spacing-lg);
          margin-bottom: var(--spacing-md);
        }

        .validation-header {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          margin-bottom: var(--spacing-md);
        }

        .validation-header .file-name {
          flex: 1;
        }

        .upload-date {
          font-size: var(--font-size-sm);
          color: var(--text-muted);
        }

        .data-preview {
          overflow-x: auto;
          margin-bottom: var(--spacing-md);
        }

        .data-preview table {
          width: 100%;
          border-collapse: collapse;
          font-size: var(--font-size-sm);
        }

        .data-preview th, .data-preview td {
          padding: var(--spacing-xs) var(--spacing-sm);
          border: 1px solid var(--border);
          text-align: left;
        }

        .data-preview th {
          background: var(--bg-dark);
          font-weight: 600;
        }

        .validation-actions {
          display: flex;
          gap: var(--spacing-md);
          justify-content: flex-end;
        }

        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.7);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
        }

        .modal {
          background: var(--bg-card);
          border-radius: var(--radius-xl);
          padding: var(--spacing-xl);
          width: 100%;
          max-width: 400px;
          border: 1px solid var(--border);
        }

        .modal h2 {
          margin-bottom: var(--spacing-lg);
        }

        .modal-actions {
          display: flex;
          gap: var(--spacing-md);
          margin-top: var(--spacing-lg);
        }

        .modal-actions .btn {
          flex: 1;
        }
      `}</style>
        </div>
    );
}

export default Upload;
