import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// English translations
const en = {
    translation: {
        // Navigation
        nav: {
            dashboard: 'Dashboard',
            upload: 'Upload Data',
            analysis: 'Analysis',
            logout: 'Logout'
        },
        // Dashboard
        dashboard: {
            title: 'Financial Health Dashboard',
            welcome: 'Welcome back',
            noCompanies: 'No companies found',
            addCompany: 'Add Your First Company',
            healthScore: 'Health Score',
            riskLevel: 'Risk Level',
            cashRunway: 'Cash Runway',
            days: 'days',
            viewAnalysis: 'View Analysis',
            askQuestion: 'Ask a question about your finances...'
        },
        // Upload
        upload: {
            title: 'Upload Financial Documents',
            dragDrop: 'Drag and drop files here',
            or: 'or',
            browse: 'Browse Files',
            supported: 'Supported formats: CSV, XLSX',
            uploading: 'Uploading...',
            success: 'File uploaded successfully',
            validate: 'Review & Validate',
            company: 'Select Company',
            newCompany: 'Create New Company'
        },
        // Analysis
        analysis: {
            title: 'Financial Analysis',
            overview: 'Overview',
            metrics: 'Key Metrics',
            benchmark: 'Industry Benchmark',
            forecast: 'Forecast',
            recommendations: 'Recommendations',
            risks: 'Risk Analysis',
            chat: 'Ask Questions'
        },
        // Common
        common: {
            loading: 'Loading...',
            error: 'Error',
            success: 'Success',
            save: 'Save',
            cancel: 'Cancel',
            submit: 'Submit',
            next: 'Next',
            back: 'Back',
            search: 'Search',
            filter: 'Filter'
        },
        // Industries
        industries: {
            Manufacturing: 'Manufacturing',
            Retail: 'Retail',
            Agriculture: 'Agriculture',
            Services: 'Services',
            Logistics: 'Logistics',
            'E-commerce': 'E-commerce'
        },
        // Risk Levels
        risk: {
            Low: 'Low',
            Medium: 'Medium',
            High: 'High',
            Critical: 'Critical'
        }
    }
};

// Hindi translations
const hi = {
    translation: {
        nav: {
            dashboard: 'डैशबोर्ड',
            upload: 'डेटा अपलोड करें',
            analysis: 'विश्लेषण',
            logout: 'लॉग आउट'
        },
        dashboard: {
            title: 'वित्तीय स्वास्थ्य डैशबोर्ड',
            welcome: 'वापस स्वागत है',
            noCompanies: 'कोई कंपनी नहीं मिली',
            addCompany: 'अपनी पहली कंपनी जोड़ें',
            healthScore: 'स्वास्थ्य स्कोर',
            riskLevel: 'जोखिम स्तर',
            cashRunway: 'कैश रनवे',
            days: 'दिन',
            viewAnalysis: 'विश्लेषण देखें',
            askQuestion: 'अपने वित्त के बारे में सवाल पूछें...'
        },
        upload: {
            title: 'वित्तीय दस्तावेज़ अपलोड करें',
            dragDrop: 'फ़ाइलें यहाँ खींचें और छोड़ें',
            or: 'या',
            browse: 'फ़ाइलें ब्राउज़ करें',
            supported: 'समर्थित प्रारूप: CSV, XLSX',
            uploading: 'अपलोड हो रहा है...',
            success: 'फ़ाइल सफलतापूर्वक अपलोड हुई',
            validate: 'समीक्षा और मान्य करें',
            company: 'कंपनी चुनें',
            newCompany: 'नई कंपनी बनाएं'
        },
        analysis: {
            title: 'वित्तीय विश्लेषण',
            overview: 'अवलोकन',
            metrics: 'मुख्य मेट्रिक्स',
            benchmark: 'उद्योग बेंचमार्क',
            forecast: 'पूर्वानुमान',
            recommendations: 'सिफारिशें',
            risks: 'जोखिम विश्लेषण',
            chat: 'प्रश्न पूछें'
        },
        common: {
            loading: 'लोड हो रहा है...',
            error: 'त्रुटि',
            success: 'सफलता',
            save: 'सहेजें',
            cancel: 'रद्द करें',
            submit: 'जमा करें',
            next: 'आगे',
            back: 'पीछे',
            search: 'खोजें',
            filter: 'फ़िल्टर'
        },
        industries: {
            Manufacturing: 'विनिर्माण',
            Retail: 'खुदरा',
            Agriculture: 'कृषि',
            Services: 'सेवाएं',
            Logistics: 'लॉजिस्टिक्स',
            'E-commerce': 'ई-कॉमर्स'
        },
        risk: {
            Low: 'कम',
            Medium: 'मध्यम',
            High: 'उच्च',
            Critical: 'गंभीर'
        }
    }
};

i18n
    .use(initReactI18next)
    .init({
        resources: {
            en,
            hi
        },
        lng: 'en',
        fallbackLng: 'en',
        interpolation: {
            escapeValue: false
        }
    });

export default i18n;
