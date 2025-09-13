import { useState, createContext, useContext } from 'react';
import api from '../api/client';

const AuthContext = createContext();

const AuthProvider = ({children}) => {
    const [user, setUser] = useState(null);

    const login = async (username, password) => {
        try {
            console.log('Attempting login...');
            const res = await api.post('/token/', { username, password }, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (res.status === 200) {
                const { access, refresh } = res.data;
                localStorage.setItem('access_token', access);
                localStorage.setItem('refresh_token', refresh);
                setUser({ username });
                console.log('Login successful:', username);
            }
        } catch (error) {
            setUser(null);
            console.error('Login failed:', error);
        }
    }

    const logout = () => {
        localStorage.clear();
        setUser(null);
    }

    return (
        <AuthContext.Provider value={{ user, login, logout}}>
            {children}
        </AuthContext.Provider>
    )
}

const useAuth = () => {
    return useContext(AuthContext);
}

export { AuthProvider, useAuth };