import React, { createContext, useContext, useState, useEffect } from 'react';

const CurrencyContext = createContext(undefined);

export const CurrencyProvider = ({ children }) => {
    const [currency, setCurrency] = useState(() => {
        return localStorage.getItem('currency') || 'USD';
    });

    useEffect(() => {
        localStorage.setItem('currency', currency);
    }, [currency]);

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency,
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }).format(amount);
    };

    const currencyOptions = [
        { code: 'USD', symbol: '$', name: 'US Dollar' },
        { code: 'EUR', symbol: '€', name: 'Euro' },
        { code: 'GBP', symbol: '£', name: 'British Pound' },
        { code: 'NGN', symbol: '₦', name: 'Nigerian Naira' },
        { code: 'JPY', symbol: '¥', name: 'Japanese Yen' },
        { code: 'CAD', symbol: 'CA$', name: 'Canadian Dollar' },
        { code: 'AUD', symbol: 'A$', name: 'Australian Dollar' },
    ];

    return (
        <CurrencyContext.Provider value={{ currency, setCurrency, formatCurrency, currencyOptions }}>
            {children}
        </CurrencyContext.Provider>
    );
};

export const useCurrency = () => {
    const context = useContext(CurrencyContext);
    if (context === undefined) {
        throw new Error('useCurrency must be used within a CurrencyProvider');
    }
    return context;
};

export default CurrencyContext;
