import React, { useState, useEffect } from 'react'
import { Container, Paper, TextField, Button, Typography, Link } from '@mui/material'
// import { useNavigate } from "react-router-dom"
import Dashboard from './dashboard'

const Login = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [token, setToken] = useState("")
    // const navigate = useNavigate()

    const handleLogin = async () => {
        try {
            const formData = new URLSearchParams()
            formData.append('username', username)
            formData.append('password', password)
            
            const response = await fetch('http://localhost:8000/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            })

            if (response.ok) {
                const json = await response.json()
                setToken(json.access_token)
                localStorage.setItem('token', json.access_token)
            }
        } catch (error) {
            alert("Error during login:", error.message)
        }
    }

    useEffect(() => {
        const storedToken = localStorage.getItem('token')
        if (storedToken) {
            setToken(storedToken)
        }
    }, [])

    return (
        <div>
            {token ? (
                <Dashboard />
            ) : (
                <Container maxWidth="xs">
                    <Paper elevation={3} style={{ padding: '20px', marginTop: '50px' }}>
                        <Typography variant="h5" align="center" gutterBottom>
                            Login
                        </Typography>
                        <TextField
                            label="Username"
                            fullWidth
                            margin="normal"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <TextField
                            label="Password"
                            fullWidth
                            margin="normal"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <Button variant="outlined" color="primary" fullWidth onClick={handleLogin} style={{ marginTop: '10px', marginBottom: '10px' }}>
                            Login
                        </Button>
                        <Typography variant="h7" align="center">
                            Don't have an account? <Link href="/signup">Sign Up</Link>
                        </Typography>
                    </Paper>
                </Container>
            )}
        </div>
    )
}

export default Login